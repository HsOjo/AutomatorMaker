import os
import sys
from typing import List

from PyQt5.QtWidgets import QMessageBox, QFileDialog, QInputDialog
from dt_automator import DTAutomator
from ojoqt import BaseApplication, BaseMainWindow
from ojoqt.common import try_exec
from ojoqt.dialog import SelectDialog
from ojoqt.dialog.form import FormDialog
from ojoqt.dialog.form.field import StringField, RectField, SelectField
from ojoqt.dialog.form.field.range import RangeField
from ojoqt.helper import TableHelper
from pyadb import PyADB, Device
from pyojo.tools.shell import get_app_shell

from .project import Project
from .scene import ActionEditor, ObjectEditor
from .scene.model import SceneModel, FeatureModel, ObjectModel, ActionModel
from .view import MainWindowView
from ..config import Config


def _auto_save(func):
    def wrapper(self: 'MainWindow', *args, **kwargs):
        auto_save = True
        if 'auto_save' in kwargs:
            auto_save = kwargs.pop('auto_save')
        result = func(self, *args, **kwargs)
        if self.auto_save and auto_save:
            project = self.project
            if project is not None:
                self.project.save()
        return result

    return wrapper


class MainWindow(BaseMainWindow, MainWindowView):
    TYPE_FEATURE = 0
    TYPE_OBJECT = 1
    TYPE_ACTION = 2

    def __init__(self, app: BaseApplication):
        self._config = Config()
        self._config._config_path = os.path.expanduser('~/.automator_maker.json')
        self._project = None  # type: Project
        self._auto_save = True
        self._device = None  # type: Device
        self._debug = '--debug' in sys.argv
        self._event = dict(
            debug=lambda: self._debug,
            process_events=lambda: self.app.processEvents(),
            sync_features=self.sync_features,
            sync_objects=self.sync_objects,
            sync_actions=self.sync_actions,
            select_feature=lambda i: self.select_item(self.TYPE_FEATURE, i),
            select_object=lambda i: self.select_item(self.TYPE_OBJECT, i),
            select_action=lambda i: self.select_item(self.TYPE_ACTION, i),
            set_params=lambda: self._callback_set_item_params_triggered(True),
            show_status=self.show_status,
        )

        super().__init__(app)
        self.scene_widget.register_event(**self._event)

        app_shell = get_app_shell()
        self._adb = PyADB('%s/app/res/libs/adb' % app_shell.get_runtime_dir())
        if self._config.load():
            self._device = self._adb.devices.get(self._config.device)
            project_dir = self._config.project
            if project_dir != '' and os.path.exists(project_dir) and os.path.isdir(project_dir):
                project = Project.open(project_dir)
                if project is not None:
                    self._project = project
                    self.sync_scenes()

    @property
    def project(self):
        return self._project

    @property
    def auto_save(self):
        return self._auto_save

    def select_item(self, type_, index):
        widgets = {
            self.TYPE_FEATURE: self.tableWidgetFeatures,
            self.TYPE_OBJECT: self.tableWidgetObjects,
            self.TYPE_ACTION: self.tableWidgetActions,
        }
        widgets[type_].setCurrentCell(index, 0)

    def sync_scenes(self):
        if self._project is None:
            return

        scenes = self._project.scenes
        data = []
        for k, v in scenes.items():
            v: SceneModel
            data.append([k, len(v.features), len(v.objects)])
        TableHelper.sync_data(self.tableWidgetScenes, data)
        TableHelper.auto_inject_columns_width(self.tableWidgetScenes)

    def sync_scene(self, scene: SceneModel):
        self.sync_features(scene.features, auto_save=False)
        self.sync_objects(scene.objects, auto_save=False)

    @_auto_save
    def sync_features(self, features: List[FeatureModel]):
        data = []
        for i, v in enumerate(features):
            v: FeatureModel
            data.append([i, v.name, v.ALL_MODES_REV.get(v.mode), v.rect, v.detect_weight])
        TableHelper.sync_data(self.tableWidgetFeatures, data)
        TableHelper.auto_inject_columns_width(self.tableWidgetFeatures)
        self.sync_scenes()

    @_auto_save
    def sync_objects(self, objects: List[ObjectModel]):
        data = []
        for i, v in enumerate(objects):
            v: ObjectModel
            data.append([i, v.name, v.rect, v.ALL_TYPES_REV.get(v.type), len(v.actions), v.params])
        TableHelper.sync_data(self.tableWidgetObjects, data)
        TableHelper.auto_inject_columns_width(self.tableWidgetObjects)
        self.sync_scenes()

    @_auto_save
    def sync_actions(self, actions: List[ActionModel]):
        data = []
        for i, v in enumerate(actions):
            v: ActionModel
            data.append([i, v.name, v.ALL_TYPES_REV.get(v.type), v.dest_scene, v.params])
        TableHelper.sync_data(self.tableWidgetActions, data)
        TableHelper.auto_inject_columns_width(self.tableWidgetActions)

    @try_exec(show=True)
    def _callback_open_triggered(self, b: bool):
        directory = QFileDialog.getExistingDirectory(self, self.tr('Open Project'))
        project = Project.open(directory)
        if project is not None:
            self._project = project
            self.sync_scenes()
            self._config.project = directory
            self._config.save()

    @try_exec(show=True)
    def _callback_save_triggered(self, b: bool):
        if project is not None:
            self._project.save()

    @_auto_save
    def _callback_capture_scene_triggered(self, b: bool):
        if self._project is None:
            QMessageBox.information(self, self.tr('Error'), self.tr('Open Project First!'))
            return
        if self._device is None:
            QMessageBox.information(self, self.tr('Error'), self.tr('Device Select First!'))
            return

        img_data = self._device.display.screen_cap()
        text, b = QInputDialog.getText(self, self.tr('Capture New Scene'), self.tr('Please input scene name.'))
        if text not in self._project.scenes:
            self._project.add_scene(img_data, text if b and text != '' else None)
        else:
            scene = self._project.scenes[text]
            with open(scene.img_path, 'wb') as io:
                io.write(img_data)
            if self.scene_widget.scene == scene:
                self.scene_widget.set_scene(scene)
        self.sync_scenes()

    def _callback_select_device_triggered(self, b: bool):
        devices = self._adb.devices
        if len(devices) == 0:
            self._adb.kill_server()
            self._adb.start_server()
        devices = self._adb.devices

        item = SelectDialog.select(
            self, title=self.tr('Select Device'),
            cols_title=[self.tr('Device'), self.tr('State')],
            rows=[(sn, device.state) for sn, device in devices.items()],
            item_keys=['sn', 'state']
        )

        if item is not None:
            self._device = devices[item['sn']]
            self._config.device = item['sn']
            self._config.save()

    @_auto_save
    def _callback_rename_scene_triggered(self, b: bool):
        index = self.tableWidgetScenes.currentRow()
        if 0 <= index < self.tableWidgetScenes.rowCount():
            item = self.tableWidgetScenes.item(index, 0)
            text, b = QInputDialog.getText(self, self.tr('Rename Scene'), self.tr('Please input new scene name.'),
                                           text=item.text())
            if b:
                if self._project.rename_scene(item.text(), text):
                    item.setText(text)

    @_auto_save
    def _callback_remove_scene_triggered(self, b: bool):
        index = self.tableWidgetScenes.currentRow()
        if 0 <= index < self.tableWidgetScenes.rowCount():
            item = self.tableWidgetScenes.item(index, 0)
            self._project.remove_scene(item.text())
            self.sync_scenes()

    def _callback_edit_item(self, item):
        self.scene_widget.set_pause(True)
        if isinstance(item, FeatureModel):
            data = FormDialog.input([
                StringField('name', item.name, title=self.tr('Name')),
                SelectField('mode', options=item.ALL_MODES, value=item.mode, title=self.tr('Mode')),
                RectField('rect', item.rect, title=self.tr('Rect')),
                RangeField(
                    'detect_weight', item.detect_weight,
                    min=item.DETECT_WEIGHT_MIN, max=item.DETECT_WEIGHT_MAX,
                    title=self.tr('Detect Weight')
                ),
            ], self.tr('Edit Feature'))
            if data is not None:
                item.load_data(**data)
                self.sync_features(self.scene_widget.scene.features)
        elif isinstance(item, ObjectModel):
            data = FormDialog.input([
                StringField('name', item.name, title=self.tr('Name')),
                RectField('rect', item.rect, title=self.tr('Rect')),
                SelectField('type', options=item.ALL_TYPES, value=item.type, title=self.tr('Type')),
            ], self.tr('Edit Object'))
            if data is not None:
                item.load_data(**data)
                self.sync_objects(self.scene_widget.scene.objects)
        elif isinstance(item, ActionModel):
            data = FormDialog.input([
                StringField('name', item.name, title=self.tr('Name')),
                SelectField('type', options=item.ALL_TYPES, value=item.type, title=self.tr('Type')),
                SelectField(
                    'dest_scene', options=[item.PARAM_NONE] + [scene for scene in self.project.scenes],
                    value=item.dest_scene, title=self.tr('Scene')
                ),
            ], self.tr('Edit Action'))
            if data is not None:
                item.load_data(**data)
                self.sync_actions(self.scene_widget.current_object.actions)
        else:
            raise Exception('Unsupport Item: %s' % item)

        self.scene_widget.callback_item_edited(item)
        self.scene_widget.set_pause(False)

    def _callback_delete_item(self, item):
        self.scene_widget.callback_item_deleted(item)
        tab_index = self.tabWidgetScene.currentIndex()
        items = self.current_items
        items.remove(item)
        if tab_index == self.TAB_FEATURES:
            self.sync_features(items)
        elif tab_index == self.TAB_OBJECTS:
            self.sync_objects(items)
        elif tab_index == self.TAB_ACTIONS:
            self.sync_actions(items)

    def _callback_set_item_params_triggered(self, b: bool):
        ce = self.scene_widget.current_editor
        item = None
        if isinstance(ce, ActionEditor):
            item = ce.current_action
        elif isinstance(ce, ObjectEditor):
            item = ce.current_object

        if item is not None:
            params_field = item.PARAMS_TYPE[item.type] + item.PARAMS_COMMON
            if len(params_field) > 0:
                params = item.params
                fields = []
                for k in params_field:
                    v = params.get(k, item.PARAMS_DEFAULT.get(k))
                    fields.append(item.PARAMS_FIELD[k](k, v, item.PARAMS_TITLE.get(k)))
                params = FormDialog.input(fields, self.tr('Set Action Parameters'))
                if params is not None:
                    item.params = params
                    self.scene_widget.callback_item_edited(self.current_item)
                    self.sync_actions(self.current_items)

    @try_exec(show=True, info_only=True)
    def _callback_export_data_triggered(self, b: bool):
        [path, _] = QFileDialog.getSaveFileName(
            parent=self, caption='Export Data', directory=self._config.export,
            filter='Data File(*.dat);;All File(*)'
        )

        if path != '':
            self._config.export = path
            self._config.save()
            dta = DTAutomator()
            dta.load_from_maker(self._project.path)
            dta.dump(path)

    def _callback_scene_changed(self, current: str, previous: str):
        # Reset tab, if in actions.
        if self.tabWidgetScene.currentIndex() == self.TAB_ACTIONS:
            self.tabWidgetScene.setCurrentIndex(self.TAB_FEATURES)

        scene = self._project.scenes.get(current)  # type: SceneModel
        if scene is not None:
            self.scene_widget.set_scene(scene)
            self.sync_scene(scene)

    def _callback_scene_tab_changed(self, current: int, previous: int) -> bool:
        super()._callback_scene_tab_changed(current, previous)
        b = self.scene_widget.set_current_editor(current)
        self.scene_widget.current_editor.select(-1)
        return b

    def showEvent(self, *args):
        super().showEvent(*args)
        TableHelper.auto_inject_columns_width(self.tableWidgetScenes)

    def resizeEvent(self, *args):
        super().resizeEvent(*args)
        current_table = self.current_table_widget
        if current_table is not None:
            TableHelper.auto_inject_columns_width(current_table)

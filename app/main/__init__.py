import sys
from typing import List

from PyQt5.QtWidgets import QMessageBox, QFileDialog, QInputDialog
from pyadb import PyADB, Device

from app.base import BaseMainWindow
from app.base.dialog import SelectDialog
from .project import Project
from .scene.model import SceneModel, FeatureModel, ObjectModel, ActionModel
from .view import MainWindowView
from .. import BaseApplication
from ..base.common import try_exec
from ..base.helper import TableHelper


def _auto_save(func):
    def wrapper(self: 'MainWindow', *args, **kwargs):
        result = func(self, *args, **kwargs)
        if self.auto_save:
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
        self._project = None  # type: Project
        self._auto_save = True
        self._device = None  # type: Device
        self._debug = '--debug' in sys.argv

        super().__init__(app)

        self.scene_widget.register_event(
            debug=lambda: self._debug,
            process_events=lambda: self.app.processEvents(),
            sync_features=self.sync_features,
            sync_objects=self.sync_objects,
            sync_actions=self.sync_actions,
            select_feature=lambda i: self.select_item(self.TYPE_FEATURE, i),
            select_object=lambda i: self.select_item(self.TYPE_OBJECT, i),
            select_action=lambda i: self.select_item(self.TYPE_ACTION, i),
        )

        if self._debug:
            self._project = Project.open('./test')
            self._device = list(PyADB('/Users/hsojo/Library/Android/sdk/platform-tools/adb').devices.values())[0]
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
        self.sync_features(scene.features)
        self.sync_objects(scene.objects)

    def sync_features(self, features: List[FeatureModel]):
        data = []
        for i, v in enumerate(features):
            v: FeatureModel
            data.append([i, v.name, '%s,%s,%s,%s' % tuple(v.rect), v.detect_weight])
        TableHelper.sync_data(self.tableWidgetFeatures, data)
        TableHelper.auto_inject_columns_width(self.tableWidgetFeatures)

    def sync_objects(self, objects: List[ObjectModel]):
        data = []
        for i, v in enumerate(objects):
            v: ObjectModel
            data.append([i, v.name, '%s,%s,%s,%s' % tuple(v.rect), v.type, len(v.actions)])
        TableHelper.sync_data(self.tableWidgetObjects, data)
        TableHelper.auto_inject_columns_width(self.tableWidgetObjects)

    def sync_actions(self, actions: List[ActionModel]):
        data = []
        for i, v in enumerate(actions):
            v: ActionModel
            data.append([i, v.name, v.type, v.dest_scene, v.params])
        TableHelper.sync_data(self.tableWidgetFeatures, data)
        TableHelper.auto_inject_columns_width(self.tableWidgetFeatures)

    @try_exec(show=True)
    def _callback_open_triggered(self, b: bool):
        directory = QFileDialog.getExistingDirectory(self, self.tr('Open Project'))
        project = Project.open(directory)
        if project is not None:
            self._project = project
            self.sync_scenes()

    @try_exec(show=True)
    def _callback_save_triggered(self, b: bool):
        if project is not None:
            self._project.save()

    @_auto_save
    def _callback_capture_triggered(self, b: bool):
        if self._project is None:
            QMessageBox.information(self, self.tr('Error'), self.tr('Open Project First!'))
            return
        if self._device is None:
            QMessageBox.information(self, self.tr('Error'), self.tr('Device Select First!'))
            return

        text, b = QInputDialog.getText(self, self.tr('Capture New Scene'), self.tr('Please input scene name.'))
        img_data = self._device.display.screen_cap()
        self._project.add_scene(img_data, text if b and text != '' else None)
        self.sync_scenes()

    def _callback_select_device_triggered(self, b: bool):
        adb = PyADB('/Users/hsojo/Library/Android/sdk/platform-tools/adb')
        devices = adb.devices
        if len(devices) == 0:
            adb.kill_server()
            adb.start_server()
        devices = adb.devices

        item = SelectDialog.select(
            self, title=self.tr('Select Device'),
            cols_title=[self.tr('Device'), self.tr('State')],
            rows=[(sn, device.state) for sn, device in devices.items()],
            item_keys=['sn', 'state']
        )

        if item is not None:
            self._device = devices[item['sn']]

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

    def _callback_scene_changed(self, current: str, previous: str):
        # Reset tab, if in actions.
        if self.tabWidgetScene.currentIndex() == self.TAB_ACTIONS:
            self.tabWidgetScene.setCurrentIndex(self.TAB_FEATURES)

        scene = self._project.scenes.get(current)  # type: SceneModel
        if scene is not None:
            self.scene_widget.set_scene(scene)
            self.sync_scene(scene)

    def _callback_scene_tab_changed(self, current: int, previous: int) -> bool:
        b = self.scene_widget.set_current_editor(current)
        if current == self.TAB_ACTIONS:
            TableHelper.auto_inject_columns_width(self.tableWidgetActions)
        elif current == self.TAB_OBJECTS:
            TableHelper.auto_inject_columns_width(self.tableWidgetObjects)
        elif current == self.TAB_FEATURES:
            TableHelper.auto_inject_columns_width(self.tableWidgetFeatures)
        return b

    def showEvent(self, *args):
        super().showEvent(*args)
        TableHelper.auto_inject_columns_width(self.tableWidgetScenes)

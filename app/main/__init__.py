import sys
import traceback

from PyQt5.QtWidgets import QMessageBox, QFileDialog, QInputDialog
from pyadb import PyADB, Device

from app.base import BaseMainWindow
from app.base.dialog import SelectDialog
from .project import Project
from .scene.model import SceneModel, FeatureModel, ObjectModel, ActionModel
from .view import MainWindowView
from .. import BaseApplication
from ..base.helper import TableHelper


class MainWindow(BaseMainWindow, MainWindowView):
    def __init__(self, app: BaseApplication):
        super().__init__(app)
        self._device = None  # type: Device
        self._project = None  # type: Project
        self._debug = '--debug' in sys.argv

        self.scene_widget.set_event(
            debug=lambda: self._debug,
            process_events=lambda: self.app.processEvents()
        )

        if self._debug:
            self._project = Project.open('./test')

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
        data = []
        for i, v in enumerate(scene.features):
            v: FeatureModel
            data.append([i, v.name, '%s,%s,%s,%s' % v.rect, v.detect_weight])
        TableHelper.sync_data(self.tableWidgetFeatures, data)
        TableHelper.auto_inject_columns_width(self.tableWidgetFeatures)

        data = []
        for i, v in enumerate(scene.objects):
            v: ObjectModel
            data.append([i, v.name, '%s,%s,%s,%s' % v.rect, v.type, len(v.actions)])
        TableHelper.sync_data(self.tableWidgetObjects, data)
        TableHelper.auto_inject_columns_width(self.tableWidgetObjects)

    def sync_object(self, object: ObjectModel):
        data = []
        for i, v in enumerate(object.actions):
            v: ActionModel
            data.append([i, v.name, v.type, v.dest_scene, v.params])
        TableHelper.sync_data(self.tableWidgetFeatures, data)
        TableHelper.auto_inject_columns_width(self.tableWidgetFeatures)

    def _callback_open_triggered(self):
        directory = QFileDialog.getExistingDirectory(self, self.tr('Open Project'))
        try:
            project = Project.open(directory)
            if project is not None:
                self._project = project
        except:
            QMessageBox.warning(self, self.tr('Error'), traceback.format_exc())

    def _callback_save_triggered(self):
        try:
            if project is not None:
                self._project.save()
        except:
            QMessageBox.warning(self, self.tr('Error'), traceback.format_exc())

    def _callback_capture_triggered(self):
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

    def _callback_select_device_triggered(self):
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

    def _callback_rename_scene_triggered(self):
        index = self.tableWidgetScenes.currentRow()
        if 0 <= index < self.tableWidgetScenes.rowCount():
            item = self.tableWidgetScenes.item(index, 0)
            text, b = QInputDialog.getText(self, self.tr('Rename Scene'), self.tr('Please input new scene name.'),
                                           text=item.text())
            if b:
                item.setText(text)

    def _callback_scene_changed(self, current: str, previous: str):
        scene = self._project.scenes.get(current)  # type: SceneModel
        if scene is not None:
            self.scene_widget.set_scene(scene)

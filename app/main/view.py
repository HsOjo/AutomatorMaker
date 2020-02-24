from PyQt5.QtWidgets import QSizePolicy, QTableWidgetItem

from app.base import BaseView
from app.res.ui.main import Ui_MainWindow
from .scene import SceneWidget


class MainWindowView(Ui_MainWindow, BaseView):
    def callback_init(self):
        self.scene_widget = SceneWidget(self.scrollAreaWidgetContents)
        self.scene_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.gridLayout_Preview.addWidget(self.scene_widget, 0, 0, 1, 1)
        self.tableWidgetScenes.setCurrentCell(-1, -1)

    def register_callback(self):
        self.actionCapture.triggered.connect(self._callback_capture_triggered)
        self.actionOpen.triggered.connect(self._callback_open_triggered)
        self.actionSave.triggered.connect(self._callback_save_triggered)
        self.actionSelectDevice.triggered.connect(self._callback_select_device_triggered)
        self.actionRenameScene.triggered.connect(self._callback_rename_scene_triggered)
        self.horizontalSliderScale.valueChanged.connect(self._callback_scale_changed)
        self.tableWidgetScenes.currentItemChanged.connect(self.__callback_scene_changed)

    def _callback_open_triggered(self):
        pass

    def _callback_save_triggered(self):
        pass

    def _callback_capture_triggered(self):
        pass

    def _callback_select_device_triggered(self):
        pass

    def _callback_rename_scene_triggered(self):
        pass

    def _callback_scale_changed(self, value):
        self.scene_widget.set_scale(value / self.horizontalSliderScale.maximum())

    def _callback_scene_changed(self, current: str, previous: str):
        pass

    def __callback_scene_changed(self, current: QTableWidgetItem, previous: QTableWidgetItem):
        name_current = self.tableWidgetScenes.item(current.row(), 0).text()
        name_previous = None
        if previous is not None:
            name_previous = self.tableWidgetScenes.item(previous.row(), 0).text()
        if name_current != name_previous:
            self._callback_scene_changed(name_current, name_previous)

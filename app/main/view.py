from PyQt5.QtWidgets import QSizePolicy

from app.base import BaseView
from app.res.ui.main import Ui_MainWindow
from .scene import SceneWidget
from ..base.helper import TableHelper


class MainWindowView(Ui_MainWindow, BaseView):
    TAB_FEATURES = 0
    TAB_OBJECTS = 1
    TAB_ACTIONS = 2

    def callback_init(self):
        self._scene_tab_event = False
        self._scene_tab_prev_index = self.tabWidgetScene.currentIndex()
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
        self.tabWidgetScene.currentChanged.connect(self.__callback_scene_tab_changed)
        self.tableWidgetScenes.currentItemChanged.connect(
            TableHelper.generate_current_item_changed_callback(self.tableWidgetScenes, self._callback_scene_changed, 0)
        )
        self.tableWidgetFeatures.currentItemChanged.connect(
            TableHelper.generate_current_item_changed_callback(self.tableWidgetFeatures, self._callback_feature_changed)
        )
        self.tableWidgetObjects.currentItemChanged.connect(
            TableHelper.generate_current_item_changed_callback(self.tableWidgetObjects, self._callback_object_changed)
        )
        self.tableWidgetActions.currentItemChanged.connect(
            TableHelper.generate_current_item_changed_callback(self.tableWidgetActions, self._callback_action_changed)
        )

    def _callback_open_triggered(self, b:bool):
        pass

    def _callback_save_triggered(self, b:bool):
        pass

    def _callback_capture_triggered(self, b:bool):
        pass

    def _callback_select_device_triggered(self, b:bool):
        pass

    def _callback_rename_scene_triggered(self, b:bool):
        pass

    def _callback_scale_changed(self, value):
        self.scene_widget.set_scale(value / self.horizontalSliderScale.maximum())

    def _callback_scene_changed(self, current: str, previous: str):
        pass

    def _callback_feature_changed(self, current: int, previous: int):
        self.scene_widget.callback_select_feature(current)

    def _callback_object_changed(self, current: int, previous: int):
        self.scene_widget.callback_select_object(current)

    def _callback_action_changed(self, current: int, previous: int):
        self.scene_widget.callback_select_action(current)

    def _callback_scene_tab_changed(self, current: int, previous: int) -> bool:
        return True

    def __callback_scene_tab_changed(self, index):
        if self._scene_tab_event:
            return
        self._scene_tab_event = True
        if self._callback_scene_tab_changed(index, self._scene_tab_prev_index):
            self._scene_tab_prev_index = index
        else:
            self.tabWidgetScene.setCurrentIndex(self._scene_tab_prev_index)
        self._scene_tab_event = False

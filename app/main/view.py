from PyQt5.QtWidgets import QSizePolicy

from app.base import BaseView
from app.res.ui.main import Ui_MainWindow
from . import ActionModel
from .scene import SceneWidget
from ..base.dialog.form import FormDialog
from ..base.dialog.form.field import NumberField, StringField
from ..base.helper import TableHelper


class MainWindowView(Ui_MainWindow, BaseView):
    TAB_FEATURES = 0
    TAB_OBJECTS = 1
    TAB_ACTIONS = 2

    def _callback_init(self):
        self._scene_tab_event = False
        self._scene_tab_prev_index = self.tabWidgetScene.currentIndex()
        self.scene_widget = SceneWidget(self.scrollAreaWidgetContents)
        self.scene_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.gridLayout_Preview.addWidget(self.scene_widget, 0, 0, 1, 1)
        self.tableWidgetScenes.setCurrentCell(-1, -1)

    def register_callback(self):
        self.actionCaptureScene.triggered.connect(self._callback_capture_scene_triggered)
        self.actionOpen.triggered.connect(self._callback_open_triggered)
        self.actionSave.triggered.connect(self._callback_save_triggered)
        self.actionSelectDevice.triggered.connect(self._callback_select_device_triggered)
        self.actionRenameScene.triggered.connect(self._callback_rename_scene_triggered)
        self.actionRemoveScene.triggered.connect(self._callback_remove_scene_triggered)
        self.actionEditItem.triggered.connect(lambda: self._callback_edit_item_triggered(self.current_item_index))
        self.actionDeleteItem.triggered.connect(lambda: self._callback_delete_item_triggered(self.current_item_index))
        self.actionSetItemParams.triggered.connect(self._callback_set_item_params_triggered)
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
        self.tableWidgetFeatures.itemDoubleClicked.connect(lambda x: self._callback_edit_item_triggered(x.row()))
        self.tableWidgetObjects.itemDoubleClicked.connect(lambda x: self._callback_edit_item_triggered(x.row()))
        self.tableWidgetActions.itemDoubleClicked.connect(lambda x: self._callback_edit_item_triggered(x.row()))
        self.tableWidgetScenes.itemDoubleClicked.connect(lambda _: self._callback_rename_scene_triggered(True))

    def _callback_open_triggered(self, b: bool):
        pass

    def _callback_save_triggered(self, b: bool):
        pass

    def _callback_capture_scene_triggered(self, b: bool):
        pass

    def _callback_select_device_triggered(self, b: bool):
        pass

    def _callback_rename_scene_triggered(self, b: bool):
        pass

    def _callback_remove_scene_triggered(self, b: bool):
        pass

    def _callback_set_item_params_triggered(self, b: bool):
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
        if current == self.TAB_ACTIONS:
            TableHelper.auto_inject_columns_width(self.tableWidgetActions)
        elif current == self.TAB_OBJECTS:
            TableHelper.auto_inject_columns_width(self.tableWidgetObjects)
        elif current == self.TAB_FEATURES:
            TableHelper.auto_inject_columns_width(self.tableWidgetFeatures)
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

    def _callback_edit_item(self, item):
        pass

    def _callback_delete_item(self, item):
        pass

    def _callback_edit_item_triggered(self, index):
        item = self.current_item
        if index == -1 or item is None:
            return
        self._callback_edit_item(item)

    def _callback_delete_item_triggered(self, index):
        item = self.current_item
        if index == -1 or item is None:
            return
        self._callback_delete_item(item)

    @property
    def current_item(self):
        items, index = self.current_items, self.current_item_index
        if items is None or index is None:
            return None
        if 0 <= index < len(items):
            return items[index]
        else:
            return None

    @property
    def current_items(self):
        # Fix Qt init crash.
        sw = getattr(self, 'scene_widget', None)  # type: SceneWidget
        if sw is None or sw.scene is None:
            return None
        scene = sw.scene
        tab_index = self.tabWidgetScene.currentIndex()
        items = None
        if tab_index == self.TAB_FEATURES:
            items = scene.features
        elif tab_index == self.TAB_OBJECTS:
            items = scene.objects
        elif tab_index == self.TAB_ACTIONS:
            object_ = self.scene_widget.current_object
            if object_ is None:
                return
            items = object_.actions

        return items

    @property
    def current_item_index(self):
        index = -1
        if self.current_table_widget is not None:
            index = self.current_table_widget.currentRow()
        return index

    @property
    def current_table_widget(self):
        widget = None
        tab_index = self.tabWidgetScene.currentIndex()
        if tab_index == self.TAB_FEATURES:
            widget = self.tableWidgetFeatures
        elif tab_index == self.TAB_OBJECTS:
            widget = self.tableWidgetObjects
        elif tab_index == self.TAB_ACTIONS:
            widget = self.tableWidgetActions
        return widget

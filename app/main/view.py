from PyQt5.QtWidgets import QSizePolicy

from app.base import BaseView
from app.res.ui.main import Ui_MainWindow
from .scene import SceneWidget


class MainWindowView(Ui_MainWindow, BaseView):
    def callback_init(self):
        self.scene_widget = SceneWidget(self.scrollAreaWidgetContents, debug=True)
        self.scene_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.gridLayout_Preview.addWidget(self.scene_widget, 0, 0, 1, 1)

    def register_callback(self):
        self.actionCapture.triggered.connect(self._callback_capture_triggered)
        self.actionOpen.triggered.connect(self._callback_open_triggered)
        self.actionSave.triggered.connect(self._callback_save_triggered)
        self.actionSelect_Device.triggered.connect(self._callback_select_device_triggered)
        self.horizontalSliderScale.valueChanged.connect(self._callback_scale_changed)

    def _callback_open_triggered(self):
        pass

    def _callback_save_triggered(self):
        pass

    def _callback_capture_triggered(self):
        pass

    def _callback_select_device_triggered(self):
        pass

    def _callback_scale_changed(self, value):
        self.scene_widget.set_scale(value / self.horizontalSliderScale.maximum())

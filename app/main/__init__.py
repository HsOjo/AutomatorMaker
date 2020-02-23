from PyQt5.QtWidgets import QMessageBox
from pyadb import PyADB, Device

from app.base import BaseMainWindow
from app.base.dialog import SelectDialog
from .view import MainWindowView
from .. import BaseApplication


class MainWindow(BaseMainWindow, MainWindowView):
    def __init__(self, app: BaseApplication):
        super().__init__(app)
        self.path_dir = None
        self._device = None  # type: Device
        # self.graphics.set_scale(True)
        self.activateWindow()

    def _callback_open_triggered(self):
        pass

    def _callback_save_triggered(self):
        pass

    def _callback_capture_triggered(self):
        if self._device is None:
            QMessageBox.information(self, 'Error', 'Device Select First!')
            return

        img_data = self._device.display.screen_cap()
        self.scene.set_screen(img_data)

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

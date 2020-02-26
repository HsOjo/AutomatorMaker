from PyQt5.QtWidgets import QMainWindow

from ..base import BaseApplication


class BaseMainWindow(QMainWindow):
    def __init__(self, app: BaseApplication):
        super().__init__()
        self._app = app

    @property
    def app(self):
        return self._app

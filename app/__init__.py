from .base import BaseApplication
from .main import MainWindow


class Application(BaseApplication):
    main_window_cls = MainWindow

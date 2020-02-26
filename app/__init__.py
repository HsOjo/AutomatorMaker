import typing

from .base import BaseApplication
from .main import MainWindow


class Application(BaseApplication):
    main_window_cls = MainWindow

    def __init__(self, argv: typing.List[str]):
        super().__init__(argv)

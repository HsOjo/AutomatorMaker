import typing

from pyojo.tools.shell import init_app_shell

from .base import BaseApplication
from .main import MainWindow


class Application(BaseApplication):
    main_window_cls = MainWindow

    def __init__(self, argv: typing.List[str]):
        super().__init__(argv)
        app_shell = init_app_shell()
        app_shell.fix_encoding()

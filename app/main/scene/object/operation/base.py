from PyQt5.QtGui import QColor


class BaseOperation:
    def __init__(self, event):
        self._event = event
        self._color_focus = QColor(255, 128, 0)
        self._color_unfocus = QColor(255, 255, 0)
        self._callback_modified = None

    def update(self):
        pass

    def draw(self):
        pass

    @property
    def event(self):
        return self._event

    @property
    def params(self) -> dict:
        return {}

    def load_params(self, **params):
        for k, v in params.items():
            if hasattr(self, k):
                setattr(self, k, v)

    @property
    def moving(self):
        return False

    @property
    def focus(self):
        return False

    @property
    def color_focus(self):
        return self._color_focus

    @property
    def color_unfocus(self):
        return self._color_unfocus

    def set_focus_color(self, focus=None, unfocus=None):
        pass

    def set_focus(self, b: bool):
        pass

    def check_point(self, x, y):
        return False

    def set_callback_modified(self, func):
        self._callback_modified = func

    def _sub_callback_modified(self):
        func = self._callback_modified
        if func is not None:
            func(self)

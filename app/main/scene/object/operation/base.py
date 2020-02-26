from PyQt5.QtGui import QColor


class BaseOperation:
    def __init__(self, event):
        self._event = event
        self._focus = False
        self._moving = False
        self._color_focus = QColor(255, 128, 0)
        self._color_unfocus = QColor(255, 255, 0)
        self._callback_moving = None

    def update(self):
        pass

    def draw(self):
        pass

    @property
    def params(self) -> dict:
        return {}

    def load_params(self, **params):
        for k, v in params.items():
            if hasattr(self, k):
                setattr(self, k, v)

    @property
    def moving(self):
        return self._moving

    @property
    def focus(self):
        return self._focus

    @property
    def color_focus(self):
        return self._color_focus

    @property
    def color_unfocus(self):
        return self._color_unfocus

    def set_focus_color(self, focus=None, unfocus=None):
        if focus is not None:
            self._color_focus = focus
        if unfocus is not None:
            self._color_unfocus = unfocus

    def set_focus(self, b: bool):
        self._focus = b

    def set_callback_moving(self, func):
        self._callback_moving = func

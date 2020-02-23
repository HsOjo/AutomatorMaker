from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QMouseEvent


class Button:
    def __init__(self, name, debug=False):
        self._name = name
        self._down = False
        self._press = False
        self._release = False
        self._debug = debug

    @property
    def down(self):
        return self._down

    @property
    def press(self):
        return self._press

    @property
    def release(self):
        return self._release

    @down.setter
    def down(self, b: bool):
        if b and self._debug:
            print(self._name, 'down')
        self._down = b

    @press.setter
    def press(self, b: bool):
        if b and self._debug:
            print(self._name, 'press')
        self._press = b

    @release.setter
    def release(self, b: bool):
        if b and self._debug:
            print(self._name, 'release')
        self._release = b


class Mouse:
    STAT_PRESS = 0
    STAT_RELEASE = 1
    BUTTON_LEFT = 0
    BUTTON_RIGHT = 1
    MAP_BUTTONS = {
        Qt.LeftButton: ['left'],
        Qt.RightButton: ['right'],
        Qt.MiddleButton: ['mid'],
        Qt.LeftButton | Qt.RightButton: ['left', 'right'],
        Qt.LeftButton | Qt.MidButton: ['left', 'mid'],
        Qt.MidButton | Qt.RightButton: ['mid', 'right'],
        Qt.LeftButton | Qt.MidButton | Qt.RightButton: ['left', 'mid', 'right'],
    }
    ALL_BUTTONS = ['left', 'right', 'mid']

    def __init__(self, event):
        self._position = QPoint(0, 0)
        self._buttons = dict((b, Button(b, debug=event['debug']())) for b in self.ALL_BUTTONS)
        self._event = event

    def update(self, e: QMouseEvent, status=None):
        self._position = e.pos()
        btns = self.MAP_BUTTONS.get(e.buttons())
        if status == self.STAT_PRESS and btns is not None:
            for k in btns:
                btn = self._buttons[k]
                if not btn.press:
                    btn.down = True
                    btn.press = True
        elif status == self.STAT_RELEASE or btns is None:
            btns = [btn for btn in self.ALL_BUTTONS if btn not in btns] if btns is not None else self.ALL_BUTTONS
            for k in btns:
                btn = self._buttons[k]
                if btn.press:
                    btn.press = False
                    btn.release = True

    def reset(self):
        for k in self.ALL_BUTTONS:
            btn = self._buttons[k]
            btn.down = False
            btn.release = False

    @property
    def scale(self) -> float:
        return self._event['scale']()

    def down(self, btn):
        return self._buttons[btn].down

    def press(self, btn):
        return self._buttons[btn].press

    def release(self, btn):
        return self._buttons[btn].release

    @property
    def position(self):
        return self.x, self.y

    @property
    def x(self):
        return self._position.x() / self.scale

    @property
    def y(self):
        return self._position.y() / self.scale

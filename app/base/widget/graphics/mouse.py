from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QMouseEvent


class Mouse:
    STAT_PRESS = 0
    STAT_RELEASE = 1

    def __init__(self):
        self._position = QPoint(0, 0)

        self._down = False
        self._press = False
        self._release = False

    def update(self, e: QMouseEvent, status=None):
        self._position = e.pos()
        if status == self.STAT_PRESS:
            if not self._press:
                self._down = True
            self._press = True
        elif status == self.STAT_RELEASE:
            self._press = False
            self._release = True

    def reset(self):
        self._down = False
        self._release = False

    @property
    def down(self):
        return self._down

    @property
    def press(self):
        return self._press

    @property
    def release(self):
        return self._release

    @property
    def position(self):
        return self._position

    @property
    def x(self):
        return self._position.x()

    @property
    def y(self):
        return self._position.y()

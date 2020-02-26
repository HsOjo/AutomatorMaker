from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QColor, QPen


class Node:
    def __init__(self, event: dict):
        self._event = event
        self._color = QColor(255, 255, 255)
        self._pen = QPen(self._color)
        self._position = QPoint(0, 0)
        self._scale_available = True

    @property
    def debug(self):
        debug = self._event.get('debug')
        if debug is not None:
            return debug()
        return False

    @property
    def pen(self):
        return self._pen

    @property
    def event(self):
        return self._event

    @property
    def x(self):
        return self._position.x()

    @property
    def y(self):
        return self._position.y()

    @property
    def position(self):
        return self.x, self.y

    @property
    def color(self):
        return self._color

    @property
    def scale_available(self):
        return self._scale_available

    @property
    def scale(self) -> float:
        return self._event['scale']() if self._scale_available else 1

    @property
    def painter(self) -> QPainter:
        return self._event['painter']()

    def set_scale_available(self, b: bool):
        self._scale_available = b

    def set_position(self, x=None, y=None):
        if x is not None:
            self._position.setX(x)
        if y is not None:
            self._position.setY(y)

    def set_color(self, color: QColor):
        if color is not None:
            self._color = color
            self._pen.setColor(color)

    def draw(self):
        p = self.painter
        p.setPen(self._pen)

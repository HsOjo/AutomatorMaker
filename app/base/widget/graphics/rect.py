from PyQt5.QtCore import QRect

from .node import Node


class Rect(Node):
    def __init__(self, event: dict, x=0, y=0, w=0, h=0):
        super().__init__(event)
        self._rect = QRect(x, y, w, h)

    @property
    def x(self):
        return self._rect.x()

    @property
    def y(self):
        return self._rect.y()

    @property
    def w(self):
        return self._rect.width()

    @property
    def h(self):
        return self._rect.height()

    @property
    def rect(self):
        return self._rect

    @property
    def size(self):
        return self.w, self.h

    def set_size(self, w=None, h=None):
        if w is not None:
            self._rect.setWidth(w)
        if h is not None:
            self._rect.setHeight(h)

    def set_position(self, x=None, y=None):
        super().set_position(x, y)
        if x is not None:
            self._rect.setX(x)
        if y is not None:
            self._rect.setY(y)

    def draw(self):
        super().draw()
        p = self.painter
        s = self.scale
        if s == 1:
            p.drawRect(self._rect)
        else:
            size = [self.x * s, self.y * s, self.w * s, self.h * s]
            size = [int(i) for i in size]
            p.drawRect(*size)

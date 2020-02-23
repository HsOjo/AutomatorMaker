from PyQt5.QtCore import QRect, QSize

from .node import Node


class Rect(Node):
    def __init__(self, event: dict, x=0, y=0, w=0, h=0):
        super().__init__(event)
        self._rect = QRect(x, y, w, h)

    @property
    def rect(self):
        return self._rect

    def set_size(self, w, h):
        self._rect.setSize(QSize(w, h))

    def set_position(self, x=None, y=None):
        if x is not None:
            self._rect.setX(x)
        if y is not None:
            self._rect.setX(y)
        super().set_position(x, y)

    def draw(self):
        p = self.painter
        p.setPen(self._pen)
        p.drawRect(self._rect)

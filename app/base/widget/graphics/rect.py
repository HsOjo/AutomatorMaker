from PyQt5.QtCore import QRect, QPoint

from .node import Node


class Rect(Node):
    def __init__(self, event: dict, x=0, y=0, w=0, h=0):
        super().__init__(event)
        self._rect = QRect(x, y, w, h)

    def copy(self):
        rect = self.__class__(self.event, *self)
        rect.set_color(self._color)
        rect.set_scale_available(self._scale_available)
        return rect

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

    def check_rect(self, x, y, w, h):
        return self._rect.intersects(QRect(x, y, w, h))

    def check_point(self, x, y):
        return self._rect.contains(QPoint(x, y))

    def set_size(self, w=None, h=None, convert_negative=False):
        if w is not None:
            if convert_negative and w < 0:
                w = abs(w)
                self._rect.setX(self.x - w)
            self._rect.setWidth(w)
        if h is not None:
            if convert_negative and h < 0:
                h = abs(h)
                self._rect.setY(self.y - h)
            self._rect.setHeight(h)

    def set_position(self, x=None, y=None):
        if x is not None:
            w = self.w
            self._rect.setX(x)
            self._rect.setWidth(w)
        if y is not None:
            h = self.h
            self._rect.setY(y)
            self._rect.setHeight(h)

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

    def __iter__(self):
        # Support unpack.
        for i in [self.x, self.y, self.w, self.h]:
            yield i

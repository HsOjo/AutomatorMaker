from PyQt5.QtGui import QPixmap, QColor

from .node import Node
from .rect import Rect


class Sprite(Node):
    def __init__(self, event: dict, img_data: bytes = None):
        super().__init__(event)
        self._pixmap = QPixmap()
        if img_data is not None:
            self.set_image(img_data)
        self._rect = Rect(event)

    @property
    def pixmap(self):
        return self._pixmap

    @property
    def rect(self):
        return self._rect

    def set_size(self, w, h):
        self._rect.set_size(w, h)

    def set_image(self, img_data: bytes):
        self._pixmap.loadFromData(img_data)
        w, h = self._pixmap.width(), self._pixmap.height()
        self.rect.set_size(w, h)

    def set_position(self, x=None, y=None):
        self._rect.set_position(x, y)
        super().set_position(x, y)

    def set_color(self, color: QColor):
        self._rect.set_color(color)
        super().set_color(color)

    def set_scale_available(self, b: bool):
        super().set_scale_available(b)
        self._rect.set_scale_available(b)

    def draw(self):
        super().draw()
        p = self.painter
        s = self.scale
        if s == 1:
            p.drawPixmap(self._rect.rect, self._pixmap)
        else:
            size = [int(i * s) for i in self._rect]
            p.drawPixmap(*size, self._pixmap)

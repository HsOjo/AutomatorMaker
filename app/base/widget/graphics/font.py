from PyQt5.QtGui import QColor, QFont, QPen

from .node import Node
from .rect import Rect


class Font(Node):
    BORDER_MODE_2 = [(-1, -1), (1, 1)]
    BORDER_MODE_4 = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    BORDER_MODE_8 = [(-1, -1), (0, 1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    def __init__(self, event: dict, name='', font_size=11):
        super().__init__(event)
        self._font = QFont(name, font_size)
        self._font_size = font_size
        self._rect = Rect(event, h=font_size)
        self._text = ''
        self._flags = 0
        self._w = 0
        self._h = 0
        self._cut = False

        self._border_pen = QPen(QColor(0, 0, 0))
        self._border_mode = None

    @property
    def font_size(self):
        return self._font_size

    @property
    def rect(self):
        return self._rect

    @property
    def size(self):
        return self._w, self._h

    @property
    def draw_size(self):
        return self._rect.size

    def set_font_size(self, size, px=False):
        self._font_size = size
        if px:
            self._font_size = px_to_pt(px)

    def set_draw_size(self, w=None, h=None):
        self._cut = w is None and h is None
        if self._cut:
            self._rect.set_size(*self.size)
        else:
            self._rect.set_size(w, h)

    def set_text(self, text: str):
        px = pt_to_px(self._font_size)
        self._text = text
        self._w = max([count_text_size(line) * px for line in text.splitlines()]) * 1.125
        self._h = px * (text.count('\n') + 1) * 1.125
        if not self._cut:
            self._rect.set_size(*self.size)

    def set_position(self, x=None, y=None):
        super().set_position(x, y)
        self._rect.set_position(x, y)

    def set_border_color(self, color: QColor):
        self._border_pen.setColor(color)

    def set_border_mode(self, mode):
        self._border_mode = mode

    def set_color(self, color: QColor):
        super().set_color(color)
        self._rect.set_color(color)

    def set_flags(self, flags):
        self._flags = flags

    def set_scale_available(self, b: bool):
        super().set_scale_available(b)
        self._rect.set_scale_available(b)

    def draw(self):
        super().draw()
        p = self.painter
        p.setFont(self._font)
        s = self.scale

        self._font.setPointSize(self._font_size * s)
        self.draw_border()
        if s == 1:
            p.drawText(self._rect.rect, 0, self._text)
        else:
            size = [int(i * s) for i in self._rect]
            p.drawText(*size, 0, self._text)

    def draw_border(self):
        p = self.painter
        s = self.scale
        pen = p.pen()
        p.setPen(self._border_pen)
        if self._border_mode is not None:
            p.setPen(self._border_pen)
            x, y = self.position
            for ox, oy in self._border_mode:
                size = [x + ox, y + oy, *self.rect.size]
                size = [int(i * s) for i in size]
                p.drawText(*size, 0, self._text)
        p.setPen(pen)


def count_text_size(text):
    small = 0
    large = 0
    for item in text:
        if 0x4E00 <= ord(item) <= 0x9FA5:
            large += 1
        else:
            small += 1
    return (small * 1.2 + large * 2) / 3


def pt_to_px(pt):
    px = pt / (3 / 4)
    return px


def px_to_pt(px):
    pt = px * (3 / 4)
    return pt

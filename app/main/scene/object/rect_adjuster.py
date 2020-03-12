from PyQt5.QtGui import QColor
from ojoqt.widget.graphics import Rect, Mouse

from app.utils import list_math


class RectAdjuster:
    COLOR_NORMAL = QColor(255, 255, 255)
    COLOR_HOVER = QColor(255, 255, 0)

    def __init__(self, event, size=8):
        self._event = event
        self._rects = [Rect(event) for _ in range(8)]
        self._lu, self._u, self._ru, self._l, self._r, self._ld, self._d, self._rd = self._rects  # type: Rect
        self._adjuster = None  # type:Rect
        self._adjusting = False
        self._rect = None  # type:Rect
        self._rect_bak = None  # type:Rect
        self._callback_adjust = None
        self.set_size(size)

    @property
    def adjusting(self):
        return self._adjusting

    def set_size(self, w, h=None):
        if h is None:
            h = w
        for rect in self._rects:
            rect.set_size(w, h)

    def move(self, rect, x, y):
        rect.set_position(x - rect.w / 2, y - rect.h / 2)

    def adjust(self, rect: Rect):
        self._rect = rect
        x, y, w, h = rect
        w2, h2 = list_math.divide([w, h], [2, 2])
        self.move(self._lu, x, y)
        self.move(self._u, x + w2, y)
        self.move(self._ru, x + w, y)
        self.move(self._l, x, y + h2)
        self.move(self._r, x + w, y + h2)
        self.move(self._ld, x, y + h)
        self.move(self._d, x + w2, y + h)
        self.move(self._rd, x + w, y + h)

    def update(self):
        mouse = self._event['mouse']()  # type: Mouse
        mouse_l = mouse.button(mouse.BUTTON_LEFT)

        if self._adjusting:
            if self._adjuster == self._lu:
                self._rect.set_position(*mouse.position)
                self._rect.set_size(*list_math.add(
                    self._rect_bak.size, list_math.reduce(self._rect_bak.position, mouse.position)
                ))
            elif self._adjuster == self._u:
                self._rect.set_position(y=mouse.y)
                self._rect.set_size(h=self._rect_bak.h + self._rect_bak.y - mouse.y)
            elif self._adjuster == self._ru:
                self._rect.set_position(y=mouse.y)
                self._rect.set_size(mouse.x - self._rect_bak.x, self._rect_bak.y - mouse.y + self._rect_bak.h)
            elif self._adjuster == self._l:
                self._rect.set_position(x=mouse.x)
                self._rect.set_size(w=self._rect_bak.w + self._rect_bak.x - mouse.x)
            elif self._adjuster == self._r:
                self._rect.set_size(w=mouse.x - self._rect_bak.x)
            elif self._adjuster == self._ld:
                self._rect.set_position(x=mouse.x)
                self._rect.set_size(self._rect_bak.w + self._rect_bak.x - mouse.x, mouse.y - self._rect_bak.y)
            elif self._adjuster == self._d:
                self._rect.set_size(h=mouse.y - self._rect_bak.y)
            elif self._adjuster == self._rd:
                self._rect.set_size(w=mouse.x - self._rect_bak.x, h=mouse.y - self._rect_bak.y)

            if mouse_l.release:
                self._adjusting = False
                if self._callback_adjust is not None:
                    self._callback_adjust(self._adjusting)
                self._rect.set_size(*self._rect.size, convert_negative=True)
                self.adjust(self._rect)
        else:
            self._adjuster = None
            for rect in self._rects:
                if rect.check_point(*mouse.position):
                    rect.set_color(self.COLOR_HOVER)
                    self._adjuster = rect
                else:
                    rect.set_color(self.COLOR_NORMAL)

            if mouse_l.down:
                if self._adjuster is not None:
                    self._rect_bak = self._rect.copy()
                    self._adjusting = True
                    if self._callback_adjust is not None:
                        self._callback_adjust(self._adjusting)

    def draw(self):
        if not self._adjusting:
            for rect in self._rects:
                rect.draw()

    def set_callback_adjust(self, func):
        self._callback_adjust = func

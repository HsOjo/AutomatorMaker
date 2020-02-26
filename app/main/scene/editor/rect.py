from typing import Dict

from PyQt5.QtGui import QColor

from app.base.widget.graphics import Rect
from .base import BaseEditor
from ..object import AdvanceRect


class RectEditor(BaseEditor):
    COLOR_NEW = QColor(0, 255, 0)
    COLOR_UNFOCUS = QColor(255, 255, 0)
    COLOR_UNFOCUS_MOVING = QColor(255, 255, 0, 128)
    COLOR_FOCUS = QColor(255, 128, 0)

    def __init__(self, event):
        super().__init__(event)
        self._rects = {}  # type: Dict[AdvanceRect]
        self._current_rect = None  # type: AdvanceRect
        self._new_rect = AdvanceRect(self.event)
        self._new_rect.set_focus_color(self.COLOR_NEW, self.COLOR_NEW)

        self._creating = False

    @property
    def rects(self):
        return list(self._rects.keys())

    def select(self, index):
        rects = self.rects
        if 0 <= index < len(rects):
            self.set_current_rect(rects[index], sync=False)

    def set_current_rect(self, rect, sync=True):
        # sync param use by overwrite function.
        if self._current_rect is not None:
            self._current_rect.set_focus(False)

        self._current_rect = rect
        if rect is not None:
            rect.set_focus(True)

    def update(self):
        mouse = self.mouse
        mouse_l = mouse.button(mouse.BUTTON_LEFT)
        rect_new = self._new_rect

        if self._creating:
            rect_new.set_size(mouse.x - rect_new.x, mouse.y - rect_new.y)
            if mouse_l.release:
                self.new_rect()
                self._creating = False
        else:
            for rect in self._rects:
                rect.update()

            if self._current_rect is not None:
                if not self._current_rect.focus:
                    self.set_current_rect(None)

            if self._current_rect is None:
                if mouse_l.down:
                    for rect in reversed(self.rects):
                        if rect.check_point(*mouse.position):
                            self.set_current_rect(rect)
                            break
                    if self._current_rect is None:
                        rect_new.set_position(*mouse.position)
                        rect_new.set_size(0, 0)
                        self._creating = True
                    else:
                        self._current_rect.update()

    def new_rect(self, rect=None, sync=True):
        rect = AdvanceRect(self.event, *(self._new_rect if rect is None else rect))
        rect.set_size(*rect.size, convert_negative=True)
        rect.set_focus_color(self.COLOR_FOCUS, self.COLOR_UNFOCUS)
        rect.set_callback_moving(lambda b: self.callback_rect_moving(rect, b))
        rect.adjuster.set_callback_adjust(lambda b: self.callback_rect_adjust(rect, b))
        if sync and self.add_item(rect):
            self.set_current_rect(rect)

        return rect

    def add_item(self, rect):
        self._rects[rect] = None
        return True

    def draw(self):
        for rect in self._rects:
            rect.draw()
        if self._creating:
            self._new_rect.draw()

    def callback_rect_modified(self, rect: AdvanceRect):
        pass

    def callback_rect_moving(self, rect_moving: AdvanceRect, moving: bool):
        if not moving:
            self.callback_rect_modified(rect_moving)
        for rect in self._rects:
            if moving:
                if rect != rect_moving:
                    rect.set_color(self.COLOR_UNFOCUS_MOVING)
            else:
                if rect != rect_moving:
                    rect.set_color(self.COLOR_UNFOCUS)

    def callback_rect_adjust(self, rect_adjust: AdvanceRect, adjust: bool):
        if not adjust:
            rect_adjust.set_size(*rect_adjust.size, convert_negative=True)
            self.callback_rect_modified(rect_adjust)

    def callback_item_edited(self, edited_item):
        for rect, item in self._rects.items():
            if edited_item == item:
                x, y, w, h = item.rect
                rect.set_position(x, y)
                rect.set_size(w, h)
                rect.adjuster.adjust(rect)
                break

    def callback_item_deleted(self, deleted_item):
        for rect, item in self._rects.items():
            if deleted_item == item:
                self._rects.pop(rect)
                if rect == self._current_rect:
                    self.set_current_rect(None)
                break

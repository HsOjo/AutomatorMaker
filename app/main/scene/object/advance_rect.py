from PyQt5.QtGui import QColor

from app.base.widget.graphics import Rect, Mouse
from app.utils import list_math
from .rect_adjuster import RectAdjuster


class AdvanceRect(Rect):
    def __init__(self, event: dict, *rect):
        super().__init__(event, *rect)
        self._event = event
        self._adjuster = RectAdjuster(event)
        self._adjuster.adjust(self)
        self._focus = False
        self._moving = False
        self._backup = None  # type:AdvanceRect
        self._color_focus = QColor(255, 128, 0)
        self._color_unfocus = QColor(255, 255, 0)
        self._callback_moving = None

    def copy(self):
        rect = super().copy()  # type:AdvanceRect
        rect._adjuster.adjust(rect)
        return rect

    @property
    def adjuster(self):
        return self._adjuster

    @property
    def moving(self):
        return self._moving

    @property
    def focus(self):
        return self._focus

    @property
    def color_focus(self):
        return self._color_focus

    @property
    def color_unfocus(self):
        return self._color_unfocus

    def set_focus_color(self, focus=None, unfocus=None):
        if focus is not None:
            self._color_focus = focus
        if unfocus is not None:
            self._color_unfocus = unfocus
        self.set_color(focus if self._focus else unfocus)

    def set_focus(self, b: bool):
        self._focus = b
        self.set_color(self._color_focus if b else self._color_unfocus)

    def set_callback_moving(self, func):
        self._callback_moving = func

    def update(self):
        mouse = self._event['mouse']()  # type: Mouse
        mouse_l = mouse.button(mouse.BUTTON_LEFT)

        if self._focus:
            self._adjuster.update()
            if not self._adjuster.adjusting:
                if self._moving:
                    self.set_position(*list_math.add(
                        self._backup.position, list_math.reduce(mouse.position, mouse_l.down_position)
                    ))
                    if mouse_l.release:
                        self._adjuster.adjust(self)
                        self._moving = False
                        if self._callback_moving is not None:
                            self._callback_moving(self._moving)
                else:
                    if mouse_l.down:
                        if self.check_point(*mouse.position):
                            self._backup = self.copy()
                            self._moving = True
                            if self._callback_moving is not None:
                                self._callback_moving(self._moving)
                        else:
                            self._focus = False

    def draw(self):
        super().draw()
        if self._focus and not self._moving:
            self._adjuster.draw()

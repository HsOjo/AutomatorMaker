from app.base.utils import point_math
from app.base.widget.graphics import Line, Font
from app.utils import list_math
from .base import BaseOperation
from ..advance_circle import AdvanceCircle


class SwipeOperation(BaseOperation):
    def __init__(self, event):
        super().__init__(event)
        self._font = Font(event)
        self._font.set_text('Swipe')
        self._circle_start = AdvanceCircle(event)
        self._circle_end = AdvanceCircle(event)
        self._circle_start.set_callback_moving(self._sub_callback_moving)
        self._circle_end.set_callback_moving(self._sub_callback_moving)
        self._line_link = Line(event)
        self._time = 1

    @property
    def circle_start(self):
        return self._circle_start

    @property
    def circle_end(self):
        return self._circle_end

    def update(self):
        self._circle_start.update()
        self._circle_end.update()

        ps, pe = self._circle_start.position, self._circle_end.position
        rs, re = self._circle_start.radius, self._circle_end.radius
        ps = point_math.move(*ps, rs, point_math.angle(*ps, *pe))
        pe = point_math.move(*pe, re, point_math.angle(*pe, *ps))
        self._line_link.set_position(*ps)
        self._line_link.set_position_end(*pe)

        p = list_math.reduce(self._circle_end.position, list_math.divide(self._font.draw_size, [2, 2]))
        self._font.set_position(*p)

        if self.focus:
            self._circle_start.set_color(self.color_focus)
            self._circle_end.set_color(self.color_focus)

    def draw(self):
        self._line_link.draw()
        self._circle_start.draw()
        self._circle_end.draw()
        self._font.draw()

    @property
    def params(self) -> dict:
        params = self._params.copy()
        ox, oy = self._origin.x(), self._origin.y()
        params.update(dict(
            start_x=self._circle_start.x - ox,
            start_y=self._circle_start.y - oy,
            end_x=self._circle_end.x - ox,
            end_y=self._circle_end.y - oy,
            time=self._time,
        ))
        return params

    def load_params(self, origin, **params):
        super().load_params(origin, **params)
        ox, oy = self._origin.x(), self._origin.y()
        start_x = params.get('start_x') + ox
        start_y = params.get('start_y') + oy
        end_x = params.get('end_x') + ox
        end_y = params.get('end_y') + oy
        self._time = params.get('time', self._time)
        self._circle_start.set_position(start_x, start_y)
        self._circle_end.set_position(end_x, end_y)

    def check_point(self, x, y):
        return self._circle_start.check_point(x, y) or self._circle_end.check_point(x, y)

    @property
    def focus(self):
        return self._circle_start.focus or self._circle_end.focus

    def set_focus(self, b: bool):
        self._circle_start.set_focus(b)
        self._circle_end.set_focus(b)

    def set_focus_color(self, focus=None, unfocus=None):
        self._circle_start.set_focus_color(focus, unfocus)
        self._circle_end.set_focus_color(focus, unfocus)

    def set_color(self, color=None):
        self._circle_start.set_color(color)
        self._circle_end.set_color(color)

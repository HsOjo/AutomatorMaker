from app.base.widget.graphics import Font
from app.utils import list_math
from .base import BaseOperation
from ..advance_circle import AdvanceCircle


class TapOperation(BaseOperation):
    def __init__(self, event):
        super().__init__(event)
        self._count = 1
        self._font = Font(event)
        self._font.set_text('Tap')
        self._circle = AdvanceCircle(event)
        self._circle.set_callback_moving(self._sub_callback_moving)
        self._press_time = 100

    @property
    def circle(self):
        return self._circle

    def update(self):
        self._circle.update()
        p = list_math.reduce(self._circle.position, list_math.divide(self._font.draw_size, [2, 2]))
        self._font.set_position(*p)

    def draw(self):
        self._font.draw()
        self._circle.draw()

    @property
    def params(self) -> dict:
        params = self._params.copy()
        params.update(dict(
            x=self._circle.x - self._origin.x(),
            y=self._circle.y - self._origin.y(),
            count=self._count,
            press_time=self._press_time,
        ))
        return params

    def load_params(self, origin, **params):
        super().load_params(origin, **params)
        x = params.get('x') + self._origin.x()
        y = params.get('y') + self._origin.y()
        self._circle.set_position(x, y)
        self._count = params.get('count')
        self._press_time = params.get('press_time')

    def check_point(self, x, y):
        return self._circle.check_point(x, y)

    @property
    def focus(self):
        return self._circle.focus

    def set_focus(self, b: bool):
        self._circle.set_focus(b)

    def set_focus_color(self, focus=None, unfocus=None):
        self._circle.set_focus_color(focus, unfocus)

    def set_color(self, color=None):
        self._circle.set_color(color)

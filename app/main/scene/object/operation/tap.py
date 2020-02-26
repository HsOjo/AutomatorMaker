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
        self._circle.set_callback_moving(lambda moving: self._sub_callback_modified() if not moving else None)

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
        return dict(
            x=self._circle.x,
            y=self._circle.y,
            count=self._count,
        )

    def load_params(self, **params):
        x = params.get('x')
        y = params.get('y')
        self._circle.set_position(x, y)
        self._count = params.get('count')

    def check_point(self, x, y):
        return self._circle.check_point(x, y)

    @property
    def focus(self):
        return self._circle.focus

    def set_focus(self, b: bool):
        self._circle.set_focus(b)

    def set_focus_color(self, focus=None, unfocus=None):
        self._circle.set_focus_color(focus, unfocus)

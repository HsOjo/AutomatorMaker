from .base import BaseOperation
from ..advance_circle import AdvanceCircle


class TapOperation(BaseOperation):
    def __init__(self, event):
        super().__init__(event)
        self._circle = AdvanceCircle(event)

    @property
    def circle(self):
        return self._circle

    def update(self):
        self._circle.update()

    def draw(self):
        self._circle.draw()

    @property
    def params(self) -> dict:
        return dict(
            x=self._circle.x,
            y=self._circle.y,
        )

    def load_params(self, **params):
        x = params.get('x')
        y = params.get('y')
        self._circle.set_position(x, y)

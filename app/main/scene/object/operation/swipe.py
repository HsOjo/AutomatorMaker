from .base import BaseOperation
from ..advance_circle import AdvanceCircle


class SwipeOperation(BaseOperation):
    def __init__(self, event):
        super().__init__(event)
        self._circle_start = AdvanceCircle(event)
        self._circle_end = AdvanceCircle(event)
        self._time = 1


    def update(self):
        self._circle_start.update()
        self._circle_end.update()

    def draw(self):
        self._circle_start.draw()
        self._circle_end.draw()

    @property
    def params(self) -> dict:
        return dict(
            start_x=self._circle_start.x,
            start_y=self._circle_start.y,
            end_x=self._circle_end.x,
            end_y=self._circle_end.y,
        )

    def load_params(self, **params):
        start_x = params.get('start_x')
        start_y = params.get('start_y')
        end_x = params.get('end_x')
        end_y = params.get('end_y')
        self._time = params.get('time', self._time)
        self._circle_start.set_position(start_x, start_y)
        self._circle_end.set_position(end_x, end_y)

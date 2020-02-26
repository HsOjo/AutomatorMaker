from .base import BaseOperation
from ..advance_circle import AdvanceCircle


class PressOperation(BaseOperation):
    def __init__(self, event):
        super().__init__(event)
        self._circle = AdvanceCircle(event)

    def update(self):
        self._circle.update()

    def draw(self):
        self._circle.draw()

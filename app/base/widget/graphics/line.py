from PyQt5.QtCore import QPoint

from .node import Node


class Line(Node):
    def __init__(self, event: dict):
        super().__init__(event)
        self._position_end = QPoint(0, 0)

    @property
    def x_end(self):
        return self._position_end.x()

    @property
    def y_end(self):
        return self._position_end.y()

    @property
    def position_end(self):
        return self.x_end, self.y_end

    def set_position_end(self, x=None, y=None):
        if x is not None:
            self._position_end.setX(x)
        if y is not None:
            self._position_end.setY(y)

    def draw(self):
        super().draw()
        p = self.painter
        s = self.scale
        if s == 1:
            p.drawLine(self._position, self._position_end)
        else:
            points = [self.x * s, self.y * s, self.x_end * s, self.y_end * s]
            points = [int(i) for i in points]
            p.drawLine(*points)

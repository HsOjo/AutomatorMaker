from .node import Node
from ...common import point_distance


class Circle(Node):
    def __init__(self, event: dict, x=0, y=0, radius=0):
        super().__init__(event)
        self._radius = radius
        self.set_position(x, y)

    def set_radius(self, radius):
        self._radius = radius

    def check_point(self, x, y):
        return point_distance(*self.position, x, y) < self._radius

    def copy(self):
        circle = Circle(self.event, *self.position, self._radius)
        circle.set_color(self.color)
        circle.set_scale_available(self.scale_available)
        return circle

    @property
    def radius(self):
        return self._radius

    def draw(self):
        p = self.painter
        r = self._radius
        p.drawEllipse(*self.position, r, r)

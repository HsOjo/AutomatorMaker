from .node import Node
from ...common import point_distance


class Circle(Node):
    def __init__(self, event: dict, x=0, y=0, radius=0):
        super().__init__(event)
        self._radius = radius
        self._ox, self._oy = 0, 0
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

    def set_origin(self, x=None, y=None):
        if x is None:
            self._ox = self._radius / 2
        if y is None:
            self._oy = self._radius / 2

    @property
    def origin(self):
        return self._ox, self._oy

    def draw(self):
        super().draw()
        s = self.scale
        p = self.painter
        r = self._radius
        if s == 1:
            x, y = self.position
            p.drawEllipse(x - self._ox, y - self._oy, r, r)
        else:
            r = r * s
            p.drawEllipse((self.x - self._ox) * s, (self.y - self._oy) * s, r, r)

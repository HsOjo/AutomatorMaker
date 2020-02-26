from .node import Node
from ...utils import point_math


class Circle(Node):
    def __init__(self, event: dict, x=0, y=0, radius=0):
        super().__init__(event)
        self._radius = radius
        self._ox, self._oy = None, None
        self.set_position(x, y)

    def set_radius(self, radius):
        self._radius = radius

    def check_point(self, x, y):
        px, py = self.position
        return point_math.distance(px, py, x, y) < self._radius

    def copy(self):
        circle = Circle(self.event, *self.position, self._radius)
        circle.set_color(self.color)
        circle.set_scale_available(self.scale_available)
        circle.set_origin(self._ox, self._oy)
        return circle

    @property
    def radius(self):
        return self._radius

    def set_origin(self, x=None, y=None):
        self._ox, self._oy = x, y

    @property
    def origin(self):
        r = self._radius
        ox = self._ox if self._ox is not None else r
        oy = self._oy if self._oy is not None else r
        return ox, oy

    def draw(self):
        super().draw()
        s = self.scale
        p = self.painter
        r = self._radius * 2
        ox, oy = self.origin

        if s == 1:
            x, y = self.position
            p.drawEllipse(x - ox, y - oy, r, r)
        else:
            r = r * s
            p.drawEllipse((self.x - ox) * s, (self.y - oy) * s, r, r)

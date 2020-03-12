from ojoqt.utils import point_math
from ojoqt.widget.graphics import Circle, Mouse
from ojoqt.widget.graphics import Line


class MouseIndicator:
    def __init__(self, event, color_origin, color_mouse, radius, press_time, swipe_distance):
        self._event = event
        self._radius = radius
        self._press_time = press_time
        self._swipe_distance = swipe_distance

        self._circle_origin = Circle(event)
        self._circle_origin.set_color(color_origin)
        self._circle_origin.pen.setWidth(2)

        self._circle_mouse = Circle(event)
        self._circle_mouse.set_color(color_mouse)
        self._circle_mouse.pen.setWidth(2)

        self._line_mouse = Line(event)

    @property
    def mouse(self) -> Mouse:
        return self._event['mouse']()

    def update(self):
        mouse = self.mouse
        mouse_l = mouse.button(mouse.BUTTON_LEFT)

        if mouse_l.press:
            p = min(mouse_l.press_time, self._press_time) / self._press_time

            rn = p * self._radius
            self._circle_mouse.set_radius(rn)
            self._circle_origin.set_radius(rn / 2)

            self._circle_mouse.set_position(*mouse.position)
            self._circle_origin.set_position(*mouse_l.down_position)

            ps, pe = self._circle_origin.position, self._circle_mouse.position
            ps = point_math.move(*ps, self._circle_origin.radius, point_math.angle(*ps, *pe))
            pe = point_math.move(*pe, self._circle_mouse.radius, point_math.angle(*pe, *ps))
            self._line_mouse.set_position(*ps)
            self._line_mouse.set_position_end(*pe)

    def draw(self):
        mouse = self.mouse
        mouse_l = mouse.button(mouse.BUTTON_LEFT)
        if mouse_l.press:
            if mouse_l.press_distance > self._swipe_distance:
                self._line_mouse.draw()
            self._circle_origin.draw()
            self._circle_mouse.draw()

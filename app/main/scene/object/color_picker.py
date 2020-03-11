from PyQt5.QtGui import QImage, QColor

from app.base.widget.graphics import Mouse, Circle, Line


class ColorPicker:
    CIRCLE_RADIUS = 16
    CIRCLE_WIDTH = 4

    def __init__(self, event):
        self._event = event
        self._line = Line(self._event)
        self._circle = Circle(self._event, radius=self.CIRCLE_RADIUS)
        self._circle.pen.setWidth(self.CIRCLE_WIDTH)
        self._visible = False
        self._color = QColor(255, 255, 255)

    @property
    def color(self):
        return self._color

    def update(self):
        mouse = self._event['mouse']()  # type: Mouse
        screen_image = self._event['screen_image']()  # type: QImage
        show_status = self._event['show_status']

        x, y = mouse.position
        self._circle.set_position(x, y)

        self._visible = screen_image is not None and mouse.button(mouse.BUTTON_RIGHT).press
        if self._visible:
            w, h = screen_image.width(), screen_image.height()
            if 0 <= x < w and 0 <= y < h:
                color = screen_image.pixelColor(x, y)
                r, g, b, a = color.red(), color.green(), color.blue(), color.alpha()
                show_status('Mouse: %a Color: %a' % ((x, y), (r, g, b, a)))
                self._circle.set_color(color)
                self._line.set_color(color)
                self._color = color

    def draw(self):
        if self._visible:
            mouse = self._event['mouse']()  # type: Mouse

            x, y = mouse.position
            r = self._circle.radius

            sx, sy, ex, ey = x, y - r, x, y + r
            self._line.set_position(sx, sy)
            self._line.set_position_end(ex, ey)
            self._line.draw()

            sx, sy, ex, ey = x - r, y, x + r, y
            self._line.set_position(sx, sy)
            self._line.set_position_end(ex, ey)
            self._line.draw()

            self._circle.draw()

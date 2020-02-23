from PyQt5.QtGui import QColor

from app.base.widget import GraphicsWidget


class SceneWidget(GraphicsWidget):
    def __init__(self, parent=None, refresh_rate=60, **kwargs):
        super().__init__(parent, refresh_rate)
        self.screen = self.new.sprite()
        self.r = self.new.rect()
        self.r.set_color(QColor(255, 0, 0))
        self.f = self.new.font()
        self.f.set_color(QColor(0, 255, 0))
        self.f.set_position(8, 16)
        self.f.set_border_mode(self.f.BORDER_MODE_4)

    def set_screen(self, img_data):
        self.screen.set_image(img_data)
        self.inject_size()

    def inject_size(self):
        pixmap = self.screen.pixmap
        scale = self.scale
        w, h = pixmap.width() * scale, pixmap.height() * scale
        self.setMinimumSize(w, h)

    def set_scale(self, scale: float):
        super().set_scale(scale)
        self.inject_size()

    def callback_resize(self, w, h):
        self.inject_size()

    def callback_update(self):
        self.f.set_text('FPS: %s' % self.fps)
        self.f.set_position(self.width() - 48, self.height() - 24)
        if self.mouse.down('left'):
            self.r.set_position(*self.mouse.position)
        if self.mouse.press('left'):
            x, y = self.r.position
            mx, my = self.mouse.position
            w, h = mx - x, my - y
            self.r.set_size(w, h)

    def callback_draw(self):
        self.screen.draw()
        self.r.draw()
        self.f.rect.draw()
        self.f.draw()

    def callback_focus(self, b: bool):
        self.set_pause(not b)

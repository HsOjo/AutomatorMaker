from PyQt5.QtGui import QColor

from app.base.widget import GraphicsWidget
from app.main.scene.model import SceneModel


class SceneWidget(GraphicsWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.screen = self.new.sprite()
        self.r = self.new.rect()
        self.r.set_color(QColor(255, 0, 0))
        self.f = self.new.font()
        self.f.set_color(QColor(0, 255, 0))
        self.f.set_border_mode(self.f.BORDER_MODE_4)

        self._scene = None

        self.current_feature = None
        self.current_object = None
        self.current_action = None

    def set_scene(self, scene: SceneModel):
        self._scene = scene
        self.current_feature = None
        self.current_object = None
        self.current_action = None
        with open(scene.img_path, 'rb') as io:
            img_data = io.read()
        self.screen.set_image(img_data)
        self.inject_size()

    def inject_size(self):
        pixmap = self.screen.pixmap
        scale = self.scale
        w, h = pixmap.width(), pixmap.height()
        sw, sh = w * scale, h * scale
        self.setMinimumSize(sw, sh)

    def set_scale(self, scale: float):
        super().set_scale(scale)
        self.inject_size()

    def callback_resize(self, w, h):
        self.inject_size()

    def callback_update(self):
        self.f.set_text('FPS: %s' % self.fps)
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

    def select_feature(self, index):
        pass

    def select_object(self, index):
        pass

    def select_action(self, index):
        pass

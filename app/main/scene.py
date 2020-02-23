from app.base.widget import GraphicsWidget


class SceneWidget(GraphicsWidget):
    def __init__(self, parent=None, refresh_rate=60, **kwargs):
        super().__init__(parent, refresh_rate)
        self.screen = self.new.sprite()

    def set_screen(self, img_data):
        self.screen.set_image(img_data)

    def callback_resize(self, w, h):
        pass

    def callback_update(self):
        pass

    def callback_draw(self):
        self.screen.draw()

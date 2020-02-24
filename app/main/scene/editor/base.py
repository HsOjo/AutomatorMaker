from app.base.widget.graphics import Mouse


class BaseEditor:
    def __init__(self, event):
        self._event = event

    @property
    def event(self):
        return self._event

    @property
    def mouse(self) -> Mouse:
        return self._event['mouse']()

    def update(self):
        pass

    def draw(self):
        pass

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

    def select(self, index):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def callback_item_edited(self, item):
        pass

    def callback_item_deleted(self, item):
        pass

    def add_item(self, item):
        pass

    def sync(self):
        pass
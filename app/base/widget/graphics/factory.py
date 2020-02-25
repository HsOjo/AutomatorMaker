from .font import Font
from .rect import Rect
from .sprite import Sprite


class Factory:
    def __init__(self, event):
        self._event = event

    def sprite(self, img_data: bytes = None):
        return Sprite(self._event, img_data)

    def rect(self, x=0, y=0, w=0, h=0):
        return Rect(self._event, x, y, w, h)

    def font(self, name='', size=11):
        return Font(self._event, name, size)

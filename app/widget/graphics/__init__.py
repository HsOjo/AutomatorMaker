from PyQt5.QtGui import QPaintEvent, QPixmap, QPainter
from PyQt5.QtWidgets import QWidget


def _update_size(func):
    def wrapper(self: 'GraphicsWidget', *args, **kwargs):
        result = func(self, *args, **kwargs)
        if self._scale:
            self.setMinimumSize(0, 0)
            self.resize(self.parent().size())
        else:
            self.setMinimumSize(self._pixmap.width(), self._pixmap.height())
            self.resize(self._pixmap.size())
        return result

    return wrapper


class GraphicsWidget(QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._pixmap = QPixmap()
        self._scale = False

    @_update_size
    def set_img(self, img_data: bytes):
        self._pixmap.loadFromData(img_data)

    @_update_size
    def set_scale(self, b: bool):
        self._scale = b

    def paintEvent(self, pe: QPaintEvent) -> None:
        x, y = 0, 0
        w, h = self.width(), self.height()
        pw, ph = self._pixmap.width(), self._pixmap.height()
        if self._scale and pw > w:
            s = w / pw
            pw, ph = pw * s, ph * s
            x, y = w / 2 - pw / 2, h / 2 - ph / 2

        painter = QPainter(self)
        if not painter.isActive():
            painter.begin(self)
        painter.drawPixmap(x, y, pw, ph, self._pixmap)

        painter.end()

import time

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QMouseEvent, QResizeEvent
from PyQt5.QtWidgets import QWidget

from .mouse import Mouse
from .node import Node
from .rect import Rect
from .sprite import Sprite


class Factory:
    def __init__(self, event):
        self._event = event

    def sprite(self, img_data: bytes = None):
        return Sprite(self._event, img_data)

    def rect(self, x, y, w, h):
        return Rect(self._event, x, y, w, h)


class GraphicsWidget(QWidget):
    def __init__(self, parent=None, refresh_rate=60, **kwargs):
        super().__init__(parent, **kwargs)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setMouseTracking(True)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._timer_timeout)

        self._painter = QPainter(self)
        self._refresh_rate = 1000 / refresh_rate
        self._dt = 0
        self._fps = 0
        self._frame_count = 0
        self._frame_count_p = 0
        self._frame_time = 0
        self._event = dict(painter=lambda: self._painter)

        self._mouse = Mouse()
        self.new = Factory(self._event)

    @property
    def dt(self):
        return self._dt

    @property
    def fps(self):
        return self._fps

    @property
    def mouse(self):
        return self._mouse

    @property
    def painter(self):
        return self._painter

    def callback_update(self):
        pass

    def callback_draw(self):
        pass

    def callback_focus(self, b: bool):
        pass

    def callback_resize(self, w, h):
        pass

    def _timer_timeout(self):
        now = time.time()
        self.callback_update()
        self.repaint()
        self._dt = time.time() - now
        self._frame_count += 1
        if now - self._frame_time > 1:
            self._frame_time = now
            self._fps = self._frame_count - self._frame_count_p
            self._frame_count_p = self._frame_count
        self._mouse.reset()

    def resizeEvent(self, re: QResizeEvent):
        super().resizeEvent(re)
        size = re.size()
        self.callback_resize(size.width(), size.height())

    def showEvent(self, *args):
        super().showEvent(*args)
        self._timer.start(self._refresh_rate)

    def hideEvent(self, *args):
        super().hideEvent(*args)
        self._timer.stop()

    def mouseMoveEvent(self, me: QMouseEvent):
        super().mouseMoveEvent(me)
        self._mouse.update(me)

    def mousePressEvent(self, me: QMouseEvent):
        super().mousePressEvent(me)
        self._mouse.update(me, status=Mouse.STAT_PRESS)

    def mouseReleaseEvent(self, me: QMouseEvent):
        super().mousePressEvent(me)
        self._mouse.update(me, status=Mouse.STAT_RELEASE)

    def focusInEvent(self, *args):
        super().focusInEvent(*args)
        self.callback_focus(True)

    def focusOutEvent(self, *args):
        super().focusOutEvent(*args)
        self.callback_focus(False)

    def paintEvent(self, *args):
        super().paintEvent(*args)
        self._painter = QPainter(self)
        if not self._painter.isActive():
            self._painter.begin(self)
        self.callback_draw()
        self._painter.end()

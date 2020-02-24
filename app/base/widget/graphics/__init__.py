import time

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QMouseEvent, QResizeEvent
from PyQt5.QtWidgets import QWidget

from .font import Font
from .mouse import Mouse
from .node import Node
from .rect import Rect
from .sprite import Sprite
from ...common import try_exec


class Factory:
    def __init__(self, event):
        self._event = event

    def sprite(self, img_data: bytes = None):
        return Sprite(self._event, img_data)

    def rect(self, x=0, y=0, w=0, h=0):
        return Rect(self._event, x, y, w, h)

    def font(self, name='', size=11):
        return Font(self._event, name, size)


class GraphicsWidget(QWidget):
    def __init__(self, parent=None, event: dict = None, refresh_rate=60, **kwargs):
        super().__init__(parent, **kwargs)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setMouseTracking(True)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._timer_timeout)

        self._painter = QPainter(self)
        self._refresh_rate = 0
        self._dt = 0
        self._fps = 0
        self._frame_count = 0
        self._frame_count_p = 0
        self._frame_time = 0
        self._scale = 1

        self._event = dict(
            painter=lambda: self._painter,
            scale=lambda: self._scale,
            mouse=lambda: self._mouse,
            dt=lambda: self._dt,
            fps=lambda: self._fps,
        )

        if event is not None:
            self._event.update(event)

        self.set_refresh_rate(refresh_rate)

        self._mouse = Mouse(self._event)
        self.new = Factory(self._event)

    @property
    def debug(self):
        debug = self._event.get('debug')
        if debug is not None:
            return debug()
        return False

    @property
    def event_(self):
        return self._event

    def register_event(self, **kwargs):
        self._event.update(**kwargs)

    def set_scale(self, scale: float):
        self._scale = scale

    def set_refresh_rate(self, refresh_rate):
        self._refresh_rate = 1000 / refresh_rate

    def set_pause(self, b: bool):
        if self.debug:
            print(self.__class__.__name__, 'pause: %a' % b)
        if b and self._timer.isActive():
            self._timer.stop()
        elif not self._timer.isActive():
            self._timer.start(self._refresh_rate)

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
    def scale(self):
        return self._scale

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

        pe = self._event.get('process_events')
        if pe is not None:
            pe()

    def resizeEvent(self, re: QResizeEvent):
        super().resizeEvent(re)
        size = re.size()
        self.callback_resize(size.width(), size.height())

    def showEvent(self, *args):
        super().showEvent(*args)
        self.set_pause(False)

    def hideEvent(self, *args):
        super().hideEvent(*args)
        self.set_pause(True)

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

import time

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QMouseEvent, QResizeEvent, QKeyEvent
from PyQt5.QtWidgets import QWidget

from .circle import Circle
from .factory import Factory
from .font import Font
from .keyboard import Keyboard
from .line import Line
from .mouse import Mouse
from .node import Node
from .rect import Rect
from .sprite import Sprite


def _ignore_on_pause(func):
    def wrapper(self: 'GraphicsWidget', *args, **kwargs):
        if not self.pause:
            return func(self, *args, **kwargs)

    return wrapper


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
        self._antialiasing = False

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
        self._keyboard = Keyboard(self._event)
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

    @property
    def pause(self):
        return not self._timer.isActive()

    def register_event(self, **kwargs):
        self._event.update(**kwargs)

    def set_antialiasing(self, b: bool):
        self._antialiasing = b

    def set_scale(self, scale: float):
        self._scale = scale

    def set_refresh_rate(self, refresh_rate):
        self._refresh_rate = 1000 / refresh_rate

    def set_pause(self, b: bool):
        if self.debug:
            print(self.__class__.__name__, 'pause: %a' % b)
        if b and not self.pause:
            self._timer.stop()
        elif self.pause:
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
    def keyboard(self):
        return self._keyboard

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
        self._keyboard.reset()

        pe = self._event.get('process_events')
        if pe is not None:
            pe()

    @_ignore_on_pause
    def resizeEvent(self, re: QResizeEvent):
        super().resizeEvent(re)
        size = re.size()
        self.callback_resize(size.width(), size.height())

    def showEvent(self, *args):
        self.set_pause(False)
        super().showEvent(*args)

    def hideEvent(self, *args):
        self.set_pause(True)
        super().hideEvent(*args)

    def closeEvent(self, *args):
        self.set_pause(True)
        super().closeEvent(*args)

    @_ignore_on_pause
    def mouseMoveEvent(self, me: QMouseEvent):
        super().mouseMoveEvent(me)
        self._mouse.update(me)

    @_ignore_on_pause
    def mousePressEvent(self, me: QMouseEvent):
        super().mousePressEvent(me)
        self._mouse.update(me, status=Mouse.STAT_PRESS)

    @_ignore_on_pause
    def mouseReleaseEvent(self, me: QMouseEvent):
        super().mouseReleaseEvent(me)
        self._mouse.update(me, status=Mouse.STAT_RELEASE)

    @_ignore_on_pause
    def keyPressEvent(self, ke: QKeyEvent) -> None:
        super().keyPressEvent(ke)
        self._keyboard.update(ke, status=Keyboard.STAT_PRESS)

    @_ignore_on_pause
    def keyReleaseEvent(self, ke: QKeyEvent) -> None:
        super().keyReleaseEvent(ke)
        self._keyboard.update(ke, status=Keyboard.STAT_RELEASE)

    @_ignore_on_pause
    def focusInEvent(self, *args):
        super().focusInEvent(*args)
        self.callback_focus(True)

    @_ignore_on_pause
    def focusOutEvent(self, *args):
        super().focusOutEvent(*args)
        self.callback_focus(False)

    def paintEvent(self, *args):
        super().paintEvent(*args)
        self._painter = QPainter(self)
        if self._antialiasing:
            self._painter.setRenderHint(QPainter.Antialiasing)
        if not self._painter.isActive():
            self._painter.begin(self)
        self.callback_draw()
        self._painter.end()

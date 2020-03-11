import time

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QMouseEvent

from ...utils import point_math


class MouseButton:
    CLICK_INTERVAL = 0.18

    def __init__(self, name, event: dict):
        self._name = name
        self._event = event
        self._down = False
        self._press = False
        self._release = False
        self._click_count = 0
        self._click_count_last = 0
        self._click_distance = 0
        self._click_end = False
        self._click_end_prev = False
        self._down_time = 0
        self._down_pos = None
        self._release_pos = None
        self._release_time = 0
        self._press_time = 0

    @property
    def name(self):
        return self._name

    @property
    def _position(self):
        return self._event['position']()

    @property
    def down(self):
        return self._down

    @property
    def press(self):
        return self._press

    @property
    def release(self):
        return self._release

    @property
    def click_count(self):
        return self._click_count

    @property
    def click_count_last(self):
        return self._click_count_last

    @property
    def click_distance(self):
        return self._click_distance

    @property
    def click_end(self):
        return self._click_end and self._click_end_prev != self._click_end

    @property
    def down_position(self):
        return self._down_pos

    @property
    def release_position(self):
        return self._release_pos

    @property
    def press_time(self):
        return time.time() - self._down_time

    @property
    def press_time_last(self):
        return self._press_time

    @property
    def press_distance(self):
        return point_math.distance(*self._down_pos, *self._position)

    @down.setter
    def down(self, b: bool):
        if b and self._down != b:
            self._down_time = time.time()
            self._down_pos = self._position
        self._down = b

    @press.setter
    def press(self, b: bool):
        self._press = b

    @release.setter
    def release(self, b: bool):
        if b and self._release != b:
            self._release_time = time.time()
            self._press_time = self._release_time - self._down_time
            if self._release_time - self._down_time < self.CLICK_INTERVAL:
                self._click_count += 1
            else:
                self._click_count = 1
            self._release_pos = self._position
            self._click_distance = point_math.distance(*self._down_pos, *self._release_pos)
        self._release = b

    def reset(self):
        self._down = False
        self._release = False
        now = time.time()
        if now - self._down_time > self.CLICK_INTERVAL:
            if self._click_count != 0:
                self._click_count_last = self._click_count
            self._click_count = 0
        self._click_end_prev = self._click_end
        self._click_end = now - self._release_time > self.CLICK_INTERVAL

    def click(self, count=1):
        return self._click_count >= count and self._release


class Mouse:
    STAT_PRESS = 0
    STAT_RELEASE = 1

    BUTTON_LEFT = 0
    BUTTON_MID = 1
    BUTTON_RIGHT = 2

    MAP_BUTTONS = {
        Qt.LeftButton: [BUTTON_LEFT],
        Qt.RightButton: [BUTTON_RIGHT],
        Qt.MiddleButton: [BUTTON_MID],
        Qt.LeftButton | Qt.RightButton: [BUTTON_LEFT, BUTTON_RIGHT],
        Qt.LeftButton | Qt.MidButton: [BUTTON_LEFT, BUTTON_MID],
        Qt.MidButton | Qt.RightButton: [BUTTON_MID, BUTTON_RIGHT],
        Qt.LeftButton | Qt.MidButton | Qt.RightButton: [BUTTON_LEFT, BUTTON_MID, BUTTON_RIGHT],
    }

    def __init__(self, event: dict):
        self._position = QPoint(0, 0)
        self._event = event.copy()
        self._event.update(
            position=lambda: self.position
        )

        self.buttons_all = {}
        for k in dir(self):
            if k[0:7] == 'BUTTON_':
                self.buttons_all[k] = getattr(self, k)
        self._buttons = dict((v, MouseButton(k, self._event)) for k, v in self.buttons_all.items())

    @property
    def debug(self):
        debug = self._event.get('debug')
        if debug is not None:
            return debug()
        return False

    def update(self, e: QMouseEvent, status=None):
        self._position = e.pos()
        btns = self.MAP_BUTTONS.get(e.buttons())
        if status == self.STAT_PRESS and btns is not None:
            for k in btns:
                btn = self._buttons[k]
                if not btn.press:
                    btn.down = True
                    btn.press = True
        elif status == self.STAT_RELEASE or btns is None:
            btns = [btn for btn in self.buttons_all.values() if btn not in btns] if btns is not None else self.buttons_all.values()
            for k in btns:
                btn = self._buttons[k]
                if btn.press:
                    btn.press = False
                    btn.release = True

    def reset(self):
        for btn in self._buttons.values():
            btn.reset()

    @property
    def scale(self) -> float:
        return self._event['scale']()

    def button(self, btn):
        return self._buttons[btn]

    @property
    def position(self):
        return self.x, self.y

    @property
    def x(self):
        return int(self._position.x() / self.scale)

    @property
    def y(self):
        return int(self._position.y() / self.scale)

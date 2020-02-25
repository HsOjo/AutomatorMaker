import time

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QMouseEvent

from app.base.common import point_distance


class MouseButton:
    CLICK_INTERVAL = 0.18

    def __init__(self, name, event: dict):
        self._event = event
        self._name = name
        self._down = False
        self._press = False
        self._release = False
        self._click_count = 0
        self._click_distance = 0
        self._down_time = 0
        self._down_pos = None
        self._release_pos = None

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
    def click_distance(self):
        return self._click_distance

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
    def press_distance(self):
        return point_distance(*self._down_pos, *self._position)

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
            if time.time() - self._down_time < self.CLICK_INTERVAL:
                self._click_count += 1
            else:
                self._click_count = 1
            self._release_pos = self._position
            self._click_distance = point_distance(*self._down_pos, *self._release_pos)
        self._release = b

    def reset(self):
        self._down = False
        self._release = False
        if time.time() - self._down_time > self.CLICK_INTERVAL:
            self._click_count = 0

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
    ALL_BUTTONS = [BUTTON_LEFT, BUTTON_RIGHT, BUTTON_MID]

    def __init__(self, event: dict):
        self._position = QPoint(0, 0)
        self._event = event.copy()
        self._event.update(
            position=lambda: self.position
        )
        self._buttons = dict((b, MouseButton(b, self._event)) for b in self.ALL_BUTTONS)

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
            btns = [btn for btn in self.ALL_BUTTONS if btn not in btns] if btns is not None else self.ALL_BUTTONS
            for k in btns:
                btn = self._buttons[k]
                if btn.press:
                    btn.press = False
                    btn.release = True

    def reset(self):
        for k in self.ALL_BUTTONS:
            btn = self._buttons[k]
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
        return self._position.x() / self.scale

    @property
    def y(self):
        return self._position.y() / self.scale

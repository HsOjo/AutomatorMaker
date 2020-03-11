import time

from PyQt5.QtGui import QKeyEvent


class Key:
    CLICK_INTERVAL = 0.18

    def __init__(self, name, event: dict):
        self._name = name
        self._event = event
        self._down = False
        self._press = False
        self._release = False
        self._click_count = 0
        self._click_count_last = 0
        self._click_end = False
        self._click_end_prev = False
        self._down_time = 0
        self._release_time = 0
        self._press_time = 0

    @property
    def name(self):
        return self._name

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
    def click_end(self):
        return self._click_end and self._click_end_prev != self._click_end

    @property
    def press_time(self):
        return time.time() - self._down_time

    @property
    def press_time_last(self):
        return self._press_time

    @down.setter
    def down(self, b: bool):
        if b and self._down != b:
            self._down_time = time.time()
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


class Keyboard:
    STAT_PRESS = 0
    STAT_RELEASE = 1

    KEY_0 = 48
    KEY_1 = 49
    KEY_2 = 50
    KEY_3 = 51
    KEY_4 = 52
    KEY_5 = 53
    KEY_6 = 54
    KEY_7 = 55
    KEY_8 = 56
    KEY_9 = 57
    KEY_A = 65
    KEY_B = 66
    KEY_C = 67
    KEY_D = 68
    KEY_E = 69
    KEY_F = 70
    KEY_G = 71
    KEY_H = 72
    KEY_I = 73
    KEY_J = 74
    KEY_K = 75
    KEY_L = 76
    KEY_M = 77
    KEY_N = 78
    KEY_O = 79
    KEY_P = 80
    KEY_Q = 81
    KEY_R = 82
    KEY_S = 83
    KEY_T = 84
    KEY_U = 85
    KEY_V = 86
    KEY_W = 87
    KEY_X = 88
    KEY_Y = 89
    KEY_Z = 90
    KEY_ESC = 16777216
    KEY_TAB = 16777217
    KEY_BACKSPACE = 16777219
    KEY_RETURN = 16777220
    KEY_INSERT = 16777222
    KEY_DELETE = 16777223
    KEY_HOME = 16777232
    KEY_END = 16777233
    KEY_LEFT = 16777234
    KEY_UP = 16777235
    KEY_RIGHT = 16777236
    KEY_DOWN = 16777237
    KEY_PAGEUP = 16777238
    KEY_PAGEDOWN = 16777239
    KEY_SHIFT = 16777248
    KEY_CONTROL = 16777249
    KEY_META = 16777250
    KEY_ALT = 16777251
    KEY_F1 = 16777264
    KEY_F2 = 16777265
    KEY_F3 = 16777266
    KEY_F4 = 16777267
    KEY_F5 = 16777268
    KEY_F6 = 16777269
    KEY_F7 = 16777270
    KEY_F8 = 16777271
    KEY_F9 = 16777272
    KEY_F10 = 16777273
    KEY_F11 = 16777274
    KEY_F12 = 16777275

    def __init__(self, event: dict):
        self._event = event.copy()

        self.keys_all = {}
        for k in dir(self):
            if k[0:4] == 'KEY_':
                self.keys_all[k] = getattr(self, k)
        self._keys = dict((v, Key(k, self._event)) for k, v in self.keys_all.items())

    @property
    def debug(self):
        debug = self._event.get('debug')
        if debug is not None:
            return debug()
        return False

    def update(self, e: QKeyEvent, status=None):
        k = e.key()
        if status == self.STAT_PRESS and k is not None:
            key = self._keys.get(k)
            if key is not None and not key.press:
                key.down = True
                key.press = True
        elif status == self.STAT_RELEASE or k is None:
            key = self._keys.get(k)
            if key is not None and key.press:
                key.press = False
                key.release = True

    def reset(self):
        for key in self._keys.values():
            key.reset()

    def key(self, key):
        return self._keys[key]

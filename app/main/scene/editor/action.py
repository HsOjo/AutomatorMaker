from typing import List

from PyQt5.QtGui import QColor

from .base import BaseEditor
from ..model import ActionModel, ObjectModel
from ..object import ObjectRect, MouseIndicator


class ActionEditor(BaseEditor):
    COLOR_OBJECT = QColor(0, 255, 255)
    COLOR_MOUSE = QColor(0, 255, 0)
    COLOR_ORIGIN = QColor(255, 255, 0)

    DISTANCE_SWIPE = 8
    TIME_PRESS = 0.3

    RADIUS_MOUSE_CIRCLE = 24

    def __init__(self, event):
        super().__init__(event)
        self._event = event
        self._object = None  # type: ObjectModel
        self._object_rect = ObjectRect(event)
        self._object_rect.set_color(self.COLOR_OBJECT)

        self._actions = None  # type: List[ActionModel]
        self._current_action = None

        self._mouse_indicator = MouseIndicator(self._event, self.COLOR_ORIGIN, self.COLOR_MOUSE,
                                               self.RADIUS_MOUSE_CIRCLE, self.TIME_PRESS, self.DISTANCE_SWIPE)

    def load_actions(self, object_: ObjectModel):
        self._object = object_
        x, y, w, h = object_.rect
        self._object_rect.set_position(x, y)
        self._object_rect.set_size(w, h)
        self._actions = object_.actions

    def select(self, index):
        pass

    def update(self):
        mouse = self.mouse
        mouse_l = mouse.button(mouse.BUTTON_LEFT)

        self._mouse_indicator.update()

        if mouse_l.click():
            cc = mouse_l.click_count
            if cc == 1:
                pt = mouse_l.press_time
                cd = mouse_l.click_distance
                if cd > self.DISTANCE_SWIPE:
                    # swipe
                    print('swipe')
                else:
                    if pt >= self.TIME_PRESS:
                        # press
                        print('press')
                    else:
                        # tap
                        print('tap')
            else:
                print('tap', cc)

    def draw(self):
        self._object_rect.draw()
        self._mouse_indicator.draw()

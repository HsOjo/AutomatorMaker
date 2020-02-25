from typing import List

from PyQt5.QtGui import QColor

from .base import BaseEditor
from ..model import ActionModel, ObjectModel
from ..object import ObjectRect


class ActionEditor(BaseEditor):
    COLOR_OBJECT = QColor(0, 255, 255)

    def __init__(self, event):
        super().__init__(event)
        self._event = event
        self._object = None  # type: ObjectModel
        self._object_rect = ObjectRect(event)
        self._object_rect.set_color(self.COLOR_OBJECT)

        self._actions = None  # type: List[ActionModel]
        self._current_action = None

    def load_actions(self, object_: ObjectModel):
        self._object = object_
        x, y, w, h = object_.rect
        self._object_rect.set_position(x, y)
        self._object_rect.set_size(w, h)
        self._actions = object_.actions

    def select(self, index):
        pass

    def draw(self):
        self._object_rect.draw()

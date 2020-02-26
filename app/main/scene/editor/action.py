from typing import List, Dict

from PyQt5.QtGui import QColor

from .base import BaseEditor
from ..model import ActionModel, ObjectModel
from ..object import ObjectRect, MouseIndicator
from ..object.operation import BaseOperation, TapOperation, PressOperation, SwipeOperation


class ActionEditor(BaseEditor):
    COLOR_OBJECT = QColor(0, 255, 255)
    COLOR_MOUSE = QColor(0, 255, 0)
    COLOR_ORIGIN = QColor(255, 255, 0)

    DISTANCE_SWIPE = 8
    TIME_PRESS = 0.3

    RADIUS_MOUSE_CIRCLE = 24
    TYPE_OPERATION = {
        ActionModel.TYPE_TAP: TapOperation,
        ActionModel.TYPE_PRESS: PressOperation,
        ActionModel.TYPE_SWIPE: SwipeOperation,
    }
    TYPE_OPERATION_REV = dict((v, k) for k, v in TYPE_OPERATION.items())

    def __init__(self, event):
        super().__init__(event)
        self._event = event
        self._operations = {}  # type: Dict[BaseOperation]
        self._current_operation = None
        self._mouse_indicator = MouseIndicator(self._event, self.COLOR_ORIGIN, self.COLOR_MOUSE,
                                               self.RADIUS_MOUSE_CIRCLE, self.TIME_PRESS, self.DISTANCE_SWIPE)

        self._object = None  # type: ObjectModel
        self._object_rect = ObjectRect(event)
        self._object_rect.set_color(self.COLOR_OBJECT)

        self._actions = None  # type: List[ActionModel]

    def load_actions(self, object_: ObjectModel):
        actions = object_.actions
        self._actions = actions
        self._object = object_

        x, y, w, h = object_.rect
        self._object_rect.set_position(x, y)
        self._object_rect.set_size(w, h)

        operations = {}
        for action in actions:
            operation = self.new_operation(action.type, action.params)
            operation.load_params(action.params)
            operations[operation] = action
        self._operations = operations
        self.set_current_operation(None, False)

    @property
    def operations(self):
        return list(self._operations.keys())

    def select(self, index):
        operations = self.operations
        if 0 <= index < len(operations):
            self.set_current_operation(operations[index], sync=False)

    @property
    def current_action(self):
        return self._operations.get(self._current_operation)

    def set_current_operation(self, operation, sync=True):
        if self._current_operation is not None:
            self._current_operation.set_focus(False)

        self._current_operation = operation
        if operation is not None:
            operation.set_focus(True)

        if sync and operation in self._operations:
            self.event['select_action'](self.operations.index(operation))

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

    def new_operation(self, type, params: dict, sync=True):
        operation_cls = self.TYPE_OPERATION.get(type)
        operation = None
        if operation_cls is not None:
            operation = operation_cls(self._event)
            operation.load_params(**params)
            if sync and self.add_item(operation):
                self.set_current_operation(operation)

        return operation

    def add_item(self, operation: BaseOperation):
        if self._actions is None:
            return False
        name = ''
        names = [action.name for action in self._actions]
        for i in range(10000):
            name = 'Untitiled_%s' % i
            if name not in names:
                break

        action = ActionModel()
        action.name = name
        action.type = self.TYPE_OPERATION_REV.get(type(operation))
        action.params = operation.params
        self._operations[operation] = action
        self._actions.append(action)
        self.sync()
        return True

    def draw(self):
        self._object_rect.draw()
        for operation in self._operations:
            operation.draw()
        self._mouse_indicator.draw()

    def callback_operation_modified(self, operation_modified: BaseOperation):
        self.sync()

    def sync(self):
        if self._actions is None:
            return

        for operation, action in self._operations.items():
            operation: BaseOperation
            action: ActionModel
            action.params = operation.params
        self.event['sync_actions'](self._actions)

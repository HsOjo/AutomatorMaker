from typing import List, Dict

from PyQt5.QtGui import QColor

from app.base.widget.graphics import Font
from .base import BaseEditor
from ..model import ActionModel, ObjectModel
from ..object import ObjectRect, MouseIndicator
from ..object.operation import BaseOperation, TapOperation, PressOperation, SwipeOperation


class ActionEditor(BaseEditor):
    COLOR_OBJECT = QColor(0, 255, 255)
    COLOR_MOUSE = QColor(0, 255, 0)
    COLOR_ORIGIN = QColor(255, 255, 0)

    COLOR_UNFOCUS = QColor(255, 255, 0)
    COLOR_UNFOCUS_MOVING = QColor(255, 255, 0, 128)
    COLOR_FOCUS = QColor(255, 128, 0)

    DISTANCE_SWIPE = 8
    TIME_PRESS = 0.3

    RADIUS_MOUSE_CIRCLE = 12
    RADIUS_TAP_CIRCLE = 16
    RADIUS_SWIPE_CIRCLE = 16
    TYPE_OPERATION = {
        ActionModel.TYPE_TAP: TapOperation,
        ActionModel.TYPE_PRESS: PressOperation,
        ActionModel.TYPE_SWIPE: SwipeOperation,
    }
    TYPE_OPERATION_REV = dict((v, k) for k, v in TYPE_OPERATION.items())

    def __init__(self, event):
        super().__init__(event)
        self._event = event
        self._operations = {}  # type: Dict[BaseOperation, ActionModel]
        self._current_operation = None
        self._mouse_indicator = MouseIndicator(self._event, self.COLOR_ORIGIN, self.COLOR_MOUSE,
                                               self.RADIUS_MOUSE_CIRCLE, self.TIME_PRESS, self.DISTANCE_SWIPE)

        self._object = None  # type: ObjectModel
        self._object_rect = ObjectRect(event)
        self._object_rect.set_color(self.COLOR_OBJECT)

        self._actions = None  # type: List[ActionModel]
        self._creating = False

    def load_actions(self, object_: ObjectModel):
        actions = object_.actions
        self._actions = actions
        self._object = object_

        x, y, w, h = object_.rect
        self._object_rect.set_position(x, y)
        self._object_rect.set_size(w, h)

        operations = {}
        for action in actions:
            operation = self.new_operation(action.type, action.params, sync=False)
            operation.load_params(**action.params)
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

        if self._creating:
            if mouse_l.click_end:
                cc = mouse_l.click_count_last
                if cc > 1:
                    dx, dy = mouse_l.down_position
                    self.new_operation(ActionModel.TYPE_TAP, dict(
                        x=dx, y=dy, count=cc
                    ))
                    self._creating = False
                elif cc > 0:
                    pt = mouse_l.press_time_last
                    cd = mouse_l.click_distance
                    dx, dy = mouse_l.down_position
                    rx, ry = mouse_l.release_position
                    if cd > self.DISTANCE_SWIPE:
                        self.new_operation(ActionModel.TYPE_SWIPE, dict(
                            start_x=dx, start_y=dy,
                            end_x=rx, end_y=ry,
                            time=mouse_l.press_time_last,
                        ))
                    else:
                        if pt >= self.TIME_PRESS:
                            self.new_operation(ActionModel.TYPE_PRESS, dict(
                                x=dx, y=dy,
                                time=mouse_l.press_time_last,
                            ))
                        else:
                            self.new_operation(ActionModel.TYPE_TAP, dict(
                                x=dx, y=dy, count=cc
                            ))
                    self._creating = False
        else:
            for operation in self._operations:
                operation.update()

            if self._current_operation is not None:
                if not self._current_operation.focus:
                    self.set_current_operation(None)

                if mouse_l.click_end and mouse_l.click_count_last == 2:
                    self._event['set_params']()

            if self._current_operation is None:
                if mouse_l.down:
                    for operation in reversed(self.operations):
                        if operation.check_point(*mouse.position):
                            self.set_current_operation(operation)
                            break
                    if self._current_operation is None:
                        if self._object_rect.check_point(*mouse.position):
                            self._creating = True
                    else:
                        self._current_operation.update()

    def new_operation(self, type_, params: dict, sync=True):
        operation_cls = self.TYPE_OPERATION.get(type_)
        operation = None
        if operation_cls is not None:
            operation = operation_cls(self._event)
            operation.load_params(**params)
            operation.set_callback_modified(self.callback_operation_modified)
            operation.set_focus_color(self.COLOR_FOCUS, self.COLOR_UNFOCUS)
            if isinstance(operation, TapOperation):
                operation.circle.set_radius(self.RADIUS_TAP_CIRCLE)
            if isinstance(operation, SwipeOperation):
                operation.circle_start.set_radius(self.RADIUS_SWIPE_CIRCLE / 2)
                operation.circle_end.set_radius(self.RADIUS_SWIPE_CIRCLE)

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
        if self._creating:
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

    def callback_item_edited(self, edited_item):
        for operation, item in self._operations.items():
            if edited_item == item:
                operation.load_params(**item.params)
                break

    def callback_item_deleted(self, deleted_item):
        for operation, item in self._operations.items():
            if deleted_item == item:
                self._operations.pop(operation)
                if operation == self._current_operation:
                    self.set_current_operation(None)
                break

from typing import List

from PyQt5.QtGui import QColor

from app.base.widget.graphics import Rect
from app.utils import list_math
from .base import BaseEditor
from .rect_adjuster import RectAdjuster
from ..model import FeatureModel


def _sync(func):
    def wrapper(self: 'FeatureEditor', *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.event['sync_features'](self._features)
        return result

    return wrapper


class FeatureEditor(BaseEditor):
    COLOR_NEW = QColor(0, 255, 0)
    COLOR_NORMAL = QColor(255, 255, 0)
    COLOR_NORMAL_MOVING = QColor(255, 255, 0, 128)
    COLOR_CURRENT = QColor(255, 128, 0)

    def __init__(self, event):
        super().__init__(event)
        self._features = None  # type: List[FeatureModel]
        self._rects = {}
        self._rect_current = None  # type: Rect
        self._rect_new = Rect(self.event)
        self._rect_new.set_color(self.COLOR_NEW)

        self._creating = False
        self._moving = False
        self._move_origin = None  # type: List[int]
        self._move_origin_rect = None  # type: List[int]

        self._rect_adjuster = RectAdjuster(event)

    @property
    def current_feature(self):
        return self._rects.get(self._rect_current)

    def load_features(self, features: List[FeatureModel]):
        self._features = features
        rects = {}
        for feature in features:
            rect = Rect(self.event, *feature.rect)
            rect.set_color(self.COLOR_NORMAL)
            rects[rect] = feature
        self._rects = rects
        self._rect_current = None

    def select(self, index):
        rects = list(self._rects.keys())
        self.set_current_rect(rects[index], sync=False)

    def set_current_rect(self, rect, sync=True):
        if self._rect_current is not None:
            self._rect_current.set_color(self.COLOR_NORMAL)

        self._rect_current = rect
        if rect is not None:
            rect.set_color(self.COLOR_CURRENT)
            self._rect_adjuster.adjust(rect)

        if rect == self._rect_new:
            rect.set_color(self.COLOR_NEW)

        if sync and rect in self._rects:
            self.event['select_feature'](list(self._rects.keys()).index(rect))

    def update(self):
        mouse = self.mouse
        rect_new = self._rect_new

        if not self._moving:
            if self._rect_current is not None:
                self._rect_adjuster.update()
            if not self._rect_adjuster.adjusting:
                # select rect.
                if mouse.down(mouse.BUTTON_LEFT):
                    if self._rect_current is None or not self._rect_current.check_point(*mouse.position):
                        self.set_current_rect(None)
                        for rect in self._rects:
                            if rect.check_point(*mouse.position):
                                self.set_current_rect(rect)
                    if self._rect_current is None:
                        rect_new.set_position(*mouse.position)
                        self.set_current_rect(rect_new)
                        self._creating = True
                    else:
                        self._move_origin_rect = self._rect_current.position
                        self._move_origin = mouse.position
                        self._moving = True
                        for rect in self._rects:
                            if rect != self._rect_current:
                                rect.set_color(self.COLOR_NORMAL_MOVING)

                # create rect.
                if self._creating:
                    rect_new.set_size(mouse.x - rect_new.x, mouse.y - rect_new.y)
                    if mouse.release(mouse.BUTTON_LEFT):
                        rect_new.set_size(*rect_new.size, convert_negative=True)
                        rect = rect_new.copy()
                        self.add_feature(rect)
                        self.set_current_rect(rect)
                        self._creating = False
        else:
            # move rect.
            self._rect_current.set_position(
                *list_math.add(
                    self._move_origin_rect,
                    list_math.reduce(mouse.position, self._move_origin)
                )
            )
            if mouse.release(mouse.BUTTON_LEFT):
                self._rect_adjuster.adjust(self._rect_current)
                self._moving = False
                for rect in self._rects:
                    if rect != self._rect_current:
                        rect.set_color(self.COLOR_NORMAL)

    @_sync
    def add_feature(self, rect: Rect):
        if self._features is None:
            return
        name = ''
        names = [feature.name for feature in self._features]
        for i in range(10000):
            name = 'Untitiled_%s' % i
            if name not in names:
                break

        feature = FeatureModel()
        feature.name = name
        feature.rect = [*rect]
        self._rects[rect] = feature
        self._features.append(feature)

    def draw(self):
        for rect in self._rects:
            rect.draw()
        if self._rect_current == self._rect_new:
            self._rect_new.draw()
        if self._rect_current is not None and not self._moving and not self._creating:
            self._rect_adjuster.draw()

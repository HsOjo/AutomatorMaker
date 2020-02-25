from typing import List

from .rect import RectEditor
from ..model import FeatureModel


class FeatureEditor(RectEditor):
    def __init__(self, event):
        super().__init__(event)
        self._features = None  # type: List[FeatureModel]

    @property
    def current_feature(self):
        return self._rects.get(self._current_rect)

    def load_features(self, features: List[FeatureModel]):
        self._features = features
        rects = {}
        for feature in features:
            rect = self.new_rect(False, feature.rect)
            rects[rect] = feature
        self._rects = rects
        self.set_current_rect(None, False)

    def set_current_rect(self, rect, sync=True):
        super().set_current_rect(rect)

        if sync and rect in self._rects:
            self.event['select_feature'](self.rects.index(rect))

    def add_item(self, rect):
        if self._features is None:
            return False
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
        self.event['sync_features'](self._features)
        return True

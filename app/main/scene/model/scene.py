from typing import List

from .feature import FeatureModel
from .object import ObjectModel


class SceneModel:
    def __init__(self, event: dict):
        self._event = event
        self.name = None
        self.img = None
        self.features = []  # type: List[FeatureModel]
        self.objects = []  # type: List[ObjectModel]

    @property
    def img_path(self):
        return self._event['get_path'](self.img)

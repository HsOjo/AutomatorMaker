from typing import List

from app.base.model import BaseModel


class FeatureModel(BaseModel):
    def __init__(self):
        self.name = ''
        self.rect = []  # type: List[int]
        self.detect_weight = 0

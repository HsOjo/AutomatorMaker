from typing import List

from app.base.model import BaseModel
from .action import ActionModel


class ObjectModel(BaseModel):
    _sub_model = dict(
        actions=(list, ActionModel),
    )

    TYPE_BUTTON = 0
    ALL_TYPES = {
        'Button': TYPE_BUTTON,
    }
    ALL_TYPES_REV = dict((v, k) for k, v in ALL_TYPES.items())

    def __init__(self):
        self.name = ''
        self.rect = []  # type: List[int]
        self.type = self.TYPE_BUTTON
        self.actions = []  # type: List[ActionModel]

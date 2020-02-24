from typing import List

from .action import ActionModel


class ObjectModel:
    TYPE_BUTTON = 0

    def __init__(self):
        self.name = None
        self.rect = None
        self.type = None
        self.actions = []  # type: List[ActionModel]

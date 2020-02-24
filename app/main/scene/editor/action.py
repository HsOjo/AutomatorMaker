from typing import List

from .base import BaseEditor
from ..model import ActionModel


class ActionEditor(BaseEditor):
    def __init__(self, event):
        super().__init__(event)

    def load_actions(self, actions: List[ActionModel]):
        pass

    def select(self, index):
        pass

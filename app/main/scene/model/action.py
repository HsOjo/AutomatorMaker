from app.base.model import BaseModel


class ActionModel(BaseModel):
    TYPE_TAP = 0
    TYPE_SWIPE = 1
    TYPE_PRESS = 2

    ALL_TYPES = {
        'Tap': TYPE_TAP,
        'Swipe': TYPE_SWIPE,
    }
    ALL_TYPES_REV = dict((v, k) for k, v in ALL_TYPES.items())

    def __init__(self, parent=None):
        self.name = ''
        self.type = self.TYPE_TAP
        self.dest_scene = ''
        self.params = {}
        self._parent = parent

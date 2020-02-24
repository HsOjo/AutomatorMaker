from app.base.model import BaseModel


class ActionModel(BaseModel):
    TYPE_TAP = 0
    TYPE_SWIPE = 0

    def __init__(self):
        self.name = ''
        self.type = self.TYPE_TAP
        self.dest_scene = ''
        self.params = {}

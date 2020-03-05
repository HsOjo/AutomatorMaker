from app.base.dialog.form.field import NumberField
from app.base.model import BaseModel


class ActionModel(BaseModel):
    TYPE_TAP = 0
    TYPE_SWIPE = 1
    TYPE_PRESS = 2

    ALL_TYPES = {
        'Tap': TYPE_TAP,
        'Swipe': TYPE_SWIPE,
        'Press': TYPE_PRESS,
    }
    ALL_TYPES_REV = dict((v, k) for k, v in ALL_TYPES.items())

    SCENE_NONE = 'None'

    PARAMS_TITLE = dict(
        x='Position X',
        y='Position Y',
        start_x='Start Position X',
        start_y='Start Position Y',
        end_x='End Position X',
        end_y='End Position Y',
        time='Operation Time',
        count='Operation Count',
    )
    PARAMS_FIELD = dict(
        x=NumberField,
        y=NumberField,
        start_x=NumberField,
        start_y=NumberField,
        end_x=NumberField,
        end_y=NumberField,
        time=NumberField,
        count=NumberField,
    )

    def __init__(self, parent=None):
        self.name = ''
        self.type = self.TYPE_TAP
        self.dest_scene = self.SCENE_NONE
        self.params = {}
        self._parent = parent

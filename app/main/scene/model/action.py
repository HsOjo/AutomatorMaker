from dt_automator.maker.model import MakerActionModel

from app.base.dialog.form.field import NumberField


class ActionModel(MakerActionModel):
    PARAMS_COMMON = ['distance', 'wait']

    PARAMS_TYPE = {
        MakerActionModel.TYPE_TAP: ['x', 'y', 'count'],
        MakerActionModel.TYPE_PRESS: ['x', 'y', 'time'],
        MakerActionModel.TYPE_SWIPE: ['start_x', 'start_y', 'end_x', 'end_y', 'time'],
    }

    PARAMS_TITLE = dict(
        x='Position X',
        y='Position Y',
        start_x='Start Position X',
        start_y='Start Position Y',
        end_x='End Position X',
        end_y='End Position Y',
        time='Operation Time',
        count='Operation Count',
        distance='Operation Distance',
        wait='Operation Wait Time (After)',
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
        distance=NumberField,
        wait=NumberField,
    )

    PARAMS_DEFAULT = dict(
        x=0,
        y=0,
        start_x=0,
        start_y=0,
        end_x=0,
        end_y=0,
        time=1,
        count=1,
        distance=1,
        wait=1,
    )

from dt_automator.maker.model import MakerActionModel

from app.base.dialog.form.field import NumberField


class ActionModel(MakerActionModel):
    PARAMS_TITLE = dict(
        x='Position X',
        y='Position Y',
        press_time='Press Time',
        count='Operation Count',

        start_x='Start Position X',
        start_y='Start Position Y',
        end_x='End Position X',
        end_y='End Position Y',
        time='Operation Time',

        distance='Operation Distance',
        wait='Operation Wait Time (After)',

        finger='Finger Number',
        finger_distance='Finger Distance',
        finger_degree='Finger Rotate Degree',
    )

    PARAMS_FIELD = dict(
        x=NumberField,
        y=NumberField,
        press_time=NumberField,
        count=NumberField,

        start_x=NumberField,
        start_y=NumberField,
        end_x=NumberField,
        end_y=NumberField,
        time=NumberField,

        distance=NumberField,
        wait=NumberField,

        finger=NumberField,
        finger_distance=NumberField,
        finger_degree=NumberField,
    )

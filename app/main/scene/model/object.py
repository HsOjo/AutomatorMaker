from dt_automator.maker.model import MakerObjectModel

from app.base.dialog.form.field.color import ColorField
from .action import ActionModel


class ObjectModel(MakerObjectModel):
    _sub_model = dict(
        actions=(list, ActionModel),
    )

    PARAMS_TITLE = dict(
        color='Color',
    )

    PARAMS_FIELD = dict(
        color=ColorField,
    )

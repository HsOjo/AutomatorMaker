from dt_automator.maker.model import MakerObjectModel
from ojoqt.dialog.form.field.color import ColorField

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

from dt_automator.maker.model import MakerObjectModel

from .action import ActionModel


class ObjectModel(MakerObjectModel):
    _sub_model = dict(
        actions=(list, ActionModel),
    )

from dt_automator.maker.model import MakerSceneModel

from .feature import FeatureModel
from .object import ObjectModel


class SceneModel(MakerSceneModel):
    _sub_model = dict(
        features=(list, FeatureModel),
        objects=(list, ObjectModel),
    )

    def rename(self, new):
        img_name = self.img
        self.name = new
        self.img = '%s.png' % new
        self._event['move_file'](img_name, self.img)

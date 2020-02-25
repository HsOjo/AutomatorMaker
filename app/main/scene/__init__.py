from PyQt5.QtGui import QColor

from app.base.widget import GraphicsWidget
from app.main.scene.editor import FeatureEditor, ObjectEditor, ActionEditor, BaseEditor
from app.main.scene.model import SceneModel, ObjectModel, FeatureModel, ActionModel


class SceneWidget(GraphicsWidget):
    EDIT_FEATURE = 0
    EDIT_OBJECT = 1
    EDIT_ACTION = 2

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.screen = self.new.sprite()
        self.rect_base = self.new.rect()
        self.rect_base.set_color(QColor(255, 0, 0))

        self._scene = None  # type: SceneModel

        self._feature_editor = FeatureEditor(self._event)
        self._object_editor = ObjectEditor(self._event)
        self._action_editor = ActionEditor(self._event)

        self._editors = {
            self.EDIT_FEATURE: self._feature_editor,
            self.EDIT_OBJECT: self._object_editor,
            self.EDIT_ACTION: self._action_editor,
        }
        self._currnet_editor = self.EDIT_FEATURE

    @property
    def current_editor(self) -> BaseEditor:
        return self._editors[self._currnet_editor]

    @property
    def scene(self):
        return self._scene

    @property
    def current_object(self):
        return self._object_editor.current_object

    def callback_update(self):
        self.current_editor.update()

    def callback_draw(self):
        self.screen.draw()
        self.current_editor.draw()

    def callback_resize(self, w, h):
        self.inject_size()

    def set_scale(self, scale: float):
        super().set_scale(scale)
        self.inject_size()

    def set_scene(self, scene: SceneModel):
        self._scene = scene
        with open(scene.img_path, 'rb') as io:
            img_data = io.read()
        self.screen.set_image(img_data)
        self._feature_editor.load_features(scene.features)
        self._object_editor.load_objects(scene.objects)
        self.inject_size()

    def set_current_editor(self, editor) -> bool:
        if editor == self.EDIT_ACTION:
            current_object = self._object_editor.current_object  # type: ObjectModel
            if current_object is None:
                return False
            self._event['sync_actions'](current_object.actions)
            self._action_editor.load_actions(current_object)
        self._currnet_editor = editor
        return True

    def inject_size(self):
        pixmap = self.screen.pixmap
        scale = self.scale
        w, h = pixmap.width(), pixmap.height()
        sw, sh = w * scale, h * scale
        self.setMinimumSize(sw, sh)

    def callback_select_feature(self, index):
        if self._scene is None:
            return
        self._feature_editor.select(index)

    def callback_select_object(self, index):
        if self._scene is None:
            return
        self._object_editor.select(index)

    def callback_select_action(self, index):
        if self.current_object is None:
            return

    def callback_item_edited(self, item):
        self.current_editor.callback_item_edited(item)
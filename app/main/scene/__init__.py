from PyQt5.QtGui import QImage

from app.base.widget import GraphicsWidget
from app.main.scene.editor import FeatureEditor, ObjectEditor, ActionEditor, BaseEditor
from app.main.scene.model import SceneModel, ObjectModel, FeatureModel, ActionModel
from app.main.scene.object import ColorPicker


class SceneWidget(GraphicsWidget):
    EDIT_FEATURE = 0
    EDIT_OBJECT = 1
    EDIT_ACTION = 2

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.set_antialiasing(True)

        self.screen = self.new.sprite()
        self._screen_image = None  # type: QImage

        self._color_picker = ColorPicker(self.event_)
        self._scene = None  # type: SceneModel

        self._feature_editor = FeatureEditor(self.event_)
        self._object_editor = ObjectEditor(self.event_)
        self._action_editor = ActionEditor(self.event_)

        self._editors = {
            self.EDIT_FEATURE: self._feature_editor,
            self.EDIT_OBJECT: self._object_editor,
            self.EDIT_ACTION: self._action_editor,
        }
        self._currnet_editor = self.EDIT_FEATURE

        self.event_.update(
            screen_image=lambda: self._screen_image,
            color_pick_current=lambda: self._color_picker.color,
        )

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
        self._color_picker.update()

    def callback_draw(self):
        self.screen.draw()
        self.current_editor.draw()
        self._color_picker.draw()

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

        self._screen_image = self.screen.pixmap.toImage()

        self._feature_editor.load_features(scene.features)
        self._object_editor.load_objects(scene.objects)
        self.inject_size()

    def set_current_editor(self, editor: int) -> bool:
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
        self._action_editor.select(index)

    def callback_item_edited(self, item):
        self.current_editor.callback_item_edited(item)

    def callback_item_deleted(self, item):
        self.current_editor.callback_item_deleted(item)

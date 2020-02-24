import os
import shutil
from typing import Dict

from app.main.scene.model import SceneModel


class Project:
    def __init__(self):
        self._path = None
        self._event = dict(
            get_path=self.get_path
        )
        self.scenes = {}  # type: Dict[SceneModel]

    @staticmethod
    def open(path):
        if os.path.exists(path) and os.path.isdir(path):
            self = Project()
            self._path = path
            return self

    def save(self):
        pass

    def get_path(self, filename, create_dir=False):
        path = '%s/%s' % (self._path, filename)
        if create_dir:
            dir_ = os.path.dirname(path)
            os.makedirs(dir_, exist_ok=True)
        return path

    def save_file(self, filename, mode='w', **kwargs):
        path = self.get_path(filename, create_dir=True)
        return open(path, mode, **kwargs)

    def move_file(self, src, dest):
        path_src = self.get_path(src)
        path_dest = self.get_path(dest, create_dir=True)
        shutil.move(path_src, path_dest)

    def add_scene(self, img_data: bytes, name=None):
        if name is None:
            for i in range(10000):
                name = 'Untitiled_%s' % i
                if self.scenes.get(name) is None:
                    break

        scene = SceneModel(self._event)
        scene.name = name
        scene.img = '%s.png' % name
        self.scenes[name] = scene

        with open(scene.img_path, 'wb') as io:
            io.write(img_data)

import json
import os
import shutil
from typing import Dict

from app.base.common import try_exec
from app.main.scene.model import SceneModel


class Project:
    FILENAME_INFO = 'info.json'

    def __init__(self):
        self._path = None
        self._event = dict(
            get_path=self.get_path,
            move_file=self.move_file,
        )
        self.scenes = {}  # type: Dict[SceneModel]

    @staticmethod
    def open(path):
        if os.path.exists(path) and os.path.isdir(path):
            self = Project()
            self._path = path
            if os.path.exists('%s/%s' % (path, self.FILENAME_INFO)):
                self.load()
            return self

    def load(self):
        path = self.get_path(self.FILENAME_INFO)
        with open(path, encoding='utf-8') as io:
            data = json.load(io)  # type: dict
        items = {}
        for k, v in data.items():
            scene = SceneModel(self._event)
            scene.load_data(**v)
            items[k] = scene
        self.scenes = items

    def save(self):
        data = dict((k, v.data) for k, v in self.scenes.items())
        with self.save_file(self.FILENAME_INFO, encoding='utf-8') as io:
            json.dump(data, io, ensure_ascii=False, indent=4)

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

    @try_exec(show=True, info_only=True)
    def rename_scene(self, old, new):
        if new in self.scenes:
            raise Exception('Already exist scene "%s"!' % new)
        scene = self.scenes.pop(old)  # type: SceneModel
        scene.rename(old, new)
        self.scenes[new] = scene

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

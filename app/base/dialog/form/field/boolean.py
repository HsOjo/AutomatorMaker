from PyQt5.QtWidgets import QCheckBox

from .base import BaseField


class BooleanField(BaseField):
    def __init__(self, name, value=None, title=None):
        super().__init__(name, title)
        self.widget = QCheckBox()
        if value is not None:
            self.widget.setChecked(value)

    @property
    def value(self):
        return self.widget.isChecked()

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit

from .base import BaseField


class IntegerField(BaseField):
    def __init__(self, name, value=None, title=None):
        super().__init__(name, title)
        self.widget = QLineEdit()
        self.widget.input.setInputMethodHints(Qt.ImhFormattedNumbersOnly)
        if value is not None:
            self.widget.setText(str(value))

    @property
    def value(self):
        value = self.widget.text()
        value = int(value) if value.isnumeric() else 0
        return value

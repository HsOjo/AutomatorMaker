from PyQt5.QtWidgets import QLineEdit

from .base import BaseField


class StringField(BaseField):
    def __init__(self, name, value=None, title=None):
        super().__init__(name, title)
        self.widget = QLineEdit()
        if value is not None:
            self.widget.setText(str(value))

    @property
    def value(self):
        value = self.widget.text()
        return value

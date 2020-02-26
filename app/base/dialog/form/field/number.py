from PyQt5.QtCore import Qt

from .string import StringField


class NumberField(StringField):
    def __init__(self, name, value=None, title=None):
        super().__init__(name, value, title)
        self.widget.setInputMethodHints(Qt.ImhFormattedNumbersOnly)

    @property
    def value(self):
        value = self.widget.text()
        if value.isdigit():
            return int(value)
        else:
            value = float(value) if value.replace('.', '', count=1).isdigit() else 0
        return value

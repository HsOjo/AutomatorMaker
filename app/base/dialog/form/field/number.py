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
            v = value
            v = v[1:] if v[0:1] == '-' else v
            v = v.replace('.', '', 1) if v.count('.') == 1 else v
            value = float(value) if v.isdigit() else 0
        return value

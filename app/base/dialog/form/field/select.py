from PyQt5.QtWidgets import QComboBox

from .base import BaseField


class SelectField(BaseField):
    def __init__(self, name, options, value=None, title=None):
        super().__init__(name, title)
        self._options = options
        self.widget = QComboBox()
        self.widget.addItems(['%s' % i for i in options])
        if isinstance(options, dict):
            options = list(options.values())
        if value in options:
            self.widget.setCurrentIndex(options.index(value))

    @property
    def value(self):
        index = self.widget.currentIndex()
        options = self._options
        if isinstance(options, dict):
            options = list(options.values())
        if 0 <= index < len(options):
            return options[index]
        else:
            return None

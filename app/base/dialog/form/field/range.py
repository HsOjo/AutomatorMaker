import math

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider

from .base import BaseField


class RangeField(BaseField):
    def __init__(self, name, value=None, min=0, max=100, accuracy=0, title=None):
        super().__init__(name, title)
        self.widget = QSlider()
        self.widget.setOrientation(Qt.Horizontal)

        self._accuracy = accuracy
        self._multiple = math.pow(10, accuracy)
        if accuracy:
            min *= self._multiple
            max *= self._multiple
            value *= self._multiple

        self.widget.setMinimum(min)
        self.widget.setMaximum(max)
        if value is not None:
            self.widget.setValue(value)

    @property
    def value(self):
        value = self.widget.value()
        if self._accuracy:
            value /= self._multiple
        return value

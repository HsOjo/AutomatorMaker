from typing import List

from .string import StringField


class ColorField(StringField):
    def __init__(self, name, value: List[int] = None, title=None):
        super().__init__(name, title=title)
        if isinstance(value, list):
            value = ','.join([str(i) for i in value])
        self.widget.setText(value)

    @property
    def value(self):
        value = []
        value_str = self.widget.text()
        if value_str.count(',') >= 2:
            value = value_str.split(',')
            value = [i.strip() for i in value]
            value = [int(i) for i in value if i.isnumeric()]

        if len(value) == 4:
            return value
        elif len(value) == 3:
            value.append(255)
            return value
        else:
            return value_str

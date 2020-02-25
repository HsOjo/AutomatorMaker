from typing import List

from .string import StringField


class RectField(StringField):
    def __init__(self, name, value: List[int] = None, title=None):
        super().__init__(name, title=title)
        if value is not None:
            value = ','.join([str(i) for i in value])
            self.widget.setText(value)

    @property
    def value(self):
        value = self.widget.text()
        value = value.split(',')
        value = [i.strip() for i in value]
        value = [int(i) for i in value if i.isnumeric()]
        if len(value) == 4:
            return value
        else:
            return None

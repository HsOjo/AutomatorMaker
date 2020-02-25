class BaseField:
    def __init__(self, name, title=None):
        self.name = name
        self.widget = None
        self._title = title

    @property
    def value(self):
        return None

    @property
    def title(self):
        return self._title if self._title is not None else self.name

class BaseOperation:
    def __init__(self, event):
        self._event = event

    def update(self):
        pass

    def draw(self):
        pass

    @property
    def params(self) -> dict:
        return {}

    def load_params(self, **params):
        for k, v in params:
            if hasattr(self, k):
                setattr(self, k, v)

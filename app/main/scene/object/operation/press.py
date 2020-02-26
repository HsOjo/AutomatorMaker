from .tap import TapOperation
from ..advance_circle import AdvanceCircle


class PressOperation(TapOperation):
    def __init__(self, event):
        super().__init__(event)
        self._font.set_text('Press')
        self._time = 1

    @property
    def params(self) -> dict:
        params = super().params
        params.update(
            time=self._time
        )
        return params

    def load_params(self, **params):
        super().load_params(**params)
        self._time = params.get('time', self._time)

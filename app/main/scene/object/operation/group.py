from .tap import TapOperation


class GroupOperation(TapOperation):
    def __init__(self, event):
        super().__init__(event)
        self._font.set_text('Group')
        self._actions = ''

    @property
    def params(self) -> dict:
        params = super().params
        params = dict((k, params[k]) for k in ['x', 'y'])
        params['actions'] = self._actions
        return params

    def load_params(self, origin, **params):
        self._actions = params.pop('actions', '')
        super().load_params(origin, **params)

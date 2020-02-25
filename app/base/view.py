class BaseView:
    def __init__(self):
        self.setupUi(self)
        self._callback_init()
        self.register_callback()

    def _callback_init(self):
        pass

    def register_callback(self):
        pass

    def setupUi(self, widget):
        pass

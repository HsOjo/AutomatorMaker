class BaseView:
    def __init__(self):
        self.setupUi(self)
        self.callback_init()
        self.callback_event_register()

    def callback_init(self):
        pass

    def callback_event_register(self):
        pass

    def setupUi(self, widget):
        pass

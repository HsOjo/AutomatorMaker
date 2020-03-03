from typing import List

from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel

from .field import BaseField
from ..ui.form import Ui_FormDialog
from ... import BaseView


class FormView(Ui_FormDialog, BaseView):
    def callback_event_register(self):
        self.buttonBox.accepted.connect(self._callback_accepted)
        self.buttonBox.rejected.connect(self._callback_rejected)

    def _callback_accepted(self):
        pass

    def _callback_rejected(self):
        pass


class FormDialog(QDialog, FormView):
    def __init__(self, fields: List[BaseField], title=None, **kwargs):
        self._fields = None
        super().__init__(**kwargs)
        self._fields = fields
        for field in fields:
            layout = QHBoxLayout()
            label = QLabel()
            label.setText(field.title)
            layout.addWidget(label)
            layout.addWidget(field.widget)
            layout.setStretch(0, 0)
            layout.setStretch(1, 1)
            self.verticalLayoutInput.addLayout(layout)
        if title is not None:
            self.setWindowTitle(title)
        ms = self.minimumSize()
        ms.setWidth(max(ms.width(), 320))
        ms.setHeight(max(ms.height(), len(fields) * 32, 240))
        self.setMinimumSize(ms)
        self.resize(ms)

    @property
    def data(self):
        if self._fields is not None:
            return dict((field.name, field.value) for field in self._fields)

    @staticmethod
    def input(fields: List[BaseField], title=None):
        fd = FormDialog(**locals())
        if fd.exec_():
            return fd.data

    def _callback_accepted(self):
        self.close()

    def _callback_rejected(self):
        self.close()

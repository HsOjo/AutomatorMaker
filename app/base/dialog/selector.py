from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

from .ui.select import Ui_SelectDialog
from ..helper import TableHelper
from ..view import BaseView


class SelectorView(Ui_SelectDialog, BaseView):
    def register_callback(self):
        self.buttonBox.accepted.connect(self._callback_accepted)
        self.buttonBox.rejected.connect(self._callback_rejected)

        self.tableWidget_Items.setCurrentCell(-1, -1)
        self.tableWidget_Items._resizeEvent = self.tableWidget_Items.resizeEvent
        self.tableWidget_Items.resizeEvent = self._callback_table_resize

    def _callback_accepted(self):
        pass

    def _callback_rejected(self):
        pass

    def _callback_table_resize(self, e: QResizeEvent) -> None:
        self.tableWidget_Items._resizeEvent(e)
        TableHelper.auto_inject_columns_width(self.tableWidget_Items)


class SelectDialog(QDialog, SelectorView):
    def __init__(self, title=None, cols_title=None, rows=None, item_keys=None, **kwargs):
        super().__init__(**kwargs)
        self._item_keys = item_keys

        if title is not None:
            self.setWindowTitle(title)

        self.tableWidget_Items.setColumnCount(len(cols_title))
        for col_index, col_title in enumerate(cols_title):
            self.tableWidget_Items.setHorizontalHeaderItem(
                col_index, QTableWidgetItem(col_title)
            )

        for row_index, row in enumerate(rows):
            self.tableWidget_Items.insertRow(row_index)
            for col_index, col in enumerate(row):
                self.tableWidget_Items.setItem(
                    row_index, col_index, QTableWidgetItem(str(col))
                )

    @staticmethod
    def select(parent=None, title=None, cols_title=None, rows=None, item_keys=None):
        sw = SelectDialog(**locals())
        if sw.exec_():
            if item_keys is None:
                return sw.index
            else:
                return sw.item

    @property
    def index(self):
        return self.tableWidget_Items.currentRow()

    @property
    def item(self):
        row_index = self.tableWidget_Items.currentRow()
        if 0 <= row_index < self.tableWidget_Items.rowCount():
            col_num = self.tableWidget_Items.columnCount()
            item = dict([(
                self._item_keys[col_index],
                self.tableWidget_Items.item(row_index, col_index).text()
            ) for col_index in range(col_num)])
            return item
        else:
            return None

    def _callback_accepted(self):
        self.close()

    def _callback_rejected(self):
        self.close()


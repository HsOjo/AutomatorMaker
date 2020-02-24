from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class TableHelper:
    @staticmethod
    def auto_inject_columns_width(table: QTableWidget):
        col_num = table.columnCount()
        col_length = [0 for _ in range(col_num)]
        for col_index in range(col_num):
            col = table.horizontalHeaderItem(col_index)
            col_length[col_index] += len(col.text())
        row_num = table.rowCount()
        for row_index in range(row_num):
            for col_index in range(col_num):
                item = table.item(row_index, col_index)
                col_length[col_index] += len(item.text())
        col_length = [l / (row_num + 1) for l in col_length]
        sum_length = sum(col_length)
        table_width = table.width() - 20
        for col_index in range(col_num):
            width = int(col_length[col_index] / sum_length * table_width)
            table.setColumnWidth(col_index, width)

    @staticmethod
    def set_text(table: QTableWidget, row, col, text):
        item = table.item(row, col)
        text = ('%s' if type(text) in [int, str] else '%a') % text
        if item is None or item.text() != text:
            table.setItem(row, col, QTableWidgetItem(text))

    @staticmethod
    def sync_data(table: QTableWidget, data):
        data_l = len(data)
        rows = table.rowCount()

        for row_index, row in enumerate(data):
            if row_index >= rows:
                table.insertRow(row_index)
            for col_index, col in enumerate(row):
                TableHelper.set_text(table, row_index, col_index, col)

        rows = table.rowCount()
        for row_index in range(rows - 1, data_l, -1):
            table.removeRow(row_index)

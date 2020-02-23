from PyQt5.QtWidgets import QTableWidget


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
        col_length = [l / row_num for l in col_length]
        sum_length = sum(col_length)
        table_width = table.width() - 20
        for col_index in range(col_num):
            width = int(col_length[col_index] / sum_length * table_width)
            table.setColumnWidth(col_index, width)

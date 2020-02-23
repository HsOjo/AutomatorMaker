# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class Ui_SelectDialog(object):
    def setupUi(self, SelectDialog):
        SelectDialog.setObjectName("SelectDialog")
        SelectDialog.resize(400, 300)
        SelectDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.verticalLayout = QtWidgets.QVBoxLayout(SelectDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget_Items = QtWidgets.QTableWidget(SelectDialog)
        self.tableWidget_Items.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_Items.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_Items.setObjectName("tableWidget_Items")
        self.tableWidget_Items.setColumnCount(0)
        self.tableWidget_Items.setRowCount(0)
        self.tableWidget_Items.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableWidget_Items)
        self.buttonBox = QtWidgets.QDialogButtonBox(SelectDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SelectDialog)
        self.buttonBox.accepted.connect(SelectDialog.accept)
        self.buttonBox.rejected.connect(SelectDialog.reject)
        self.tableWidget_Items.itemDoubleClicked['QTableWidgetItem*'].connect(SelectDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(SelectDialog)

    def retranslateUi(self, SelectDialog):
        _translate = QtCore.QCoreApplication.translate
        SelectDialog.setWindowTitle(_translate("SelectDialog", "Select Dialog"))

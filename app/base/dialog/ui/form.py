# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FormDialog(object):
    def setupUi(self, FormDialog):
        FormDialog.setObjectName("FormDialog")
        FormDialog.resize(400, 300)
        FormDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.verticalLayout = QtWidgets.QVBoxLayout(FormDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayoutInput = QtWidgets.QVBoxLayout()
        self.verticalLayoutInput.setObjectName("verticalLayoutInput")
        self.verticalLayout.addLayout(self.verticalLayoutInput)
        self.buttonBox = QtWidgets.QDialogButtonBox(FormDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(FormDialog)
        self.buttonBox.accepted.connect(FormDialog.accept)
        self.buttonBox.rejected.connect(FormDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FormDialog)

    def retranslateUi(self, FormDialog):
        _translate = QtCore.QCoreApplication.translate
        FormDialog.setWindowTitle(_translate("FormDialog", "Form Dialog"))

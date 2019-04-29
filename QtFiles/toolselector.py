# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toolselector.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(341, 484)
        self.Browse = QtWidgets.QPushButton(Dialog)
        self.Browse.setGeometry(QtCore.QRect(40, 450, 75, 23))
        self.Browse.setObjectName("Browse")
        self.Select = QtWidgets.QPushButton(Dialog)
        self.Select.setGeometry(QtCore.QRect(140, 450, 75, 23))
        self.Select.setObjectName("Select")
        self.Cancel = QtWidgets.QPushButton(Dialog)
        self.Cancel.setGeometry(QtCore.QRect(240, 450, 75, 23))
        self.Cancel.setObjectName("Cancel")
        self.Description = QtWidgets.QGroupBox(Dialog)
        self.Description.setGeometry(QtCore.QRect(10, 10, 321, 431))
        self.Description.setObjectName("Description")
        self.Icon = QtWidgets.QLabel(self.Description)
        self.Icon.setScaledContents(True)
        self.Icon.setGeometry(QtCore.QRect(20, 340, 50, 50))
        self.Icon.setMinimumSize(QtCore.QSize(50, 50))
        self.Icon.setObjectName("Icon")
        self.ToolDescription = QtWidgets.QLabel(self.Description)
        self.ToolDescription.setGeometry(QtCore.QRect(100, 300, 211, 121))
        self.ToolDescription.setObjectName("ToolDescription")
        self.treeView = QtWidgets.QTreeView(self.Description)
        self.treeView.setGeometry(QtCore.QRect(20, 20, 281, 311))
        self.treeView.setObjectName("treeView")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Browse.setText(_translate("Dialog", "Browse"))
        self.Select.setText(_translate("Dialog", "Select"))
        self.Cancel.setText(_translate("Dialog", "Cancel"))
        self.Description.setTitle(_translate("Dialog", "Tool Description"))
        self.Icon.setText(_translate("Dialog", "TextLabel"))
        self.ToolDescription.setText(_translate("Dialog", "TextLabel"))


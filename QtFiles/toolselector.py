# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toolselector.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Tool_Selector(object):
    def setupUi(self, Tool_Selector):
        Tool_Selector.setObjectName("Tool_Selector")
        Tool_Selector.resize(341, 484)
        self.Description = QtWidgets.QGroupBox(Tool_Selector)
        self.Description.setGeometry(QtCore.QRect(10, 10, 321, 431))
        self.Description.setStyleSheet("")
        self.Description.setObjectName("Description")
        self.Icon = QtWidgets.QLabel(self.Description)
        self.Icon.setGeometry(QtCore.QRect(30, 350, 50, 50))
        self.Icon.setMinimumSize(QtCore.QSize(50, 50))
        self.Icon.setObjectName("Icon")
        self.ToolDescription = QtWidgets.QLabel(self.Description)
        self.ToolDescription.setGeometry(QtCore.QRect(100, 340, 211, 81))
        self.ToolDescription.setObjectName("ToolDescription")
        self.treeView = QtWidgets.QTreeView(self.Description)
        self.treeView.setGeometry(QtCore.QRect(20, 20, 281, 311))
        self.treeView.setObjectName("treeView")
        self.Cancel = QtWidgets.QPushButton(Tool_Selector)
        self.Cancel.setGeometry(QtCore.QRect(250, 450, 75, 23))
        self.Cancel.setObjectName("Cancel")
        self.Select = QtWidgets.QPushButton(Tool_Selector)
        self.Select.setGeometry(QtCore.QRect(170, 450, 75, 23))
        self.Select.setObjectName("Select")

        self.retranslateUi(Tool_Selector)
        QtCore.QMetaObject.connectSlotsByName(Tool_Selector)

    def retranslateUi(self, Tool_Selector):
        _translate = QtCore.QCoreApplication.translate
        Tool_Selector.setWindowTitle(_translate("Tool_Selector", "Dialog"))
        self.Description.setTitle(_translate("Tool_Selector", "Tool Description"))
        self.Icon.setText(_translate("Tool_Selector", "TextLabel"))
        self.ToolDescription.setText(_translate("Tool_Selector", "TextLabel"))
        self.Cancel.setText(_translate("Tool_Selector", "Cancel"))
        self.Select.setText(_translate("Tool_Selector", "Select"))


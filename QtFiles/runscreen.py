# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'runscreen.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(944, 472)
        self.groupBox_6 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_6.setGeometry(QtCore.QRect(620, 0, 311, 361))
        self.groupBox_6.setObjectName("groupBox_6")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.groupBox_6)
        self.scrollArea_2.setGeometry(QtCore.QRect(20, 20, 281, 331))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 279, 329))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Report_Label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.Report_Label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.Report_Label.setObjectName("Report_Label")
        self.verticalLayout.addWidget(self.Report_Label)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 0, 600, 461))
        self.groupBox_2.setMinimumSize(QtCore.QSize(600, 450))
        self.groupBox_2.setAutoFillBackground(True)
        self.groupBox_2.setObjectName("groupBox_2")
        self.cameraLabel = QtWidgets.QLabel(self.groupBox_2)
        self.cameraLabel.setGeometry(QtCore.QRect(19, 30, 540, 405))
        self.cameraLabel.setMinimumSize(QtCore.QSize(100, 405))
        self.cameraLabel.setMaximumSize(QtCore.QSize(540, 405))
        self.cameraLabel.setObjectName("cameraLabel")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(620, 370, 171, 91))
        self.groupBox.setAutoFillBackground(True)
        self.groupBox.setObjectName("groupBox")
        self.StopButton = QtWidgets.QPushButton(self.groupBox)
        self.StopButton.setGeometry(QtCore.QRect(10, 30, 71, 50))
        self.StopButton.setMinimumSize(QtCore.QSize(65, 50))
        self.StopButton.setObjectName("StopButton")
        self.runButton = QtWidgets.QPushButton(self.groupBox)
        self.runButton.setGeometry(QtCore.QRect(90, 30, 65, 50))
        self.runButton.setMinimumSize(QtCore.QSize(65, 50))
        self.runButton.setObjectName("runButton")
        self.SetupMode = QtWidgets.QPushButton(Dialog)
        self.SetupMode.setGeometry(QtCore.QRect(800, 400, 121, 50))
        self.SetupMode.setMinimumSize(QtCore.QSize(65, 50))
        self.SetupMode.setObjectName("SetupMode")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox_6.setTitle(_translate("Dialog", "GroupBox"))
        self.Report_Label.setText(_translate("Dialog", "TextLabel"))
        self.groupBox_2.setTitle(_translate("Dialog", "Camera "))
        self.cameraLabel.setText(_translate("Dialog", "Camera Screen"))
        self.groupBox.setTitle(_translate("Dialog", "Controls"))
        self.StopButton.setText(_translate("Dialog", "Stop"))
        self.runButton.setText(_translate("Dialog", "Run"))
        self.SetupMode.setText(_translate("Dialog", "Go to \n"
"Setup Mode"))


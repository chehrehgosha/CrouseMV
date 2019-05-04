# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'binarymask.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 640)
        self.ThresholdSlider = QtWidgets.QSlider(Dialog)
        self.ThresholdSlider.setGeometry(QtCore.QRect(19, 530, 441, 20))
        self.ThresholdSlider.setMinimum(0)
        self.ThresholdSlider.setMaximum(255)
        self.ThresholdSlider.setProperty("value", 127)
        self.ThresholdSlider.setOrientation(QtCore.Qt.Horizontal)
        self.ThresholdSlider.setObjectName("ThresholdSlider")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 590, 461, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.OutputName = QtWidgets.QLineEdit(Dialog)
        self.OutputName.setGeometry(QtCore.QRect(120, 590, 113, 20))
        self.OutputName.setObjectName("OutputName")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 590, 81, 16))
        self.label.setObjectName("label")
        self.ChangedLabel = QtWidgets.QLabel(Dialog)
        self.ChangedLabel.setGeometry(QtCore.QRect(10, 2, 461, 521))
        self.ChangedLabel.setObjectName("ChangedLabel")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(190, 550, 101, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Output Name:"))
        self.ChangedLabel.setText(_translate("Dialog", "TextLabel"))
        self.label_2.setText(_translate("Dialog", "Threshold"))


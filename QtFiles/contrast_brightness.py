# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'contrast_brightness.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 640)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 600, 461, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.ChangedLabel = QtWidgets.QLabel(Dialog)
        self.ChangedLabel.setGeometry(QtCore.QRect(10, 12, 461, 521))
        self.ChangedLabel.setObjectName("ChangedLabel")
        self.ContrastSlider = QtWidgets.QSlider(Dialog)
        self.ContrastSlider.setGeometry(QtCore.QRect(30, 540, 160, 19))
        self.ContrastSlider.setMaximum(100)
        self.ContrastSlider.setSingleStep(1)
        self.ContrastSlider.setProperty("value", 0)
        self.ContrastSlider.setOrientation(QtCore.Qt.Horizontal)
        self.ContrastSlider.setObjectName("ContrastSlider")
        self.BrightnessSlider = QtWidgets.QSlider(Dialog)
        self.BrightnessSlider.setGeometry(QtCore.QRect(300, 540, 160, 19))
        self.BrightnessSlider.setMaximum(100)
        self.BrightnessSlider.setMinimum(0)
        self.BrightnessSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.BrightnessSlider.setTickInterval(5)
        self.BrightnessSlider.setValue(1)
        self.BrightnessSlider.setOrientation(QtCore.Qt.Horizontal)
        self.BrightnessSlider.setObjectName("BrightnessSlider")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(330, 560, 101, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(80, 560, 61, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ChangedLabel.setText(_translate("Dialog", "TextLabel"))
        self.label_2.setText(_translate("Dialog", "Brightness"))
        self.label_3.setText(_translate("Dialog", "Contrast"))


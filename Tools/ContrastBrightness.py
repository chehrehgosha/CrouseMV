import random
import time
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog,QVBoxLayout,QPushButton,\
    QSpacerItem,QGroupBox,QLabel,QCheckBox,QHBoxLayout,QLineEdit,QFileDialog
from PyQt5.QtGui import QPixmap
import cv2,os,globalVariables
from components import regionInspector
import numpy as np
class Tool(object):
    def __init__(self,
                 settings = None,
                 index=None,
                 status='initialize',
                 sourcePath = None,
                 resultPath = None):

        if status=='initialize':
            self.dlg = QFileDialog()
            self.dlg.setFileMode(QFileDialog.AnyFile)
            self.dlg.setNameFilters(["Images (*.jpg)"])
            self.dlg.selectNameFilter("Images (*.jpg)")

            self.dlg.exec()
            self.filenames = self.dlg.selectedFiles()
            # while(len(filenames)==0):
            #     time.sleep(0.01)
            self.ContBright = QDialog()
            self.UI = self.Ui_Dialog()

            self.UI.setupUi(self.ContBright)
            self.UI.buttonBox.accepted.connect(self.accepted)
            image = QPixmap(self.filenames[0])
            image = image.scaled(self.UI.ChangedLabel.width(), self.UI.ChangedLabel.height(), Qt.KeepAspectRatio)
            # self.UI.ChangedLabel.setScaledContents(True)
            self.UI.ChangedLabel.setPixmap(image)
            self.UI.ContrastSlider.valueChanged.connect(self.SliderChanged)
            self.UI.BrightnessSlider.valueChanged.connect(self.SliderChanged)
            self.ContBright.exec()

        elif status=='modify':
            self.dlg = QFileDialog()
            self.dlg.setFileMode(QFileDialog.AnyFile)
            self.dlg.setNameFilters(["Images (*.jpg)"])
            self.dlg.selectNameFilter("Images (*.jpg)")

            self.dlg.exec()
            self.filenames = self.dlg.selectedFiles()
            # while(len(filenames)==0):
            #     time.sleep(0.01)
            self.ContBright = QDialog()
            self.UI = self.Ui_Dialog()

            self.UI.setupUi(self.ContBright)
            self.UI.buttonBox.accepted.connect(self.accepted)
            image = QPixmap(self.filenames[0])
            image = image.scaled(self.UI.ChangedLabel.width(), self.UI.ChangedLabel.height(), Qt.KeepAspectRatio)
            # self.UI.ChangedLabel.setScaledContents(True)
            self.UI.ChangedLabel.setPixmap(image)
            self.UI.ContrastSlider.valueChanged.connect(self.SliderChanged)
            self.UI.BrightnessSlider.valueChanged.connect(self.SliderChanged)
            self.ContBright.exec()

        elif status == 'run':
            img = cv2.imread(settings['input'])
            img2 = np.array(img, np.int16)
            img2 = np.multiply(img2, settings['contrast'] / 100)
            img2 = np.add(img2, settings['brightness'])
            img2[img2 > 255] = 255
            img2[img2 < 0] = 0
            img = np.array(img2, np.uint8)
            # print(img)
            cv2.imwrite('temp/'+settings['output']+'.jpg', img)
            cv2.imwrite(resultPath, img)
            self.report = '* * * * * * * * *\n Brightness/Contrast Tool Done\n\n* * * * * * * * *\n'

    def SliderChanged(self):
        img = cv2.imread(self.filenames[0])
        img2 = np.array(img,np.int16)
        img2 = np.multiply(img2,self.UI.ContrastSlider.value()/100)
        img2 = np.add(img2, self.UI.BrightnessSlider.value())
        img2[img2 > 255] = 255
        img2[img2 < 0] = 0
        img = np.array(img2, np.uint8)
        # print(img)
        cv2.imwrite('temp/X.jpg', img)
        image = QPixmap('temp/X.jpg')
        image = image.scaled(self.UI.ChangedLabel.width(), self.UI.ChangedLabel.height(), Qt.KeepAspectRatio)
        # self.UI.ChangedLabel.setScaledContents(True)
        self.UI.ChangedLabel.setPixmap(image)

    def accepted(self):
        img = cv2.imread('temp/X.jpg')
        cv2.imwrite('temp/'+self.UI.OutputName.text()+'.jpg',img)
        self.ContBright.close()
        globalVariables.toolsListText.append({'toolType': 'ContBright',
                                                     'filePath': os.path.abspath(__file__),
                                                     'fileName': os.path.basename(__file__),
                                                     'brightness':self.UI.BrightnessSlider.value(),
                                                     'contrast':self.UI.ContrastSlider.value(),
                                                     'output': self.UI.ChangedLabel.text(),
                                                     'input':self.filenames[0]})
        globalVariables.timeLineFlag.value = 1

    class Ui_Dialog(object):
        def setupUi(self, Dialog):
            Dialog.setObjectName("Dialog")
            Dialog.resize(480, 640)
            self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
            self.buttonBox.setGeometry(QtCore.QRect(10, 600, 461, 32))
            self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
            self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
            self.buttonBox.setObjectName("buttonBox")
            self.ChangedLabel = QtWidgets.QLabel(Dialog)
            self.ChangedLabel.setGeometry(QtCore.QRect(10, 12, 461, 521))
            self.ChangedLabel.setObjectName("ChangedLabel")
            self.ContrastSlider = QtWidgets.QSlider(Dialog)
            self.ContrastSlider.setGeometry(QtCore.QRect(30, 540, 160, 19))
            self.ContrastSlider.setMinimum(0)
            self.ContrastSlider.setMaximum(300)
            self.ContrastSlider.setSingleStep(1)
            self.ContrastSlider.setProperty("value", 100)
            self.ContrastSlider.setOrientation(QtCore.Qt.Horizontal)
            self.ContrastSlider.setObjectName("ContrastSlider")
            self.BrightnessSlider = QtWidgets.QSlider(Dialog)
            self.BrightnessSlider.setGeometry(QtCore.QRect(300, 540, 160, 19))
            self.BrightnessSlider.setMinimum(-200)
            self.BrightnessSlider.setMaximum(200)
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
            self.OutputName = QtWidgets.QLineEdit(Dialog)
            self.OutputName.setGeometry(QtCore.QRect(120, 600, 113, 20))
            self.OutputName.setObjectName("OutputName")
            self.label = QtWidgets.QLabel(Dialog)
            self.label.setGeometry(QtCore.QRect(30, 600, 81, 16))
            self.label.setObjectName("label")

            self.retranslateUi(Dialog)

            self.buttonBox.rejected.connect(Dialog.reject)
            QtCore.QMetaObject.connectSlotsByName(Dialog)

        def retranslateUi(self, Dialog):
            _translate = QtCore.QCoreApplication.translate
            Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
            self.ChangedLabel.setText(_translate("Dialog", "TextLabel"))
            self.label_2.setText(_translate("Dialog", "Brightness"))
            self.label_3.setText(_translate("Dialog", "Contrast"))
            self.label.setText(_translate("Dialog", "Output Name:"))


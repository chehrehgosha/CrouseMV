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

from components import Camera


class Tool(object):
    def __init__(self,
                 settings = None,
                 index=None,
                 status='initialize',
                 sourcePath = None,
                 resultPath = None):

        if status=='initialize':
            self.status = status
            self.BinaryMaskInit = QDialog()
            self.mainLayout = QHBoxLayout()
            self.BinaryMaskInit.setLayout(self.mainLayout)

            self.ImgBtn = QPushButton('Select Existing\n File')
            self.ImgBtn.setObjectName('StaticImage')
            self.ImgBtn.setMinimumSize(QtCore.QSize(130, 50))
            self.mainLayout.addWidget(self.ImgBtn)
            self.CamBtn = QPushButton('Capture from\n Camera')
            self.CamBtn.setObjectName('CameraImage')
            self.CamBtn.setMinimumSize(QtCore.QSize(130, 50))
            self.mainLayout.addWidget(self.CamBtn)

            self.ImgBtn.clicked.connect(self.image_source)
            self.CamBtn.clicked.connect(self.camera_source)
            globalVariables.guide_value.value = 'Status:\nChoose one of the options'
            globalVariables.guide_flag.value = 1
            self.BinaryMaskInit.exec()



            # while(len(filenames)==0):
            #     time.sleep(0.01)


        elif status=='modify':
            self.status = status
            self.index = index
            self.BinaryMaskInit = QDialog()
            self.mainLayout = QHBoxLayout()
            self.BinaryMaskInit.setLayout(self.mainLayout)

            self.ImgBtn = QPushButton('Select Existing\n File')
            self.ImgBtn.setObjectName('StaticImage')
            self.ImgBtn.setMinimumSize(QtCore.QSize(130, 50))
            self.mainLayout.addWidget(self.ImgBtn)
            self.CamBtn = QPushButton('Capture from\n Camera')
            self.CamBtn.setObjectName('CameraImage')
            self.CamBtn.setMinimumSize(QtCore.QSize(130, 50))
            self.mainLayout.addWidget(self.CamBtn)
            self.del_btn = QPushButton('Delete Tool')
            self.del_btn.setObjectName('DelTool')
            self.del_btn.setMinimumSize(QtCore.QSize(130, 50))
            self.mainLayout.addWidget(self.del_btn)

            self.ImgBtn.clicked.connect(self.image_source)
            self.CamBtn.clicked.connect(self.camera_source)
            self.del_btn.clicked.connect(self.accepted)
            globalVariables.guide_value.value = 'Status:\nChoose one of the options'
            globalVariables.guide_flag.value = 1
            self.BinaryMaskInit.exec()

        elif status == 'run':
            img = cv2.imread(settings['input'], cv2.IMREAD_GRAYSCALE)
            ret, th1 = cv2.threshold(img, settings['threshold'], 255, cv2.THRESH_BINARY)
            cv2.imwrite('temp/' + settings['output']+'.jpg', th1)
            cv2.imwrite(resultPath, th1)
            self.report = '* * * * * * * * *\n Binary Mask Tool Done\n\n* * * * * * * * *\n'
    def image_source(self):
        self.BinaryMaskInit.close()
        globalVariables.guide_value.value = 'Status:\nChoose Desired File'
        globalVariables.guide_flag.value = 1
        self.dlg = QFileDialog()
        self.dlg.setFileMode(QFileDialog.AnyFile)
        self.dlg.setNameFilters(["Images (*.jpg)"])
        self.dlg.selectNameFilter("Images (*.jpg)")

        self.dlg.exec()
        self.filenames = self.dlg.selectedFiles()
        self.set_attributes()


    def camera_source(self):
        self.BinaryMaskInit.close()
        globalVariables.guide_value.value = 'Status:\nAdjust the Camera'
        globalVariables.guide_flag.value = 1
        Cam = Camera.Camera()
        Cam.setup_capture('temp/temp_image_for_contbri_tool.jpg')
        Cam.checkFile('temp/temp_image_for_contbri_tool.jpg')
        self.filenames = []
        self.filenames.append('temp/temp_image_for_contbri_tool.jpg')
        self.set_attributes()


    def set_attributes(self):
        self.BinaryMask = QDialog()
        self.UI = self.Ui_Dialog()

        self.UI.setupUi(self.BinaryMask)
        self.UI.buttonBox.accepted.connect(self.accepted)
        image = QPixmap(self.filenames[0])
        image = image.scaled(self.UI.ChangedLabel.width(), self.UI.ChangedLabel.height(), Qt.KeepAspectRatio)
        # self.UI.ChangedLabel.setScaledContents(True)
        self.UI.ChangedLabel.setPixmap(image)
        self.UI.ThresholdSlider.valueChanged.connect(self.ThresholdSliderChanged)
        # self.UI.BrightnessSlider.valueChanged.connect(self.BrightnessSliderChanged)
        self.BinaryMask.exec()

    def ThresholdSliderChanged(self):
        img = cv2.imread(self.filenames[0],cv2.IMREAD_GRAYSCALE)
        ret, th1 = cv2.threshold(img, self.UI.ThresholdSlider.value(), 255, cv2.THRESH_BINARY)
        # print(img)
        cv2.imwrite('temp/X.jpg', th1)
        image = QPixmap('temp/X.jpg')
        image = image.scaled(self.UI.ChangedLabel.width(), self.UI.ChangedLabel.height(), Qt.KeepAspectRatio)
        # self.UI.ChangedLabel.setScaledContents(True)
        self.UI.ChangedLabel.setPixmap(image)

    def accepted(self):
        self.BinaryMaskInit.close()
        button = self.mainLayout.sender()
        if button.objectName() == 'DelTool':
            del globalVariables.toolsListText[self.index]
            globalVariables.timeLineFlag.value = 1
        elif self.status is 'modify':
            globalVariables.guide_value.value = 'Status:\n-'
            globalVariables.guide_flag.value = 1
            img = cv2.imread('temp/X.jpg')
            cv2.imwrite('temp/' + self.UI.OutputName.text() + '.jpg', img)
            self.BinaryMask.close()
            globalVariables.toolsListText[self.index] = {'toolType': 'BinaryMask',
                                                     'filePath': os.path.abspath(__file__),
                                                     'fileName': os.path.basename(__file__),
                                                     'output': self.UI.OutputName.text(),
                                                      'input': self.filenames[0],
                                                      'threshold':self.UI.ThresholdSlider.value()}
            globalVariables.timeLineFlag.value = 1
        elif self.status is 'initialize':
            globalVariables.guide_value.value = 'Status:\n-'
            globalVariables.guide_flag.value = 1
            img = cv2.imread('temp/X.jpg')
            cv2.imwrite('temp/' + self.UI.OutputName.text() + '.jpg', img)
            self.BinaryMask.close()
            globalVariables.toolsListText.append({'toolType': 'BinaryMask',
                                                     'filePath': os.path.abspath(__file__),
                                                     'fileName': os.path.basename(__file__),
                                                     'output': self.UI.OutputName.text(),
                                                      'input': self.filenames[0],
                                                      'threshold':self.UI.ThresholdSlider.value()})
            globalVariables.timeLineFlag.value = 1

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
            self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
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

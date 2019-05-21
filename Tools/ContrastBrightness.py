
from PyQt5.QtCore import Qt
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
import cv2,os,globalVariables
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
            self.ContBrightInit = QDialog()
            self.mainLayout = QHBoxLayout()
            self.ContBrightInit.setLayout(self.mainLayout)

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
            self.ContBrightInit.exec()




        elif status=='modify':
            self.status = status
            self.index = index
            self.ContBrightInit = QDialog()
            self.mainLayout = QHBoxLayout()
            self.ContBrightInit.setLayout(self.mainLayout)

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
            self.ContBrightInit.exec()


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
    def image_source(self):
        self.ContBrightInit.close()
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
        self.ContBrightInit.close()

        Cam = Camera.Camera()
        Cam.setup_capture('temp/temp_image_for_contbri_tool.jpg')
        Cam.checkFile('temp/temp_image_for_contbri_tool.jpg')
        self.filenames = []
        self.filenames.append('temp/temp_image_for_contbri_tool.jpg')
        self.set_attributes()
    def set_attributes(self):
        self.ContBright = QDialog()
        self.UI = self.Ui_Dialog()
        globalVariables.guide_value.value = 'Status:\nAdjust Contrast and Brightness'
        globalVariables.guide_flag.value = 1
        self.UI.setupUi(self.ContBright)
        self.UI.buttonBox.accepted.connect(self.accepted)
        image = QPixmap(self.filenames[0])
        image = image.scaled(self.UI.ChangedLabel.width(), self.UI.ChangedLabel.height(), Qt.KeepAspectRatio)
        # self.UI.ChangedLabel.setScaledContents(True)
        self.UI.ChangedLabel.setPixmap(image)
        self.UI.ContrastSlider.valueChanged.connect(self.SliderChanged)
        self.UI.BrightnessSlider.valueChanged.connect(self.SliderChanged)
        self.ContBright.exec()

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
        self.ContBrightInit.close()
        button = self.mainLayout.sender()
        if button.objectName() == 'DelTool':
            del globalVariables.toolsListText[self.index]
            globalVariables.timeLineFlag.value = 1
        elif self.status is 'modify':
            globalVariables.guide_value.value = 'Status:\n-'
            globalVariables.guide_flag.value = 1
            img = cv2.imread('temp/X.jpg')
            cv2.imwrite('temp/' + self.UI.OutputName.text() + '.jpg', img)
            self.ContBright.close()
            globalVariables.toolsListText[self.index] = {'toolType': 'ContBright',
                                                  'filePath': os.path.abspath(__file__),
                                                  'fileName': os.path.basename(__file__),
                                                  'brightness': self.UI.BrightnessSlider.value(),
                                                  'contrast': self.UI.ContrastSlider.value(),
                                                  'output': self.UI.ChangedLabel.text(),
                                                  'input': self.filenames[0]}
            globalVariables.timeLineFlag.value = 1
        elif self.status is 'initialize':
            globalVariables.guide_value.value = 'Status:\n-'
            globalVariables.guide_flag.value = 1
            img = cv2.imread('temp/X.jpg')
            cv2.imwrite('temp/' + self.UI.OutputName.text() + '.jpg', img)
            self.ContBright.close()
            globalVariables.toolsListText.append({'toolType': 'ContBright',
                                                         'filePath': os.path.abspath(__file__),
                                                         'fileName': os.path.basename(__file__),
                                                         'brightness': self.UI.BrightnessSlider.value(),
                                                         'contrast': self.UI.ContrastSlider.value(),
                                                         'output': self.UI.ChangedLabel.text(),
                                                         'input': self.filenames[0]})
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


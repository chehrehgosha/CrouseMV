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
            self.UI.ContrastSlider.valueChanged.connect(self.ContrastSliderChanged)
            self.UI.BrightnessSlider.valueChanged.connect(self.BrightnessSliderChanged)
            self.ContBright.exec()
        # TODO modify according to new tool
        elif status=='modify':
            self.settings = settings
            self.index = index

            self.LEDDetection = QDialog()
            self.mainLayout = QVBoxLayout()
            self.LEDDetection.setLayout(self.mainLayout)


            self.secondQbox = QGroupBox("Input settings")
            self.mainLayout.addWidget(self.secondQbox)
            self.layout2 = QHBoxLayout()
            self.secondQbox.setLayout(self.layout2)
            self.layout2.addWidget(QLabel("Input File Name:"))
            self.layout2.setStretch(0, 1)
            self.InputFile = QLineEdit()
            self.InputFile.setObjectName('InputFile')
            self.layout2.addWidget(self.InputFile)
            self.layout2.setStretch(1, 1)

            self.thirdQbox = QGroupBox("Output settings")
            self.mainLayout.addWidget(self.thirdQbox)
            self.layout3 = QHBoxLayout()
            self.thirdQbox.setLayout(self.layout3)
            self.layout3.addWidget(QLabel("Input File Name:"))
            self.layout3.setStretch(0, 1)
            self.OutputFile = QLineEdit()
            self.OutputFile.setObjectName('InputFile')
            self.layout3.addWidget(self.OutputFile)
            self.layout3.setStretch(1, 1)

            self.fourthQbox = QGroupBox("LED settings")
            self.mainLayout.addWidget(self.fourthQbox)
            self.layout4 = QHBoxLayout()
            self.fourthQbox.setLayout(self.layout4)
            self.layout4.addWidget(QLabel("LED Name:"))
            self.layout4.setStretch(0, 1)
            self.LEDName = QLineEdit()
            self.LEDName.setObjectName('LED Name')
            self.layout4.addWidget(self.LEDName)
            self.layout4.setStretch(1, 1)

            self.spacer = QSpacerItem(100, 100)
            self.mainLayout.addItem(self.spacer)
            self.acceptBtn = QPushButton('Accept')
            self.acceptBtn.setObjectName('acceptBtn')
            self.mainLayout.addWidget(self.acceptBtn)
            self.deleteBtn = QPushButton('Delete')
            self.deleteBtn.setObjectName('deleteBtn')
            self.mainLayout.addWidget(self.deleteBtn)
            # self.firstQbox.setMaximumHeight(70)
            self.roiCheckBox = QCheckBox('Do you want to define ROI? (Region of Interest)')
            self.mainLayout.addWidget(self.roiCheckBox)
            self.acceptBtn.clicked.connect(self.toolModified)
            self.deleteBtn.clicked.connect(self.toolModified)
            self.LEDDetection.exec()

        elif status == 'run':

            img = cv2.imread('temp/'+settings['input'])
            # img =  cv2.imread('temp/rotatedp.jpg')
            template = cv2.imread('temp/'+settings['pattern_name']+'.jpg')
            # template = cv2.imread('temp/rotatedp.jpg')
            w, h = template.shape[1],template.shape[0]

            temp = settings['region']

            rect = temp[0]
            # circle = temp[1]

            RectCoordinates = rect['coordinates']
            self.MainMask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
            cv2.rectangle(self.MainMask,(RectCoordinates[0],RectCoordinates[1]),(RectCoordinates[2],RectCoordinates[3]),(255,255,255),-1)

            masked_data = cv2.bitwise_and(img, img, mask=self.MainMask)
            # Apply template Matching
            res = cv2.matchTemplate(masked_data, template, cv2.TM_CCORR_NORMED)

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if (max_val > settings['accuracy']):
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)

                cv2.rectangle(img, top_left, bottom_right, (0,255,255), 2)

                cv2.putText(img, settings['pattern_name'], (top_left[0],top_left[1]-8),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                cv2.imwrite('temp/' + settings['output'], img)
                cv2.imwrite(resultPath, img)
                self.report =  '* * * * * * * * *\n Pattern\tStatus\tAccuracy\n '  + settings['pattern_name']+ ' \tFounded \t '+str("{0:.2f}".format(max_val))+'\n\n* * * * * * * * *\n'
                self.out1 = top_left[0] + w/2
                self.out2 = top_left[1] + h/2
                ResultCode = 'globalVariables.'+ settings['pattern_name'] +' =[top_left[0] + w/2 , top_left[1] + h/2]'
                exec(ResultCode)
            else:
                cv2.imwrite('temp/' + settings['output'], img)
                cv2.imwrite(resultPath, img)
                self.report = '* * * * * * * * *\n Pattern\tStatus\n ' + settings[
                    'pattern_name'] + ' \tNot Found\n\n* * * * * * * * *\n'
    def BrightnessSliderChanged(self):
        img = cv2.imread(self.filenames[0])
        img2 = np.array(img,np.int16)

        img2 = np.add(img2, self.UI.BrightnessSlider.value())
        # print(img)
        img2[img2 > 255] = 255
        img2[img2 < 0] = 0
        img = np.array(img2,np.uint8)
        # print(img)
        cv2.imwrite('X.jpg', img)
        image = QPixmap('X.jpg')
        image = image.scaled(self.UI.ChangedLabel.width(), self.UI.ChangedLabel.height(), Qt.KeepAspectRatio)
        # self.UI.ChangedLabel.setScaledContents(True)
        self.UI.ChangedLabel.setPixmap(image)
    def ContrastSliderChanged(self):
        img = cv2.imread(self.filenames[0])
        img = np.multiply(img,self.UI.ContrastSlider.value()/100)
        cv2.imwrite('X.jpg',img)
        image = QPixmap('X.jpg')
        image = image.scaled(self.UI.ChangedLabel.width(), self.UI.ChangedLabel.height(), Qt.KeepAspectRatio)

        # self.UI.ChangedLabel.setScaledContents(True)
        self.UI.ChangedLabel.setPixmap(image)
    # TODO modify according to new tool
    def toolModified(self):
        self.LEDDetection.close()
        button = self.mainLayout.sender()
        if button.objectName() == 'acceptBtn':
            originArray=[]
            if self.roiCheckBox.isChecked() is True:
                inspectorModule = regionInspector.regionInspector(originArray, 'temp/' + self.InputFile.text(),'LedDetector')
                originArray = inspectorModule.getOriginArray()

            self.ValueDialog = QDialog()
            self.ValueDialogUi = Ui_ValueDialog()
            self.ValueDialogUi.setupUi(self.ValueDialog)

            self.ValueDialogUi.buttonBox.accepted.connect(self.buttonAccept)
            self.ValueDialog.exec()

            if len(originArray) is not 0:
                globalVariables.toolsListText[self.index]={'toolType':'LEDDetection',
                                                  # 'illumination':str(illuPercent),
                                                  'filePath':os.path.abspath(__file__),
                                                  'fileName':os.path.basename(__file__),
                                                  'inspection':globalVariables.toolsListText[self.index]['inspection'],
                                                  'region':originArray,
                                                  'HSVValues':self.Values,
                                                  'output':self.OutputFile.text(),
                                                  'input':self.InputFile.text(),
                                                  'led_name':self.LEDName.text()}
            else:
                globalVariables.toolsListText[self.index]={'toolType':'LEDDetection',
                                                  # 'illumination':str(illuPercent),
                                                  'filePath':os.path.abspath(__file__),
                                                  'fileName':os.path.basename(__file__),
                                                  'inspection':globalVariables.toolsListText[self.index]['inspection'],
                                                  'region':originArray,
                                                  'HSVValues':self.Values,
                                                  'output':self.OutputFile.text(),
                                                  'input':self.InputFile.text(),
                                                  'led_name':self.LEDName.text()}
            globalVariables.timeLineFlag.value = 1

        elif button.objectName() == 'deleteBtn':
            del globalVariables.toolsListText[self.index]
            globalVariables.timeLineFlag.value = 1
            self.LEDDetection.close()

    def illuAccepted(self):
        self.PatternCheckTool.close()

        img = cv2.imread('temp/'+self.TargetFile.text())
        r = cv2.selectROI("Please select region of pattern",img)
        cv2.destroyWindow("Please select region of pattern")

        #TODO How the selectROI returns:

        CheckRegion = [{"style":'rect',
                       'coordinates':[ int(r[0]),int(r[1]),int(r[0] + r[2]),int(r[1] + r[3])]}]

        r = cv2.selectROI('Please select your pattern',img)
        cv2.destroyWindow('Please select your pattern')
        imCrop = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        cv2.imwrite('temp/'+self.PatternName.text()+'.jpg',imCrop)

        if len(CheckRegion) is not 0:

            globalVariables.toolsListText.append({'toolType':'PatternCheckTool',
                                                  # 'illumination':str(illuPercent),
                                                  'filePath':os.path.abspath(__file__),
                                                  'fileName':os.path.basename(__file__),
                                                  'inspection':True,
                                                  'region':CheckRegion,
                                                  'accuracy':float(self.AccuracyLine.text()),
                                                  # 'HSVValues':self.Values,
                                                  'output':self.OutputFile.text(),
                                                  'input':self.TargetFile.text(),
                                                  'pattern_name':self.PatternName.text()})
        else:
            globalVariables.toolsListText.append({'toolType': 'PatternCheckTool',
                                                  # 'illumination': str(illuPercent),
                                                  'filePath': os.path.abspath(__file__),
                                                  'fileName': os.path.basename(__file__),
                                                  'inspection': False,
                                                  # 'region': originArray,
                                                  'output':self.OutputFile.text(),
                                                  'input':self.InputFile.text(),
                                                  'pattern_name': self.PatternName.text()})
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
    def accepted(self):
        img = cv2.imread('X.jpg')
        cv2.imwrite(self.UI.OutputName.text()+'.jpg',img)
        self.ContBright.close()
        globalVariables.toolsListText[self.index] = {'toolType': 'ContBright',
                                                     'filePath': os.path.abspath(__file__),
                                                     'fileName': os.path.basename(__file__),
                                                     'output': self.UI.ChangedLabel.text()}

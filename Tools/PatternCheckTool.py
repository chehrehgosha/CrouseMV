import ctypes
import random
import string
import threading
from PyQt5.QtWidgets import QDialog,QVBoxLayout,QPushButton,\
    QSpacerItem,QGroupBox,QLabel,QCheckBox,QHBoxLayout,QLineEdit
import cv2,os,globalVariables
from components import regionInspector,Camera
import numpy as np
from PyQt5 import QtCore
class Tool(object):
    def __init__(self,
                 settings = None,
                 index=None,
                 status='initialize',
                 resultPath = None,
                 sourcePath = None):
        if status=='initialize':
            self.PatternCheckTool = QDialog()
            self.mainLayout = QVBoxLayout()
            self.PatternCheckTool.setLayout(self.mainLayout)

            self.secondQbox = QGroupBox("Target Image")
            self.mainLayout.addWidget(self.secondQbox)
            self.layout2 = QHBoxLayout()
            self.secondQbox.setLayout(self.layout2)
            self.layout2.addWidget(QLabel("Name of the image where you want to search the pattern"))
            self.layout2.setStretch(0, 1)
            self.TargetFile = QLineEdit('ww.jpg')
            self.TargetFile.setObjectName('InputFile')
            self.layout2.addWidget(self.TargetFile)
            self.layout2.setStretch(1, 1)


            self.Accuracy = QGroupBox("Accuracy:")
            self.mainLayout.addWidget(self.Accuracy)
            self.AccuracyLayout = QHBoxLayout()
            self.Accuracy.setLayout(self.AccuracyLayout)
            self.AccuracyLayout.addWidget(QLabel("The threshold for the accurcay (-1 to +1):"))
            self.AccuracyLayout.setStretch(0, 1)
            self.AccuracyLine = QLineEdit('0.7')
            self.AccuracyLine.setObjectName('InputFile')
            self.AccuracyLayout.addWidget(self.AccuracyLine)
            self.AccuracyLayout.setStretch(1, 1)

            self.thirdQbox = QGroupBox("Output settings")
            self.mainLayout.addWidget(self.thirdQbox)
            self.layout3 = QHBoxLayout()
            self.thirdQbox.setLayout(self.layout3)
            self.layout3.addWidget(QLabel("Output File Name:"))
            self.layout3.setStretch(0, 1)
            self.OutputFile = QLineEdit('result.jpg')
            self.OutputFile.setObjectName('OutputFile')
            self.layout3.addWidget(self.OutputFile)
            self.layout3.setStretch(1, 1)

            self.fourthQbox = QGroupBox("Pattern settings")
            self.mainLayout.addWidget(self.fourthQbox)
            self.layout4 = QHBoxLayout()
            self.fourthQbox.setLayout(self.layout4)
            self.layout4.addWidget(QLabel("Pattern Name:"))
            self.layout4.setStretch(0, 1)
            self.PatternName = QLineEdit('p')
            self.PatternName.setObjectName('LED Name')
            self.layout4.addWidget(self.PatternName)
            self.layout4.setStretch(1, 1)

            self.spacer = QSpacerItem(100, 100)
            self.mainLayout.addItem(self.spacer)
            self.acceptBtn = QPushButton('Accept')
            self.acceptBtn.setObjectName('acceptBtn')
            self.mainLayout.addWidget(self.acceptBtn)
            self.roiCheckBox = QCheckBox('Do you want to use Camera as source of input?')
            self.roiCheckBox.setChecked(True)
            self.mainLayout.addWidget(self.roiCheckBox)
            # self.firstQbox.setMaximumHeight(70)
            self.acceptBtn.clicked.connect(self.illuAccepted)
            self.PatternCheckTool.exec()

        # TODO modify according to new tool
        elif status=='modify':
            self.PatternCheckTool = QDialog()
            self.mainLayout = QVBoxLayout()
            self.PatternCheckTool.setLayout(self.mainLayout)

            self.secondQbox = QGroupBox("Target Image")
            self.mainLayout.addWidget(self.secondQbox)
            self.layout2 = QHBoxLayout()
            self.secondQbox.setLayout(self.layout2)
            self.layout2.addWidget(QLabel("Name of the image where you want to search the pattern"))
            self.layout2.setStretch(0, 1)
            self.TargetFile = QLineEdit('ww.jpg')
            self.TargetFile.setObjectName('InputFile')
            self.layout2.addWidget(self.TargetFile)
            self.layout2.setStretch(1, 1)

            self.Accuracy = QGroupBox("Accuracy:")
            self.mainLayout.addWidget(self.Accuracy)
            self.AccuracyLayout = QHBoxLayout()
            self.Accuracy.setLayout(self.AccuracyLayout)
            self.AccuracyLayout.addWidget(QLabel("The threshold for the accurcay (-1 to +1):"))
            self.AccuracyLayout.setStretch(0, 1)
            self.AccuracyLine = QLineEdit('0.7')
            self.AccuracyLine.setObjectName('InputFile')
            self.AccuracyLayout.addWidget(self.AccuracyLine)
            self.AccuracyLayout.setStretch(1, 1)

            self.thirdQbox = QGroupBox("Output settings")
            self.mainLayout.addWidget(self.thirdQbox)
            self.layout3 = QHBoxLayout()
            self.thirdQbox.setLayout(self.layout3)
            self.layout3.addWidget(QLabel("Output File Name:"))
            self.layout3.setStretch(0, 1)
            self.OutputFile = QLineEdit('result.jpg')
            self.OutputFile.setObjectName('OutputFile')
            self.layout3.addWidget(self.OutputFile)
            self.layout3.setStretch(1, 1)

            self.fourthQbox = QGroupBox("Pattern settings")
            self.mainLayout.addWidget(self.fourthQbox)
            self.layout4 = QHBoxLayout()
            self.fourthQbox.setLayout(self.layout4)
            self.layout4.addWidget(QLabel("Pattern Name:"))
            self.layout4.setStretch(0, 1)
            self.PatternName = QLineEdit('p')
            self.PatternName.setObjectName('LED Name')
            self.layout4.addWidget(self.PatternName)
            self.layout4.setStretch(1, 1)

            self.spacer = QSpacerItem(100, 100)
            self.mainLayout.addItem(self.spacer)
            self.acceptBtn = QPushButton('Accept')
            self.acceptBtn.setObjectName('acceptBtn')
            self.mainLayout.addWidget(self.acceptBtn)
            self.roiCheckBox = QCheckBox('Do you want to use Camera as source of input?')
            self.roiCheckBox.setChecked(True)
            self.mainLayout.addWidget(self.roiCheckBox)
            # self.firstQbox.setMaximumHeight(70)
            self.acceptBtn.clicked.connect(self.illuAccepted)
            self.PatternCheckTool.exec()

        elif status == 'run':
            if settings['camera'] is True:
                Cam = Camera.Camera()
                Cam.run_capture('temp/'+settings['input'])
                Cam.checkFile('temp/'+settings['input'])
            img = cv2.imread(os.getcwd()+'/temp/'+settings['input'])
            template = cv2.imread('temp/'+settings['pattern_name']+'.jpg')
            w, h = template.shape[1],template.shape[0]

            temp = settings['region']

            rect = temp[0]
            # circle = temp[1]

            RectCoordinates = rect['coordinates']
            self.MainMask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
            cv2.rectangle(self.MainMask,(RectCoordinates[0],RectCoordinates[1]),(RectCoordinates[2],RectCoordinates[3]),(255,255,255),-1)

            masked_data = cv2.bitwise_and(img, img, mask=self.MainMask)
            # Apply template Matching
            res = cv2.matchTemplate(masked_data, template, cv2.TM_CCOEFF_NORMED)

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

        if self.roiCheckBox.isChecked() is True:
            Cam = Camera.Camera()
            Cam.setup_capture('temp/' + self.TargetFile.text())
            Cam.checkFile('temp/' + self.TargetFile.text())
        img = cv2.imread('temp/'+self.TargetFile.text())
        winname = "Test"
        cv2.namedWindow(winname, cv2.WINDOW_NORMAL)  # Create a named window
        cv2.moveWindow(winname, 25, 260)
        cv2.resizeWindow(winname, 890, 400)
        r = cv2.selectROI(winname,img)
        cv2.destroyWindow(winname)

        #TODO How the selectROI returns:

        CheckRegion = [{"style":'rect',
                       'coordinates':[ int(r[0]),int(r[1]),int(r[0] + r[2]),int(r[1] + r[3])]}]
        winname = "Test"
        cv2.namedWindow(winname, cv2.WINDOW_NORMAL)  # Create a named window
        cv2.moveWindow(winname, 25, 260)
        cv2.resizeWindow(winname, 890, 400)
        r = cv2.selectROI(winname,img)
        cv2.destroyWindow(winname)
        imCrop = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        cv2.imwrite('temp/'+self.PatternName.text()+'.jpg',imCrop)

        if len(CheckRegion) is not 0:

            globalVariables.toolsListText.append({'toolType':'PatternCheckTool',
                                                  'filePath':os.path.abspath(__file__),
                                                  'fileName':os.path.basename(__file__),
                                                  'inspection':True,
                                                  'region':CheckRegion,
                                                  'accuracy':float(self.AccuracyLine.text()),

                                                  'output':self.OutputFile.text(),
                                                  'input':self.TargetFile.text(),
                                                  'pattern_name':self.PatternName.text(),
                                                  'camera':True})
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

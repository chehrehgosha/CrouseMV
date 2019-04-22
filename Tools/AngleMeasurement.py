from PyQt5.QtWidgets import QDialog,QVBoxLayout,QPushButton,\
    QSpacerItem,QGroupBox,QLabel,QCheckBox,QHBoxLayout,QLineEdit
import cv2,os,globalVariables
from components import regionInspector
import numpy as np
import math
class Tool(object):
    def __init__(self,
                 settings = None,
                 index=None,
                 status='initialize',
                 sourcePath = None,
                 resultPath = None):

        if status=='initialize':
            self.AngleMeasurementTool = QDialog()
            self.mainLayout = QVBoxLayout()
            self.AngleMeasurementTool.setLayout(self.mainLayout)

            self.secondQbox = QGroupBox("Target Image")
            self.mainLayout.addWidget(self.secondQbox)
            self.layout2 = QHBoxLayout()
            self.secondQbox.setLayout(self.layout2)
            self.layout2.addWidget(QLabel("Name of the image where you want to search the pattern"))
            self.layout2.setStretch(0, 1)
            self.TargetFile = QLineEdit()
            self.TargetFile.setObjectName('InputFile')
            self.layout2.addWidget(self.TargetFile)
            self.layout2.setStretch(1, 1)

            # self.PatternSource = QGroupBox("Pattern Source:")
            # self.mainLayout.addWidget(self.PatternSource)
            # self.PatternSourceLayout = QHBoxLayout()
            # self.PatternSource.setLayout(self.PatternSourceLayout)
            # self.PatternSourceLayout.addWidget(QLabel("Name of the image where you want to sepcify the pattern"))
            # self.PatternSourceLayout.setStretch(0, 1)
            # self.PatternSourceLine = QLineEdit()
            # self.PatternSourceLine.setObjectName('InputFile')
            # self.PatternSourceLayout.addWidget(self.PatternSourceLine)
            # self.PatternSourceLayout.setStretch(1, 1)

            # self.Accuracy = QGroupBox("Accuracy:")
            # self.mainLayout.addWidget(self.Accuracy)
            # self.AccuracyLayout = QHBoxLayout()
            # self.Accuracy.setLayout(self.AccuracyLayout)
            # self.AccuracyLayout.addWidget(QLabel("The threshold for the accurcay (-1 to +1):"))
            # self.AccuracyLayout.setStretch(0, 1)
            # self.AccuracyLine = QLineEdit()
            # self.AccuracyLine.setObjectName('InputFile')
            # self.AccuracyLayout.addWidget(self.AccuracyLine)
            # self.AccuracyLayout.setStretch(1, 1)

            self.thirdQbox = QGroupBox("Output settings")
            self.mainLayout.addWidget(self.thirdQbox)
            self.layout3 = QHBoxLayout()
            self.thirdQbox.setLayout(self.layout3)
            self.layout3.addWidget(QLabel("Output File Name:"))
            self.layout3.setStretch(0, 1)
            self.OutputFile = QLineEdit()
            self.OutputFile.setObjectName('OutputFile')
            self.layout3.addWidget(self.OutputFile)
            self.layout3.setStretch(1, 1)

            self.fourthQbox = QGroupBox("Pattern settings")
            self.mainLayout.addWidget(self.fourthQbox)
            self.layout4 = QHBoxLayout()
            self.fourthQbox.setLayout(self.layout4)
            self.layout4.addWidget(QLabel("Pattern Name:"))
            self.layout4.setStretch(0, 1)
            self.LineName = QLineEdit()
            self.LineName.setObjectName('LED Name')
            self.layout4.addWidget(self.LineName)
            self.layout4.setStretch(1, 1)

            self.spacer = QSpacerItem(100, 100)
            self.mainLayout.addItem(self.spacer)
            self.acceptBtn = QPushButton('Accept')
            self.acceptBtn.setObjectName('acceptBtn')
            self.mainLayout.addWidget(self.acceptBtn)
            self.roiCheckBox = QCheckBox('Do you want to define ROI? (Region of Interest)')
            self.roiCheckBox.setChecked(True)
            self.mainLayout.addWidget(self.roiCheckBox)
            # self.firstQbox.setMaximumHeight(70)
            self.acceptBtn.clicked.connect(self.illuAccepted)
            self.AngleMeasurementTool.exec()

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

            im = cv2.imread('temp/'+settings['input'])
            self.MainMask = np.zeros((im.shape[0], im.shape[1]), dtype=np.uint8)

            temp = settings['region']

            rect = temp[0]
            RectCoordinates = rect['coordinates']
            cv2.rectangle(self.MainMask, (RectCoordinates[0], RectCoordinates[1]),
                          (RectCoordinates[2], RectCoordinates[3]), (255, 255, 255), -1)
            # circle = temp[1]

            RectCoordinates = rect['coordinates']
            self.MainMask = np.zeros((im.shape[0], im.shape[1]), dtype=np.uint8)
            cv2.rectangle(self.MainMask,(RectCoordinates[0],RectCoordinates[1]),(RectCoordinates[2],RectCoordinates[3]),(255,255,255),-1)


            # Apply template Matching
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200, apertureSize=3)
            kernel = np.ones((5, 5), np.uint8)


            masked_data = cv2.bitwise_and(edges, edges, mask=self.MainMask)
            cv2.imshow('daz',masked_data)
            cv2.waitKey(0)
            print(settings['line_length'])
            lines = cv2.HoughLines(masked_data, 0, np.pi / 180, 100)
            for x in lines:
                for rho, theta in x:
                    print(theta)
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    x1 = int(x0 + 1000 * (-b))
                    y1 = int(y0 + 1000 * (a))
                    x2 = int(x0 - 1000 * (-b))
                    y2 = int(y0 - 1000 * (a))

                cv2.line(im, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.imwrite('temp/' + settings['output'], im)
            cv2.imwrite(resultPath, im)
            self.report = '* * * * * * * * *\n PATTERN ' + settings[
                'pattern_name'] + ' \nHAS NOT BEEN FOUND\n\n\n* * * * * * * * *\n'
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
        self.AngleMeasurementTool.close()
        originArray = []
        img = cv2.imread('temp/'+self.TargetFile.text())
        # if self.roiCheckBox.isChecked() is True:
        inspectorModule = regionInspector.regionInspector(originArray, 'temp/' + self.TargetFile.text(),
                                                          'AngleMeasurement')
        originArray = inspectorModule.getOriginArray()

        im = cv2.imread('temp/' + self.TargetFile.text())
        self.MainMask = np.zeros((im.shape[0], im.shape[1]), dtype=np.uint8)

        rect = originArray[0]
        CircCoordinates = rect['coordinates']
        cv2.circle(self.MainMask,CircCoordinates[0],CircCoordinates[1],(255,255,255),1)

        rect = originArray[1]
        CircCoordinates = rect['coordinates']
        cv2.circle(self.MainMask, CircCoordinates[0], CircCoordinates[1], (255, 255, 255),1)

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200, apertureSize=3)
        kernel = np.ones((5, 5), np.uint8)
        cv2.dilate(edges, kernel, dst=edges, iterations=3)
        cv2.erode(edges, kernel, dst=edges, iterations=4)
        masked_data = cv2.bitwise_and(edges, edges, mask=self.MainMask)


        cv2.imshow('sad',masked_data)
        cv2.waitKey(0)
        lines = cv2.HoughLines(masked_data,1, np.pi / 180, 1)
        for x in lines:
            for rho, theta in x:
                print(theta)
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

            cv2.line(im, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.imshow('hello',im)
        cv2.waitKey(0)



        if len(originArray) is not 0:

            globalVariables.toolsListText.append({'toolType':'AngleMeasurementTool',
                                                  # 'illumination':str(illuPercent),
                                                  'filePath':os.path.abspath(__file__),
                                                  'fileName':os.path.basename(__file__),
                                                  'inspection':True,
                                                  'region':originArray,
                                                  # 'line_length':Diagonal,
                                                  # 'accuracy':float(self.AccuracyLine.text()),
                                                  # 'HSVValues':self.Values,
                                                  'output':self.OutputFile.text(),
                                                  'input':self.TargetFile.text(),
                                                  'pattern_name':self.LineName.text()})
        else:
            globalVariables.toolsListText.append({'toolType': 'AngleMeasurementTool',
                                                  # 'illumination': str(illuPercent),
                                                  'filePath': os.path.abspath(__file__),
                                                  'fileName': os.path.basename(__file__),
                                                  'inspection': False,
                                                  # 'region': originArray,
                                                  'output':self.OutputFile.text(),
                                                  'input':self.InputFile.text(),
                                                  'pattern_name': self.PatternName.text()})
        globalVariables.timeLineFlag.value = 1

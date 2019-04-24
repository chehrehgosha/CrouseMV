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
            self.TargetFile = QLineEdit('cluster.jpg')
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
            self.OutputFile = QLineEdit('result.jpg')
            self.OutputFile.setObjectName('OutputFile')
            self.layout3.addWidget(self.OutputFile)
            self.layout3.setStretch(1, 1)

            self.fourthQbox = QGroupBox("Angle settings")
            self.mainLayout.addWidget(self.fourthQbox)
            self.layout4 = QHBoxLayout()
            self.fourthQbox.setLayout(self.layout4)
            self.layout4.addWidget(QLabel("Angle:"))
            self.layout4.setStretch(0,1)
            self.MinDegree = QLineEdit('-50')
            self.MinDegree.setObjectName('MinDegree')
            self.layout4.addWidget(self.MinDegree)
            self.layout4.setStretch(0, 1)
            self.MaxDegree = QLineEdit('-40')
            self.MaxDegree.setObjectName('MaxDegree')
            self.layout4.addWidget(self.MaxDegree)
            self.layout4.setStretch(0,1)

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
        #TODO get yourself together
        elif status == 'run':

            im = cv2.imread('temp/' + settings['input'])
            self.MainMask = np.zeros((im.shape[0], im.shape[1]), dtype=np.uint8)

            rect = settings['region'][0]
            CircCoordinates = rect['coordinates']
            cv2.circle(self.MainMask, CircCoordinates[0], CircCoordinates[1], (255, 255, 255), 1)

            rect = settings['region'][1]
            CircCoordinates = rect['coordinates']
            cv2.circle(self.MainMask, CircCoordinates[0], CircCoordinates[1], (255, 255, 255), 1)


            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200, apertureSize=3)
            # kernel = np.ones((5, 5), np.uint8)

            masked_data = cv2.bitwise_and(edges, edges, mask=self.MainMask)
            # cv2.dilate(masked_data, kernel, dst=masked_data, iterations=4)
            # cv2.imshow('sad', masked_data)
            # cv2.waitKey(0)
            # cv2.erode(masked_data, kernel, dst=masked_data, iterations=4)
            # cv2.imshow('sad', masked_data)
            # cv2.waitKey(0)
            im2, contours, hierarchy = cv2.findContours(masked_data, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # cv2.imshow('sad', im2)
            # cv2.waitKey(0)
            cv2.drawContours(im, contours, -1, (255, 255, 255), 2)
            # print(contours)
            print('here')
            # cv2.polylines(im,
            #               contours,
            #               isClosed=False,
            #               color=(0, 255, 0),
            #               thickness=3)
            # cv2.imshow('sad', im)
            notFound = True
            dist = 0
            self.report = ''
            for contour1 in contours:
                point1 = contour1[0][0].reshape(-1)
                # print(point1)
                for contour2 in contours:
                    # print('here you can see the point1:',point1)
                    point2 = contour2[0][0].reshape(-1)
                    # print('here you can see the point2:',point2)
                    if point2[0] == point1[0]:
                        continue
                    angle = math.atan2((point2[1] - point1[1]) , (point2[0] - point1[0]))
                    if math.degrees(angle) > int(settings['min_angle']) and math.degrees(angle) < int(settings['max_angle']):
                            self.report = self.report +'* * * * * * * * *\n Angle ' + str("{0:.2f}".format(math.degrees(angle))) + ' \nHAS BEEN FOUND\n\n\n* * * * * * * * *\n'
                            notFound = False
            if notFound is True:
                self.report = '* * * * * * * * *\n ANGLE ' + ' \nHAS NOT BEEN FOUND\n\n\n* * * * * * * * *\n'
            cv2.imwrite('temp/' + settings['output'], im)
            cv2.imwrite(resultPath, im)

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
        # img = cv2.imread('temp/'+self.TargetFile.text())
        # if self.roiCheckBox.isChecked() is True:
        inspectorModule = regionInspector.regionInspector(originArray, 'temp/' + self.TargetFile.text(),
                                                          'AngleMeasurement')
        originArray = inspectorModule.getOriginArray()

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
                                                  'min_angle':self.MinDegree.text(),
                                                  'max_angle':self.MaxDegree.text()})
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

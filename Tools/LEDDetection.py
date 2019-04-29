from PyQt5.QtWidgets import QDialog,QVBoxLayout,QPushButton,\
    QSpacerItem,QGroupBox,QLabel,QCheckBox,QHBoxLayout,QLineEdit
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
            self.LEDDetection = QDialog()
            self.mainLayout = QVBoxLayout()
            self.LEDDetection.setLayout(self.mainLayout)

            self.secondQbox = QGroupBox("Input settings")
            self.mainLayout.addWidget(self.secondQbox)
            self.layout2 = QHBoxLayout()
            self.secondQbox.setLayout(self.layout2)
            self.layout2.addWidget(QLabel("Input File Name:"))
            self.layout2.setStretch(0, 1)
            self.InputFile = QLineEdit('board.jpg')
            self.InputFile.setObjectName('InputFile')
            self.layout2.addWidget(self.InputFile)
            self.layout2.setStretch(1, 1)

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

            self.fourthQbox = QGroupBox("LED settings")
            self.mainLayout.addWidget(self.fourthQbox)
            self.layout4 = QHBoxLayout()
            self.fourthQbox.setLayout(self.layout4)
            self.layout4.addWidget(QLabel("LED Name:"))
            self.layout4.setStretch(0, 1)
            self.LEDName = QLineEdit('1')
            self.LEDName.setObjectName('LED Name')
            self.layout4.addWidget(self.LEDName)
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
            self.LEDDetection.exec()

        # TODO modify according to input output
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
            imgray = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

            found = 0
            self.MainMask = np.zeros((im.shape[0], im.shape[1]), dtype=np.uint8)
            if settings['inspection'] is True:
                temp = settings['region']


                rect = temp[0]
                circle = temp[1]

                RectCoordinates = rect['coordinates']
                CircleCoordinates = circle['coordinates']

                for x in range(RectCoordinates[0]+CircleCoordinates[2],RectCoordinates[2]-CircleCoordinates[2]):
                    for y in range(RectCoordinates[1] + CircleCoordinates[2],RectCoordinates[3] - CircleCoordinates[2]):
                        mask = np.zeros((im.shape[0], im.shape[1]), dtype=np.uint8)
                        cv2.circle(mask,
                                   (x, y),
                                   CircleCoordinates[2],
                                   (255, 255, 255),
                                   -1)
                        masked_data = cv2.bitwise_and(imgray, imgray, mask=mask)
                        # cv2.imshow('hello',masked_data)
                        # cv2.waitKey(0)

                        h, s, v = cv2.split(masked_data)
                        Hmean = cv2.mean(h, mask)
                        Smean = cv2.mean(s, mask)
                        Vmean = cv2.mean(v, mask)
                        # self.MainMask = None
                        if Hmean[0] > int(settings['HSVValues'][0]) and Hmean[0] < int(settings['HSVValues'][1]):
                            if Smean[0] > int(settings['HSVValues'][2]) and Smean[0] < int(settings['HSVValues'][3]):
                                if  Vmean[0] > int(settings['HSVValues'][4]) and Vmean[0] < int(settings['HSVValues'][5]):
                                    self.MainMask = cv2.bitwise_or(self.MainMask, mask)
                                    found = 1
                if found is 0:
                    self.report = '* * * * * * * * *\n LED' + settings['led_name']+ ' \nHAS NOT BEEN FOUND\n\n* * * * * * * * *'
                else:
                    _, contours, hierarchy = cv2.findContours(self.MainMask,
                                                              cv2.RETR_TREE,
                                                              cv2.CHAIN_APPROX_SIMPLE)
                    hull = []
                    for i in range(len(contours)):
                        # creating convex hull object for each contour
                        hull.append(cv2.convexHull(contours[i], False))
                    # sorted(hull, key=cv2.contourArea, reverse=True)
                    cv2.drawContours(im, hull, -1, (0, 0, 0), 1)
                    print('here')
                    for i in range(len(hull)):
                        # rect = cv2.minAreaRect(contours[i])
                        # box = cv2.boxPoints(rect)
                        # box = np.int0(box)
                        # im = cv2.drawContours(im, [box], 0, (0, 0, 255), 2)
                        (x, y), radius = cv2.minEnclosingCircle(contours[i])
                        center = (int(x), int(y))
                        radius = int(radius)
                        cv2.circle(im, center, radius, (0, 0, 255), 3)
                        cv2.putText(im, settings['led_name'], (int(x), int(y) - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                    # for element in temp:
                    #     if element['style'] == 'rect':
                    #
                    #         coordinates = element['coordinates']
                    #         mask = np.zeros((im.shape[0], im.shape[1]), dtype=np.uint8)
                    #         cv2.rectangle(mask,
                    #                    (int(coordinates[0]), int(coordinates[1])),
                    #                     (int(coordinates[2]), int(coordinates[3])),
                    #                    (255,255,255),
                    #                    thickness=-1)
                            # cv2.imshow('x',mask)
                            # cv2.waitKey(0)
                            # invMask = cv2.bitwise_not(mask)
                            # masked_data = cv2.bitwise_and(imgray, imgray, mask=mask)
                            # roi = imgray [coordinates[1]:coordinates[3],coordinates[0]:coordinates[2]]
                            # cv2.imshow('x',masked_data)
                            # cv2.waitKey(0)
                            # SplitedData1, SplitedData2, SplitedData3 = cv2.split(masked_data)
                            # thresh1 = cv2.inRange(SplitedData1,
                            #                      int(settings['HSVValues'][0]),
                            #                      int(settings['HSVValues'][1]))
                            # thresh2 = cv2.inRange(SplitedData2,
                            #                       int(settings['HSVValues'][2]),
                            #                       int(settings['HSVValues'][3]))
                            # thresh3 = cv2.inRange(SplitedData3,
                            #                       int(settings['HSVValues'][4]),
                            #                       int(settings['HSVValues'][5]))
                            # thresh = thresh1+thresh3+thresh2


                            # cv2.imshow('x',thresh1)
                            # cv2.waitKey(0)
                            # cv2.imshow('x',thresh2)
                            # cv2.waitKey(0)
                            # cv2.imshow('x',thresh3)
                            # cv2.waitKey(0)
                            #
                            #
                            # thresh1 = cv2.erode(thresh1,None,iterations=2)
                            # thresh1 = cv2.dilate(thresh1,None,iterations=2)
                            #
                            # thresh2 = cv2.erode(thresh2, None, iterations=2)
                            # thresh2 = cv2.dilate(thresh2, None, iterations=2)
                            #
                            # thresh3 = cv2.erode(thresh3, None, iterations=2)
                            # thresh3 = cv2.dilate(thresh3, None, iterations=2)
                            #
                            # cv2.imshow('x', thresh1)
                            # cv2.waitKey(0)
                            # cv2.imshow('x', thresh2)
                            # cv2.waitKey(0)
                            # cv2.imshow('x', thresh3)
                            # cv2.waitKey(0)
                            #
                            # thresh = cv2.bitwise_and(thresh1, thresh2)
                            # thresh = cv2.bitwise_and(thresh, thresh3)
                            # # thresh = cv2.erode(thresh,None,iterations=2)
                            # cv2.imshow('x', thresh)
                            # cv2.waitKey(0)
                            # thresh = cv2.bitwise_and(thresh, thresh, mask=mask)
                            # thresh = cv2.inRange(imgray, np.array([10, 100, 100]), np.array([100, 255, 255]))
                            # cv2.imshow('x', thresh)
                            # cv2.waitKey(0)
                            # thresh = cv2.inRange(masked_data,
                            #                      np.array([float(settings['HSVValues'][0]),
                            #                                float(settings['HSVValues'][2]),
                            #                                float(settings['HSVValues'][4])]),
                            #                      np.array([float(settings['HSVValues'][1]),
                            #                                float(settings['HSVValues'][3]),
                            #                                float(settings['HSVValues'][5])]))

                            # thresh = cv2.inRange(cv2.split(masked_data)[0],
                            #                      float(settings['HSVValues'][0]),
                            #                      float(settings['HSVValues'][1]))

                            # ret, thresh = cv2.threshold(roi,
                            #                             255 * float(settings['illumination']),
                            #                             255,
                            #                             cv2.THRESH_BINARY)
                            # _, contours, _ = cv2.findContours(thresh,
                            #                                           cv2.RETR_TREE,
                            #                                           cv2.CHAIN_APPROX_SIMPLE)
                            # sorted(contours, key=cv2.contourArea, reverse=True)
                            # contours = contours[
                            # :3]
                            # for cnt in contours:
                            #     rect = cv2.minAreaRect(cnt)
                            #     box = cv2.boxPoints(rect)
                            #     box = np.int0(box)
                            #     im = cv2.drawContours(im, [box], 0, (0, 0, 255), 2)
                            # hull = []
                            #
                            # calculate points for each contour
                            # sorted(contours,key=cv2.contourArea,reverse=True)
                            # print(cv2.contourArea(contours[0]))
                            # print(cv2.contourArea(contours[1]))
                            # print(cv2.contourArea(contours[2]))
                            # for i in range(len(contours)):
                            #     # creating convex hull object for each contour
                            #     hull.append(cv2.convexHull(contours[i], False))

                            # sorted(hull, key=cv2.contourArea, reverse=True)
                            # print(cv2.contourArea(hull[0]))
                            # print(cv2.contourArea(hull[1]))
                            # print(cv2.contourArea(hull[2]))
                            #
                            # for i in range(len(hull)):
                            #     # rect = cv2.minAreaRect(cnt)
                            #     # box = cv2.boxPoints(rect)
                            #     # box = np.int0(box)
                            #     # im = cv2.drawContours(im, [box], 0, (0, 0, 255), 2)
                            #     (x, y), radius = cv2.minEnclosingCircle(hull[i])
                            #     center = (int(x), int(y))
                            #     radius = int(radius)
                            #     cv2.circle(im, center, radius, (0, 255, 0), 1)
                    # cv2.drawContours(im, contours, -1, (0, 255, 0), 3)
                    cv2.imwrite('temp/' + settings['output'], im)
                    cv2.imwrite(resultPath, im)
                    self.report =  '* * * * * * * * *\n LED '  + settings['led_name']+ ' \nHAS BEEN FOUND\n\n\n* * * * * * * * *\n'
                    # globalVariables.cameraScreenFlag.value = 1
                    # globalVariables.reportFlag.value = 1


                    # if element['style'] == 'circle':
                    #     coordinates = element['coordinates']
                    #     mask = np.zeros((im.shape[0], im.shape[1]),dtype=np.uint8)
                    #     cv2.circle(mask,
                    #                (int(coordinates[0]), int(coordinates[1])),
                    #                int(math.floor(coordinates[2]/2.86)),
                    #                (255,255,255),
                    #                thickness=-1)
                    #     invMask = cv2.bitwise_not(mask)
                    #     masked_data = cv2.bitwise_and(imgray, imgray, mask=mask)
                    #     ret, thresh = cv2.threshold(masked_data,
                    #                                 255 * float(settings['illumination']),
                    #                                 255,
                    #                                 cv2.THRESH_BINARY)
                    #     hierarchy, contours, _ = cv2.findContours(thresh,
                    #                                               cv2.RETR_TREE,
                    #                                               cv2.CHAIN_APPROX_SIMPLE)
                    #     cv2.drawContours(im, contours, -1, (0, 255, 0), 3)
                    #     cv2.imwrite('temp/'+settings['output'], im)
                    #     cv2.imwrite(resultPath, im)
                    #     globalVariables.cameraScreenFlag = 1

            # else:
            #     print('there')
            #     im = cv2.imread('temp/'+settings['input'])
            #     imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            #     ret, thresh = cv2.threshold(imgray,
            #                                 255 * float(settings['illumination']),
            #                                 255,
            #                                 cv2.THRESH_BINARY)
            #     hierarchy, contours, _ = cv2.findContours(thresh,
            #                                               cv2.RETR_TREE,
            #                                               cv2.CHAIN_APPROX_SIMPLE)
            #     cv2.drawContours(im, contours, -1, (0, 255, 0), 3)
            #     cv2.imwrite('temp/' + settings['output'], im)
            #     cv2.imwrite(resultPath, im)
            #     globalVariables.cameraScreenFlag = 1

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
        self.LEDDetection.close()
        originArray = []
        if self.roiCheckBox.isChecked() is True:
            inspectorModule = regionInspector.regionInspector(originArray, 'temp/'+self.InputFile.text(),module='LedDetector')
            originArray = inspectorModule.getOriginArray()
        # illuPercent = self.qLine.text()
        # illuPercent = float(illuPercent)


        self.ValueDialog = QDialog()
        self.ValueDialogUi = Ui_ValueDialog()
        self.ValueDialogUi.setupUi(self.ValueDialog)

        self.ValueDialogUi.buttonBox.accepted.connect(self.buttonAccept)
        self.ValueDialog.exec()
        if len(originArray) is not 0:

            globalVariables.toolsListText.append({'toolType':'LEDDetection',
                                                  # 'illumination':str(illuPercent),
                                                  'filePath':os.path.abspath(__file__),
                                                  'fileName':os.path.basename(__file__),
                                                  'inspection':True,
                                                  'region':originArray,
                                                  'HSVValues':self.Values,
                                                  'output':self.OutputFile.text(),
                                                  'input':self.InputFile.text(),
                                                  'led_name':self.LEDName.text()})
        else:
            globalVariables.toolsListText.append({'toolType': 'LEDDetection',
                                                  # 'illumination': str(illuPercent),
                                                  'filePath': os.path.abspath(__file__),
                                                  'fileName': os.path.basename(__file__),
                                                  'inspection': False,
                                                  'region': originArray,
                                                  'output':self.OutputFile.text(),
                                                  'input':self.InputFile.text(),
                                                  'led_name': self.LEDName.text()})
        globalVariables.timeLineFlag.value = 1

    def buttonAccept(self):
        self.ValueDialog.close()
        self.Values = [self.ValueDialogUi.HueValueMin.text(),
                       self.ValueDialogUi.HueValueMax.text(),
                       self.ValueDialogUi.SatValueMin.text(),
                       self.ValueDialogUi.SatValueMax.text(),
                       self.ValueDialogUi.IlluValueMin.text(),
                       self.ValueDialogUi.IlluValueMax.text()]

from PyQt5 import QtCore, QtWidgets

class Ui_ValueDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(322, 201)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 301, 181))
        self.groupBox.setObjectName("groupBox")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.groupBox)
        self.buttonBox.setGeometry(QtCore.QRect(20, 150, 271, 21))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 19, 281, 121))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_7.addWidget(self.label)
        self.HueValueMin = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HueValueMin.sizePolicy().hasHeightForWidth())
        self.HueValueMin.setSizePolicy(sizePolicy)
        self.HueValueMin.setObjectName("HueValueMin")
        self.horizontalLayout_7.addWidget(self.HueValueMin)
        self.HueValueMax = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HueValueMax.sizePolicy().hasHeightForWidth())
        self.HueValueMax.setSizePolicy(sizePolicy)
        self.HueValueMax.setObjectName("HueValueMax")
        self.horizontalLayout_7.addWidget(self.HueValueMax)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.SatValueMin = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SatValueMin.sizePolicy().hasHeightForWidth())
        self.SatValueMin.setSizePolicy(sizePolicy)
        self.SatValueMin.setObjectName("SatValueMin")
        self.horizontalLayout_6.addWidget(self.SatValueMin)
        self.SatValueMax = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SatValueMax.sizePolicy().hasHeightForWidth())
        self.SatValueMax.setSizePolicy(sizePolicy)
        self.SatValueMax.setObjectName("SatValueMax")
        self.horizontalLayout_6.addWidget(self.SatValueMax)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.IlluValueMin = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IlluValueMin.sizePolicy().hasHeightForWidth())
        self.IlluValueMin.setSizePolicy(sizePolicy)
        self.IlluValueMin.setObjectName("IlluValueMin")
        self.horizontalLayout_5.addWidget(self.IlluValueMin)
        self.IlluValueMax = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IlluValueMax.sizePolicy().hasHeightForWidth())
        self.IlluValueMax.setSizePolicy(sizePolicy)
        self.IlluValueMax.setObjectName("IlluValueMax")
        self.horizontalLayout_5.addWidget(self.IlluValueMax)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Dialog)
        # self.buttonBox.accepted.connect(Dialog.accept)
        # self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "HSV Value Settings:"))
        self.label.setText(_translate("Dialog", "Hue Value"))
        self.HueValueMin.setPlaceholderText(_translate("Dialog", "Min Value"))
        self.HueValueMax.setPlaceholderText(_translate("Dialog", "Max Value"))
        self.label_2.setText(_translate("Dialog", "Saturation Value"))
        self.SatValueMin.setPlaceholderText(_translate("Dialog", "Min Value"))
        self.SatValueMax.setPlaceholderText(_translate("Dialog", "Max Value"))
        self.label_3.setText(_translate("Dialog", "Illumination Value"))
        self.IlluValueMin.setPlaceholderText(_translate("Dialog", "Min Value"))
        self.IlluValueMax.setPlaceholderText(_translate("Dialog", "Max Value"))


import math
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, \
    QSpacerItem, QGroupBox, QLabel, QCheckBox, QHBoxLayout, QLineEdit
import  os, globalVariables



class Tool(object):
    def __init__(self,
                 settings=None,
                 index=None,
                 status='initialize',
                 sourcePath=None,
                 resultPath=None):

        if status == 'initialize':
            self.ObjectDistance = QDialog()
            self.mainLayout = QVBoxLayout()
            self.ObjectDistance.setLayout(self.mainLayout)

            self.secondQbox = QGroupBox("First Object")
            self.mainLayout.addWidget(self.secondQbox)
            self.layout2 = QHBoxLayout()
            self.secondQbox.setLayout(self.layout2)
            self.layout2.addWidget(QLabel("Name of First Object"))
            self.layout2.setStretch(0, 1)
            self.FirstObject = QLineEdit('p2')
            self.FirstObject.setObjectName('FirstObject')
            self.layout2.addWidget(self.FirstObject)
            self.layout2.setStretch(1, 1)



            self.thirdQbox = QGroupBox("Second Object settings")
            self.mainLayout.addWidget(self.thirdQbox)
            self.layout3 = QHBoxLayout()
            self.thirdQbox.setLayout(self.layout3)
            self.layout3.addWidget(QLabel("Second Object:"))
            self.layout3.setStretch(0, 1)
            self.SecondObject = QLineEdit('p1')
            self.SecondObject.setObjectName('SecondObject')
            self.layout3.addWidget(self.SecondObject)
            self.layout3.setStretch(1, 1)



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
            self.ObjectDistance.exec()

        # TODO modify according to new tool
        elif status == 'modify':
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
            self.SecondObject = QLineEdit()
            self.SecondObject.setObjectName('InputFile')
            self.layout3.addWidget(self.SecondObject)
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

            command = 'globalVariables.' + settings['input']
            FirstObject = eval(command)
            command = ' globalVariables.' + settings['output']
            SecondObject = eval(command)
            dist = math.sqrt((FirstObject[0]-SecondObject[0])**2+(FirstObject[1]-SecondObject[1])**2)
            self.report = '* * * * * * * * *\n Distance\n '+str(dist)+'\n\n* * * * * * * * *\n'

    # TODO modify according to new tool
    def toolModified(self):
        self.LEDDetection.close()
        button = self.mainLayout.sender()
        if button.objectName() == 'acceptBtn':
            originArray = []

            globalVariables.toolsListText[self.index] = {'toolType': 'ObjectDistance',
                                                             # 'illumination':str(illuPercent),
                                                             'filePath': os.path.abspath(__file__),
                                                             'fileName': os.path.basename(__file__),
                                                             'inspection': globalVariables.toolsListText[self.index][
                                                                 'inspection'],
                                                             'region': originArray,
                                                             'HSVValues': self.Values,
                                                             'output': self.SecondObject.text(),
                                                             'input': self.InputFile.text()}

            globalVariables.timeLineFlag.value = 1

        elif button.objectName() == 'deleteBtn':
            del globalVariables.toolsListText[self.index]
            globalVariables.timeLineFlag.value = 1
            self.LEDDetection.close()

    def illuAccepted(self):
        self.ObjectDistance.close()



        globalVariables.toolsListText.append({'toolType': 'ObjectDistance',
                                                  # 'illumination':str(illuPercent),
                                                  'filePath': os.path.abspath(__file__),
                                                  'fileName': os.path.basename(__file__),
                                                  'inspection': True,
                                                  'region': [],
                                                  # 'accuracy': float(self.AccuracyLine.text()),
                                                  # 'HSVValues':self.Values,
                                                  'output': self.SecondObject.text(),
                                                  'input': self.FirstObject.text()})

        globalVariables.timeLineFlag.value = 1

from PyQt5.QtWidgets import QDialog,QVBoxLayout,QPushButton,\
    QSpacerItem,QGroupBox,QLabel,QCheckBox,QHBoxLayout,QLineEdit
import cv2,os,globalVariables
from components import regionInspector,Camera
import numpy as np
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
            self.PatternName.setObjectName('Pattern Name')
            self.layout4.addWidget(self.PatternName)
            self.layout4.setStretch(1, 1)

            self.spacer = QSpacerItem(100, 100)
            self.mainLayout.addItem(self.spacer)
            self.acceptBtn = QPushButton('Accept')
            self.acceptBtn.setObjectName('acceptBtn')
            self.mainLayout.addWidget(self.acceptBtn)
            self.CameraCheckBox = QCheckBox('Do you want to use Camera as source of input?')
            self.CameraCheckBox.setChecked(True)
            self.mainLayout.addWidget(self.CameraCheckBox)
            # self.firstQbox.setMaximumHeight(70)
            self.acceptBtn.clicked.connect(self.toolAccepted)
            self.PatternCheckTool.exec()

        # TODO modify according to new tool
        elif status=='modify':
            self.settings = settings
            self.index = index

            self.PatternCheckTool = QDialog()
            self.mainLayout = QVBoxLayout()
            self.PatternCheckTool.setLayout(self.mainLayout)

            self.secondQbox = QGroupBox("Target Image")
            self.mainLayout.addWidget(self.secondQbox)
            self.layout2 = QHBoxLayout()
            self.secondQbox.setLayout(self.layout2)
            self.layout2.addWidget(QLabel("Name of the image where you want to search the pattern"))
            self.layout2.setStretch(0, 1)
            self.TargetFile = QLineEdit(globalVariables.toolsListText[self.index]['input'])
            self.TargetFile.setObjectName('InputFile')
            self.layout2.addWidget(self.TargetFile)
            self.layout2.setStretch(1, 1)

            self.Accuracy = QGroupBox("Accuracy:")
            self.mainLayout.addWidget(self.Accuracy)
            self.AccuracyLayout = QHBoxLayout()
            self.Accuracy.setLayout(self.AccuracyLayout)
            self.AccuracyLayout.addWidget(QLabel("The threshold for the accurcay (-1 to +1):"))
            self.AccuracyLayout.setStretch(0, 1)
            self.AccuracyLine = QLineEdit(str(globalVariables.toolsListText[self.index]['accuracy']))
            self.AccuracyLine.setObjectName('InputFile')
            self.AccuracyLayout.addWidget(self.AccuracyLine)
            self.AccuracyLayout.setStretch(1, 1)

            self.thirdQbox = QGroupBox("Output settings")
            self.mainLayout.addWidget(self.thirdQbox)
            self.layout3 = QHBoxLayout()
            self.thirdQbox.setLayout(self.layout3)
            self.layout3.addWidget(QLabel("Output File Name:"))
            self.layout3.setStretch(0, 1)
            self.OutputFile = QLineEdit(globalVariables.toolsListText[self.index]['output'])
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
            self.PatternName.setObjectName('Pattern Name')
            self.layout4.addWidget(self.PatternName)
            self.layout4.setStretch(1, 1)

            self.spacer = QSpacerItem(100, 100)
            self.mainLayout.addItem(self.spacer)
            self.acceptBtn = QPushButton('Accept')
            self.acceptBtn.setObjectName('acceptBtn')
            self.mainLayout.addWidget(self.acceptBtn)
            self.deleteBtn = QPushButton('Delete')
            self.deleteBtn.setObjectName('deleteBtn')
            self.mainLayout.addWidget(self.deleteBtn)
            self.CameraCheckBox = QCheckBox('Do you want to use Camera as source of input?')
            self.CameraCheckBox.setChecked(True)
            self.mainLayout.addWidget(self.CameraCheckBox)
            self.acceptBtn.clicked.connect(self.toolModified)
            self.deleteBtn.clicked.connect(self.toolModified)
            self.PatternCheckTool.exec()

        elif status == 'run':
            globalVariables.guide_value.value = 'Status:\nRunning'
            globalVariables.guide_flag.value = 1
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
                #ACK How to store coordinates of a pattern or object.
                self.out1 = top_left[0] + w/2
                self.out2 = top_left[1] + h/2
                ResultCode = 'globalVariables.'+ settings['pattern_name'] +' =[top_left[0] + w/2 , top_left[1] + h/2]'
                exec(ResultCode)
            else:
                cv2.imwrite('temp/' + settings['output'], img)
                cv2.imwrite(resultPath, img)
                self.report = '* * * * * * * * *\n Pattern\tStatus\n ' + settings[
                    'pattern_name'] + ' \tNot Found\n\n* * * * * * * * *\n'
            globalVariables.guide_value.value = 'Status:\n -'
            globalVariables.guide_flag.value = 1


    def toolModified(self):
        self.PatternCheckTool.close()
        button = self.mainLayout.sender()
        if button.objectName() == 'acceptBtn':
            if self.CameraCheckBox.isChecked() is True:
                Cam = Camera.Camera()
                Cam.setup_capture('temp/' + self.TargetFile.text())
                Cam.checkFile('temp/' + self.TargetFile.text())
                img = cv2.imread('temp/' + self.TargetFile.text())
                winname = "Test"
                cv2.namedWindow(winname, cv2.WINDOW_NORMAL)  # Create a named window
                cv2.moveWindow(winname, 25, 260)
                cv2.resizeWindow(winname, 890, 400)
                r = cv2.selectROI(winname, img)
                cv2.destroyWindow(winname)
                CheckRegion = [{"style": 'rect',
                                'coordinates': [int(r[0]), int(r[1]), int(r[0] + r[2]), int(r[1] + r[3])]}]
                winname = "Test"
                cv2.namedWindow(winname, cv2.WINDOW_NORMAL)  # Create a named window
                cv2.moveWindow(winname, 25, 260)
                cv2.resizeWindow(winname, 890, 400)
                r = cv2.selectROI(winname, img)
                cv2.destroyWindow(winname)
                imCrop = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
                cv2.imwrite('temp/' + self.PatternName.text() + '.jpg', imCrop)
                globalVariables.toolsListText[self.index] = {'toolType': 'PatternCheckTool',
                                                      'filePath': os.path.abspath(__file__),
                                                      'fileName': os.path.basename(__file__),
                                                      'inspection': True,
                                                      'region': CheckRegion,
                                                      'accuracy': float(self.AccuracyLine.text()),
                                                      'output': self.OutputFile.text(),
                                                      'input': self.TargetFile.text(),
                                                      'pattern_name': self.PatternName.text(),
                                                      'camera': True}
            else:
                img = cv2.imread('temp/' + self.TargetFile.text())
                winname = "Test"
                cv2.namedWindow(winname, cv2.WINDOW_NORMAL)  # Create a named window
                cv2.moveWindow(winname, 25, 260)
                cv2.resizeWindow(winname, 890, 400)
                r = cv2.selectROI(winname, img)
                cv2.destroyWindow(winname)
                CheckRegion = [{"style": 'rect',
                                'coordinates': [int(r[0]), int(r[1]), int(r[0] + r[2]), int(r[1] + r[3])]}]
                winname = "Test"
                cv2.namedWindow(winname, cv2.WINDOW_NORMAL)  # Create a named window
                cv2.moveWindow(winname, 25, 260)
                cv2.resizeWindow(winname, 890, 400)
                r = cv2.selectROI(winname, img)
                cv2.destroyWindow(winname)
                imCrop = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
                cv2.imwrite('temp/' + self.PatternName.text() + '.jpg', imCrop)
                globalVariables.toolsListText[self.index] = {'toolType': 'PatternCheckTool',
                                                             'filePath': os.path.abspath(__file__),
                                                             'fileName': os.path.basename(__file__),
                                                             'inspection': True,
                                                             'region': globalVariables.toolsListText[self.index]['region'],
                                                             'accuracy': float(self.AccuracyLine.text()),
                                                             'output': self.OutputFile.text(),
                                                             'input': self.TargetFile.text(),
                                                             'pattern_name': globalVariables.toolsListText[self.index]['pattern_name'],
                                                             'camera': False}
        elif button.objectName() == 'deleteBtn':
            del globalVariables.toolsListText[self.index]
            globalVariables.timeLineFlag.value = 1

    def toolAccepted(self):
        self.PatternCheckTool.close()

        if self.CameraCheckBox.isChecked() is True:

            Cam = Camera.Camera()
            Cam.setup_capture('temp/' + self.TargetFile.text())
            Cam.checkFile('temp/' + self.TargetFile.text())
        globalVariables.guide_value.value = 'Status:\n-'
        globalVariables.guide_flag.value = 1
        img = cv2.imread('temp/'+self.TargetFile.text())
        winname = "Region of Interest"
        cv2.namedWindow(winname, cv2.WINDOW_NORMAL)  # Create a named window
        cv2.moveWindow(winname, 25, 260)
        cv2.resizeWindow(winname, 890, 400)
        globalVariables.guide_value.value = 'Status:\nSelect the Region of Interest'
        globalVariables.guide_flag.value = 1
        r = cv2.selectROI(winname,img)
        cv2.destroyWindow(winname)
        globalVariables.guide_value.value = 'Status:\n -'
        globalVariables.guide_flag.value = 1
        #TODO How the selectROI returns:

        CheckRegion = [{"style":'rect',
                       'coordinates':[ int(r[0]),int(r[1]),int(r[0] + r[2]),int(r[1] + r[3])]}]
        winname = "Pattern of Interest"
        cv2.namedWindow(winname, cv2.WINDOW_NORMAL)  # Create a named window
        cv2.moveWindow(winname, 25, 260)
        cv2.resizeWindow(winname, 890, 400)
        globalVariables.guide_value.value = 'Status:\nSelect the Desired Patttern'
        globalVariables.guide_flag.value = 1
        r = cv2.selectROI(winname,img)
        cv2.destroyWindow(winname)
        globalVariables.guide_value.value = 'Status:\n-'
        globalVariables.guide_flag.value = 1
        imCrop = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        cv2.imwrite('temp/'+self.PatternName.text()+'.jpg',imCrop)

        if self.CameraCheckBox.isChecked():

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
            globalVariables.toolsListText.append({'toolType':'PatternCheckTool',
                                                  'filePath':os.path.abspath(__file__),
                                                  'fileName':os.path.basename(__file__),
                                                  'inspection':True,
                                                  'region':CheckRegion,
                                                  'accuracy':float(self.AccuracyLine.text()),

                                                  'output':self.OutputFile.text(),
                                                  'input':self.TargetFile.text(),
                                                  'pattern_name':self.PatternName.text(),
                                                  'camera':False})
        globalVariables.timeLineFlag.value = 1

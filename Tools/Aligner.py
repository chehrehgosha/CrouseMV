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
            self.Aligner = QDialog()
            self.mainLayout = QVBoxLayout()
            self.Aligner.setLayout(self.mainLayout)
            self.firstQbox = QGroupBox("Reference Image Setting")
            self.mainLayout.addWidget(self.firstQbox)
            self.layout1 = QHBoxLayout()
            self.firstQbox.setLayout(self.layout1)
            self.layout1.addWidget(QLabel("Reference Image Name:"))
            self.layout1.setStretch(0, 1)
            self.RefImg = QLineEdit()
            self.RefImg.setObjectName('RefImg')
            self.layout1.addWidget(self.RefImg)
            self.layout1.setStretch(1, 1)

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

            self.spacer = QSpacerItem(100, 100)
            self.mainLayout.addItem(self.spacer)
            self.acceptBtn = QPushButton('Accept')
            self.acceptBtn.setObjectName('acceptBtn')
            self.mainLayout.addWidget(self.acceptBtn)
            self.roiCheckBox = QCheckBox('Do you want to define ROI? (Region of Interest)')
            self.mainLayout.addWidget(self.roiCheckBox)
            self.firstQbox.setMaximumHeight(70)
            self.acceptBtn.clicked.connect(self.settingAccepted)
            self.Aligner.exec()
        # TODO modify according to input/output
        elif status=='modify':
            self.settings = settings
            self.index = index

            self.Aligner = QDialog()
            self.mainLayout = QVBoxLayout()
            self.Aligner.setLayout(self.mainLayout)
            self.firstQbox = QGroupBox("Reference Image Setting")
            self.mainLayout.addWidget(self.firstQbox)
            self.layout1 = QHBoxLayout()
            self.firstQbox.setLayout(self.layout1)
            self.layout1.addWidget(QLabel("Reference Image Name:"))
            self.layout1.setStretch(0, 1)
            self.RefImg = QLineEdit()
            self.RefImg.setObjectName('RefImg')
            self.layout1.addWidget(self.RefImg)
            self.layout1.setStretch(1, 1)

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

            self.spacer = QSpacerItem(100, 100)
            self.mainLayout.addItem(self.spacer)

            self.acceptBtn = QPushButton('Accept')
            self.acceptBtn.setObjectName('acceptBtn')
            self.mainLayout.addWidget(self.acceptBtn)
            self.deleteBtn = QPushButton('Delete')
            self.deleteBtn.setObjectName('deleteBtn')
            self.mainLayout.addWidget(self.deleteBtn)
            self.roiCheckBox = QCheckBox('Do you want to define ROI? (Region of Interest)')
            self.mainLayout.addWidget(self.roiCheckBox)
            self.firstQbox.setMaximumHeight(70)
            self.acceptBtn.clicked.connect(self.toolModified)
            self.deleteBtn.clicked.connect(self.toolModified)
            self.Aligner.exec()

        elif status == 'run':
            if settings['inspection'] is True:
                im1 = cv2.imread('temp/' + settings['input'], cv2.IMREAD_COLOR)
                im2 = cv2.imread('temp/' + settings['reference'], cv2.IMREAD_COLOR)

                im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
                im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

                mask2 = np.zeros(im2Gray.shape[:2], dtype=np.uint8)
                temp = settings['region']
                for element in temp:
                    x1, y1, x2, y2 = element['coordinates'][0],element['coordinates'][1],element['coordinates'][2],element['coordinates'][3]
                    cv2.rectangle(mask2, (x1, y1), (x2, y2), (255), thickness=-1)
                    # cv2.imshow('iggg',mask2)
                # Detect ORB features and compute descriptors.
                orb = cv2.ORB_create(500)
                keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
                keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, mask2)

                # Match features.
                matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
                matches = matcher.match(descriptors1, descriptors2, None)

                # Sort matches by score
                matches.sort(key=lambda x: x.distance, reverse=False)

                # Remove not so good matches
                # print(len(matches))
                # if len(matches)<400:
                #     numGoodMatches = 4
                # else:
                #     numGoodMatches = int(len(matches) * 0.5)
                numGoodMatches = int(len(matches) * 0.5)
                matches = matches[:numGoodMatches]

                # Draw top matches
                imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
                cv2.imwrite("temp/matches.jpg", imMatches)

                # Extract location of good matches
                points1 = np.zeros((len(matches), 2), dtype=np.float32)
                points2 = np.zeros((len(matches), 2), dtype=np.float32)

                for i, match in enumerate(matches):
                    points1[i, :] = keypoints1[match.queryIdx].pt
                    points2[i, :] = keypoints2[match.trainIdx].pt

                # Find homography
                h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

                # Use homography
                height, width, channels = im2.shape
                im1Reg = cv2.warpPerspective(im1, h, (width, height))
                cv2.imwrite('temp/' + settings['output'], im1Reg)
                cv2.imwrite(resultPath, im1Reg)
                globalVariables.cameraScreenFlag = 1
            else:

                im1 = cv2.imread('temp/'+settings['input'], cv2.IMREAD_COLOR)
                im2 = cv2.imread('temp/'+settings['reference'], cv2.IMREAD_COLOR)

                im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
                im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

                # Detect ORB features and compute descriptors.
                orb = cv2.ORB_create(10000)
                keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
                keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

                # Match features.
                matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
                matches = matcher.match(descriptors1, descriptors2, None)

                # Sort matches by score
                matches.sort(key=lambda x: x.distance, reverse=False)

                # Remove not so good matches
                numGoodMatches = int(len(matches) * 0.9)
                matches = matches[:numGoodMatches]

                # Draw top matches
                imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
                cv2.imwrite("temp/matches.jpg", imMatches)

                # Extract location of good matches
                points1 = np.zeros((len(matches), 2), dtype=np.float32)
                points2 = np.zeros((len(matches), 2), dtype=np.float32)

                for i, match in enumerate(matches):
                    points1[i, :] = keypoints1[match.queryIdx].pt
                    points2[i, :] = keypoints2[match.trainIdx].pt

                # Find homography
                h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

                # Use homography
                height, width, channels = im2.shape
                im1Reg = cv2.warpPerspective(im1, h, (width, height))
                cv2.imwrite('temp/'+settings['output'], im1Reg)
                cv2.imwrite(resultPath, im1Reg)
                globalVariables.cameraScreenFlag = 1

    # TODO modify according to input/output
    def toolModified(self):
        self.Aligner.close()
        button = self.mainLayout.sender()
        if button.objectName() == 'acceptBtn':
            originArray = []
            if self.roiCheckBox.isChecked() is True:
                inspectorModule = regionInspector.regionInspector(originArray, 'temp/' + self.InputFile.text())
                originArray = inspectorModule.getOriginArray()
            if len(originArray) is not 0:
                globalVariables.toolsListText[self.index] = {'toolType':'Aligner',
                                                  'reference':self.RefImg.text(),
                                                  'filePath':os.path.abspath(__file__),
                                                  'fileName':os.path.basename(__file__),
                                                  'input':self.InputFile.text(),
                                                  'output':self.OutputFile.text(),
                                                  'inspection': True,
                                                  'region': originArray}
            else:
                globalVariables.toolsListText[self.index] = {'toolType':'Aligner',
                                                  'reference':self.RefImg.text(),
                                                  'filePath':os.path.abspath(__file__),
                                                  'fileName':os.path.basename(__file__),
                                                  'input':self.InputFile.text(),
                                                  'output':self.OutputFile.text(),
                                                  'inspection': False,
                                                  'region': originArray}
            globalVariables.timeLineFlag.value = 1

        elif button.objectName() == 'deleteBtn':
            del globalVariables.toolsListText[self.index]
            globalVariables.timeLineFlag.value = 1
            self.Aligner.close()


    def settingAccepted(self):
        self.Aligner.close()
        originArray = []
        if self.roiCheckBox.isChecked() is True:
            inspectorModule = regionInspector.regionInspector(originArray,'temp/'+self.RefImg.text())
            originArray = inspectorModule.getOriginArray()
        if len(originArray) is not 0:

            globalVariables.toolsListText.append({'toolType':'Aligner',
                                                  'reference':self.RefImg.text(),
                                                  'filePath':os.path.abspath(__file__),
                                                  'fileName':os.path.basename(__file__),
                                                  'input':self.InputFile.text(),
                                                  'output':self.OutputFile.text(),
                                                  'inspection': True,
                                                  'region': originArray})
        else:
            globalVariables.toolsListText.append({'toolType':'Aligner',
                                              'reference':self.RefImg.text(),
                                              'filePath':os.path.abspath(__file__),
                                              'fileName':os.path.basename(__file__),
                                              'input':self.InputFile.text(),
                                              'output':self.OutputFile.text(),
                                              'inspection': False,
                                              'region': originArray})
        globalVariables.timeLineFlag.value = 1
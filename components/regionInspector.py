import cv2
import globalVariables
import numpy as np
import math
from PyQt5.QtWidgets import QWidget,QRadioButton,QVBoxLayout,QButtonGroup,QLabel
class regionInspector(object):
    def __init__(self,originArray, InspectionSource,module):
        self.Module = module
        self.originArray = originArray

        if self.Module is "LedDetector":
            self.originArray = originArray
            self.drawing = False  # true if mouse is pressed
            self.ix, self.iy = -1, -1
            self.mode = True

            self.img = cv2.imread(InspectionSource, 1)
            self.img2 = self.img.copy()
            cv2.namedWindow('image', 0)

            cv2.setMouseCallback('image', self.draw_circle)

            self.temp = 0
            self.inspectionDialog = QWidget()
            self.inspectionLayout = QVBoxLayout()
            self.inspectionDialog.setLayout(self.inspectionLayout)
            self.rectRadio = QRadioButton('Rectangle')
            self.resetRadio = QRadioButton('Reset')
            self.circRadio = QRadioButton('Circle')
            self.groupButton = QButtonGroup()
            self.groupButton.addButton(self.rectRadio)
            self.groupButton.addButton(self.circRadio)
            self.groupButton.addButton(self.resetRadio)
            self.inspectionLayout.addWidget(self.rectRadio)
            self.inspectionLayout.addWidget(self.circRadio)
            self.inspectionLayout.addWidget(self.resetRadio)
            self.HueLabel = QLabel()
            self.SatLabel = QLabel()
            self.ValLabel = QLabel()
            self.inspectionLayout.addWidget(self.HueLabel)
            self.inspectionLayout.addWidget(self.SatLabel)
            self.inspectionLayout.addWidget(self.ValLabel)
            # self.HueLabelc = QLabel()
            # self.SatLabelc = QLabel()
            # self.ValLabelc = QLabel()
            # self.inspectionLayout.addWidget(self.HueLabelc)
            # self.inspectionLayout.addWidget(self.SatLabelc)
            # self.inspectionLayout.addWidget(self.ValLabelc)

            self.inspectionDialog.show()
            while (1):
                cv2.imshow('image', self.img2)

                k = cv2.waitKey(1) & 0xFF
                if cv2.getWindowProperty('image',0)== -1:
                    self.inspectionDialog.close()
                    break;
                if k == 27:
                    self.inspectionDialog.close()
                    break
                elif self.resetRadio.isChecked() is True:
                    cv2.destroyWindow('image')
                    cv2.namedWindow('image', 0)
                    self.img = cv2.imread(InspectionSource)
                    self.img2 = self.img.copy()
                    cv2.setMouseCallback('image', self.draw_circle)
                    self.originArray = []
                    self.rectRadio.setChecked(True)
                    self.RectNow = True
                    self.CircNow = False
            cv2.destroyAllWindows()

        if self.Module is "AngleMeasurement":
            self.drawing = False  # True if mouse is pressed
            self.mode = True  # if True, draw rectangle. Press 'm' to toggle to curve
            self.ix, self.iy = -1, -1

            # mouse callback function


            self.img = cv2.imread(InspectionSource, 1)
            self.img2 = self.img.copy()

            # make cv2 windows, set mouse callback
            cv2.namedWindow('image')
            cv2.setMouseCallback('image', self.draw_circle)

            self.inspectionDialog = QWidget()
            self.inspectionLayout = QVBoxLayout()
            self.inspectionDialog.setLayout(self.inspectionLayout)
            self.HueLabel = QLabel()
            self.inspectionLayout.addWidget(self.HueLabel)
            self.HueLabel.setText('Press R for reset\n')
            self.inspectionDialog.show()
            while (1):
                cv2.imshow('image', self.img2)

                # This is where we get the keyboard input
                # Then check if it's "m" (if so, toggle the drawing mode)
                k = cv2.waitKey(1) & 0xFF
                # if k == ord('m'):
                #     self.mode = not self.mode
                if k == ord('r'):
                    cv2.destroyWindow('image')
                    cv2.namedWindow('image', 0)
                    self.img = cv2.imread(InspectionSource)
                    self.img2 = self.img.copy()
                    cv2.setMouseCallback('image', self.draw_circle)
                    self.originArray = []
                    # self.rectRadio.setChecked(True)
                    # self.RectNow = True
                    # self.CircNow = False
                elif k == 27:
                    cv2.destroyWindow('image')
                    self.inspectionDialog.close()
                    break

        if self.Module is 'Aligner':
            img = cv2.imread(InspectionSource)
            r = cv2.selectROI("Please select region of pattern", img)
            cv2.destroyWindow("Please select region of pattern")

            # TODO How the selectROI returns:

            self.originArray = [{"style": 'rect',
                            'coordinates': [int(r[0]), int(r[1]), int(r[0] + r[2]), int(r[1] + r[3])]}]
    def draw_circle(self,event, x, y, flags, param):
        if self.Module is 'LedDetector':
            overlay = self.img.copy()
            output = self.img.copy()
            alpha = 0.5
            if event == cv2.EVENT_LBUTTONDOWN:
                self.drawing = True
                self.ix, self.iy = x, y
                self.RectNow = True
                X= False
            elif event == cv2.EVENT_MOUSEMOVE:
                if self.drawing == True:
                    if self.mode == True:
                        if self.rectRadio.isChecked() is True:
                            cv2.rectangle(overlay, (self.ix, self.iy),
                                          (x,y), (0, 0, 255), 2)
                            cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img2)
                            cv2.imshow('image', self.img2)
                        if self.circRadio.isChecked() is True:
                            cv2.circle(overlay, (self.ix, self.iy),
                                       int(math.sqrt((self.ix - x) ** 2 + (self.iy - y) ** 2)), (0, 255, 0), 2)
                            cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img2)
                            cv2.imshow('image', self.img2)
            elif event == cv2.EVENT_LBUTTONUP:
                if self.drawing == True:
                    if self.rectRadio.isChecked() is True:
                        if self.RectNow is True:
                            cv2.rectangle(overlay, (self.ix, self.iy),
                                       (x,y), (0, 0, 255), 2)
                            cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img)
                            # param[0] = True
                            self.originArray.append({'style': 'rect',
                                             'coordinates': [self.ix, self.iy, x, y]})
                            self.circRadio.setChecked(True)
                            self.RectNow = False
                            self.CircNow = True
                    elif self.circRadio.isChecked() is True:
                        if self.CircNow is True:
                            mask = np.zeros((self.img.shape[0], self.img.shape[1]), dtype=np.uint8)

                            cv2.circle(mask,
                                       (int((self.ix + x) / 2), int((self.iy + y) / 2)),
                                       int(math.sqrt(((self.ix - x) ** 2) + ((self.iy - y) ** 2)) / 2),
                                       (255, 255, 255),
                                       -1)
                            self.originArray.append({'style':'circle',
                                                     'coordinates':[int((self.ix + x) / 2),int((self.iy + y) / 2),int(math.sqrt(((self.ix - x) ** 2) + ((self.iy - y) ** 2)) / 2)]})
                            # print(cv2.contourArea(mask))
                            # MaskedImg = cv2.bitwise_and(self.img,self.img,mask=mask)
                            HSVImg = cv2.cvtColor(self.img,cv2.COLOR_BGR2HSV)
                            # cv2.imshow('x',mask)
                            # cv2.waitKey(0)
                            # cv2.imshow('x',HSVImg)
                            # cv2.waitKey(0)

                            # meanHSV = cv2.mean(HSVImg,mask)
                            # print(meanHSV)
                            h,s,v = cv2.split(HSVImg)
                            Hmean = cv2.mean(h,mask)
                            Smean = cv2.mean(s,mask)
                            Vmean = cv2.mean(v,mask)
                            print(Hmean,Smean,Vmean)
                            # self.HueLabel = QLabel()
                            # self.SatLabel = QLabel()
                            # self.ValLabel = QLabel()
                            # self.inspectionLayout.addWidget(self.HueLabel)
                            # self.inspectionLayout.addWidget(self.SatLabel)
                            # self.inspectionLayout.addWidget(self.ValLabel)
                            # print(Hmean)
                            # print(Smean)
                            # print(Vmean)
                            # print(meanHSV)
                            # print(s)
                            # print(v)
                            self.HueLabel.setText("Hue Value for inspected Region is: " + str(Hmean[0]))
                            self.SatLabel.setText("Saturation Value for inspected Region is: " + str(Smean[0]))
                            self.ValLabel.setText("Illumination Value for inspected Region is: " + str(Vmean[0]))

                            # self.originArray.append({'style': 'circle',
                            #                  'coordinates': [(self.ix + x) / 2, (self.iy + y) / 2,
                            #                                  math.sqrt(((self.ix - x) ** 2) + ((self.iy - y) ** 2)) / 2]})
                            cv2.circle(overlay, (self.ix, self.iy),
                                       int(math.sqrt((self.ix - x) ** 2 + (self.iy - y) ** 2)), (0, 255, 0), 2)
                            cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img)
                            self.CircNow = False
                self.drawing = False

        if self.Module is 'AngleMeasurement':
            # global ix, iy, drawing, mode, overlay, output, alpha
            overlay = self.img.copy()
            output = self.img.copy()
            alpha = 0.5
            #ACK Here the region of inspection is dynamically resizable
            if event == cv2.EVENT_LBUTTONDOWN:
                self.drawing = True
                self.ix, self.iy = x, y

            elif event == cv2.EVENT_MOUSEMOVE:
                if self.drawing == True:
                    if self.mode == True:
                        cv2.circle(overlay, (self.ix, self.iy),
                                   int(math.sqrt((self.ix - x) ** 2 + (self.iy - y) ** 2)), (0, 0, 255), 1)
                        cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img2)
                        cv2.imshow('image', self.img2)
                    # else:
                    #     cv2.rectangle(overlay, (self.ix, self.iy), (x, y), (0, 255, 0), 4)
                    #     cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img2)
                    #     cv2.imshow('image', self.img2)

            elif event == cv2.EVENT_LBUTTONUP:
                self.drawing = False
                if self.mode == True:
                    cv2.circle(overlay, (self.ix, self.iy),
                               int(math.sqrt((self.ix - x) ** 2 + (self.iy - y) ** 2)), (0, 0, 255), 1)
                    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img)
                    self.originArray.append({'style': 'circle',
                                             'coordinates': [(int((x + self.ix) / 2), int((y + self.iy) / 2)),
                                                             int(math.sqrt((self.ix - x) ** 2 + (self.iy - y) ** 2) / 2.8)]})
                # else:
                #     cv2.rectangle(overlay, (self.ix, self.iy), (x, y), (0, 255, 0), 4)
                #     cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img)


    def getOriginArray(self):
        return self.originArray



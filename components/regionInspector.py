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
            self.drawing = False  # True if mouse is pressed
            # self.mode = True  # if True, draw rectangle. Press 'm' to toggle to curve
            self.ix, self.iy = -1, -1

            # mouse callback function

            self.img = cv2.imread(InspectionSource, 1)
            self.img2 = self.img.copy()

            # make cv2 windows, set mouse callback
            self.winname = "Angle Measurement"
            cv2.namedWindow(self.winname, cv2.WINDOW_NORMAL)  # Create a named window
            cv2.setMouseCallback(self.winname, self.draw_circle)

            globalVariables.guide_value.value = 'Status:\nDraw the intersecting Circles\n' \
                                                'Press R to reset\n' \
                                                'Press Esc to finish'
            globalVariables.guide_flag.value = 1
            self.rectangle = False
            self.circle = False
            while (1):

                cv2.moveWindow(self.winname, 25, 260)
                cv2.resizeWindow(self.winname, 890, 400)
                cv2.imshow(self.winname, self.img2)

                # This is where we get the keyboard input
                # Then check if it's "m" (if so, toggle the drawing mode)
                k = cv2.waitKey(1) & 0xFF
                # if k == ord('m'):
                #     self.mode = not self.mode
                if k == ord('r'):
                    cv2.destroyWindow(self.winname)
                    cv2.namedWindow(self.winname, 0)
                    self.img = cv2.imread(InspectionSource)
                    self.img2 = self.img.copy()
                    cv2.setMouseCallback(self.winname, self.draw_circle)
                    self.originArray = []
                elif k == ord('a'):
                    self.circle = False
                    self.rectangle = True
                elif k == ord('b'):
                    self.rectangle = False
                    self.circle = True
                elif k == 27:
                    cv2.destroyWindow(self.winname)
                    break

        if self.Module is "AngleMeasurement":
            self.drawing = False  # True if mouse is pressed
            # self.mode = True  # if True, draw rectangle. Press 'm' to toggle to curve
            self.ix, self.iy = -1, -1

            # mouse callback function


            self.img = cv2.imread(InspectionSource, 1)
            self.img2 = self.img.copy()

            # make cv2 windows, set mouse callback
            self.winname = "Angle Measurement"
            cv2.namedWindow(self.winname, cv2.WINDOW_NORMAL)  # Create a named window
            cv2.setMouseCallback(self.winname, self.draw_circle)


            globalVariables.guide_value.value = 'Status:\nDraw the intersecting Circles\n' \
                                                'Press R to reset\n' \
                                                'Press Esc to finish'
            globalVariables.guide_flag.value = 1
            while (1):

                cv2.moveWindow(self.winname, 25, 260)
                cv2.resizeWindow(self.winname, 890, 400)
                cv2.imshow(self.winname, self.img2)

                # This is where we get the keyboard input
                # Then check if it's "m" (if so, toggle the drawing mode)
                k = cv2.waitKey(1) & 0xFF
                # if k == ord('m'):
                #     self.mode = not self.mode
                if k == ord('r'):
                    cv2.destroyWindow(self.winname)
                    cv2.namedWindow(self.winname, 0)
                    self.img = cv2.imread(InspectionSource)
                    self.img2 = self.img.copy()
                    cv2.setMouseCallback(self.winname, self.draw_circle)
                    self.originArray = []

                elif k == 27:
                    cv2.destroyWindow(self.winname)
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
            # global ix, iy, drawing, mode, overlay, output, alpha
            overlay = self.img.copy()
            output = self.img.copy()
            alpha = 0.5
            # ACK Here the region of inspection is dynamically resizable
            if event == cv2.EVENT_LBUTTONDOWN:
                self.drawing = True
                self.ix, self.iy = x, y

            elif event == cv2.EVENT_MOUSEMOVE:
                if self.drawing == True:
                    # if self.mode == True:
                    if self.rectangle == True:
                        cv2.rectangle(overlay, (self.ix, self.iy),
                                      (x, y), (0, 0, 255), 2)
                        cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img2)
                        cv2.imshow(self.winname, self.img2)
                    elif self.circle == True:
                        cv2.circle(overlay, (self.ix, self.iy),
                                   int(math.sqrt((self.ix - x) ** 2 + (self.iy - y) ** 2)), (0, 255, 0), 2)
                        cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img2)
                        cv2.imshow(self.winname, self.img2)



            elif event == cv2.EVENT_LBUTTONUP:
                self.drawing = False
                if self.rectangle == True:
                    cv2.rectangle(overlay, (self.ix, self.iy),
                                  (x, y), (0, 0, 255), 2)
                    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img)
                    # param[0] = True
                    self.originArray.append({'style': 'rect',
                                             'coordinates': [self.ix, self.iy, x, y]})
                elif self.circle == True:
                    mask = np.zeros((self.img.shape[0], self.img.shape[1]), dtype=np.uint8)

                    cv2.circle(mask,
                               (int((self.ix + x) / 2), int((self.iy + y) / 2)),
                               int(math.sqrt(((self.ix - x) ** 2) + ((self.iy - y) ** 2)) / 2),
                               (255, 255, 255),
                               -1)
                    self.originArray.append({'style': 'circle',
                                             'coordinates': [int((self.ix + x) / 2), int((self.iy + y) / 2), int(
                                                 math.sqrt(((self.ix - x) ** 2) + ((self.iy - y) ** 2)) / 2)]})
                    # print(cv2.contourArea(mask))
                    # MaskedImg = cv2.bitwise_and(self.img,self.img,mask=mask)
                    HSVImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

                    h, s, v = cv2.split(HSVImg)
                    Hmean = cv2.mean(h, mask)
                    Smean = cv2.mean(s, mask)
                    Vmean = cv2.mean(v, mask)
                    globalVariables.guide_value.value = 'Press "R" to reset\n' \
                                                        'Hue mean value:' + str("{0:.3f}".format(Hmean[0])) + '\n' \
                                                                                                           'Saturation mean value' + str(
                        "{0:.3f}".format(Smean[0])) + '\n' \
                                                   'Illumination mean value' + str("{0:.3f}".format(Vmean[0]))
                    globalVariables.guide_flag.value = 1

                    # self.originArray.append({'style': 'circle',
                    #                  'coordinates': [(self.ix + x) / 2, (self.iy + y) / 2,
                    #                                  math.sqrt(((self.ix - x) ** 2) + ((self.iy - y) ** 2)) / 2]})
                    cv2.circle(overlay, (self.ix, self.iy),
                               int(math.sqrt((self.ix - x) ** 2 + (self.iy - y) ** 2)), (0, 255, 0), 2)
                    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img)
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
                    # if self.mode == True:
                    cv2.circle(overlay, (self.ix, self.iy),
                               int(math.sqrt((self.ix - x) ** 2 + (self.iy - y) ** 2)), (0, 0, 255), 1)
                    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img2)
                    cv2.imshow(self.winname, self.img2)


            elif event == cv2.EVENT_LBUTTONUP:
                self.drawing = False
                # if self.mode == True:
                cv2.circle(overlay, (self.ix, self.iy),
                           int(math.sqrt((self.ix - x) ** 2 + (self.iy - y) ** 2)), (0, 0, 255), 1)
                cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img)
                self.originArray.append({'style': 'circle',
                                         'coordinates': [(int((x + self.ix) / 2), int((y + self.iy) / 2)),
                                                         int(math.sqrt((self.ix - x) ** 2 + (self.iy - y) ** 2) / 2.8)]})



    def getOriginArray(self):
        return self.originArray



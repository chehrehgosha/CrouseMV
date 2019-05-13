import ctypes

from PyQt5.QtWidgets import QDialog,QFileSystemModel
from PyQt5.QtGui import QPixmap
from QtFiles.toolselector import Ui_Dialog
import os
import sys
import importlib.util
import cv2
# import Tools.ObjectDistance

class Camera:
    def __init__(self,):
        self.x = 0
    def remFile(self,target_address):
        print('removing file: ',os.getcwd()+'/'+target_address)
        if os.path.isfile(os.getcwd()+'/'+target_address) is True:
            os.remove(os.getcwd()+'/'+target_address)
    def setup_capture(self, target_address,lock=None):

        print('11')
        self.Capture = cv2.VideoCapture(0)
        while (True):
            ret, frame = self.Capture.read()

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                print(os.getcwd()+'/'+target_address)
                cv2.imwrite(os.getcwd()+'/'+target_address,frame)
                cv2.destroyAllWindows()
                break
        print('22')
    def run_capture(self,target_address):
        self.Capture = cv2.VideoCapture(0)
        while (self.x < 5):
            ret, frame = self.Capture.read()
            self.x = self.x + 1
        ret, frame = self.Capture.read()
        cv2.imwrite(os.getcwd() + '/' + target_address, frame)
    def checkFile(self,target_address):
        print('checking file for: '+os.getcwd()+'/'+target_address)
        while (True):
            # print(os.getcwd()+'/'+target_address)
            x = os.path.exists(os.getcwd()+'/'+target_address)
            # print(x)
            if x is True:
                break
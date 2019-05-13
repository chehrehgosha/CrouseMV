import ctypes
import multiprocessing
import globalVariables
import importlib
import cv2
from PyQt5.QtGui import QPixmap, QImage
import time
from PyQt5.QtWidgets import QPushButton
import sys

class runEngine():
    def __init__(self,
                 toolsListText,
                 cameraFlag,
                 resultPath,
                 sourcePath,
                 reportFlag,
                 report,
                 ChangeColorFlag,
                 ChangeColorIndex,
                 status):

        # TemporaryVariables = {}
        # x11 = ctypes.cdll.LoadLibrary('libX11.so')
        if status=='main_run':
            report.value = ''
            for i in range(len(toolsListText)):

                setting = toolsListText[i]
                toolType = setting['toolType']
                fileName = setting['fileName']
                fullPath = setting['filePath']
                fileDir = fullPath[:-len(fileName)]
                moduleName = fileName[:fileName.rfind(".")]
                sys.path.insert(0, fileDir)
                module = importlib.import_module(moduleName)
                selectedTool = getattr(module, 'Tool')
                alpha = selectedTool(setting,
                             status='run',
                             sourcePath= sourcePath.value,
                             resultPath = resultPath.value)
                report.value = report.value + alpha.report
                cameraFlag.value = 1
                reportFlag.value = 1
                if alpha.report.find('Not')== -1:
                    ChangeColorFlag.value = 1
                else:
                    ChangeColorFlag.value = -1
                ChangeColorIndex.value = i
                time.sleep(2)

                # print(globalVariables.out1)
            print(toolsListText)
        elif status=='pre_run':
            # toolsListText[0]['report']='ji'
            for setting in toolsListText:
                toolType = setting['toolType']
                fileName = setting['fileName']
                fullPath = setting['filePath']
                fileDir = fullPath[:-len(fileName)]
                moduleName = fileName[:fileName.rfind(".")]
                sys.path.insert(0, fileDir)
                module = importlib.import_module(moduleName)
                selectedTool = getattr(module, 'Tool')
                _ = selectedTool(setting,
                             status='run',
                             sourcePath= sourcePath.value,
                             resultPath = resultPath.value)

                # cameraFlag.value = 1
                time.sleep(2)


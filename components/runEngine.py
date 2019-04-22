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
                 status):
        if status=='main_run':
            report.value = ''
            for setting in toolsListText:
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
                time.sleep(2)
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
                alpha = selectedTool(setting,
                             status='run',
                             sourcePath= sourcePath.value,
                             resultPath = resultPath.value)

                # cameraFlag.value = 1
                time.sleep(2)


import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow,QPushButton,QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer,QSize,Qt
from components.addTool import addTool
from QtFiles.mainwindow import Ui_MainWindow
from components.runEngine import runEngine
from multiprocessing import Process, Manager
import importlib.util
import globalVariables
import pickle

class Application():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.UI = Ui_MainWindow()
        self.UI.setupUi(self.window)

        self.UI.runButton.clicked.connect(self.runButton_clicked)
        self.UI.addTool.clicked.connect(self.addTool_clicked)
        self.UI.LoadProgramButton.clicked.connect(self.load_program)
        self.UI.SaveProgramButton.clicked.connect(self.save_program)


        self.window.show()

        self.manager = Manager()
        globalVariables.toolsListText = self.manager.list()
        globalVariables.timeLineFlag = self.manager.Value(value=0,typecode=int)
        globalVariables.toolsListIndex = self.manager.Value(value=0, typecode=int)
        globalVariables.cameraScreenFlag = self.manager.Value(value=0, typecode=int)
        globalVariables.report = self.manager.Value(value='',typecode=str)
        globalVariables.reportFlag = self.manager.Value(value=0, typecode=int)
        globalVariables.sourcePath = self.manager.Value(value='images/BackLightImg.jpg', typecode=str)
        globalVariables.resultPath = self.manager.Value(value='images/result.jpg', typecode=str)
        self.TestExecutionTimer = QTimer()
        self.TestExecutionTimer.timeout.connect(self.GUIrenderer)
        self.TestExecutionTimer.start(1000)

        sys.exit(self.app.exec_())

    def runButton_clicked(self):
        toolRunnerInstance = Process(target=runEngine,args=(globalVariables.toolsListText,
                                                            globalVariables.cameraScreenFlag,
                                                            globalVariables.resultPath,
                                                            globalVariables.sourcePath,
                                                            globalVariables.reportFlag,
                                                            globalVariables.report,
                                                            'main_run'))
        toolRunnerInstance.start()
    def load_program(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilters(["Text files (*.txt)"])
        dlg.selectNameFilter("Images (*.png *.jpg)")
        # filenames = []

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            f = open(filenames[0], 'r')

            with f:
                globalVariables.toolsListText = eval(f.readline())
        # with open(self.UI.ProgramName.text()+".txt", "r") as file:
        #     globalVariables.toolsListText = eval(file.readline())
        globalVariables.timeLineFlag.value = 1
        return
    def save_program(self):
        program_name = self.UI.ProgramName.text()
        # with open(program_name+'.txt', 'w') as f:
        #     for item in globalVariables.toolsListText:
        #         f.write("%s\n" % item)
        with open(program_name+".txt", "w") as file:
            file.write(str(globalVariables.toolsListText))
        return
    def GUIrenderer(self):
        if globalVariables.timeLineFlag.value == 1:
            print(globalVariables.toolsListText)
            toolRunnerInstance = Process(target=runEngine, args=(globalVariables.toolsListText,
                                                                 globalVariables.cameraScreenFlag,
                                                                 globalVariables.resultPath,
                                                                 globalVariables.sourcePath,
                                                                 globalVariables.reportFlag,
                                                                 globalVariables.report,
                                                                 'pre_run'))
            toolRunnerInstance.start()
            while isinstance(self.UI.horizontalLayout.itemAt(0), PyQt5.QtWidgets.QWidgetItem):
                globalVariables.toolsListIndex.value = globalVariables.toolsListIndex.value - 1
                item = self.UI.horizontalLayout.itemAt(0)
                # self.UI.horizontalLayout.removeWidget(item.widget())
                item = item.widget()
                item.setParent(None)
                globalVariables.timeLineFlag.value = 0
                # item.delete()
            for i in range(len(globalVariables.toolsListText)):
                newButton = QPushButton(globalVariables.toolsListText[i]['toolType'])
                newButton.index = i
                newButton.clicked.connect(self.timeLineClicked)
                newButton.setMinimumSize(QSize(65, 50))
                self.UI.horizontalLayout.insertWidget(globalVariables.toolsListIndex.value,newButton)
                globalVariables.toolsListIndex.value = globalVariables.toolsListIndex.value + 1
                globalVariables.timeLineFlag.value = 0
            # print(globalVariables.toolsListText)
        if globalVariables.cameraScreenFlag.value == 1:
            # print('salam')
            image = QPixmap(globalVariables.resultPath.value)
            image = image.scaled(self.UI.cameraLabel.width(),self.UI.cameraLabel.height(),Qt.KeepAspectRatio)
            # self.UI.cameraLabel.setScaledContents(True)
            self.UI.cameraLabel.setPixmap(image)

            globalVariables.cameraScreenFlag.value = 0
        if globalVariables.reportFlag.value == 1:
            print(globalVariables.toolsListText)
            # Report_text = ''
            # for tool in globalVariables.toolsListText:
            #     Report_text = Report_text + tool['report']
            self.UI.Report_Label.setText(globalVariables.report.value)
            globalVariables.reportFlag.value = 0
    def timeLineClicked(self):
        Icon = self.UI.horizontalLayout.sender()
        index = Icon.index
        setting = globalVariables.toolsListText[index]
        fileName = setting['fileName']
        fullPath = setting['filePath']
        fileDir = fullPath[:-len(fileName)]
        moduleName = fileName[:fileName.rfind(".")]
        sys.path.insert(0, fileDir)
        module = importlib.import_module(moduleName)
        selectedTool = getattr(module, 'Tool')
        selectedTool(setting,index,status='modify')
    def addTool_clicked(self):
        x = addTool()

if __name__ == '__main__':
    Application()



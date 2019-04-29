from PyQt5.QtWidgets import QDialog,QFileSystemModel
from PyQt5.QtGui import QPixmap
from QtFiles.toolselector import Ui_Dialog
import os
import sys
import importlib.util
# import Tools.ObjectDistance

class addTool(object):
    def __init__(self):
        self.toolSelectorDialog = QDialog()
        self.toolSelector = Ui_Dialog()
        self.toolSelector.setupUi(self.toolSelectorDialog)
        self.fileSystemModel = QFileSystemModel(self.toolSelector.treeView)
        self.fileSystemModel.setReadOnly(False)
        self.fileSystemModel.setNameFilters(["*.py"])
        self.fileSystemModel.setNameFilterDisables(False);
        self.root = self.fileSystemModel.setRootPath(os.path.abspath(os.path.join(os.path.join(os.path.abspath(__file__),os.pardir),'..\Tools')))
        # print(os.path.abspath(os.path.join(os.path.join(os.path.abspath(__file__),os.pardir),'..\Tools')))
        # self.root = self.root + '/Tools/'
        self.toolSelector.treeView.setModel(self.fileSystemModel)
        self.toolSelector.treeView.setRootIndex(self.root)
        self.toolSelector.treeView.hideColumn(1)
        self.toolSelector.treeView.hideColumn(2)
        self.toolSelector.treeView.hideColumn(3)
        self.toolSelector.treeView.clicked.connect(self.changed)
        self.toolSelector.Select.clicked.connect(self.select)
        self.toolSelector.Cancel.clicked.connect(self.cancel)
        self.toolSelector.ToolDescription.setText(None)
        self.toolSelector.Icon.setPixmap(QPixmap(None))
        self.toolSelectorDialog.exec()

    def cancel(self):
        self.toolSelectorDialog.close()

    def select(self):
        selectedNode = self.toolSelector.treeView.selectedIndexes()
        model = self.toolSelector.treeView.model()
        selectedNodeModelIndex = selectedNode[0]
        selectedNodeAddress = model.filePath(selectedNodeModelIndex)
        index = selectedNodeAddress.rfind("/")
        selectedRoot = selectedNodeAddress [:index]
        sys.path.insert(0, selectedRoot)
        selectedModule = selectedNodeAddress [index+1:]
        index = selectedModule.rfind(".")
        selectedModule = selectedModule[:index]
        module = importlib.import_module(selectedModule)
        selectedTool = getattr(module,'Tool')
        self.toolSelectorDialog.close()
        selectedTool()

    def changed(self):
        changedNode = self.toolSelector.treeView.selectedIndexes()
        model = self.toolSelector.treeView.model()
        changedNodeModelIndex = changedNode[0]
        changedNodeAddress = model.filePath(changedNodeModelIndex)
        changedNodeAddress = str(changedNodeAddress)
        if os.path.isdir(changedNodeAddress):
            self.toolSelector.ToolDescription.setText(os.path.basename(changedNodeAddress+' Folder'))
            self.toolSelector.Icon.setPixmap(QPixmap(None))
        elif os.path.isfile(changedNodeAddress):
            index = changedNodeAddress.rfind('.')
            rawAddress = changedNodeAddress[:index]
            #TODO change dynamically for each tool
            iconAddress = 'temp/icon.png'
            self.toolSelector.Icon.setPixmap(QPixmap(iconAddress))
            self.toolSelector.ToolDescription.setText(os.path.basename(rawAddress + ' Tool'))

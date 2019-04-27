import sys,importlib,os
class ScriptEngine(object):
    def __init__(self,ProgramName,ProgramFolder,ReportFolder):
        self.ProgramName = ProgramName
        self.ProgramFolder = ProgramFolder
        self.ReportFolder = ReportFolder
        self.report = ''
        if not os.path.exists(self.ReportFolder+'/results'):
            os.makedirs(self.ReportFolder + '/results')

    def run(self):
        f = open(self.ProgramFolder+'/'+self.ProgramName+'.txt', 'r')
        with f:
            toolsListText = eval(f.readline())
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
                                 sourcePath=None,
                                 resultPath=self.ReportFolder+'/result.jpg')
            self.report = self.report + alpha.report
        with open(self.ReportFolder+'/'+'report'+".txt", "w") as file:
            file.write(self.report)
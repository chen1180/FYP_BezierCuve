from PyQt5.QtCore import pyqtSignal,QObject
class sceneNode(QObject):
    sceneNodeChanged=pyqtSignal(QObject)
    sceneNodeDraw=pyqtSignal(list)
    def __init__(self):
        super(sceneNode, self).__init__()
        self.sceneNodes=[]
    def addNode(self,node):
        self.sceneNodes.append(node)
        self.sceneNodeChanged.emit(node)
    def deleteNode(self,node):
        pass
    def updateNode(self,node:list):
        self.sceneNodes=node
        self.sceneNodeDraw.emit(self.sceneNodes)
    def render(self):
        pass
    def create(self):
        pass
    def setupCameraMatrix(self,view,model,projection):
        pass

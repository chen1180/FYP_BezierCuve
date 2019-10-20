from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from curve_modernGL.model.SceneNode import *

class SceneObjects(QObject):
    sceneNodeAdded = pyqtSignal(QObject)
    sceneNodeDeleted = pyqtSignal(QObject)
    sceneNodeChanged=pyqtSignal(int,QObject)
    sceneNodeDraw=pyqtSignal(list)
    def __init__(self):
        super(SceneObjects, self).__init__()
        self.sceneNodes = []
    def addNode(self,node):
        self.sceneNodes.append(node)
        self.sceneNodeAdded.emit(node)
    def modifyNode(self,position:int,node):
        self.sceneNodes[position]=node
        self.sceneNodeChanged.emit(position,node)
    def deleteNode(self,node):
        self.sceneNodes.remove(node)
        self.sceneNodeDeleted.emit(node)
    def updateNode(self,node:list):
        self.sceneNodes=node
        self.sceneNodeDraw.emit(self.sceneNodes)
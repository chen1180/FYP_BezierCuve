from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from curve_modernGL.controller.SceneManager import *
from curve_modernGL.view.SceneDockWidget import *
from curve_modernGL.model.SceneNode import *
"""
    This controller updates the view on sceneDockWidget when scene nodes change
"""
class SceneController(QObject):
    '''
        Function: connect the signal emitted from SceneManager to the slots in SceneDockWidget,
        So when each model in SceneManager updates, the view of SceneDockWidget will update accordingly
    '''
    def __init__(self,sceneModel,sceneDockWidget):
        self.model=sceneModel
        self.sceneWidget=sceneDockWidget
        #signal connection
        self.model[0].sceneNodeChanged.connect(self.addItem)
    def addItem(self, item:AbstractSceneNode):
        self.sceneWidget[0].addItem(item)
        self.sceneWidget[0].setCurrentItem(item)
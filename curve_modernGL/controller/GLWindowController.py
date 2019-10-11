from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from curve_modernGL.controller.SceneManager import *
from curve_modernGL.view.GLWindow import *
"""
    This controller updates the view on PropertyDockWidget when scene nodes change
"""
class GLController(QObject):
    '''
        Function: connect the signal emitted from SceneManager to the slots in PropertyDockWidget,
        So when each model in SceneManager updates, the view of SceneDockWidget will update accordingly
    '''
    def __init__(self,sceneModel,GLWindow):
        self.model=sceneModel
        self.glWindow=GLWindow
        #signal connection
        self.model[0].sceneNodeDraw.connect(self.glWindow[0].addToScene)
from model.geometry.SceneNode import *
"""
    This controller updates the view on PropertyDockWidget when scene nodes change
"""
class PropertyController(QObject):
    '''
        Function: connect the signal emitted from SceneManager to the slots in PropertyDockWidget,
        So when each model in SceneManager updates, the view of SceneDockWidget will update accordingly
    '''
    def __init__(self,sceneModel,propertyDockWidget):
        self.model=sceneModel
        self.propertyWidget=propertyDockWidget
        #signal connection
        self.model[0].sceneNodeChanged.connect(self.addItem)
    def addItem(self, item:AbstractSceneNode):
        self.propertyWidget[0].coordinateForm.displayTable(item)
        self.propertyWidget[0].transformWidget.setLineEdit(item.transform)
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
class AbstractSceneNode(QObject):
    def __init__(self):
        super(AbstractSceneNode, self).__init__()
        #sceneNode common properties
        self.vertices=[]
        self.transform=QVector3D(0,0,0)
        self.m_shaderCompiled=False
        #Shader
        self.program=QOpenGLShaderProgram()
        self.commonProgram=QOpenGLShaderProgram()
        self.lightProgram=QOpenGLShaderProgram()
        #color
        self.verticesColor=QVector3D(1,1,1)
        self.polygonColor=QVector3D(0,1,0)
        self.color=QVector3D(1,0,0)
        #Camera transformation
        self.viewMatrix=QMatrix4x4()
        self.modelMatrix=QMatrix4x4()
        self.projectionMatrix=QMatrix4x4()
        #Display Properties
        self.m_showPoint=False
        self.m_showPolygon=False
        self.m_showWireframe=False

    def initialize(self):
        self.setupMainShaderProgram()
        self.setupCommonShaderProgram()
    def render(self):
        if self.m_showPoint==True:
            self.drawVertices()
        if self.m_showPolygon==True:
            self.drawPolygons()
        self.drawItem()
    #Setup shader
    def setupCommonShaderProgram(self):
        pass
    def setupMainShaderProgram(self):
        pass
    #Drawing method
    def drawVertices(self):
        pass
    def drawPolygons(self):
        pass
    def drawItem(self):
        pass
    #Camera matrix
    def setupCameraMatrix(self,view,model,projection):
        self.view = view
        self.model = model
        self.projection = projection
    #common method
    def QVec3DtoNumpyArray(self, data):
        tmp=[]
        for vector in data:
            tmp+=[vector[0],vector[1],vector[2]]
        npArray=np.array(tmp,dtype="float32")
        return npArray
    def modifyTransform(self,x:float,y:float,z:float):
        self.transform.setX(x)
        self.transform.setY(y)
        self.transform.setZ(z)
    def modifyColor(self,verticesColor:QVector3D,polygonColor:QVector3D,color:QVector3D):
        self.verticesColor=verticesColor
        self.polygonColor=polygonColor
        self.color=color
    def modifyVertices(self, data):
        pass

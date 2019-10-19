from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
class AbstractSceneNode(QObject):
    def __init__(self):
        super(AbstractSceneNode, self).__init__()
        #status
        self.STATUS_Changed= True
        #sceneNode common properties
        self.vertices=[]
        self.transform=QVector3D(0,0,0)
        self.m_shaderCompiled=False
        #Shader
        self.program=QOpenGLShaderProgram()
        self.commonProgram=QOpenGLShaderProgram()
        self.lightProgram=QOpenGLShaderProgram()
        #curve
        self.resolution = 50
        self.order = 3
        self.clamped = True
        self.knots = None
        self.weights = None
        #color
        self.verticesColor=QVector3D(1,1,1)
        self.polygonColor=QVector3D(0,1,0)
        self.color=QVector3D(1,1,1)
        #texture
        self.textureID=None
        #Camera transformation
        self.viewMatrix=QMatrix4x4()
        self.modelMatrix=QMatrix4x4()
        self.projectionMatrix=QMatrix4x4()
        self.lookat=QVector3D()
        #Display Properties
        self.m_showPoint=False
        self.m_showPolygon=False
        self.m_showWireframe=False

    def initialize(self):
        self.setupMainShaderProgram()
        self.setupCommonShaderProgram()
    def render(self):
        pass
    #Setup shader
    def setupCommonShaderProgram(self):
        pass
    def setupMainShaderProgram(self):
        pass
    #Camera matrix
    def setupMatrix(self,view,model,projection):
        self.view = view
        self.model = model
        self.projection = projection
    def setupCamera(self,cameraViewPos):
        self.cameraViewPos=cameraViewPos
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
    def loadTexture(self,filePath:str):
        buffer=QImage()
        if buffer.load(filePath)==False:
            qWarning("Can't open the image..")
            dummy=QImage(128,128,QImage.Format_RGB32)
            dummy.fill(Qt.green)
            buffer=dummy
        return buffer
    #Curve property method
    def changeResolution(self,new_resolution:int):
        self.resolution=new_resolution
    def changeEndPointType(self,new_clamped:bool):
        self.clamped=new_clamped
    def changeOrder(self,new_order:int):
        self.order=new_order
    def changeKnots(self,pos:int,value:float):
        self.knots[pos]=value
    def changeWeights(self,pos:int,value:float):
        self.weights[pos]=value


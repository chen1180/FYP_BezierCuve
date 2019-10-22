from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
class AbstractSceneNode(QObject):
    def __init__(self):
        super(AbstractSceneNode, self).__init__()
        #Used to compile shader once
        self.Vertices_Dirty=False
        #sceneNode common properties
        self.vertices=[]
        self.transform=QVector3D(0,0,0)
        self.m_shaderCompiled=False
        #Shader
        self.program=QOpenGLShaderProgram()
        self.commonProgram=QOpenGLShaderProgram()
        self.lightProgram=QOpenGLShaderProgram()
        self.vao = QOpenGLVertexArrayObject()
        self.vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
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
        #Display Properties
        self.m_showPoint=True
        self.m_showPolygon=True
        self.m_showWireframe=False
        self.boundingBox=[QVector3D(0,0,0),QVector3D(2,2,2)]

    def initialize(self):
        if self.m_shaderCompiled==False:
            self.setupMainShaderProgram()
            self.setupCommonShaderProgram()
            self.m_shaderCompiled =True
    def updateVBO(self):
        # if vbo(vertices location) changed, then update vbo data
        if self.Vertices_Dirty==True:
            self.vbo.bind()
            self.vbo.write(0,self.vertices, self.vertices.shape[0] * self.vertices.itemsize)
            self.vbo.release()
            self.Vertices_Dirty =False
    #Camera matrix
    def setupMatrix(self,view:QMatrix4x4,model:QMatrix4x4,projection:QMatrix4x4):
        #important note: take a copy of above matrix!
        self.view = QMatrix4x4(view)
        self.model = QMatrix4x4(model)
        self.projection = QMatrix4x4(projection)
    def setupCamera(self,cameraViewPos:QVector3D):
        self.cameraViewPos=QVector3D(cameraViewPos)
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
        self.verticesColor=QVector3D(verticesColor)
        self.polygonColor=QVector3D(polygonColor)
        self.color=QVector3D(color)
    def modifyVertices(self, data):
        # This step is important, Qlistwidget item may return to original state without this statement
        self.setData(Qt.UserRole,list(data))
        self.vertices = self.QVec3DtoNumpyArray(list(data))
        self.Vertices_Dirty = True
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

    def setupCommonShaderProgram(self):
        pass

    def setupMainShaderProgram(self):
        pass

    def render(self):
        pass
    def TestRayOBBIntersection(self,ray_origin,ray_direction,aabb_min,aabb_max,ModelMatrix):
        tMin=0.0
        tMax=100000.0
        print(ModelMatrix[12],ModelMatrix[13],ModelMatrix[14])
        OBBposition_worldSpace=QVector3D(ModelMatrix[12],ModelMatrix[13],ModelMatrix[14])
        delta=OBBposition_worldSpace-ray_origin
        xaxis=QVector3D(ModelMatrix[0],ModelMatrix[1],ModelMatrix[2])

        e=QVector3D.dotProduct(xaxis,delta)
        f=QVector3D.dotProduct(ray_direction,xaxis)
        if f==0:
            return
        t1=(e+aabb_min.x())/f
        t2=(e+aabb_max.x())/f
        if t1>t2:
            t1,t2=t2,t1
        if t2<tMax:
            tMax=t2
        if t1>tMin:
            tMin=t1
        if tMax<tMin:
            return False


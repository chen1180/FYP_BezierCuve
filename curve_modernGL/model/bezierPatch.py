from PyQt5.QtWidgets import QListWidgetItem,QApplication
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from PyQt5.QtGui import QVector3D,QOpenGLBuffer,QOpenGLVertexArrayObject,QOpenGLShaderProgram,QOpenGLShader,QMatrix4x4
import sys
from curve_modernGL.view.sceneDockWidget import sceneDockWidget
from curve_modernGL.model.sceneNode import sceneNode
import numpy as np
import curve_modernGL.resources.resources
class BezierPatch(QListWidgetItem,sceneNode):
    def __init__(self,parent=None,name:str=None,data:QVector3D=None):
        super(BezierPatch, self).__init__()
        self.setText(str(name))
        self.setData(Qt.UserRole,data)
        self.vertices=self.QVectorListToArray(self.data(Qt.UserRole))
        #vertices data
        self.originalData=data
        #camera setting
        self.model=QMatrix4x4()
        self.view=QMatrix4x4()
        self.projection=QMatrix4x4()
    def QVectorListToArray(self,data):
        tmp=list()
        for vector in data:
            tmp+=[vector[0],vector[1],vector[2]]
        npArray=np.array(tmp,dtype="float32")
        return npArray
    def modifyInputData(self,data):
        self.setData(Qt.UserRole,data) #This step is important, Qlistwidget item may return to original state without this statement
        self.vertices=self.QVectorListToArray(list(data))

    def create(self):
        self.vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.vbo.create()
        self.vbo.bind()
        self.vbo.setUsagePattern(QOpenGLBuffer.StaticDraw)
        self.vbo.allocate(self.vertices,self.vertices.shape[0] * self.vertices.itemsize)
        self.program=QOpenGLShaderProgram()
        # patch vertices
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex,":BezierShader/bezierShader.vert")
        self.program.addShaderFromSourceFile(QOpenGLShader.TessellationControl, ":BezierShader/bezierShader.cs")
        self.program.addShaderFromSourceFile(QOpenGLShader.TessellationEvaluation, ":BezierShader/bezierShader.es")
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, ":BezierShader/bezierShader.frag")
        self.program.link()
        self.program.setPatchVertexCount(4)
        self.vao = QOpenGLVertexArrayObject()
        self.vao.create()
        self.vao.bind()
    def render(self):
        self.program.bind()
        self.program.enableAttributeArray(0)
        self.program.setAttributeBuffer(0, GL_FLOAT, 0, 3)
        Model=QMatrix4x4()
        Model.translate(QVector3D(0,0,-1))
        Model=self.model*Model
        self.MVP=self.projection*self.view*Model
        self.program.setUniformValue("MVP", self.MVP)
        self.vao.bind()
        # Actually draw the triangles
        glDrawArrays(GL_PATCHES, 0, len(self.vertices))
    def setupCameraMatrix(self,view,model,projection):
        self.view=view
        self.model=model
        self.projection=projection
#For debug purpose
if __name__ == '__main__':
    sys._excepthook = sys.excepthook
    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = my_exception_hook
    application=QApplication([])
    # The follow format can set up the OPENGL context
    window = sceneDockWidget() #Opengl window creation
    window.addItem(Bezier(window,"asd",[QVector3D(0,0,0),QVector3D(0,0,2)]))
    window.show()
    application.exec_()
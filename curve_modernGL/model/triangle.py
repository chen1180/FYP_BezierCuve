from PyQt5.QtWidgets import QListWidgetItem,QApplication
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from PyQt5.QtGui import QVector3D,QOpenGLBuffer,QOpenGLVertexArrayObject,QOpenGLShaderProgram,QOpenGLShader
import sys
from curve_modernGL.view.SceneDockWidget import SceneDockWidget
from curve_modernGL.model.SceneNode import AbstractSceneNode
import numpy as np
import curve_modernGL.resources.resources
class Triangle(QListWidgetItem, AbstractSceneNode):
    def __init__(self,parent=None,name:str=None,data:QVector3D=None):
        super(Triangle, self).__init__()
        self.setText(str(name))
        self.setData(Qt.UserRole,data)
        self.vertices=self.QVectorListToArray(self.data(Qt.UserRole))
        print(self.vertices)
    def QVectorListToArray(self,data):
        tmp=[]
        for vector in data:
            tmp+=[vector[0],vector[1],vector[2]]
        npArray=np.array(tmp,dtype="float32")
        return npArray
    def modifyInputData(self,data):
        self.vertices=self.QVectorListToArray(data)
    def initialize(self):
        self.vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.vbo.create()
        self.vbo.bind()
        self.vbo.setUsagePattern(QOpenGLBuffer.StaticDraw)
        self.vbo.allocate(self.vertices,self.vertices.shape[0] * self.vertices.itemsize)
        self.program=QOpenGLShaderProgram()
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex,":TriangleShader/vertexShader.vert")
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, ":TriangleShader/fragmentShader.frag")
        self.program.link()
        self.vao = QOpenGLVertexArrayObject()
        self.vao.create()
        self.vao.bind()

    def render(self):
        self.program.enableAttributeArray(0)
        self.program.setAttributeBuffer(0, GL_FLOAT, 0, 3)
        self.vao.bind()
        # Actually draw the triangles
        self.program.bind()
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices))
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
    window = SceneDockWidget() #Opengl window creation
    window.addItem(Triangle(window,"asd",[QVector3D(0,0,0),QVector3D(0,0,2)]))
    window.show()
    application.exec_()
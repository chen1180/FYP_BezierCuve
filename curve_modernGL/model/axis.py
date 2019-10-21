from PyQt5.QtWidgets import QListWidgetItem,QApplication
from PyQt5.QtCore import Qt,qDebug
from OpenGL.GL import *
from PyQt5.QtGui import QVector3D,QOpenGLBuffer,QOpenGLVertexArrayObject,QOpenGLShaderProgram,QOpenGLShader,QMatrix4x4
import sys
from view.SceneDockWidget import SceneDockWidget
from model.SceneNode import AbstractSceneNode
import numpy as np
import resources.resources
class Axis(AbstractSceneNode):
    def __init__(self,size):
        super(Axis, self).__init__()
        self.size=size
        self.color=QVector3D(0.5,0.5,0.5)
        self.XColor=QVector3D(1,0,0)
        self.YColor = QVector3D(0, 1, 0)
        self.ZColor=QVector3D(0,0,1)
        self.coordinateVertices = self.GenerateAxisVertices(self.size)
        self.coordinateVertices = self.QVec3DtoNumpyArray(self.coordinateVertices)
    def GenerateAxisVertices(self,size):
        coordinateVertices=[]
        # x - axis
        coordinateVertices.append(QVector3D(-size, 0, 0))
        coordinateVertices.append(self.XColor)
        coordinateVertices.append(QVector3D(size, 0, 0))

        coordinateVertices.append(self.XColor)
        # Y - axis
        coordinateVertices.append(QVector3D(0, -size, 0))
        coordinateVertices.append(self.YColor)
        coordinateVertices.append(QVector3D(0, size, 0))

        coordinateVertices.append(self.YColor)
        #z - axis
        coordinateVertices.append(QVector3D(0, 0, -size))
        coordinateVertices.append(self.ZColor)
        coordinateVertices.append(QVector3D(0, 0, size))

        coordinateVertices.append(self.ZColor)
        return coordinateVertices
    def setupMainShaderProgram(self):
        #Bind Coordinate Vertices
        self.axisProgram = QOpenGLShaderProgram()
        self.axisProgram.addShaderFromSourceFile(QOpenGLShader.Vertex, ":CommonShader/axis.vert")
        self.axisProgram.addShaderFromSourceFile(QOpenGLShader.Fragment, ":CommonShader/axis.frag")
        self.axisProgram.link()
        qDebug(self.axisProgram.log())
        self.axisProgram.bind()
        self.axisVAO=QOpenGLVertexArrayObject()
        self.axisVAO.create()
        self.axisVAO.bind()
        self.axisVBO = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.axisVBO.create()
        self.axisVBO.bind()
        self.axisVBO.setUsagePattern(QOpenGLBuffer.StaticDraw)
        self.axisVBO.allocate(self.coordinateVertices, self.coordinateVertices.shape[0] * self.coordinateVertices.itemsize)
        self.axisProgram.enableAttributeArray(0)
        self.axisProgram.setAttributeBuffer(0, GL_FLOAT, 0, 3,6* self.coordinateVertices.itemsize)
        self.axisProgram.enableAttributeArray(1)
        self.axisProgram.setAttributeBuffer(1, GL_FLOAT, 3* self.coordinateVertices.itemsize,3,6* self.coordinateVertices.itemsize)
        qDebug(self.axisProgram.log())
        # release
        self.axisVBO.release()
        self.axisVAO.release()
        self.axisProgram.release()
    def render(self):
        # Camera transformation
        self.MVP = self.projection * self.view * self.model
        # Draw Axis
        self.axisProgram.bind()
        # --------------------------------Transformation---------------------------------------
        self.axisProgram.setUniformValue("MVP", self.MVP)

        self.axisVAO.bind()
        self.axisVBO.bind()
        glDrawArrays(GL_LINES, 0, self.coordinateVertices.shape[0] // 6)
        # Clear up cache
        self.axisVBO.release()
        self.axisVAO.release()
        self.axisProgram.release()
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
    window=Quads(10,1)
    window.show()
    application.exec_()
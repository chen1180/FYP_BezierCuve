from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import qDebug
from OpenGL.GL import *
from PyQt5.QtGui import QVector3D,QOpenGLBuffer,QOpenGLVertexArrayObject,QOpenGLShaderProgram,QOpenGLShader
import sys
from model.geometry.SceneNode import AbstractSceneNode


class Quads(AbstractSceneNode):
    def __init__(self,size:float,step:float):
        super(Quads, self).__init__()
        self.size=size
        self.step=step
        self.vertices=self.GenerateGridVertices(self.size,self.step)
        self.vertices=self.QVec3DtoNumpyArray(self.vertices)
        self.color=QVector3D(0.5,0.5,0.5)
        self.XColor=QVector3D(0.5,0,0)
        self.YColor = QVector3D(0, 0.5, 0)
        self.ZColor=QVector3D(0,0,0.5)
        self.coordinateVertices = self.GenerateAxisVertices(self.size)
        self.coordinateVertices = self.QVec3DtoNumpyArray(self.coordinateVertices)
    def GenerateGridVertices(self,size,step):
        verticies=[]
        for i in range(0,size,step):
            if i==0:
                continue #avoid grid overlay on the x,y,z axis which locate at(0,0,+-size),(0,+-size,0),(+-size,0,0)
            verticies.append(QVector3D(-size,0,i)) #lines parallel to X-axis
            verticies.append(QVector3D(size, 0, i))
            verticies.append(QVector3D(-size, 0, -i)) #lines parallel to X-axis
            verticies.append(QVector3D(size, 0, -i))

            verticies.append(QVector3D(i, 0, -size)) #lines parallel to Z-axis
            verticies.append(QVector3D(i, 0, size))
            verticies.append(QVector3D(-i, 0, -size)) #lines parallel to Z-axis
            verticies.append(QVector3D(-i, 0, size))
        return verticies
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
        # patch vertices
        self.program=QOpenGLShaderProgram()
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex,":CommonShader/vertices.vert")
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment,":CommonShader/vertices.frag")
        self.program.link()
        self.program.bind()
        #setup vao
        self.vao = QOpenGLVertexArrayObject()
        self.vao.create()
        self.vao.bind()
        # initiate all the VBO and VAO
        self.vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.vbo.create()
        self.vbo.bind()
        self.vbo.setUsagePattern(QOpenGLBuffer.StaticDraw)
        self.vbo.allocate(self.vertices, self.vertices.shape[0] * self.vertices.itemsize)
        self.program.enableAttributeArray(0)
        self.program.setAttributeBuffer(0, GL_FLOAT, 0, 3)

        #release
        self.vbo.release()
        self.vao.release()
        self.program.release()
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

        self.program.bind()
        # --------------------------------Transformation---------------------------------------
        self.program.setUniformValue("MVP", self.MVP)
        self.program.setUniformValue("color", self.color)

        self.vbo.bind()
        self.vao.bind()
        #Draw quads
        glDrawArrays(GL_LINES, 0, self.vertices.shape[0]//3)
        # Clear up cache
        self.vbo.release()
        self.vao.release()
        self.program.release()

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
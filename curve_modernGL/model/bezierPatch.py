from PyQt5.QtWidgets import QListWidgetItem,QApplication
from PyQt5.QtCore import Qt,qDebug
from OpenGL.GL import *
from PyQt5.QtGui import QVector3D,QOpenGLBuffer,QOpenGLVertexArrayObject,QOpenGLShaderProgram,QOpenGLShader,QMatrix4x4,QOpenGLTexture
import sys
from curve_modernGL.view.SceneDockWidget import SceneDockWidget
from curve_modernGL.model.SceneNode import AbstractSceneNode
import numpy as np
import curve_modernGL.resources.resources
class BezierPatch(QListWidgetItem, AbstractSceneNode):
    def __init__(self,parent=None,name:str=None,data:QVector3D=None):
        super(BezierPatch, self).__init__()
        self.setText(str(name))
        self.setData(Qt.UserRole,data)
        self.vertices=self.QVec3DtoNumpyArray(self.data(Qt.UserRole))
        #vertices data
        self.originalData=data
        self.counter=0
    def modifyVertices(self,data):
        self.setData(Qt.UserRole,data) #This step is important, Qlistwidget item may return to original state without this statement
        self.vertices=self.QVec3DtoNumpyArray(list(data))
    def setupMainShaderProgram(self):
        # patch vertices
        self.program=QOpenGLShaderProgram()
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex,":BezierPatchShader/bezierShader.vert")
        self.program.addShaderFromSourceFile(QOpenGLShader.TessellationControl, ":BezierPatchShader/bezierShader.tesc")
        self.program.addShaderFromSourceFile(QOpenGLShader.TessellationEvaluation, ":BezierPatchShader/bezierShader.tese")
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, ":BezierPatchShader/bezierShader.frag")
        self.program.link()
        self.program.bind()
        self.program.setPatchVertexCount(16)

        self.vao = QOpenGLVertexArrayObject()
        self.vao.create()
        self.vao.bind()

        self.vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.vbo.create()
        self.vbo.bind()
        self.vbo.setUsagePattern(QOpenGLBuffer.StaticDraw)
        self.vbo.allocate(self.vertices, self.vertices.shape[0] * self.vertices.itemsize)
        self.program.enableAttributeArray(0)
        self.program.setAttributeBuffer(0, GL_FLOAT, 0, 3)
        #Texture creation
        buffer=self.loadTexture(":texture/texture1.jpg")
        self.textureID = QOpenGLTexture(buffer.mirrored(), QOpenGLTexture.GenerateMipMaps)
        self.textureID.setMinificationFilter(QOpenGLTexture.LinearMipMapLinear)
        self.textureID.setMagnificationFilter(QOpenGLTexture.Linear)

        self.vbo.release()
        self.vao.release()
        self.program.release()
    def setupCommonShaderProgram(self):
        # normal program
        self.commonProgram = QOpenGLShaderProgram()
        self.commonProgram.addShaderFromSourceFile(QOpenGLShader.Vertex, ":CommonShader/vertices.vert")
        self.commonProgram.addShaderFromSourceFile(QOpenGLShader.Geometry, ":CommonShader/vertices.gs")
        self.commonProgram.addShaderFromSourceFile(QOpenGLShader.Fragment, ":CommonShader/vertices.frag")
        self.commonProgram.link()
        self.commonProgram.bind()
        self.verticesVao = QOpenGLVertexArrayObject()
        self.verticesVao.create()
        self.verticesVao.bind()
        self.vbo.bind()
        self.commonProgram.enableAttributeArray(0)
        self.commonProgram.setAttributeBuffer(0, GL_FLOAT, 0, 3)
        # release
        self.vbo.release()
        self.vao.release()
        self.commonProgram.release()
    def render(self):
        self.counter+=1
        Model = QMatrix4x4()
        Model.translate(self.transform)
        self.model = Model*self.model
        self.MVP = self.projection * self.view * Model
        self.program.bind()
        # --------------------------------Transformation---------------------------------------
        self.program.setUniformValue("Model", self.model)
        self.program.setUniformValue("View", self.view)
        self.program.setUniformValue("Projection", self.projection)
        #---------------------------------Light---------------------------------------
        self.program.setUniformValue("objectColor", self.color)
        self.program.setUniformValue("lightColor", QVector3D(1,1,1))
        self.program.setUniformValue("lightPos", QVector3D(0,-2,-1))
        self.program.setUniformValue("viewPos", self.cameraViewPos)

        #---------------------------------Texture---------------------------------------------
        self.textureID.bind()
        self.program.setUniformValue("texture0", 0)
        qDebug(self.program.log())

        # Actually draw the triangles
        self.vao.bind()

        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glDrawArrays(GL_PATCHES, 0, self.vertices.shape[0]//3)# (draw type,start_vertices,total_vertices)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        self.textureID.release()
        self.program.release()
        self.vao.release()
        #Draw vertices and polygon
        # Draw vertices
        # Actually rendering of data
        self.commonProgram.bind()
        self.commonProgram.setUniformValue("MVP", self.MVP)
        self.commonProgram.setUniformValue("color", self.polygonColor)

        self.verticesVao.bind()
        #draw polygon connection in row
        for i in range(0,self.vertices.shape[0] // 3,4):
            glDrawArrays(GL_LINE_STRIP, i,4)
        glPointSize(5)
        self.commonProgram.setUniformValue("color", self.verticesColor)
        glDrawArrays(GL_POINTS, 0, self.vertices.shape[0] // 3)

        # Clear up cache
        self.commonProgram.release()
        self.program.release()
        self.verticesVao.release()
        self.vbo.release()
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
    window.addItem(BezierPatch(window,"asd",[QVector3D(0,0,0),QVector3D(0,0,2)]))
    window.show()
    application.exec_()
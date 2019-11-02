from PyQt5.QtWidgets import QListWidgetItem,QApplication
from PyQt5.QtCore import Qt,qDebug
from OpenGL.GL import *
from PyQt5.QtGui import QVector3D,QOpenGLBuffer,QOpenGLVertexArrayObject,QOpenGLShaderProgram,QOpenGLShader,QMatrix4x4,QOpenGLTexture
import sys
from view.SceneDockWidget import SceneDockWidget
from model.geometry.SceneNode import AbstractSceneNode


class BezierPatch(QListWidgetItem, AbstractSceneNode):
    def __init__(self,parent=None,name:str=None,data:QVector3D=None):
        super(BezierPatch, self).__init__()
        self.setText(str(name))
        self.setData(Qt.UserRole,data)
        self.vertices=self.QVec3DtoNumpyArray(self.data(Qt.UserRole))
        self.resolution=10
    def setupMainShaderProgram(self):
        # patch vertices
        self.program=QOpenGLShaderProgram()
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex,":Shaders/bezierPatch.vert")
        self.program.addShaderFromSourceFile(QOpenGLShader.TessellationEvaluation, ":Shaders/bezierPatch.tese")
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, ":Shaders/bezierPatch.frag")
        self.program.link()
        if self.program.log():
            qDebug(self.program.log())
        self.program.bind()
        self.program.setPatchVertexCount(16)
        self.program.setDefaultOuterTessellationLevels([self.resolution] * 4)
        self.program.setDefaultInnerTessellationLevels([self.resolution] * 2)

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
    def setupPickingShaderProgram(self):
        # patch vertices
        self.pickingProgram = QOpenGLShaderProgram()
        self.pickingProgram.addShaderFromSourceFile(QOpenGLShader.Vertex, ":Shaders/bezierPatch.vert")
        self.pickingProgram.addShaderFromSourceFile(QOpenGLShader.TessellationEvaluation, ":Shaders/bezierPatch.tese")
        self.pickingProgram.addShaderFromSourceFile(QOpenGLShader.Fragment, ":CommonShader/picking.frag")
        self.pickingProgram.link()
        if self.pickingProgram.log():
            qDebug(self.pickingProgram.log())
        self.pickingProgram.bind()
        self.pickingProgram.setPatchVertexCount(16)
        self.pickingProgram.setDefaultOuterTessellationLevels([self.resolution] * 4)
        self.pickingProgram.setDefaultInnerTessellationLevels([self.resolution] * 2)
        self.vao.bind()
        self.vbo.bind()
        self.pickingProgram.enableAttributeArray(0)
        self.pickingProgram.setAttributeBuffer(0, GL_FLOAT, 0, 3)
        self.vbo.release()
        self.vao.release()
        self.pickingProgram.release()
    def setupOutlineShaderProgram(self):
        # stencil buffer
        self.stencilProgram = QOpenGLShaderProgram()
        self.stencilProgram.addShaderFromSourceFile(QOpenGLShader.Vertex, ":Shaders/bezierPatch.vert")
        self.stencilProgram.addShaderFromSourceFile(QOpenGLShader.TessellationEvaluation, ":Shaders/bezierPatch.tese")
        self.stencilProgram.addShaderFromSourceFile(QOpenGLShader.Fragment, ":CommonShader/solid_color.frag")
        self.stencilProgram.link()
        self.stencilProgram.bind()
        self.stencilProgram.setPatchVertexCount(16)
        self.stencilProgram.setDefaultOuterTessellationLevels([self.resolution] * 4)
        self.stencilProgram.setDefaultInnerTessellationLevels([self.resolution] * 2)
        self.vao.bind()
        self.vbo.bind()
        self.stencilProgram.enableAttributeArray(0)
        self.stencilProgram.setAttributeBuffer(0, GL_FLOAT, 0, 3)
        self.vbo.release()
        self.vao.release()
        self.stencilProgram.release()
    def renderPicking(self,pickIndex,drawIndex):
        Model = QMatrix4x4()
        Model.translate(self.transform)
        self.model = Model * self.model
        self.MVP = self.projection * self.view * Model
        self.pickingProgram.bind()
        self.pickingProgram.setPatchVertexCount(16)
        self.pickingProgram.setDefaultOuterTessellationLevels([self.resolution] * 4)
        self.pickingProgram.setDefaultInnerTessellationLevels([self.resolution] * 2)
        self.vbo.bind()
        # --------------------------------Transformation---------------------------------------
        self.pickingProgram.setUniformValue("Model", self.model)
        self.pickingProgram.setUniformValue("View", self.view)
        self.pickingProgram.setUniformValue("Projection", self.projection)
        # ---------------------------------Light---------------------------------------
        self.pickingProgram.setUniformValue("lightPos", QVector3D(0, -2, -1))
        #----------------------------------Indexing--------------------------------------------
        self.pickingProgram.setUniformValue("gDrawIndex",drawIndex)
        self.pickingProgram.setUniformValue("gObjectIndex", pickIndex)
        self.vao.bind()
        glDrawArrays(GL_PATCHES, 0, self.vertices.shape[0] // 3)
        self.vbo.release()
        self.vao.release()
        self.pickingProgram.release()
    def renderOutline(self):
        self.stencilProgram.bind()
        Model = QMatrix4x4()
        Model.translate(self.transform)
        self.model.scale(1.02)
        self.model = Model * self.model
        self.MVP = self.projection * self.view * Model

        # --------------------------------Transformation---------------------------------------
        self.stencilProgram.setUniformValue("Model", self.model)
        self.stencilProgram.setUniformValue("View", self.view)
        self.stencilProgram.setUniformValue("Projection", self.projection)
        # ---------------------------------Light---------------------------------------
        self.stencilProgram.setUniformValue("lightPos", QVector3D(0, -2, -1))
        self.vbo.bind()
        self.vao.bind()
        if self.m_showWireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glDrawArrays(GL_PATCHES, 0, self.vertices.shape[0] // 3)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glDrawArrays(GL_PATCHES, 0, self.vertices.shape[0] // 3)
        self.vbo.release()
        self.vao.release()
        self.stencilProgram.release()
    def render(self):
        Model = QMatrix4x4()
        Model.translate(self.transform)
        self.model = Model*self.model
        self.MVP = self.projection * self.view * Model
        self.program.bind()
        self.program.setPatchVertexCount(16)
        self.program.setDefaultOuterTessellationLevels([self.resolution] * 4)
        self.program.setDefaultInnerTessellationLevels([self.resolution] * 2)
        self.vbo.bind()
        # --------------------------------Transformation---------------------------------------
        self.program.setUniformValue("Model", self.model)
        self.program.setUniformValue("View", self.view)
        self.program.setUniformValue("Projection", self.projection)
        #---------------------------------Light---------------------------------------
        self.program.setUniformValue("objectColor", self.color)
        self.program.setUniformValue("lightColor", QVector3D(1,1,1))
        self.program.setUniformValue("lightPos", QVector3D(0,-2,-1))
        self.program.setUniformValue("viewPos", self.cameraViewPos)
        self.program.setUniformValue("wireFrameMode", self.m_showWireframe)
        #---------------------------------Texture---------------------------------------------
        self.textureID.bind()
        self.program.setUniformValue("texture0", 0)
        if self.program.log():
            qDebug(self.program.log())

        # Actually draw the triangles
        self.vao.bind()
        if self.m_showWireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glDrawArrays(GL_PATCHES, 0, self.vertices.shape[0] // 3)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glDrawArrays(GL_PATCHES, 0, self.vertices.shape[0] // 3)
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
        self.vao.release()
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
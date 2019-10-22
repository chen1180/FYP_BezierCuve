from PyQt5.QtWidgets import QListWidgetItem,QApplication
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from PyQt5.QtGui import QVector3D,QOpenGLBuffer,QOpenGLVertexArrayObject,QOpenGLShaderProgram,QOpenGLShader,QMatrix4x4
import sys
from view.SceneDockWidget import SceneDockWidget
from model.SceneNode import AbstractSceneNode
import resources.resources
class Bezier(QListWidgetItem, AbstractSceneNode):
    def __init__(self,parent=None,name:str=None,data:QVector3D=None):
        super(Bezier, self).__init__()
        self.setText(str(name))
        self.setData(Qt.UserRole,data)
        self.vertices=self.QVec3DtoNumpyArray(self.data(Qt.UserRole))
        #vertices data
        self.originalData=data
        self.order=len(self.data(Qt.UserRole))-1
    def modifyVertices(self, data):
        self.setData(Qt.UserRole,data) #This step is important, Qlistwidget item may return to original state without this statement
        self.vertices=self.QVec3DtoNumpyArray(data)
        self.Vertices_Dirty = True
        self.Shader_Dirty = True
    def setupMainShaderProgram(self):
        # patch vertices
        self.program=QOpenGLShaderProgram()
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex,":Shaders/bezier.vert")
        self.program.addShaderFromSourceFile(QOpenGLShader.TessellationEvaluation, ":Shaders/bezier.tese")
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, ":Shaders/bezier.frag")
        self.program.link()
        self.program.bind()
        self.program.setDefaultOuterTessellationLevels([1, self.resolution])
        # Qpengl Tesselation Control Shader attribute
        self.program.setPatchVertexCount(self.vertices.shape[0] // 3)  # Maximum patch vertices
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
    def render(self):
        # Camera transformation
        Model = QMatrix4x4()
        Model.translate(self.transform)
        self.model *=Model
        self.MVP = self.projection * self.view *  self.model
        # Actually rendering of data
        self.program.bind()
        self.vbo.bind()
        self.updateVBO()
        self.program.setUniformValue("MVP", self.MVP)
        # Rencently add code for lighting
        # ------------------------------------------------------------------------------
        self.program.setUniformValue("objectColor", self.color)
        self.program.setUniformValue("lightColor", QVector3D(1, 1, 1))
        # ------------------------------------------------------------------------------
        #Draw primitives
        self.vao.bind()
        glDrawArrays(GL_PATCHES, 0, self.vertices.shape[0]//3)
        self.vao.release()
        self.program.release()

        #Draw vertices
        # Actually rendering of data
        self.commonProgram.bind()
        self.commonProgram.setUniformValue("MVP", self.MVP)
        self.commonProgram.setUniformValue("color",self.polygonColor)
        self.verticesVao.bind()

        glDrawArrays(GL_LINE_STRIP,0,self.vertices.shape[0]//3)

        glPointSize(5)
        self.commonProgram.setUniformValue("color",self.verticesColor)
        glDrawArrays(GL_POINTS, 0, self.vertices.shape[0] // 3)

        #Clear up cache
        self.commonProgram.release()
        self.verticesVao.release()

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
    window.addItem(Bezier(window,"asd",[QVector3D(0,0,0),QVector3D(0,0,2)]))
    window.show()
    application.exec_()
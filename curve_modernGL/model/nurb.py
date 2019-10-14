from PyQt5.QtWidgets import QListWidgetItem,QApplication
from PyQt5.QtCore import Qt,qDebug
from OpenGL.GL import *
from PyQt5.QtGui import QVector3D,QOpenGLBuffer,QOpenGLVertexArrayObject,QOpenGLShaderProgram,QOpenGLShader,QMatrix4x4
import sys
from curve_modernGL.view.SceneDockWidget import SceneDockWidget
from curve_modernGL.model.SceneNode import AbstractSceneNode
import curve_modernGL.resources.resources
class Nurbs(QListWidgetItem, AbstractSceneNode):
    def __init__(self,parent=None,name:str=None,data:QVector3D=None):
        super(Nurbs, self).__init__()
        self.setText(str(name))
        self.setData(Qt.UserRole,data)
        self.vertices=self.QVec3DtoNumpyArray(self.data(Qt.UserRole))
        self.order=2
        self.knots=self.generateKnots(len(data),2)
    def generateKnots(self,n,k):
        #For open B-spline curves, the domain is [uk, um-k]. k is the degree,m is n+k+1
        nKnots = n + k + 1
        knots = []
        for i in range(nKnots):
            knots.append([i])
        print(knots)
        return knots
    def modifyVertices(self, data):
        self.setData(Qt.UserRole,data) #This step is important, Qlistwidget item may return to original state without this statement
        self.vertices=self.QVec3DtoNumpyArray(data)
        print(self.vertices,self.vertices.shape[0]/3.0)
    def setupMainShaderProgram(self):
        # patch vertices
        self.program=QOpenGLShaderProgram()
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex,":NurbsShader/nurbsShader.vert")
        # self.program.addShaderFromSourceFile(QOpenGLShader.TessellationControl, ":NurbsShader/nurbsShader.tesc")
        self.program.addShaderFromSourceFile(QOpenGLShader.TessellationEvaluation, ":NurbsShader/nurbsShader.tese")
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, ":NurbsShader/nurbsShader.frag")
        self.program.link()
        self.program.bind()
        #Tesslation control shader attribute
        #(No need to use tesslation control shader since all the property can be modified by the following command)
        self.program.setPatchVertexCount(4)
        self.program.setDefaultOuterTessellationLevels([1, 10])
        # Qpengl Tesselation Control Shader attribute
        self.program.setPatchVertexCount(4)  # Maximum patch vertices
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
    def render(self):
        # Camera transformation
        Model = QMatrix4x4()
        Model.translate(self.transform)
        self.model *=Model
        self.MVP = self.projection * self.view *  self.model
        # Actually rendering of data
        self.program.bind()
        self.program.setUniformValue("MVP", self.MVP)
        # Rencently add code for lighting
        # ------------------------------------------------------------------------------
        self.program.setUniformValue("objectColor", self.color)
        self.program.setUniformValue("lightColor", QVector3D(1, 1, 1))
        self.program.setUniformValueArray("knots", self.knots)
        self.program.setUniformValue("knots_size",len(self.knots))
        self.program.setUniformValue("order", self.order)
        qDebug(self.program.log())
        # ------------------------------------------------------------------------------
        #Draw primitives
        self.vao.bind()
        glDrawArrays(GL_PATCHES, 0, self.vertices.shape[0]//3)
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
    window.addItem(Nurbs(window,"asd",[QVector3D(0,0,0),QVector3D(0,0,2)]))
    window.show()
    application.exec_()
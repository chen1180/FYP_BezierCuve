from OpenGL.GL import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from model.trackBall import Trackball
import sys
import numpy as np
import resources.resources
class OpenGLWindow(QOpenGLWidget):
    OPENGL_NEED_UPDATE=pyqtSignal(bool)
    VIEWPORT_PERSPECTIVE=0
    VIEWPORT_ORTHO=1
    VIEWPORT_XY_PLANE=2
    VIEWPORT_YZ_PLANE = 3
    VIEWPORT_XZ_PLANE = 4
    def __init__(self,parent=None):
        super(OpenGLWindow, self).__init__(parent)
        format = QSurfaceFormat()
        format.setDepthBufferSize(24)
        format.setStencilBufferSize(8)
        format.setVersion(4, 1)
        format.setSwapBehavior(QSurfaceFormat.DoubleBuffer)
        format.setProfile(QSurfaceFormat.CoreProfile)
        self.setFormat(format)
        self.camera=Trackball(QVector3D(0,0,-5),QVector3D(0,0,0),QVector3D(0,1,0))
        #default plane
        self.viewPortState=self.VIEWPORT_PERSPECTIVE
        self.viewPlane=self.VIEWPORT_XY_PLANE
    def loadTexture(self,filePath:str):
        buffer=QImage()
        if buffer.load(filePath)==False:
            qWarning("Can't open the image..")
            dummy=QImage(128,128,QImage.Format_RGB32)
            dummy.fill(Qt.green)
            buffer=dummy
        return buffer
    def initializeGL(self) -> None:
        QOpenGLWidget.initializeGL(self)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0, 0, 0, 1.0)
        self.vertices=np.array([-0.5, -0.5, -0.5,  0.0, 0.0,
         0.5, -0.5, -0.5,  1.0, 0.0,
         0.5,  0.5, -0.5,  1.0, 1.0,
         0.5,  0.5, -0.5,  1.0, 1.0,
        -0.5,  0.5, -0.5,  0.0, 1.0,
        -0.5, -0.5, -0.5,  0.0, 0.0,

        -0.5, -0.5,  0.5,  0.0, 0.0,
         0.5, -0.5,  0.5,  1.0, 0.0,
         0.5,  0.5,  0.5,  1.0, 1.0,
         0.5,  0.5,  0.5,  1.0, 1.0,
        -0.5,  0.5,  0.5,  0.0, 1.0,
        -0.5, -0.5,  0.5,  0.0, 0.0,

        -0.5,  0.5,  0.5,  1.0, 0.0,
        -0.5,  0.5, -0.5,  1.0, 1.0,
        -0.5, -0.5, -0.5,  0.0, 1.0,
        -0.5, -0.5, -0.5,  0.0, 1.0,
        -0.5, -0.5,  0.5,  0.0, 0.0,
        -0.5,  0.5,  0.5,  1.0, 0.0,

         0.5,  0.5,  0.5,  1.0, 0.0,
         0.5,  0.5, -0.5,  1.0, 1.0,
         0.5, -0.5, -0.5,  0.0, 1.0,
         0.5, -0.5, -0.5,  0.0, 1.0,
         0.5, -0.5,  0.5,  0.0, 0.0,
         0.5,  0.5,  0.5,  1.0, 0.0,

        -0.5, -0.5, -0.5,  0.0, 1.0,
         0.5, -0.5, -0.5,  1.0, 1.0,
         0.5, -0.5,  0.5,  1.0, 0.0,
         0.5, -0.5,  0.5,  1.0, 0.0,
        -0.5, -0.5,  0.5,  0.0, 0.0,
        -0.5, -0.5, -0.5,  0.0, 1.0,

        -0.5,  0.5, -0.5,  0.0, 1.0,
         0.5,  0.5, -0.5,  1.0, 1.0,
         0.5,  0.5,  0.5,  1.0, 0.0,
         0.5,  0.5,  0.5,  1.0, 0.0,
        -0.5,  0.5,  0.5,  0.0, 0.0,
        -0.5,  0.5, -0.5,  0.0, 1.0],dtype="float32")
        self.program = QOpenGLShaderProgram()
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex, ":CommonShader/cube.vert")
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, ":CommonShader/cube.frag")
        self.program.link()
        self.vao = QOpenGLVertexArrayObject()
        self.vao.create()
        self.vao.bind()

        self.vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.vbo.create()
        self.vbo.bind()
        self.vbo.setUsagePattern(QOpenGLBuffer.StaticDraw)
        self.vbo.allocate(self.vertices, self.vertices.shape[0] * self.vertices.itemsize)

        self.program.enableAttributeArray(0)
        self.program.setAttributeBuffer(0, GL_FLOAT, 0, 3, 5 * self.vertices.itemsize)
        self.program.enableAttributeArray(1)
        self.program.setAttributeBuffer(1, GL_FLOAT, 3 * self.vertices.itemsize, 2, 5 * self.vertices.itemsize)

        buffer = self.loadTexture(":texture/texture.png")
        self.textureID = QOpenGLTexture(buffer.mirrored(), QOpenGLTexture.GenerateMipMaps)
        self.textureID.setMinificationFilter(QOpenGLTexture.LinearMipMapLinear)
        self.textureID.setMagnificationFilter(QOpenGLTexture.Linear)

        self.vbo.release()
        self.vao.release()
        self.program.release()
        #frame buffer

        self.m_fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.m_fbo)
        # Create the texture object for the primitive information buffer
        self.m_pickingTexture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.m_pickingTexture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB32F, self.width(), self.height(), 0, GL_RGB, GL_FLOAT, None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.m_pickingTexture, 0)
        # Create the texture object for the depth buffer
        self.m_depthTexture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.m_depthTexture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, self.width(), self.height(), 0, GL_DEPTH_COMPONENT, GL_FLOAT,None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.m_depthTexture, 0)

        self.rbo = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.rbo)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, self.width(), self.height())
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, self.rbo)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
        if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE):
            qDebug("ERROR::FRAMEBUFFER:: Framebuffer is not complete!")
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        #generate random transformation
        size=np.random.randint(-5,5,size=(5,3))
        self.transform=[QVector3D(i[0],i[1],i[2]) for i in size]
    def paintGL(self) -> None:
        originalFBO = glGetIntegerv(GL_FRAMEBUFFER_BINDING)
        glBindFramebuffer(GL_FRAMEBUFFER, self.m_fbo)
        glClearColor(0.5, 0.5, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        Projection = self.setupProjectionMatrix()
        View = self.setupViewMatrix()
        self.program.bind()
        self.vbo.bind()
        self.program.enableAttributeArray(0)
        self.program.setAttributeBuffer(0, GL_FLOAT, 0, 3, 5*self.vertices.itemsize)
        self.program.enableAttributeArray(1)
        self.program.setAttributeBuffer(1, GL_FLOAT, 2*self.vertices.itemsize, 2, 5*self.vertices.itemsize)
        for transform in self.transform:
            Model = QMatrix4x4()
            Model.translate(transform)
            MVP = Projection * View * Model
            self.program.setUniformValue("MVP", MVP)
            self.vao.bind()
            # Actually draw the triangles
            glDrawArrays(GL_TRIANGLES, 0, self.vertices.shape[0] // 5)
        self.program.release()
        glBindFramebuffer(GL_FRAMEBUFFER, originalFBO)
        glClearColor(0, 0, 0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        self.program.bind()
        self.vbo.bind()
        self.vao.bind()
        for transform in self.transform:
            Model = QMatrix4x4()
            Model.translate(transform)
            MVP = Projection * View * Model
            self.program.setUniformValue("MVP", MVP)
            self.textureID.bind()
            # glBindTexture(GL_TEXTURE_2D, self.m_pickingTexture)
            self.program.setUniformValue("texture1", 0)
            glDrawArrays(GL_TRIANGLES, 0, self.vertices.shape[0] // 5)
        self.vao.release()
        self.update()
    def resizeGL(self, w: int, h: int) -> None:
        side = min(w, h)
        glViewport((w - h) // 2, (w - h) // 2, side,side)


    # -----------------------------Projection and View matrix -----------------------------------#
    def pixelPosToViewPos(self,p:QPointF):
        return QPointF(2*p.x()/self.width()-1.0,1.0-2.0*p.y()/self.height())
    def PerspectiveToOrtho(self,state:bool):
        if state==False:
            self.viewPortState=self.VIEWPORT_PERSPECTIVE
        else:
            self.viewPortState=self.VIEWPORT_ORTHO
    def setupProjectionMatrix(self):
        Projection = QMatrix4x4()
        if self.viewPortState == self.VIEWPORT_ORTHO:
            Projection.ortho(-0.5 * self.camera.radius, 0.5* self.camera.radius, -0.5 * self.camera.radius,
                             0.5 * self.camera.radius, 0.1, 100)
        elif self.viewPortState == self.VIEWPORT_PERSPECTIVE:
            Projection.perspective(45.0, self.width() / self.height(), 0.1, 100)
        return Projection
    def setupViewMatrix(self,enableCameraPan=True):
        if self.viewPlane==self.VIEWPORT_XY_PLANE:
            rotation=QQuaternion()
        elif self.viewPlane==self.VIEWPORT_YZ_PLANE:
            rotation=QQuaternion().fromAxisAndAngle(QVector3D(0, 0, 1), 90)
        elif self.viewPlane==self.VIEWPORT_XZ_PLANE:
            rotation=QQuaternion().fromAxisAndAngle(QVector3D(1,0,0),90)
        View = QMatrix4x4()
        if enableCameraPan:
            View.lookAt(self.camera.cameraPos, self.camera.targetPos, self.camera.cameraUp)
        else:
            View.lookAt(self.camera.viewPos,QVector3D(0,0,0), self.camera.cameraUp)
        View.rotate(rotation)
        return View
    # -----------------------------Signal and Slots -----------------------------------#
    def addToScene(self, scene):
        self.scene=list(scene)
        self.update()
    def removeFromScene(self,item):
        self.scene.remove(item)
        self.update()
    # -----------------------------Mouse and Keyboards -----------------------------------#
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        super(OpenGLWindow, self).mousePressEvent(a0)
        if a0.isAccepted():
            return
        if (a0.modifiers()& Qt.ControlModifier)and(a0.buttons()&Qt.LeftButton): #Control+Left click
            self.camera.pushRotation(self.pixelPosToViewPos(a0.windowPos()))
            a0.accept()
        if a0.buttons()&Qt.RightButton:#Right click
            self.camera.pushPanning(self.pixelPosToViewPos(a0.windowPos()))
            a0.accept()
        self.update()
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        super(OpenGLWindow, self).mouseMoveEvent(a0)
        if a0.isAccepted():
            return
        if (a0.modifiers()& Qt.ControlModifier)and(a0.buttons()&Qt.LeftButton): #Control+Left click
            self.camera.moveRotation(self.pixelPosToViewPos(a0.windowPos()))
            a0.accept()
        if a0.buttons()&Qt.RightButton:#Right click
            self.camera.movePannning(self.pixelPosToViewPos(a0.windowPos()))
            a0.accept()
        self.update()
    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        super(OpenGLWindow, self).mouseReleaseEvent(a0)
        if a0.isAccepted():
            return
        if (a0.modifiers()& Qt.ControlModifier)and(a0.buttons()&Qt.LeftButton): #Control+Left click
            self.camera.releaseRotation(self.pixelPosToViewPos(a0.windowPos()))
            a0.accept()
        if a0.buttons()&Qt.RightButton:#Right click
            self.camera.releasePanning()
            a0.accept()
        self.update()
    def wheelEvent(self, a0: QWheelEvent) -> None:
        super(OpenGLWindow, self).wheelEvent(a0)
        if not a0.isAccepted():
            self.camera.moveZooming(a0.angleDelta().y())
            a0.accept()
        self.update()
# -----------------------------Debugging-----------------------------------#
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
    format=QSurfaceFormat()
    format.setDepthBufferSize(24)
    format.setStencilBufferSize(8)
    format.setVersion(4,1)
    format.setProfile(QSurfaceFormat.CoreProfile)
    QSurfaceFormat.setDefaultFormat(format) #it must be called before OpenGL window, set OPENGL format globally
    window = OpenGLWindow() #Opengl window creation
    window.show()
    application.exec_()


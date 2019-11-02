from OpenGL.GL import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from model.trackBall import Trackball
import sys
import numpy as np
import resources.resources
from model.geometry.bezierPatch import BezierPatch
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
        self.patch = BezierPatch(None, "BeizerPatch",
                                 [QVector3D(-1, -0.5, -0.5), QVector3D(-1, 1, -0.5), QVector3D(0, 1, -0.5),
                                  QVector3D(1, -1, -0.5),
                                  QVector3D(-1, -0.2, -0.2), QVector3D(-1, 0.7, -0.2), QVector3D(0, 0.7, -0.2),
                                  QVector3D(1, -1.3, -0.2),
                                  QVector3D(-1, 0.1, 0.2), QVector3D(-1, 0.4, 0.2), QVector3D(0, 0.4, 0.2),
                                  QVector3D(1, -1.6, 0.2),
                                  QVector3D(-1, -0.2, 0.5), QVector3D(-1, 0.1, 0.5), QVector3D(0, 0.1, 0.5),
                                  QVector3D(2, -2, 0.5)])
    def loadTexture(self,filePath:str):
        buffer=QImage()
        if buffer.load(filePath)==False:
            qWarning("Can't open the image..")
            dummy=QImage(128,128,QImage.Format_RGB32)
            dummy.fill(Qt.green)
            buffer=dummy
        return buffer
    def calculateFPS(self):
        self.frameCount+=1
        if self.frameTimer.elapsed()>=1000:
            self.fps=self.frameCount/(self.frameTimer.elapsed()/1000.0)
            self.frameCount=0
            self.frameTimer.restart()
    def initializeGL(self) -> None:
        QOpenGLWidget.initializeGL(self)
        #configure global opengl state
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        # -----------------------------
        #constant
        self.frameCount=0
        self.frameTimer = QTime()
        self.frameTimer.start()
        self.fps=0
        # -----------------------------
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
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, ":CommonShader/multiple_render_object.frag")
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
        #stencil buffer
        self.stencilProgram = QOpenGLShaderProgram()
        self.stencilProgram.addShaderFromSourceFile(QOpenGLShader.Vertex, ":CommonShader/cube.vert")
        self.stencilProgram.addShaderFromSourceFile(QOpenGLShader.Fragment, ":CommonShader/cube.frag")
        self.stencilProgram.link()
        self.vao.bind()
        self.vbo.bind()
        self.stencilProgram.enableAttributeArray(0)
        self.stencilProgram.setAttributeBuffer(0, GL_FLOAT, 0, 3, 5 * self.vertices.itemsize)
        self.stencilProgram.enableAttributeArray(1)
        self.stencilProgram.setAttributeBuffer(1, GL_FLOAT, 3 * self.vertices.itemsize, 2, 5 * self.vertices.itemsize)
        self.vbo.release()
        self.vao.release()
        self.stencilProgram.release()
        # The full screen quad
        self.quadVertices = np.array([-1.0, -1.0, 0.0, 0.0, 0.0,
                                      1.0, -1.0, 0.0, 1.0, 0.0,
                                      1.0, 1.0, 0.0, 1.0, 1.0,
                                      -1.0, 1.0, 0.0, 0.0, 1.0, ], dtype="float32")

        self.quadProgram = QOpenGLShaderProgram()
        self.quadProgram.addShaderFromSourceFile(QOpenGLShader.Vertex, ":CommonShader/quad.vert")
        self.quadProgram.addShaderFromSourceFile(QOpenGLShader.Fragment, ":post_processing/color_picker.frag")
        self.quadProgram.link()
        self.quadVao = QOpenGLVertexArrayObject()
        self.quadVao.create()
        self.quadVao.bind()

        self.quadVbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.quadVbo.create()
        self.quadVbo.bind()
        self.quadVbo.setUsagePattern(QOpenGLBuffer.StaticDraw)
        self.quadVbo.allocate(self.quadVertices, self.quadVertices.shape[0] * self.quadVertices.itemsize)

        self.quadProgram.enableAttributeArray(0)
        self.quadProgram.setAttributeBuffer(0, GL_FLOAT, 0, 3, 5 * self.quadVertices.itemsize)
        self.quadProgram.enableAttributeArray(1)
        self.quadProgram.setAttributeBuffer(1, GL_FLOAT, 3 * self.quadVertices.itemsize, 2,
                                            5 * self.quadVertices.itemsize)
        self.quadVbo.release()
        self.quadVao.release()
        self.quadProgram.release()
        # frame buffer
        self.m_fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.m_fbo)
        # Create the texture object for the primitive information buffer
        self.m_pickingTexture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.m_pickingTexture)
        # Poor filtering. Needed
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB32F, self.width(), self.height(), 0, GL_RGB, GL_FLOAT, None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.m_pickingTexture, 0)
        glBindTexture(GL_TEXTURE_2D, 0)
        # real texture
        self.m_finalTexture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.m_finalTexture)
        # Poor filtering. Needed
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB32F, self.width(), self.height(), 0, GL_RGB, GL_FLOAT, None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT1, GL_TEXTURE_2D, self.m_finalTexture, 0)
        glBindTexture(GL_TEXTURE_2D, 0)
        # Create the texture object for the depth buffer
        self.m_depthTexture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.m_depthTexture)
        # Poor filtering. Needed
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT24, self.width(), self.height(), 0, GL_DEPTH_COMPONENT,
                     GL_FLOAT, None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.m_depthTexture, 0)
        glBindTexture(GL_TEXTURE_2D, 0)

        self.rbo = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.rbo)
        #Render buffer support depth and stencil buffer
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, self.width(), self.height())
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, self.rbo)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
        DrawBuffers = [GL_COLOR_ATTACHMENT0,GL_COLOR_ATTACHMENT1]
        glDrawBuffers(len(DrawBuffers), DrawBuffers)
        if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE):
            qDebug("ERROR::FRAMEBUFFER:: Framebuffer is not complete!")

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        size = np.random.randint(-2, 2, size=(10, 3))
        self.transform = [QVector3D(i[0], i[1], i[2]) for i in size]
        # custom shape
        self.patch.initialize()
    def paintGL(self) -> None:
        #Transformation
        Projection = self.setupProjectionMatrix()
        View = self.setupViewMatrix()
        # off screen FBO rendering
        originalFBO = glGetIntegerv(GL_FRAMEBUFFER_BINDING)
        glBindFramebuffer(GL_FRAMEBUFFER, self.m_fbo)
        # On screen rendering
        glClearColor(0, 0, 0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glViewport(0, 0, self.width(), self.height())
        self.program.bind()
        self.vbo.bind()
        self.vao.bind()
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, self.m_fbo)
        for transform in self.transform:
            Model = QMatrix4x4()
            Model.translate(transform)
            Model.rotate(30, transform)
            MVP = Projection * View * Model
            self.program.setUniformValue("MVP", MVP)
            self.textureID.bind()
            self.program.setUniformValue("texture1", self.textureID.textureId())
            glDrawArrays(GL_TRIANGLES, 0, self.vertices.shape[0] // 5)
        self.patch.setupMatrix(View, Model, Projection)
        self.patch.setupCamera(self.camera.cameraPos)
        self.patch.render()
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)
        # calculate frame rate
        self.calculateFPS()

        self.vbo.release()
        self.vao.release()
        self.program.release()
        # After painter start, opengl state will be changed to some state
        painter = QPainter(self)
        self.drawInstructions(painter)
        painter.end()
        # Restore to previous OpenGL state
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        # -----------------------------
        # On screen rendering
        glBindFramebuffer(GL_FRAMEBUFFER, originalFBO)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glViewport(0, 0, self.width(), self.height())
        '''
        Render fbo as a quad on screen
        '''
        self.quadProgram.bind()
        self.quadVbo.bind()
        self.quadVao.bind()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.m_finalTexture)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.m_pickingTexture)
        self.quadProgram.setUniformValue("texFramebuffer", 0)
        self.quadProgram.setUniformValue("color_texture", 1)
        self.quadProgram.setUniformValue("pickingID", 1.0)
        self.quadProgram.setUniformValue("width", float(self.width()))
        self.quadProgram.setUniformValue("height", float(self.height()))
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.quadVertices.shape[0] // 5)
        self.quadVao.release()
        self.quadVbo.release()
        self.quadProgram.release()
        self.update()
    def resizeGL(self, w: int, h: int) -> None:
        side = min(w, h)
        glViewport((w - h) // 2, (w - h) // 2, side,side)
    def drawInstructions(self, painter):
        # Draw operation instruction on the scrren
        font = painter.font()
        font.setPointSize(12)
        painter.setFont(font)
        painter.setPen(QPen(Qt.white))
        instruction = "FPS {}".format(int(self.fps))
        rect = QRect(10, 10, self.width() / 4, self.height() / 4)
        painter.drawText(rect, Qt.AlignLeft | Qt.TextWordWrap, instruction)
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
    # -----------------------------Mouse and Keyboards -----------------------------------#
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        super(OpenGLWindow, self).mousePressEvent(a0)
        if a0.isAccepted():
            return
        if a0.buttons()&Qt.LeftButton:#Right click
            a0.accept()

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
def qt_message_handler(mode, context, message):
    if mode == QtInfoMsg:
        mode = 'INFO'
    elif mode == QtWarningMsg:
        mode = 'WARNING'
    elif mode == QtCriticalMsg:
        mode = 'CRITICAL'
    elif mode == QtFatalMsg:
        mode = 'FATAL'
    else:
        mode = 'DEBUG'
    print('qt_message_handler: line: %d, func: %s(), file: %s' % (
          context.line, context.function, context.file))
    print('  %s: %s\n' % (mode, message))

if __name__ == '__main__':
    sys._excepthook = sys.excepthook
    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = my_exception_hook
    qInstallMessageHandler(qt_message_handler)
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


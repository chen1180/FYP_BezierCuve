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
        glEnable(GL_STENCIL_TEST)
        glStencilFunc(GL_NOTEQUAL, 1, 0xFF)
        glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
        # -----------------------------
        #constant
        self.frameCount=0
        self.frameTimer = QTime()
        self.frameTimer.start()
        self.fps=0
        # -----------------------------
        glClearColor(0, 0, 0, 1.0)
        from geomdl import BSpline

        # Create a 3-dimensional B-spline Curve
        curve = BSpline.Curve()

        # Set degree
        curve.degree = 3

        # Set control points
        curve.ctrlpts = [[-1, 0, 0], [-1, -1, -.3], [0, 0, 0], [1, .5, 0]]

        # Set knot vector
        curve.knotvector = [0, 0, 0, 0, 1, 1, 1, 1]

        # Set evaluation delta (controls the number of curve points)
        curve.delta = 0.01

        # Get curve points (the curve will be automatically evaluated)
        curve_points = curve.evalpts
        self.vertices=np.array(curve_points,dtype="float32")
        self.program = QOpenGLShaderProgram()
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex, ":CommonShader/vertices.vert")
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, ":CommonShader/vertices.frag")
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
        self.program.setAttributeBuffer(0, GL_FLOAT, 0, 3, 3 * self.vertices.itemsize)
        buffer = self.loadTexture(":texture/texture.png")
        self.textureID = QOpenGLTexture(buffer.mirrored(), QOpenGLTexture.GenerateMipMaps)
        self.textureID.setMinificationFilter(QOpenGLTexture.LinearMipMapLinear)
        self.textureID.setMagnificationFilter(QOpenGLTexture.Linear)

        self.vbo.release()
        self.vao.release()
        self.program.release()
        #stencil buffer
        self.stencilProgram = QOpenGLShaderProgram()
        self.stencilProgram.addShaderFromSourceFile(QOpenGLShader.Vertex, ":CommonShader/vertices.vert")
        self.stencilProgram.addShaderFromSourceFile(QOpenGLShader.Fragment, ":CommonShader/solid_color.frag")
        self.stencilProgram.link()
        self.vao.bind()
        self.vbo.bind()
        self.stencilProgram.enableAttributeArray(0)
        self.stencilProgram.setAttributeBuffer(0, GL_FLOAT, 0, 3, 3 * self.vertices.itemsize)
        self.vbo.release()
        self.vao.release()
        self.stencilProgram.release()

        size = np.random.randint(-1, 1, size=(1, 3))
        self.transform = [QVector3D(i[0], i[1], i[2]) for i in size]
    def paintGL(self) -> None:
        #Transformation
        Projection = self.setupProjectionMatrix()
        View = self.setupViewMatrix()
        #On screen rendering
        glClearColor(0, 0, 0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        glViewport(0, 0, self.width(), self.height())
        self.program.bind()
        self.vbo.bind()
        self.vao.bind()
        # 1st. render pass, draw objects as normal, writing to the stencil buffer
        glStencilFunc(GL_ALWAYS, 1, 0xFF)
        glStencilMask(0xFF)
        for transform in self.transform:
            Model = QMatrix4x4()
            Model.translate(transform)
            Model.rotate(30,transform)
            MVP = Projection * View * Model
            self.program.setUniformValue("gWVP", MVP)
            self.textureID.bind()
            self.program.setUniformValue("texture1", 0)
            glDrawArrays(GL_LINE_STRIP, 0, self.vertices.shape[0] // 3)
        # 2nd. render pass: now draw slightly scaled versions of the objects, this time disabling stencil writing.
        #Because the stencil buffer is now filled with several 1s. The parts of the buffer that are 1 are not drawn, thus only drawing
        #the objects' size differences, making it look like borders.
        glStencilFunc(GL_NOTEQUAL, 1, 0xFF)
        glStencilMask(0x00)
        glDisable(GL_DEPTH_TEST)
        scale_factor=1.1
        self.stencilProgram.bind()
        for transform in self.transform:
            Model = QMatrix4x4()
            Model.translate(transform)
            Model.rotate(30, transform)
            Model.scale(scale_factor)
            MVP = Projection * View * Model
            self.program.setUniformValue("gWVP", MVP)
            glDrawArrays(GL_LINE_STRIP, 0, self.vertices.shape[0] // 3)
        #calculate frame rate
        self.calculateFPS()

        self.vbo.release()
        self.vao.release()
        self.program.release()
        self.stencilProgram.release()
        glStencilMask(0xFF)
        glEnable(GL_DEPTH_TEST)
        # After painter start, opengl state will be changed to some state
        painter = QPainter(self)
        self.drawInstructions(painter)
        painter.end()
        #Restore to previous OpenGL state
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glEnable(GL_STENCIL_TEST)
        glStencilFunc(GL_NOTEQUAL, 1, 0xFF)
        glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
        # -----------------------------
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


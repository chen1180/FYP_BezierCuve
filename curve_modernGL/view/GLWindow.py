from builtins import super
from OpenGL.GL import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from model.trackBall import Trackball
import sys
from model.planes import Quads
from model.bezier import *
from model.axis import Axis
from model.nurbPatch import *
from model.pickingTexture import *
from model.pickingEffect import *
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
        self.scene=[]
        self.camera=Trackball(QVector3D(0,0,-5),QVector3D(0,0,0),QVector3D(0,1,0))
        #default plane
        self.viewPortState=self.VIEWPORT_PERSPECTIVE
        self.viewPlane=self.VIEWPORT_XY_PLANE
        self.quads=Quads(10,1)
        self.axis=Axis(0.5)
        #picking
        self.pickingTexture=PickingTexture()
        self.pickingEffect=PickingEffect()
    def initializeGL(self) -> None:
        QOpenGLWidget.initializeGL(self)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0, 0, 0, 1.0)
        self.pickingTexture.Init(self.width(),self.height())
        self.pickingEffect.Init()
        try:
            self.quads.initialize()
            self.axis.initialize()
        except Exception as e:
            print(e)
    def pickingPhase(self):
        Projection = self.setupProjectionMatrix()
        View = self.setupViewMatrix()
        Model = QMatrix4x4()
        MVP = Projection * View * Model
        print(glGetIntegerv(GL_DRAW_FRAMEBUFFER_BINDING))
        originalFBO=glGetIntegerv(GL_FRAMEBUFFER_BINDING)

        self.pickingTexture.EnableWriting()
        print(glGetIntegerv(GL_DRAW_FRAMEBUFFER_BINDING))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.pickingEffect.Enable()
        if self.scene:
            for i in range(len(self.scene)):
                self.pickingEffect.SetObjectIndex(i)
                self.pickingEffect.SetMVP(MVP)
                self.pickingEffect.DrawStartCB(i)
        self.pickingTexture.DisableWriting()

    def renderingPhase(self):
        glViewport(0,0,self.width(),self.height())
        glClearColor(0,0,0,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Projection = self.setupProjectionMatrix()
        View = self.setupViewMatrix()
        Model = QMatrix4x4()
        MVP = Projection * View * Model
        # glViewport(self.width() - 100, self.height() - 100, 100, 100);
        # try:
        #     axisProjection=QMatrix4x4()
        #     axisProjection.ortho(-1, 1, -1 ,1 , 0.1, 100)
        #     axisView =self.setupViewMatrix(enableCameraPan=False)
        #     self.axis.setupMatrix(axisView, Model, axisProjection)
        #     self.axis.render()
        # except Exception as e:
        #     print(e)
        # glViewport(0, 0, self.width(), self.height());
        try:
            self.quads.setupMatrix(View, Model, Projection)
            self.quads.render()
            if self.scene:
                for item in self.scene:
                    item.setupMatrix(View, Model, Projection)
                    item.setupCamera(self.camera.cameraPos)
                    item.initialize()
                    item.render()
        except Exception as e:
            print(e)
    def paintGL(self) -> None:
        self.makeCurrent()
        self.pickingPhase()
        # fbo=QOpenGLFramebufferObject(self.width(),self.height(),QOpenGLFramebufferObject.Depth)
        # fbo.bind()
        # fbo.addColorAttachment(self.width(),self.height(),1)
        # fbo.release()
        self.renderingPhase()

        self.update()
    def resizeGL(self, w: int, h: int) -> None:
        side = min(w, h)
        glViewport((w - h) // 2, (w - h) // 2, side,side)
    # -----------------------------OPENGL window 2D overpaint -----------------------------------#
    # def paintEvent(self, e: QPaintEvent) -> None:
    #     super(OpenGLWindow, self).paintEvent(e)
    #     self.makeCurrent()
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.Antialiasing)
    #     self.drawInstructions(painter)
    #     painter.end()
    #     self.doneCurrent()

    def drawInstructions(self, painter):
        if self.viewPortState==self.VIEWPORT_PERSPECTIVE:
            text = "Perspective"
        else:
            text = "Ortho"
        metrics = QFontMetrics(self.font())
        border = max(4, metrics.leading())

        rect = metrics.boundingRect(0, 0, self.width() - 2*border,
                                    int(self.height()*0.125), Qt.AlignCenter | Qt.TextWordWrap,
                                    text)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.fillRect(QRect(0, 0, self.width(), rect.height() + 2*border),
                         QColor(0, 0, 0, 127))
        painter.setPen(Qt.white)
        painter.fillRect(QRect(0, 0, self.width(), rect.height() + 2*border),
                         QColor(0, 0, 0, 127))
        painter.drawText((self.width() - rect.width())/2, border, rect.width(),
                         rect.height(), Qt.AlignCenter | Qt.TextWordWrap, text)
        #Draw operation instruction on the scrren
        font=painter.font()
        font.setPointSize(12)
        painter.setFont(font)
        instruction="Rotation: Control+Left Mouse\nPan: Right Mouse\nZoom: Mouse scroller"
        rect =QRect(10, 10,self.width()/4,self.height()/4)
        painter.drawText(rect, Qt.AlignLeft | Qt.TextWordWrap, instruction)
        #Draw axis on the screen
        # origin=QPointF(self.width()-100,self.height()/16)
        # x_axis=QLineF(origin,origin+QPointF(50,0))
        # x_axis.setAngle(60)
        # y_axis=QLineF(origin,origin+QPointF(0,-50))
        # z_axis=QLineF(origin,origin)
        # painter.setPen(QPen(Qt.red))
        # painter.drawLine(x_axis)
        # painter.setPen(QPen(Qt.green))
        # painter.drawLine(y_axis)
        # painter.setPen(QPen(Qt.blue))
        # painter.drawLine(z_axis)

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
    def changeViewPlane(self,plane:int):
        self.viewPlane=plane
        self.camera.resetCamera()
        self.update()
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
        if (a0.buttons()&Qt.LeftButton):
            pos=self.pixelPosToViewPos(a0.windowPos())
            print(a0.windowPos().x(),a0.windowPos().y())
            pixel=self.pickingTexture.ReadPixel(a0.windowPos().x(),a0.windowPos().y())
            print(pixel[0])
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
    format.setVersion(4,4)
    format.setProfile(QSurfaceFormat.CoreProfile)
    QSurfaceFormat.setDefaultFormat(format) #it must be called before OpenGL window, set OPENGL format globally
    window = OpenGLWindow() #Opengl window creation
    window.show()
    application.exec_()


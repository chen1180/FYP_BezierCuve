from builtins import super
from OpenGL.GL import *
from PyQt5.QtCore import pyqtSignal,QPointF,Qt,qDebug
from PyQt5.QtWidgets import QApplication,QOpenGLWidget
from PyQt5.QtGui import (QSurfaceFormat,QOpenGLContext,QOpenGLShaderProgram,
                         QOpenGLShader,QOpenGLVersionProfile,QAbstractOpenGLFunctions,QVector3D,QMouseEvent,QWheelEvent,QKeyEvent,QMatrix4x4,QQuaternion)
from curve_modernGL.model.trackBall import Trackball
import sys
from curve_modernGL.model.planes import Quads

class OpenGLWindow(QOpenGLWidget):
    OPENGL_NEED_UPDATE=pyqtSignal(bool)
    def __init__(self,parent=None):
        super(OpenGLWindow, self).__init__(parent)
        format = QSurfaceFormat()
        format.setDepthBufferSize(24)
        format.setStencilBufferSize(8)
        format.setVersion(4, 1)
        format.setProfile(QSurfaceFormat.CoreProfile)
        self.setFormat(format)
        self.scene=[]
        self.camera=Trackball(QVector3D(0,1,-5),QVector3D(0,0,0),QVector3D(0,1,0))
        self.quads=Quads(10,1)
    def initializeGL(self) -> None:
        QOpenGLWidget.initializeGL(self)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        try:
            self.quads.initialize()
        except Exception as e:
            print(e)
    def paintGL(self) -> None:
        glClearColor(0, 0, 0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        # self.setDisplayViewPort(0,0,self.width()//2,self.height()//2,QQuaternion())
        # self.setDisplayViewPort(self.width() // 2,0, self.width() // 2, self.height() //2, QQuaternion().fromAxisAndAngle(QVector3D(0,1,0),-90))
        # self.setDisplayViewPort(0,self.height()//2, self.width() // 2, self.height() // 2, QQuaternion().fromAxisAndAngle(QVector3D(1,0,0),-90))
        # glViewport(self.width()//2,self.height()//2, self.width() // 2, self.height() // 2)
        Projection=QMatrix4x4()
        Projection.perspective(45.0,self.width()/self.height(),0.1,100)
        View=QMatrix4x4()
        View.lookAt(self.camera.cameraPos, self.camera.targetPos, self.camera.cameraUp)
        Model=QMatrix4x4()
        MVP=Projection*View*Model
        try:
            self.quads.setupMatrix(View, Model, Projection)
            self.quads.render()
        except Exception as e:
            print(e)
        try:
            if self.scene:
                for item in self.scene:
                    item.setupMatrix(View, Model, Projection)
                    item.setupCamera(self.camera.cameraPos)
                    item.initialize()
                    item.render()
        except Exception as e:
            print(e)
        self.update()
    def setDisplayViewPort(self,x,y,width,height,rotation):
        glViewport(x,y,width,height)
        Projection = QMatrix4x4()
        Projection.ortho(-1,1,-1,1,-1,1)
        View = QMatrix4x4()
        View.rotate(rotation)
        Model = QMatrix4x4()
        MVP = Projection * View * Model
        try:
            self.quads.setupMatrix(View, Model, Projection)
            self.quads.render()
        except Exception as e:
            print(e)
        try:
            if self.scene:
                for item in self.scene:
                    item.setupMatrix(View, Model, Projection)
                    item.setupCamera(self.camera.cameraPos)
                    item.initialize()
                    item.render()
        except Exception as e:
            print(e)
    def addToScene(self, scene):
        self.scene=list(scene)
        self.update()
    def pixelPosToViewPos(self,p:QPointF):
        return QPointF(2*p.x()/self.width()-1.0,1.0-2.0*p.y()/self.height())
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        super(OpenGLWindow, self).mousePressEvent(a0)
        if a0.isAccepted():
            return
        if a0.buttons()&Qt.MiddleButton:
            self.camera.pushMiddleButton(self.pixelPosToViewPos(a0.windowPos()))
            a0.accept()
        if a0.buttons()&Qt.RightButton:
            self.camera.pushRightButton(self.pixelPosToViewPos(a0.windowPos()))
            a0.accept()
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        super(OpenGLWindow, self).mouseMoveEvent(a0)
        if a0.isAccepted():
            return
        if a0.buttons() & Qt.MiddleButton:
            self.camera.moveMiddleButton(self.pixelPosToViewPos(a0.windowPos()))
            a0.accept()
        if a0.buttons()&Qt.RightButton:
            self.camera.moveRightButton(self.pixelPosToViewPos(a0.windowPos()))
            a0.accept()
        self.update()
    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        super(OpenGLWindow, self).mouseReleaseEvent(a0)
        if a0.isAccepted():
            return
        if a0.buttons() & Qt.MiddleButton:
            self.camera.releaseMiddleButton(self.pixelPosToViewPos(a0.windowPos()))
            a0.accept()
        if a0.buttons()&Qt.RightButton:
            self.camera.releaseRightButton()
            a0.accept()
    def wheelEvent(self, a0: QWheelEvent) -> None:
        super(OpenGLWindow, self).wheelEvent(a0)
        if not a0.isAccepted():
            self.camera.moveMiddleScroller(a0.angleDelta().y())
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


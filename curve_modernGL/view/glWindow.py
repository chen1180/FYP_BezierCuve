from builtins import super

from OpenGL.GL import *
from PyQt5.QtCore import pyqtSignal,QPointF,Qt,qDebug
from PyQt5.QtWidgets import QApplication,QOpenGLWidget
from PyQt5.QtGui import (QSurfaceFormat,QOpenGLContext,QOpenGLShaderProgram,
QOpenGLShader,QOpenGLVersionProfile,QAbstractOpenGLFunctions,QVector3D,QMouseEvent,QWheelEvent,QKeyEvent,QMatrix4x4)
from curve_modernGL.model.trackBall import Trackball
import sys
from curve_modernGL.model.bezier import Bezier
from curve_modernGL.model.triangle import Triangle
class openGLWindow(QOpenGLWidget):
    OPENGL_NEED_UPDATE=pyqtSignal(bool)
    def __init__(self,parent=None):
        super(openGLWindow, self).__init__(parent)
        format = QSurfaceFormat()
        format.setDepthBufferSize(24)
        format.setStencilBufferSize(8)
        format.setVersion(4, 1)
        format.setProfile(QSurfaceFormat.CoreProfile)
        self.setFormat(format)
        self.scene=[]
        self.camera=Trackball(QVector3D(1,1,-1),QVector3D(0,0,0),QVector3D(0,1,0))
        # self.triangle=Triangle(None, "Beizer", [QVector3D(-0.5,0,0),QVector3D(0.5,0,0),QVector3D(0,0.5,0),QVector3D(1,0.5,0)])
        self.transform=QMatrix4x4()
    def getFileContent(self,filename):
        return open(filename,"r").read()
    def initializeGL(self) -> None:
        QOpenGLWidget.initializeGL(self)
        # self.triangle.create()
    def paintGL(self) -> None:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Projection=QMatrix4x4()
        Projection.perspective(45.0,self.width()/self.height(),0.1,100)
        View=QMatrix4x4()
        # View.lookAt(self.camera.cameraPos, self.camera.center, self.camera.WorldUp)
        View.translate(QVector3D(0,0,-1)*self.camera.zoomFactor)
        View.rotate(self.camera.m_rotation)
        Model=QMatrix4x4()
        MVP=Projection*View*Model
        # self.triangle.program.bind()
        # self.location=self.triangle.program.uniformLocation('MVP')
        # self.triangle.program.setUniformValue(self.location, MVP)
        # self.triangle.render()
        try:
            if self.scene:
                for item in self.scene:
                    item.setupCameraMatrix(View,Model,Projection)
                    item.create()
                    item.render()
        except Exception as e:
            print(e)
        self.update()
    def drawScene(self,scene):
        self.scene=list(scene)
        self.update()
    def pixelPosToViewPos(self,p:QPointF):
        return QPointF(2*p.x()/self.width()-1.0,1.0-2.0*p.y()/self.height())
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        super(openGLWindow, self).mousePressEvent(a0)
        if a0.isAccepted():
            return
        if a0.buttons()&Qt.MiddleButton:
            self.camera.pushMiddleButton(self.pixelPosToViewPos(a0.windowPos()))
            a0.accept()
        if a0.buttons()&Qt.RightButton:
            self.camera.pushRightButton(self.pixelPosToViewPos(a0.windowPos()))
            a0.accept()
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        super(openGLWindow, self).mouseMoveEvent(a0)
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
        super(openGLWindow, self).mouseReleaseEvent(a0)
        if a0.isAccepted():
            return
        if a0.buttons() & Qt.MiddleButton:
            self.camera.releaseMiddleButton()
            a0.accept()
        if a0.buttons()&Qt.RightButton:
            self.camera.releaseRightButton()
            a0.accept()
    def keyPressEvent(self, a0: QKeyEvent) -> None:
        super(openGLWindow, self).keyPressEvent(a0)
        if a0.isAccepted():
            return
        if a0.key()==Qt.Key_Up:
            self.transform.translate(QVector3D(0,0.1,0))
            print("up")
            a0.accept()
        if a0.key()==Qt.Key_Down:
            self.transform.translate(QVector3D(0,-0.1,0))
            print("down")
            a0.accept()
    def wheelEvent(self, a0: QWheelEvent) -> None:
        super(openGLWindow, self).wheelEvent(a0)
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
    window = openGLWindow() #Opengl window creation
    window.show()
    application.exec_()


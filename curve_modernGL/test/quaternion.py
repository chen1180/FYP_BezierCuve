from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtDataVisualization import Q3DCamera
import sys
from OpenGL.GL import *
from curve_modernGL.model.triangle import Triangle
import math
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
        self.triangle=Triangle(None, "Beizer", [QVector3D(-0.5,0,0),QVector3D(0.5,0,0),QVector3D(0,0.5,0),QVector3D(0.5,0.5,0)])
        self.cameraPos=QVector3D(0,0,-1)
        self.cameraEye=QVector3D(0,0,0)
        self.worldUp=QVector3D(0,1,0)
        self.m_rotationTrigger = False
        self.m_panningTrigger=False
        self.m_lastPos = QPointF()
        self.m_rotation=QQuaternion()
        self.radius=1.0
    def initializeGL(self) -> None:
        QOpenGLWidget.initializeGL(self)
        self.triangle.initialize()
        self.degree=0
    def paintGL(self) -> None:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Projection=QMatrix4x4()
        Projection.perspective(45.0,self.width()/self.height(),0.1,100)
        View=QMatrix4x4()
        # View.lookAt(self.cameraPos,self.cameraEye,self.worldUp)
        View.translate(self.cameraPos*self.radius)
        View.rotate(self.m_rotation)
        # View.translate(self.cameraEye)
        Model=QMatrix4x4()
        Model.translate(self.cameraEye)
        MVP=Projection*View*Model
        self.triangle.program.bind()
        self.location=self.triangle.program.uniformLocation('MVP')
        self.triangle.program.setUniformValue(self.location, MVP)
        self.triangle.render()
        self.update()
    def pixelPosToViewPos(self,p:QPointF):
        return QPointF(2*p.x()/self.width()-1.0,1.0-2.0*p.y()/self.height())
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        super(openGLWindow, self).mousePressEvent(a0)
        if a0.isAccepted():
            return
        if a0.buttons()&Qt.MiddleButton:
            self.pushMiddleButton(self.pixelPosToViewPos(a0.windowPos()))
            a0.accept()
        if a0.buttons()&Qt.RightButton:
            print("right button click")
            self.pushRightButton(self.pixelPosToViewPos(a0.windowPos()))
            a0.accept()
        self.update()
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        super(openGLWindow, self).mouseMoveEvent(a0)
        if a0.isAccepted():
            return
        if a0.buttons()&Qt.MiddleButton:
            self.moveMiddleButton(self.pixelPosToViewPos(a0.windowPos()))
            a0.accept()
        if a0.buttons()&Qt.RightButton:
            print("right button move")
            self.moveRightButton(self.pixelPosToViewPos(a0.windowPos()))
            a0.accept()
        self.update()
    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        super(openGLWindow, self).mouseReleaseEvent(a0)
        if a0.isAccepted():
            return
        if a0.button()==Qt.MiddleButton:
            self.releaseMiddleButton()
            a0.accept()
        if a0.button()==Qt.RightButton:
            self.releaseRightButton()
            a0.accept()
        self.update()
    def wheelEvent(self, a0: QWheelEvent) -> None:
        super(openGLWindow, self).wheelEvent(a0)
        if a0.angleDelta().y()>0:
            self.radius+=0.2
        else:
            self.radius-=0.2
        if self.radius<=1:
            self.radius=1
        self.update()

    def pushMiddleButton(self,p:QPointF):
        self.m_rotationTrigger=True
        self.m_lastPos=p
    def moveMiddleButton(self,p:QPointF):
        if self.m_rotationTrigger==False:
            return
        lastPos3D=QVector3D(self.m_lastPos.x(),self.m_lastPos.y(),0)
        sqrZ=1-QVector3D.dotProduct(lastPos3D,lastPos3D)
        if sqrZ>0:
            lastPos3D.setZ(math.sqrt(sqrZ))
        else:
            lastPos3D.normalize()
        currentPos3D = QVector3D(p.x(), p.y(), 0)
        sqrZ = 1 - QVector3D.dotProduct(currentPos3D, currentPos3D)
        if sqrZ > 0:
            currentPos3D.setZ(math.sqrt(sqrZ))
        else:
            currentPos3D.normalize()
        axis=QVector3D.crossProduct(lastPos3D,currentPos3D)
        angle=math.degrees(math.asin(axis.length()))
        print(angle)
        axis.normalize()
        self.m_rotation=QQuaternion.fromAxisAndAngle(axis,angle)*self.m_rotation
        # self.cameraPos = self.m_rotation.rotatedVector(self.cameraPos - self.cameraEye) + self.cameraEye
        self.m_lastPos=p
    def releaseMiddleButton(self):
        print("release")
        self.m_rotationTrigger=False
        # self.cameraPos = self.m_rotation.rotatedVector(self.cameraPos - self.cameraEye) + self.cameraEye
    #camera panning
    def pushRightButton(self,p:QPointF):
        self.m_panningTrigger = True
        self.m_lastPos = p
    def moveRightButton(self,p:QPointF):
        if self.m_panningTrigger==False:
            return
        dx = (p - self.m_lastPos).x()
        dy = (self.m_lastPos-p).y()
        look = self.m_rotation.rotatedVector(self.cameraPos) -self.cameraEye
        print(self.m_rotation,look)
        right = QVector3D.crossProduct(look, self.worldUp)
        up = QVector3D.crossProduct(look, right)
        # self.cameraPos+=transVec
        self.cameraEye+= (right * dx + up * dy)
        self.m_lastPos = p
    def releaseRightButton(self):
        self.m_panningTrigger=False
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
if __name__ == '__main__':
    p1=QVector3D(1,0,0)
    rotation=QQuaternion.fromAxisAndAngle(QVector3D(0,1,0),90)
    #rotate p1 90 degree with respect to y axis
    print("test1",rotation.rotatedVector(p1))
    #rotation quaternion multiply it's own rotation
    new_rotation=QQuaternion.fromAxisAndAngle(QVector3D(0,1,0),-90)*rotation
    print("test2",rotation)
    print("test2",new_rotation)
    #rotate camera position to new position with quaternion
    cameraPos=QVector3D(0,0,1)
    cameraPos=rotation.rotatedVector(cameraPos)
    print("test3",cameraPos)
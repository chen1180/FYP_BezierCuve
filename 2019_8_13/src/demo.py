from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.QtOpenGL import *
import numpy as np
import tmp
from geometry import point
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()
    def setupUi(self):
        self.ui=tmp.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.openGLWidget.close()
        self.glWidget=glWidget(self)
        self.ui.openGLWidget.close()
        self.ui.horizontalLayout_2.replaceWidget(self.ui.openGLWidget,self.glWidget)
class glWidget(QGLWidget):
    xRotationChanged = QtCore.pyqtSignal(int)
    yRotationChanged = QtCore.pyqtSignal(int)
    zRotationChanged = QtCore.pyqtSignal(int)
    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.status=0
        self.control_points = [point(-0.25, 0, 0), point(0, 0.25, 0), point(0.25, 0.25, 0), point(0.5, -0.5, 0)]
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.xTrans=0
        self.yTrans=0
        self.zTrans=0
        self.lastPos = QtCore.QPoint()

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.update()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.update()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.update()
    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.xTrans+=dx*0.01
            self.yTrans += dy*0.01
        self.lastPos = event.pos()
        self.update()
    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle
    def initializeGL(self):
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        #define the opengl window unit
        glViewport(0,0, self.width(), self.height())
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #gluOrtho2D(0,self.width(),0,self.height())

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        glTranslated(self.xTrans,self.xTrans,0.0)
        lx = 1
        ly = 1
        # x axis
        glMatrixMode(GL_MODELVIEW)
        glColor3f(1, 0, 0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(10, 0, 0)
        glEnd()
        # y axis
        glColor3f(0, 1, 0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 1, 0)
        glEnd()
        # z axis
        glColor3f(0, 0, 1)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1)
        glEnd()
        # x-y plane
        glColor3f(0.1, 0.1, 0.1)
        glBegin(GL_QUADS)
        glVertex3f(-lx / 2, 0, -ly / 2)
        glVertex3f(lx / 2, 0, -ly / 2)
        glVertex3f(lx / 2, 0, ly / 2)
        glVertex3f(-lx / 2, 0, ly / 2)
        glEnd()
        glFlush()
    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        glViewport((width - side) // 2, (height - side) // 2, side, side)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #glFrustum(-1.0, +1.0, -1.0, 1.0, -0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -1.0)
if __name__ == '__main__':
    app = QtWidgets.QApplication(['Yo'])
    window = MainWindow()
    window.show()
    app.exec_()
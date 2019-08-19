from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PyQt5.QtCore import QSize, Qt
from math import *
from PyQt5 import QtCore, QtGui, QtWidgets


class MyGL(QtWidgets.QOpenGLWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.ratio = 1
        self.width, self.height = 1, 1

        self.coord = [
            [0,0,0], [1,0,0], [2,0,0],
            [0,1,0], [1,1,0], [2,1,0],
            [0,2,0], [1,2,0], [2,2,0]
        ]

        self.radialD, self.xzAngle, self.xAngle = 30, 0, 90

        self.xCam = self.radialD*cos(self.xzAngle*pi/180)*cos(self.xAngle*pi/180)
        self.yCam = self.radialD*sin(self.xzAngle*pi/180)
        self.zCam = self.radialD*cos(self.xzAngle*pi/180)*sin(self.xAngle*pi/180)

    def initializeGL(self):
        self.setFocusPolicy(Qt.StrongFocus)
        glutInit()



    def resizeGL(self, w, h):
        if h==0:
            h=1
        self.ratio =  w * 1.0 / h
        self.width, self.height = w, h
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, w, h)
        gluPerspective(45.0, self.ratio, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # glClearDepth(1)
        glLoadIdentity()
        glClearColor(1.0,1.0,1.0,1.0)
        self.xCam = self.radialD*cos(self.xzAngle*pi/180)*cos(self.xAngle*pi/180)
        self.yCam = self.radialD*sin(self.xzAngle*pi/180)
        self.zCam = self.radialD*cos(self.xzAngle*pi/180)*sin(self.xAngle*pi/180)
        gluLookAt(self.xCam,  self.yCam, self.zCam, 0, 0,  0,   0.0, 1.0,  0.0)
        self.draw(GL_RENDER)

    def draw(self, mode):

        i=1

        for p in self.coord:

            glColor3f(0,0,0)
            glPushMatrix()
            glTranslatef(p[0], p[1], p[2])

            if mode == GL_SELECT:
                glLoadName(i)
                i+=1

            glutSolidSphere(0.1, 30, 30)
            glPopMatrix()

    def mousePressEvent(self, event):

        self.makeCurrent()

        viewport = glGetIntegerv(GL_VIEWPORT)

        selectBuf = glSelectBuffer(100)
        glRenderMode(GL_SELECT)

        glInitNames()
        glPushName(-1)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()

        gluPickMatrix( event.x(),  (viewport[3] - event.y()), 50.0, 50.0, viewport)

        gluPerspective(45.0, self.ratio, 0.1, 100.0)
        self.draw(GL_SELECT)
        glPopMatrix()

        glFlush()

        hits = glRenderMode(GL_RENDER)
        for x in hits:
            print(x.names)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.doneCurrent()

        self.update()

    def mouseReleaseEvent(self, event):

        self.update()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Down:
            self.xzAngle -= 1
            if self.xzAngle < 0:
                self.xzAngle = 359
        if event.key() == Qt.Key_Up:
            self.xzAngle += 1
            if self.xzAngle > 360:
                self.xzAngle = 1
        if event.key() == Qt.Key_Left:
            self.xAngle += 1
            if self.xAngle > 360:
                self.xAngle = 1
        if event.key() == Qt.Key_Right:
            self.xAngle -= 1
            if self.xAngle < 0:
                self.xAngle = 359
        if event.key() == Qt.Key_Plus:
            self.radialD -= 0.3
        if event.key() == Qt.Key_Plus:
            self.radialD += 0.3

        self.update()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.openGLWidget = MyGL(self.centralWidget)
        self.openGLWidget.setObjectName("openGLWidget")
        self.verticalLayout.addWidget(self.openGLWidget)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
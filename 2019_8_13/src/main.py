from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.QtOpenGL import *
import numpy as np
import tmp
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
        self.ui.drawBtn.clicked.connect(lambda state,x=1:self.glWidget.changeStatus(x))
        self.ui.pushButton.clicked.connect(lambda state,x=2:self.glWidget.changeStatus(x))
class glWidget(QGLWidget):

    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.status=0
        self.control_points = [(-0.25, 0, 0), (0, 0.25, 0), (0.25, 0.25, 0), (0.5, -0.5, 0)]
    def initializeGL(self):
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #gluPerspective(45.0,1.33,0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
    def paintGL(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        #glTranslatef(-2.5, 0.5, -6.0)
        glPolygonMode(GL_FRONT, GL_FILL)
        if self.status==1:
            self.drawCurve()
        elif self.status==2:
            self.splitCurve()
        else:
            self.update()
        glFlush()
    def changeStatus(self,newStatus=0):
        self.status=newStatus
        self.update()
    def drawCurve(self):
        glColor3f(1.0, 1.5, 0.0)
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for i in self.control_points:
            glVertex3f(i[0], i[1], i[2])
        glEnd()
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINE_STRIP)
        for t in np.linspace(0, 1, 100):
            Px = self.decasteljau(self.control_points[0][0], self.control_points[1][0], self.control_points[2][0],
                                  self.control_points[3][0], t)
            Py = self.decasteljau(self.control_points[0][1], self.control_points[1][1], self.control_points[2][1],
                                  self.control_points[3][1], t)
            Pz = self.decasteljau(self.control_points[0][2], self.control_points[1][2], self.control_points[2][2],
                                  self.control_points[3][2], t)
            glVertex3f(Px, Py, Pz)
        glEnd()
    def decasteljau(self,p1,p2,p3,p4,t):
        p12=(1 - t) * p1 + t * p2
        p23 = (1 - t) * p2 + t * p3
        p34 = (1 - t) * p3 + t * p4
        p1223 = (1 - t) * p12 + t * p23
        p2334 = (1 - t) * p23 + t * p34
        return (1-t)*p1223+t*p2334
    def decasteljau_split(self,p1,p2,p3,p4,t):
        p12 = (1 - t) * p1 + t * p2
        p23 = (1 - t) * p2 + t * p3
        p34 = (1 - t) * p3 + t * p4
        p1223 = (1 - t) * p12 + t * p23
        p2334 = (1 - t) * p23 + t * p34
        p=(1-t)*p1223+t*p2334
        return [p1,p12,p1223,p],[p,p2334,p34,p4]
    def splitCurve(self):
        t=0.5
        curve1_x, curve2_x = self.decasteljau_split(self.control_points[0][0],
                                                self.control_points[1][0],
                                                self.control_points[2][0],
                                                self.control_points[3][0],
                                                t)
        curve1_y, curve2_y = self.decasteljau_split(self.control_points[0][1],
                                                    self.control_points[1][1],
                                                    self.control_points[2][1],
                                                    self.control_points[3][1],
                                                    t)
        curve1_z, curve2_z = self.decasteljau_split(self.control_points[0][2],
                                                    self.control_points[1][2],
                                                    self.control_points[2][2],
                                                    self.control_points[3][2],
                                                    t)
        glColor3f(0.0, 1.0, 0.0)
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for i in range(0,4):
            glVertex3f(curve1_x[i],curve1_y[i],curve1_z[i])
        glEnd()
        glColor3f(0.0, 0.0, 1.0)
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for i in range(0, 4):
            glVertex3f(curve2_x[i], curve2_y[i], curve2_z[i])
        glEnd()
        glFlush()


if __name__ == '__main__':
    app = QtWidgets.QApplication(['Yo'])
    window = MainWindow()
    window.show()
    app.exec_()
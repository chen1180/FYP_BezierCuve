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
        self.ui.drawBtn.clicked.connect(lambda state,x=1:self.glWidget.changeStatus(x))
        self.ui.splitBtn.clicked.connect(lambda state,x=2:self.glWidget.changeStatus(x))
        self.ui.drawSurfaceBtn.clicked.connect(lambda state,x=3:self.glWidget.changeStatus(x))
class glWidget(QGLWidget):

    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.status=0
        self.control_points = [point(-0.25, 0, 0), point(0, 0.25, 0), point(0.25, 0.25, 0), point(0.5, -0.5, 0)]

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
            self.drawCurve(self.control_points)
        elif self.status==2:
            self.splitCurve(self.control_points)
        elif self.status==3:
            self.drawBeizerSurface()
        else:
            self.update()
        glFlush()
    def changeStatus(self,newStatus=0):
        self.status=newStatus
        self.update()
    def drawCurve(self,control_points,c_color=(1,1,1)):
        glColor3f(c_color[0], c_color[1], c_color[2])
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for p in control_points:
            p.glVertex3()
        glEnd()
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINE_STRIP)
        for t in np.linspace(0, 1, 10):
            p = self.decasteljau(control_points[0], control_points[1], control_points[2],control_points[3], t)
            p.glVertex3()
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
    def splitCurve(self,control_points,t=0.2,c1_color=(1,0,0),c2_color=(0,0,1)):
        curve1, curve2 = self.decasteljau_split(control_points[0],
                                                control_points[1],
                                                control_points[2],
                                                control_points[3],
                                                t)
        glColor3f(c1_color[0], c1_color[1], c1_color[2])
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for point in curve1:
            point.glVertex3()
        glEnd()
        glColor3f(c2_color[0], c2_color[1], c2_color[2])
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for point in curve2:
            point.glVertex3()
        glEnd()
        self.drawCurve(curve1, c_color=c1_color)
        self.drawCurve(curve2, c_color=c2_color)
        glFlush()

    def drawBeizerSurface(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glRotatef(45.0,-10.0,1.0,-10.0)
        control_points=[[[  -0.25, 0.0, 0.0],[ 0, 0, 0.0],[  0.25, -0.2, 0.0],[  0.5, 0.2, 0.0]],
[[  -0.5, -0.5, 0.0],[ 0, -0.9, 0.0],[  0.25, -0.2, 0.0],[  0.5, -0.6, 0.0]]]
        glMap2f(GL_MAP2_VERTEX_3,0,1,0,1,control_points)
        glEnable(GL_MAP2_VERTEX_3)
        glMapGrid2f(10,0,1,10,0,1)
        glEvalMesh2(GL_LINE,0,10,0,10)
        glPointSize(5)
        glColor3f(1, 0, 0)
        glBegin(GL_POINTS)
        for line in control_points:
            for point in line:
                glVertex3f(point[0], point[1], point[2])
        glEnd()
        glFlush()
        glPopMatrix()

        '''
    def drawBeizerSurface(self):
        glClear(GL_COLOR_BUFFER_BIT)
        control_points = [(-0.25, 0, 0), (0, 0.25, 0),(0.25, 0.25, 0), (0.5, -0.5, 0)]
        glMap1f(GL_MAP1_VERTEX_3, 0, 1, control_points)
        glEnable(GL_MAP1_VERTEX_3)
        glColor3f(1, 0, 0)
        glBegin(GL_POINTS)
        for i in range(31):
            glEvalCoord1f(float(i) / 31)
        glEnd()
        glPointSize(5)
        glColor3f(1, 0, 0)
        glBegin(GL_POINTS)
        for point in control_points:
            glVertex3f(point[0],point[1],point[2])
        glEnd()
        glFlush()
        '''


if __name__ == '__main__':
    app = QtWidgets.QApplication(['Yo'])
    window = MainWindow()
    window.show()
    app.exec_()
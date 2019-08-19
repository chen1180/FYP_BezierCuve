from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.QtOpenGL import *
import numpy as np
import tmp
from geometry import point
import sys
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
        self.ui.clearBtn.clicked.connect(lambda state, x=0: self.glWidget.changeStatus(x))
        self.ui.drawBtn.clicked.connect(lambda state,x=1:self.glWidget.changeStatus(x))
        self.ui.splitBtn.clicked.connect(lambda state,x=2:self.glWidget.changeStatus(x))
        self.ui.drawSurfaceBtn.clicked.connect(lambda state,x=3:self.glWidget.changeStatus(x))
        self.ui.pushButton.clicked.connect(lambda state,x=4:self.glWidget.changeStatus(x))
        self.ui.horizontalSlider.valueChanged.connect(self.glWidget.changeT)
        #toobar
        #self.ui.actionSelect_mode.triggered.connect(self.glWidget.changeMode)
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
        self.fov=45.0
        self.zoomScale=1.0
        self.lastPos = QtCore.QPoint()
        self.t=0.5
    def changeT(self,t):
        self.t=t/100.0
        self.update()
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

    def mouseMoveEvent(self, event:QtGui.QMouseEvent):
        dx = event.x() - self.lastPos.x()
        dy = self.lastPos.y() - event.y()
        print(dx,dy)
        if event.buttons() & QtCore.Qt.MiddleButton:
            self.setXRotation(self.xRot + 8*dy)
            self.setYRotation(self.yRot + 8*dx)
        if event.buttons() & QtCore.Qt.LeftButton:
            pass
        self.lastPos = event.pos()
        self.update()
    def selectObject(self,x,y):
        #picking mode reference:
        #https://blog.csdn.net/lcphoenix/article/details/6588033
        #https://stackoverflow.com/questions/56755950/why-object-selection-using-mouse-click-by-glselect-is-not-working-after-moving-c
        # s4t render mode and pick matrix
        viewport = glGetIntegerv(GL_VIEWPORT)
        selectBuffer = glSelectBuffer(100)

        glRenderMode(GL_SELECT)
        glInitNames()
        glPushName(0)
        # render object
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()

        gluPickMatrix(x, viewport[3] - y, 10.0, 10.0, viewport)
        # multiply projection matrix
        gluPerspective(45.0, self.width() / self.height(), 0.1, 100.0)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glLoadName(1)
        self.drawCurve(self.control_points)
        glLoadName(2)
        self.drawBeizerSurface()
        glFlush()
        hits = glRenderMode(GL_RENDER)
        if hits:
            print([x.names for x in hits])
        self.updateGL()
    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle
    def initializeGL(self):
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        #glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, self.width() / self.height(), 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
        #gluOrtho2D(0,self.widt h(),0,self.height())
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glScaled(self.zoomScale,self.zoomScale,self.zoomScale)
        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        self.drawCoordinateAxis()
        if self.status==0:
            self.clearScreen()
        elif self.status==1:
            self.drawCurve(self.control_points)
        elif self.status==2:
            self.splitCurve(self.control_points,self.t)
        elif self.status==3:
            self.drawBeizerSurface()
        elif self.status==4:
            self.drawBezierCircle()
        else:
            self.update()
        glFlush()

    def changeStatus(self,newStatus=0):
        self.status=newStatus
        self.update()
    def changeMode(self):
        self.selectionMode= not self.selectionMode
        self.update()

    def drawCurve(self,control_points,c_color=(1,1,1)):
        glColor3f(c_color[0], c_color[1], c_color[2])
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for i,p in enumerate(control_points):
            p.glVertex3()
        glEnd()
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
        glMatrixMode(GL_MODELVIEW)
        glColor3f(0.5,0.5,0.5)
        glPushMatrix()
        #glRotatef(45.0,-10.0,1.0,-10.0)
        control_points=[[[  -0.25, 0.0, -0.5],[ 0, 0, 0.0],[  0.25, -0.2, 0.0],[  0.5, 0.2, 0.0]],
[[  -0.5, -0.5, 0.0],[ 0, -0.9, 0.0],[  0.25, -0.2, 0.0],[  0.5, -0.6, 0.0]]]
        glMap2f(GL_MAP2_VERTEX_3,0,1,0,1,control_points)
        glEnable(GL_MAP2_VERTEX_3)
        glMapGrid2f(50,0,1,50,0,1)
        glEvalMesh2(GL_LINE,0,50,0,50)
        glPointSize(5)
        glColor3f(1, 1, 1)
        glBegin(GL_POINTS)
        for line in control_points:
            for point in line:
                glVertex3f(point[0], point[1], point[2])
        glEnd()
        glPopMatrix()
    def clearScreen(self):
        glFlush()
    def drawCoordinateAxis(self):
        lx=10
        ly=10
        #x axis
        glColor3f(1,0,0)
        glBegin(GL_LINES)
        glVertex3f(0,0,0)
        glVertex3f(1,0,0)
        glEnd()
        #y axis
        glColor3f(0, 1, 0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 1, 0)
        glEnd()
        #z axis
        glColor3f(0, 0, 1)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1)
        glEnd()
        #x-y plane
        # glColor3f(0.5, 0.5, 0.5)
        # glBegin(GL_QUADS)
        # glVertex3f(-lx/2,0,-ly/2)
        # glVertex3f(lx / 2, 0, -ly / 2)
        # glVertex3f(lx / 2, 0, ly / 2)
        # glVertex3f(-lx / 2, 0, ly / 2)
        # glEnd()
    def resizeGL(self, width, height):
        side = min(width, height)
        print(width,height)
        if side < 0:
            return
        #glViewport((width - side) // 2, (height - side) // 2, side, side)
        glViewport(0,0,width,height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, self.width() / self.height(), 0.1, 100)
    def drawBezierCircle(self,center=point(0.0,0,0.0),radius=0.5):
        #Bezier curve approximation constant
        #reference: https://www.jianshu.com/p/5198d8aa80c1
        C_MAGIC_NUMNER= 0.552284749831

        difference=C_MAGIC_NUMNER*radius
        c_x=center[0]
        c_y=center[1]
        c_z=center[2]
        p0=point(c_x,c_y+radius, c_z)
        c1 = point(c_x+difference,c_y+radius,c_z)
        c2 = point(c_x+radius, c_y+difference, c_z)
        p1=point(c_x+radius,c_y,c_z)
        c3 = point(c_x+radius,c_y-difference,c_z)
        c4 =point(c_x+difference,c_y-radius,c_z)
        p2=point(c_x,c_y-radius, c_z)
        c5 = point(c_x-difference,c_y-radius, c_z)
        c6 = point(c_x-radius,c_y-difference, c_z)
        p3=point(c_x-radius,c_y, c_z)
        c7=point(c_x-radius,c_y+difference, c_z)
        c8 = point(c_x-difference,c_y+radius, c_z)
        self.drawCurve([p0,c1,c2,p1])
        self.drawCurve([p1, c3, c4, p2])
        self.drawCurve([p2, c5, c6, p3])
        self.drawCurve([p3, c7, c8, p0])
    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        ###http://goldsequence.blogspot.com/2016/04/how-to-zoom-in-in-opengl-qt.html
        degree=a0.angleDelta().y()
        print(degree)
        if degree<0:
            self.zoomScale/=1.1
        if degree>0:
            self.zoomScale*=1.1
        self.update()
sys._excepthook = sys.excepthook
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook
if __name__ == '__main__':
    app = QtWidgets.QApplication(['Yo'])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

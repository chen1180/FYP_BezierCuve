from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.QtOpenGL import *
import tmp
from geometry import point
import sys
import camera
from curve import BezierCurve,BSpline
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
        self.control_points = [point(-0,-0.5, 0), point(-0.4, -0.4, 0), point(0, 0.3, 0), point(0.2, 0.2, 0), point(0.2, -0.2, 0), point(-0.15, -0.15, 0), point(0.1, 0.1, 0),point(0.1,0,0)]
        #self.control_points = [point(-0.5, -0.5, 0), point(-0.4, 0.4, 0), point(-0.0, -0.3, 0), point(0.2, 0.2, 0),point(0.5, -0.2, 0)]
        self.lastPos = point(0,0,0)
        self.t=0.5
        self.zoomScale=1.0
        self.camera=camera.Camera()
    def changeT(self,t):
        self.t=t/100.0
        self.update()
    def mousePressEvent(self, event):
        self.lastPos = point(event.x(), event.y(), 0)
        self.update()
    def mouseMoveEvent(self, event):
        #https://community.khronos.org/t/orbit-around-object/66465/4
        #PAN FUNCTION:https://computergraphics.stackovernet.com/cn/q/58
        if event.buttons()&QtCore.Qt.MiddleButton:
            dx = event.x() - self.lastPos.x
            dy = self.lastPos.y - event.y()
            self.camera.rotate(dx,dy)
        if event.buttons() & QtCore.Qt.LeftButton:
            dTheta = (self.lastPos.x-event.x())/10
            dPhi = (self.lastPos.y-event.y())/10
            self.camera.pan(dTheta,dPhi)
        self.lastPos = point(event.x(), event.y(), 0)
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
    def initializeGL(self):
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMouseTracking(True)
        glClearDepth(1.0)
        glDepthFunc(GL_ALWAYS)
        glEnable(GL_DEPTH_TEST)
        #glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.camera.updateProjectionMatrix(self.width(),self.height())
        #gluOrtho2D(0,self.widt h(),0,self.height())
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.camera.updateViewMatrix()
        self.drawCoordinateAxis()
        if self.status==0:
            self.clearScreen()
        elif self.status==1:
            BezierCurve().drawMultiBeizerCurve(self.control_points)
            BSpline().drawBSplineCurve(self.control_points)
        elif self.status==2:
            BezierCurve().splitCurve(self.control_points,self.t)
        elif self.status==3:
            BezierCurve().drawBeizerSurface()
        elif self.status==4:
            BezierCurve().drawBezierCircle()
        else:
            self.update()
        glFlush()
    def changeStatus(self,newStatus=0):
        self.status=newStatus
        self.update()
    def changeMode(self):
        self.selectionMode= not self.selectionMode
        self.update()

    def clearScreen(self):
        glFlush()
    def drawCoordinateAxis(self):
        lx=1
        ly=1
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
        self.camera.updateProjectionMatrix(width,height)

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        ###http://goldsequence.blogspot.com/2016/04/how-to-zoom-in-in-opengl-qt.html
        degree=a0.angleDelta().y()
        self.camera.zoom(degree/1000)
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

from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.QtOpenGL import *
import mainForm
from geometry import point,surface,curve
import sys
import camera
from curve import BezierCurve,BSpline,BeizerSurface

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()
    def setupUi(self):
        self.ui=mainForm.Ui_MainWindow()
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.ui.setupUi(self)
        self.ui.openGLWidget.close()
        self.glWidget=glWidget(self)
        self.ui.openGLWidget.close()
        self.ui.horizontalLayout_2.replaceWidget(self.ui.openGLWidget,self.glWidget)
        #toobar
        #self.ui.actionSelect_mode.triggered.connect(self.glWidget.changeMode)
class glWidget(QGLWidget):
    knotsTypeChanged = QtCore.pyqtSignal(str)
    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.status = 100
        self.lastPos = point(0, 0, 0)
        self.t = 0.5
        self.zoomScale = 1.0
        self.camera = camera.Camera()
        self.parent = parent
        self.selectionMode = False
        self.board=None
    def initBoard(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j]=0
        glClearColor(0.0,0.0,0.0,0.0)
    def drawSquares(self,mode):
        for i in range(3):
            if mode==GL_SELECT:
                glLoadName(i)
            for j in range(3):
                if mode==GL_SELECT:
                    glLoadName(j)
                glColor3f(i/3,j/3,self.board[i][j]/3)
                glRecti(i,j,i+1,j+1)
                if mode==GL_SELECT:
                    glPopName()
    def drawTriangle(self, x1, y1, x2, y2, x3, y3, z):
        glBegin(GL_TRIANGLES)
        glVertex3f(x1, y1, z)
        glVertex3f(x2, y2, z)
        glVertex3f(x3, y3, z)
        glEnd()

    def drawViewVolume(self, x1, y1, z1, x2, y2, z2):
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINE_LOOP)
        glVertex3f(x1, y1, -z1)
        glVertex3f(x2, y1, -z1)
        glVertex3f(x2, y2, -z1)
        glVertex3f(x1, y2, -z1)
        glEnd()

        glBegin(GL_LINE_LOOP)
        glVertex3f(x1, y1, -z2)
        glVertex3f(x2, y1, -z2)
        glVertex3f(x2, y2, -z2)
        glVertex3f(x1, y2, -z2)
        glEnd()

        glBegin(GL_LINES)
        glVertex3f(x1, y1, -z1)
        glVertex3f(x1, y1, -z2)
        glVertex3f(x1, y2, -z1)
        glVertex3f(x1, y2, -z2)
        glVertex3f(x2, y1, -z1)
        glVertex3f(x2, y1, -z2)
        glVertex3f(x2, y2, -z1)
        glVertex3f(x2, y2, -z2)
        glEnd()

    def drawScene(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.0, 4.0 / 3.0, 1.0, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(7.5, 7.5, 12.5, 2.5, 2.5, -5.0, 0.0, 1.0, 0.0)
        glColor3f(0.0, 1.0, 0.0)
        self.drawTriangle(2.0, 2.0, 3.0, 2.0, 2.5, 3.0, -5.0)
        glColor3f(1.0, 0.0, 0.0)
        self.drawTriangle(2.0, 7.0, 3.0, 7.0, 2.5, 8.0, -5.0)
        glColor3f(1.0, 1.0, 0.0)
        self.drawTriangle(2.0, 2.0, 3.0, 2.0, 2.5, 3.0, 0.0)
        self.drawTriangle(2.0, 2.0, 3.0, 2.0, 2.5, 3.0, -10.0)
        self.drawViewVolume(0.0, 5.0, 0.0, 5.0, 0.0, 10.0)

    def processHit(self,hits, buffer):
        print("Hits: {}".format(hits))
        print("Buffer:{}".format(buffer))
        for i,hit in enumerate(hits):
            print("name:".format(buffer[5*i]))
            print("z1:".format(buffer[5*i+1]/0x7fffffff))

    # define BUFSIZE 512

    def selectObject(self):
        # picking mode reference:
        # https://blog.csdn.net/lcphoenix/article/details/6588033
        # https://stackoverflow.com/questions/56755950/why-object-selection-using-mouse-click-by-glselect-is-not-working-after-moving-c
        # https://www.glprogramming.com/red/chapter13.html
        # s4t render mode and pick matrix
        viewport = glGetIntegerv(GL_VIEWPORT)
        selectBuffer = glSelectBuffer(100)
        glRenderMode(GL_SELECT)
        glInitNames()
        glPushName(0)
        glPushMatrix()

        # render object
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # multiply projection matrix
        glOrtho(0, 5, 0, 5, 0, 10)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glLoadName(1)
        self.drawTriangle(2.0, 2.0, 3.0, 2.0, 2.5, 3.0, -5.0)
        glLoadName(2)
        self.drawTriangle(2.0, 7.0, 3.0, 7.0, 2.5, 8.0, -5.0)
        glLoadName(3)
        self.drawTriangle(2.0, 2.0, 3.0, 2.0, 2.5, 3.0, 0.0)
        self.drawTriangle(2.0, 2.0, 3.0, 2.0, 2.5, 3.0, -10.0)
        glPopMatrix()
        glFlush()
        hits = glRenderMode(GL_RENDER)
        self.processHit(hits, selectBuffer)

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_FLAT)

    def paintGL(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.drawScene()
        self.selectObject()
        glFlush()


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
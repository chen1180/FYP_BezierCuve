from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.QtOpenGL import *
import mainForm
from geometry import point,surface,curve
import sys
from curve import BezierCurve,BSpline
from surface import BeizerSurface,BSplineSurface
import selectMode
import arcball
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
        self.ui.clearBtn.clicked.connect(lambda state, x=0: self.glWidget.changeStatus(x))
        self.ui.drawBezierBtn.clicked.connect(lambda state,x=1:self.glWidget.changeStatus(x))
        self.ui.splitBtn.clicked.connect(lambda state,x=2:self.glWidget.changeStatus(x))
        self.ui.drawBezierSurfaceBtn.clicked.connect(lambda state,x=3:self.glWidget.changeStatus(x))
        self.ui.pushButton.clicked.connect(lambda state,x=4:self.glWidget.changeStatus(x))
        self.ui.horizontalSlider.valueChanged.connect(self.glWidget.changeT)
        self.ui.bSplineBtn.clicked.connect(lambda state,x=5:self.glWidget.changeStatus(x))
        self.ui.drawMultiBezierBtn.clicked.connect(lambda state, x=6: self.glWidget.changeStatus(x))
        self.ui.actionSelect_mode.toggled.connect(self.glWidget.changeMode)
        self.ui.degreeBeziercomboBox.currentText()
        self.ui.displayMeshcheckBox.isChecked()
        self.ui.steps_uBezierSurfacespinBox.value()
        #toobar
        #self.ui.actionSelect_mode.triggered.connect(self.glWidget.changeMode)
class glWidget(QGLWidget):
    knotsTypeChanged = QtCore.pyqtSignal(str)
    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.status=100
        self.lastPos = point(0,0,0)
        self.currentPos=point(0,0,0)
        self.t=0.5
        self.zoomScale=1.0
        self.arcball=arcball.Arcball()
        #self.camera=camera.Camera()
        self.parent=parent
        self.selectionMode=False
    def initializeGL(self):
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMouseTracking(True)
        glClearDepth(1.0)
        glDepthFunc(GL_ALWAYS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_TEXTURE_2D)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0,self.width(),0,self.height())
        #Define data structure for drawing
        self.surface=surface.convertListToPoint(
            [[[-0.75, -0.75, -0.50], [-0.25, -0.75, 0.00], [0.25, -0.75, 0.00], [0.75, -0.75, -0.50],[1.0,-0.75,-0.5]],
             [[-0.75, -0.25, -0.75], [-0.25, -0.25, 0.50], [0.25, -0.25, 0.50], [0.75, -0.25, -0.75],[1.0,-0.25,-0.5]],
             [[-0.75, 0.25, 0.00], [-0.25, 0.25, -0.50], [0.25, 0.25, -0.50], [0.75, 0.25, 0.00],[1.0,0.25,0.0]],
             [[-0.75, 0.75, -0.50], [-0.25, 0.75, -1.00], [0.25, 0.75, -1.00], [0.75, 0.75, -0.50],[0.75,0.75,-0.5]],
             [[-0.75, 1.0, -0.50], [-0.25, 1.0, -1.00], [0.25, 1.0, -1.00], [0.75, 1.0, -0.50],[0.75,1.0,-0.5]]])
        # self.surface=surface.generateRandomMatrix(dim=[4,4,3])
        #self.control_points = curve.generateMatrix(dim=[8, 3])
        # self.control_points=curve.listToPoint([[-1.0, -0.0, -0.00], [-0.5, -1.0, 0.00], [0.0, 1.0, 0.00],[0.5, 0.5, 0],[0.75, -0.25, -0.50], [1.0, 1.0,0],[1.5, -0.5,0]])
        self.control_points = curve.listToPoint(
            [[-1.0, 1.0, -0.00], [-0, 1, 0.00], [1.0, 1.0, 0.00], [1.0, 0, 0], [1, -1, 0.00],
             [0.0, -1, 0], [-1, -1, 0],[-1.0,0, 0]])
        self.element=[]
        self.selectEngine=selectMode.SelectionEngine()
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        self.arcball.cameraUpdate()
        #self.camera.updateViewMatrix()
        self.drawCoordinateAxis()
        self.instantiateObject()
        self.drawViewVolume(0.0, 0.5, 0.0, 0.5, 0.0, 1.0)
        self.selectObject()
        self.renderObject()
        # x,y,z=self.getOGLPos(self.lastPos.x,self.lastPos.y)
        # x1,y1,z1=self.getOGLPos(self.currentPos.x,self.currentPos.y)
        # print(x,y,z,x1,y1,z1)
        # self.selectEngine.drawSelectSquare(x,y,z,x1,y1,z1)
        # print(self.lastPos,self.currentPos)

        glFlush()
    def instantiateObject(self):
        if self.status==0:
            self.clearScreen()
        elif self.status==1:
            bezier=BezierCurve(self.control_points,self.parent.ui.degreeBeziercomboBox.currentText(),self.parent.ui.stepsBeizerspinBox.value())
            self.element.append([self.status, bezier])
        elif self.status==2:
            self.curve.splitCurve(self.t)
        elif self.status==3:
            showPolygon=self.parent.ui.displayMeshcheckBox.isChecked()
            divs= self.parent.ui.steps_uBezierSurfacespinBox.value()
            curves=BeizerSurface(self.surface,divs,showPolygon)
            curves.dlbPatch=curves.genBezierSurface()
            splineSurface=BSplineSurface(self.surface,divs,showPolygon)
            splineSurface.dlbPatch=splineSurface.genBSplineSurface()
            self.element.append([self.status, curves])
            self.element.append([self.status, splineSurface])
        elif self.status==4:
            for ele in self.element:
                if ele[0]==1 or ele[0]==6:
                    ele[1].degreeElevationBezier()
        elif self.status==5:
            bSpline=BSpline(self.control_points,order=2,knotsType=self.parent.ui.knotTypecomboBox.currentText())
            self.element.append([self.status, bSpline])
        elif self.status==6:
            bezier = BezierCurve(self.control_points, self.parent.ui.degreeMultiBeziercomboBox.currentText(),
                                 self.parent.ui.stepsMultiBezierspinBox.value())
            self.element.append([self.status, bezier])
        else:
            self.update()
        self.status=100
    def renderObject(self):
        #print(self.element)
        if self.element:
            for ele in self.element:
                status=ele[0]
                shape=ele[1]
                if status == 0:
                    self.clearScreen()
                elif status == 1:
                    shape.drawCurve()
                elif status == 2:
                    pass
                elif status == 3:
                    glCallList(shape.dlbPatch)
                    shape.genMesh()
                elif status == 4:
                    pass
                elif status == 5:
                    shape.drawBSplineCurve()
                elif status== 6:
                    shape.drawMultiBeizerCurve()
                else:
                    self.update()

    def changeStatus(self,newStatus=0):
        self.status=newStatus
        self.update()
    def changeMode(self,mode):
        self.selectionMode= mode
        #print(self.selectionMode)
        self.update()

    def clearScreen(self):
        glFlush()
        self.status=100
        self.element.clear()
        self.update()
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
        glViewport(0,0,width,height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0,self.width(),0,self.height())

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        ###http://goldsequence.blogspot.com/2016/04/how-to-zoom-in-in-opengl-qt.html
        degree=a0.angleDelta().y()
        self.arcball.mouseScroll(degree)
        # self.camera.zoom(degree)
        self.update()

    def changeT(self, t):
        self.t = t / 100.0
        self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.lastPos = point(event.x(), event.y(), 0)
        if event.buttons() & QtCore.Qt.LeftButton:
            self.arcball.startPan(event.x(), event.y(),self.width(),self.height())
            if self.selectionMode:
                self.selectEngine.changeDrawSquare(True)
        if event.button()==QtCore.Qt.MiddleButton:
            self.arcball.startMotion(event.x(), event.y(),self.width(),self.height())
        self.update()
    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.lastPos = point(event.x(), event.y(), 0)
        if self.selectionMode:
            self.selectEngine.changeDrawSquare(False)
        if event.button()==QtCore.Qt.LeftButton:
            self.arcball.stopPan(event.x(), event.y(),self.width(),self.height())
        if event.button()==QtCore.Qt.MiddleButton:
            self.arcball.stopMotion(event.x(), event.y(),self.width(),self.height())

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        # https://community.khronos.org/t/orbit-around-object/66465/4
        # PAN FUNCTION:https://computergraphics.stackovernet.com/cn/q/58
        self.currentPos = point(event.x(), event.y(), 0)
        dTheta = (self.lastPos.x - event.x()) / 10
        dPhi = ( event.y()-self.lastPos.y) / 10
        if event.buttons() & QtCore.Qt.MiddleButton:
            # self.camera.rotate(dTheta,dPhi)
             self.arcball.mouseMotion(event.x(),event.y(),self.width(),self.height())
        if event.buttons() & QtCore.Qt.LeftButton:
            self.arcball.mousePan(event.x(),event.y(),self.width(),self.height(),dTheta,dPhi)
            if self.selectionMode:
                pass
            else:
                # self.camera.pan(dTheta,dPhi)
                self.lastPos = point(event.x(), event.y(), 0)
        self.update()
    def drawViewVolume(self,x1,y1,z1,x2,y2,z2):
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
    def processHit(self,hits,buffer):
        for i in hits:
            print("name:".format(i))
    def selectObject(self):
        #picking mode reference:
        #https://blog.csdn.net/lcphoenix/article/details/6588033
        #https://stackoverflow.com/questions/56755950/why-object-selection-using-mouse-click-by-glselect-is-not-working-after-moving-c
        #https://www.glprogramming.com/red/chapter13.html
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
        # glOrtho(0,5,0,5,0,10)
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
        self.processHit(hits,selectBuffer)
    def drawTriangle(self,x1,y1,x2,y2,x3,y3,z):
        glBegin (GL_TRIANGLES)
        glVertex3f (x1, y1, z)
        glVertex3f (x2, y2, z)
        glVertex3f (x3, y3, z)
        glEnd ()
    def screenSpaceToWorldSpace(self,x,y):
        w=self.width()/2
        h=self.height()/2
        return (x-w)/w,(h-y)/h
    def getOGLPos(self,x,y):
        modelview=glGetDoublev(GL_MODELVIEW_MATRIX)
        projection=glGetDoublev(GL_PROJECTION_MATRIX)
        viewport=glGetIntegerv(GL_VIEWPORT)
        winX=x
        winY=viewport[3]-y
        winZ=glReadPixels(x,winY,1,1,GL_DEPTH_COMPONENT,GL_FLOAT)
        posX,posY,posZ=gluUnProject(winX, winY, winZ, modelview, projection, viewport)
        return posX,posY,posZ
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

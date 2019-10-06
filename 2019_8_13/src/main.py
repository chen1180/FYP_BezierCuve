from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui,QtWidgets,QtCore,QtOpenGL
from ui import weightForm, textureLoadingDialog, cubeOverlay, mainForm
from geometry import point,surface,curve
import sys
from curve import BezierCurve,BSpline,NURBS
from surface import BeizerSurface,BSplineSurface,NurbsSurface
import selectMode
import arcball
import modelLoader
import copy
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()
    def setupUi(self):
        self.ui= mainForm.Ui_MainWindow()
        # self.setWindowState(QtCore.Qt.WindowMaximized)
        self.ui.setupUi(self)
        self.glWidget = glWidget(self)
        self.ui.graphicsView.close()
        # self.graphicsView=graphicView()
        # self.graphicsView.setViewport(self.glWidget)
        # self.graphicsView.setViewportUpdateMode(self.graphicsView.FullViewportUpdate)
        self.ui.centralwidget.layout().replaceWidget(self.ui.graphicsView,self.glWidget)
        #pushbutton
        self.ui.drawBezierBtn.clicked.connect(lambda state,x=1:self.glWidget.changeStatus(x))
        self.ui.elevateDegreeBezierCurveBtn.clicked.connect(lambda state,x=2:self.glWidget.changeStatus(x))
        self.ui.drawBezierSurfaceBtn.clicked.connect(lambda state,x=3:self.glWidget.changeStatus(x))
        self.ui.elevateDegreeBezierCurveBtn.clicked.connect(lambda state,x=4:self.glWidget.changeStatus(x))
        self.ui.bSplineBtn.clicked.connect(lambda state,x=5:self.glWidget.changeStatus(x))
        self.ui.drawMultiBezierBtn.clicked.connect(lambda state, x=6: self.glWidget.changeStatus(x))
        self.ui.drawBSplineSurfaceBtn.clicked.connect(lambda state, x=7: self.glWidget.changeStatus(x))
        self.ui.drawNURBS_Btn.clicked.connect(lambda state, x=8: self.glWidget.changeStatus(x))
        self.ui.weightNURBS_Btn.clicked.connect(lambda state, x=9: self.glWidget.changeStatus(x))
        self.ui.bsplineModel_Btn.clicked.connect(lambda state, x=10: self.glWidget.changeStatus(x))
        self.ui.circleNURBS_btn.clicked.connect(lambda state, x=11: self.glWidget.changeStatus(x))
        self.ui.sphereNURBS_Btn.clicked.connect(lambda state, x=12: self.glWidget.changeStatus(x))
        self.ui.bsplineTexture_Btn.clicked.connect(lambda state, x=13: self.glWidget.changeStatus(x))
        self.ui.cylinderNURBS_Btn.clicked.connect(lambda state, x=14: self.glWidget.changeStatus(x))
        self.ui.bilinearNURBS_Btn.clicked.connect(lambda state, x=15: self.glWidget.changeStatus(x))
        self.ui.revolutedShapeNURBS_Btn.clicked.connect(lambda state, x=16: self.glWidget.changeStatus(x))
        self.ui.sphereNURBS_Btn.clicked.connect(lambda state, x=17: self.glWidget.changeStatus(x))
        self.ui.torusNURBS_Btn.clicked.connect(lambda state, x=18: self.glWidget.changeStatus(x))
        root=QtWidgets.QTreeWidgetItem(self.ui.scenetreeWidget)
        self.ui.degreeBSplineSurface_spinBox.value()
        self.ui.bSplineSurface_displayTexture_checkBox.toggled
        self.ui.bsplineTexture_Btn
        #toolbar
        self.ui.actionClearScreen.triggered.connect(lambda state, x=0: self.glWidget.changeStatus(x))
        self.ui.actionSelect_mode.toggled.connect(self.glWidget.changeMode)
        self.ui.degreeBeziercomboBox.currentText()
        self.ui.displayMeshcheckBox.isChecked()
        self.ui.steps_uBezierSurfacespinBox.value()
class graphicView(QtWidgets.QGraphicsView):
    def __init__(self,parent=None):
        super(graphicView, self).__init__(parent)
        self.show()
    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF) -> None:
        painter.beginNativePainting()
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        self.initGL()
        glPopAttrib()
        painter.endNativePainting()
        if painter.paintEngine().type()!=QtGui.QPaintEngine.OpenGL2:
            print("OpenGLScene: drawBackground needs a "
                     "QGLWidget to be set as viewport on the "
                     "graphics view")
    def initGL(self):
        glClearColor(1, 1, 1, 1);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        glMatrixMode(GL_PROJECTION);
        glPushMatrix();
        glLoadIdentity();
        gluOrtho2D(0, 1, 0, 1)

class glWidget(QtWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super(glWidget, self).__init__()
        self.status=100
        self.lastPos = point(0,0,0)
        self.currentPos=point(0,0,0)
        self.t=0.5
        self.zoomScale=1.0
        self.arcball=arcball.Arcball()
        #self.camera=camera.Camera()
        self.parent=parent
        self.selectionMode=False
        self.imgPath=None
        self.bubble=cubeOverlay.cubeRotator()
    def initializeGL(self):
        #TODO: Change traditional opengl pipeline to modern opengl pipeline
        print(self.getOpenglInfo())
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMouseTracking(True)
        glClearDepth(1.0)
        # glDepthFunc(GL_LESS)
        # glEnable(GL_CULL_FACE)
        # glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_TEXTURE_2D)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-1,1,-1,1)
        #Define data structure for drawing
        self.surface=surface.convertListToPoint(
            [[[-1, -0.5, -0.5], [-1, 1, -0.5], [1, 1, -0.5], [1, -1, -0.5]],
             [[-1, -0.2, -0.2], [-1, 1, -0.2], [1, 1, -0.2], [1, -1,-0.2]],
              [[-1, 0.2, 0.2], [-1, 1,  0.2], [1, 1,  0.2], [1, -1,  0.2]],
               [[-1, 0.5,  0.5], [-1, 1, 0.5], [1, 1, 0.5], [1, -1, 0.5]],
                [[-1, 1, 1], [-1, 1, 1], [1, 1, 1], [1, -1, 1]]])
        # self.surface=surface.generateRandomMatrix(dim=[4,4,3])
        #self.control_points = curve.generateMatrix(dim=[8, 3])
        # self.control_points=curve.listToPoint([[-1.0, -0.0, -0.00], [-0.5, -1.0, 0.00], [0.0, 1.0, 0.00],[0.5, 0.5, 0],[0.75, -0.25, -0.50], [1.0, 1.0,0],[1.5, -0.5,0]])
        self.control_points = curve.listToPoint(
            [[1,0,0],[2,1,0],[1,1,0],[1,2,0]])
        self.weight=[1]*len(self.control_points)
        # self.weight=[1.0,2**0.5/2]*len(self.control_points)
        self.element=[]
        self.selectEngine=selectMode.SelectionEngine()
    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.arcball.cameraUpdate()
        # self.camera.updateViewMatrix()
        self.drawCoordinateAxis()
        self.instantiateObject()
        # self.drawViewVolume(0.0, 0.5, 0.0, 0.5, 0.0, 1.0)
        self.selectObject()
        self.renderObject()
        glFlush()
    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        self.makeCurrent()
        self.setupViewport(self.width(),self.height())
        self.paintGL()
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.white)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        # painter.drawText(100, 100, "Test")
        # self.bubble.drawBubble(painter)

    def instantiateObject(self):
        if self.status==0:
            self.clearScreen()
        elif self.status==1:
            bezier=BezierCurve(self.control_points,self.parent.ui.degreeBeziercomboBox.currentText(),self.parent.ui.stepsBeizerspinBox.value())
            self.element.append([self.status, bezier])
        elif self.status==2:
            for i in self.element:
                if i[0] == 1:
                    i[1].degreeElevationBezier()
        elif self.status==3:
            showPolygon=self.parent.ui.displayMeshcheckBox.isChecked()
            divs= self.parent.ui.steps_uBezierSurfacespinBox.value()
            curves=BeizerSurface(self.surface,divs,showPolygon)
            curves.dlbPatch=curves.genBezierSurface()
            self.element.append([self.status, curves])
        elif self.status==4:
            for ele in self.element:
                if ele[0]==1 or ele[0]==6:
                    ele[1].degreeElevationBezier()
        elif self.status==5:
            bSpline=BSpline(copy.deepcopy(self.control_points),order=self.parent.ui.degreeBSpline_spinBox.value(),knotsType=self.parent.ui.knotTypecomboBox.currentText())
            self.element.append([self.status, bSpline])
        elif self.status==6:
            bezier = BezierCurve(self.control_points, self.parent.ui.degreeMultiBeziercomboBox.currentText(),
                                 self.parent.ui.stepsMultiBezierspinBox.value())
            self.element.append([self.status, bezier])
        elif self.status==7:
            showTexture=self.parent.ui.bSplineSurface_displayTexture_checkBox.isChecked()
            divs = self.parent.ui.divsSplineSurfaceBox_spinBox.value()
            order=self.parent.ui.degreeBSplineSurface_spinBox.value()
            knotsType=self.parent.ui.bSplineSurface_comboBox.currentText()
            splineSurface = BSplineSurface(copy.deepcopy(self.surface),order,divs,knotsType, self.imgPath,showTexture)
            splineSurface.dlbPatch=splineSurface.genClampedBSplineSurface()
            self.element.append([self.status, splineSurface])
        elif self.status==8:
            nurbs = NURBS(self.control_points,weights=self.weight,order=self.parent.ui.degreeNURBS_spinBox.value(),
                          knotsType=self.parent.ui.NURBS_knotTypecomboBox.currentText())
            print(nurbs.controlPoints)
            self.element.append([self.status, nurbs])
        elif self.status==9:
            self.weightForm = weightForm.NURBS_WeightForm(len(self.control_points), self.weight)
            self.weightForm.setupUI()
        elif self.status==10:
            model=modelLoader.Model("./teapotCGA.bpt")
            model.loadModel()
            self.element.append([self.status, model])
        elif self.status==11:
            circles=curve.listToPoint(
            [[0.0, 1.0, 0.00], [1.0, 1.0, 0.00], [1, 0, 0.00], [1.0, -1, 0.00], [0, -1, 0.00], [-1, -1, 0.00],
             [-1, 0, 0.00], [-1, 1, 0.00], [0.0, 1.0, 0.00]])
            weight=[1,2**0.5/2,1,2**0.5/2,1,2**0.5/2,1,2**0.5/2,1]
            nurbs = NURBS(circles,weights=weight,order=self.parent.ui.degreeNURBS_spinBox.value(),knotsType="Circle")
            print(nurbs.controlPoints)
            self.element.append([self.status, nurbs])
        elif self.status==13:
            self.textureDialog=textureLoadingDialog.textureFileDialog(self)
            self.textureDialog.okButton.clicked.connect(self.textureDialogOk)
        elif self.status==14:
            nurbsSurface=NurbsSurface()
            self.element.append([self.status, nurbsSurface])
        elif self.status==15:
            nurbsSurface=NurbsSurface()
            self.element.append([self.status, nurbsSurface])
        elif self.status==16:
            nurbsSurface=NurbsSurface()
            nurbsSurface.getNURBS_SurfaceRevolution(point(0,0,0),point(0,0,1),360, curve.listToPoint(
            [[2,0,-1],[1,0,-1],[1,0,0],[2,0,1],[1,0,1],[1,0,2]]),[1,1,1,1,1,1],knotsType="Clamped",order=3,divs=20)
            self.element.append([self.status, nurbsSurface])
        elif self.status==17:
            nurbsSurface=NurbsSurface()
            nurbsSurface.getNURBS_SurfaceRevolution(point(0,0,0),point(0,1,0),360, curve.listToPoint(
            [[0.0, 1.0, 0.00], [1.0, 1.0, 0.00], [1, 0, 0.00], [1.0, -1, 0.00], [0, -1, 0.00]]),[1,2**0.5/2,1,2**0.5/2,1],knotsType="Circle",order=2,divs=20)
            self.element.append([self.status, nurbsSurface])
        elif self.status==18:
            nurbsSurface=NurbsSurface()
            nurbsSurface.getNURBS_Torus(point(-2,0,0),point(0,1,0),90, curve.listToPoint(
                [[0.0, 1.0, 0.00], [1.0, 1.0, 0.00], [1, 0, 0.00], [1.0, -1, 0.00], [0, -1, 0.00], [-1, -1, 0.00],
                 [-1, 0, 0.00], [-1, 1, 0.00], [0.0, 1.0, 0.00]]),[1,2**0.5/2,1,2**0.5/2,1,2**0.5/2,1,2**0.5/2,1],knotsType="Circle",order=2,divs=20)
            self.element.append([self.status, nurbsSurface])
        else:
            self.update()
        self.status=100
    def textureDialogOk(self):
        self.imgPath=self.textureDialog.imgPath
        self.textureDialog.close()

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
                elif status==7:
                    glCallLists(shape.dlbPatch)
                elif status==8:
                    shape.drawNURBS()
                elif status==10:
                    shape.renderModel()
                elif status==11:
                    shape.drawNURBS()
                elif status==14:
                    shape.drawNURBS_Cylinder()
                elif status == 15:
                    shape.drawNURBS_BilinearSurface()
                elif status == 16:
                    shape.drawNURBS_SurfaceRevolution(shape.result)
                elif status == 17:
                    shape.drawNURBS_SurfaceRevolution(shape.result)
                elif status == 18:
                    shape.drawNURBS_SurfaceRevolution(shape.result)
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
        print(self.element)
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
        # #x-y plane
        # glColor3f(0.5, 0.5, 0.5)
        # glBegin(GL_QUADS)
        # glVertex3f(-lx/2,0,-ly/2)
        # glVertex3f(lx / 2, 0, -ly / 2)
        # glVertex3f(lx / 2, 0, ly / 2)
        # glVertex3f(-lx / 2, 0, ly / 2)
        # glEnd()

    def resizeGL(self, w: int, h: int) -> None:
        self.setupViewport(w,h)
    def setupViewport(self,w,h):
        aspect = float(w / h)
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-1, 1, -1, 1)
        glMatrixMode(GL_MODELVIEW)
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
    def createOverlayDialog(self):
        dialog=QtWidgets.QDialog(self,QtCore.Qt.CustomizeWindowHint|QtCore.Qt.WindowTitleHint)
        dialog.setWindowOpacity(0.5)
        dialog.setWindowTitle("Overlay")
        return dialog
    def getOpenglInfo(self):
     info = """ 
      Vendor: {0} 
      Renderer: {1} 
      OpenGL Version: {2} 
      Shader Version: {3} 
     """.format(
      glGetString(GL_VENDOR),
      glGetString(GL_RENDERER),
      glGetString(GL_VERSION),
      glGetString(GL_SHADING_LANGUAGE_VERSION)
     )
     return info

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
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling,True)
    app = QtWidgets.QApplication(['Yo'])
    window = MainWindow()
    fmt = QtGui.QSurfaceFormat()
    fmt.setSamples(4)
    QtGui.QSurfaceFormat.setDefaultFormat(fmt)
    window.show()
    sys.exit(app.exec_())
#TODO
# "C:\Users\Chen Baocheng\AppData\Local\Programs\Python\Python37-32\Scripts\pyuic5.exe" mainForm.ui -o mainForm.py"
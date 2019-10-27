from PyQt5.QtGui import (QIcon, QColor)
from view.GLWindow import *
from view.SceneDockWidget import SceneDockWidget
from view.PropertyDockWidget import PropertyDockWidget
from model.geometry.bezier import Bezier
from model.geometry.nurb import Nurbs
from model.geometry.nurbPatch import NurbsPatch
from model.geometry.bezierPatch import BezierPatch
from controller import SceneManager


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.glWindow =OpenGLWindow(self)
        self.setCentralWidget(self.glWindow)

        self.createActions()
        self.createDrawActions()
        self.createViewAction()

        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()

        self.setWindowTitle("Curve and Surface")

        #Model for rendering and manipulation
        self.model=SceneManager.SceneObjects()
        #Model signal and slots
        self.model.sceneNodeAdded.connect(self.addItemToWidget)
        self.model.sceneNodeDeleted.connect(self.removeItemFromWidget)
        self.model.sceneNodeDraw.connect(self.glWindow.addToScene)
        #sceneDockWidget view signal and slots
        self.sceneWidget.itemClicked.connect(self.itemClick)

        # propertyDockWidget view signal and slots
        self.propertyWidget.coordinateForm.table.itemChanged.connect(self.updateSceneNode)
        # Signal and custom slots
        self.propertyWidget.coordinateForm.table.itemDoubleClicked.connect(self.onItemDoubleClick)
        #Signal and custom slots: Curve property widget
        self.propertyWidget.splineWidget.degreeForm.valueChanged.connect(self.changeCurve_Degree)
        self.propertyWidget.splineWidget.resolutionForm.valueChanged.connect(self.changeCurve_Resolution)
        self.propertyWidget.splineWidget.clampedTickBox.stateChanged.connect(self.changeCurve_Clamped)
        self.propertyWidget.splineWidget.knotsTable.itemChanged.connect(self.changeCurve_Knots)
        self.propertyWidget.splineWidget.weightsTable.itemChanged.connect(self.changeCurve_Weights)
        #Transformation from signal and slots
        self.propertyWidget.transformWidget.lineEditFinished.connect(self.changeTransform)
        #color widget signal and slots
        self.propertyWidget.colorWidget.colorChanged.connect(self.changeColor)
    def about(self):
        QMessageBox.about(self, "About FYP",
                "Under construction")

    def createActions(self):

        self.quitAct = QAction("&Quit", self, shortcut="Ctrl+Q",
                statusTip="Quit the application", triggered=self.close)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)
    def createViewAction(self):
        self.changeProjection_action = QAction(QIcon(":images/perspective.png"), "Perspective/Ortho", self,
                                               statusTip="Switch between Perspective/Ortho",
                                               triggered=self.changeProjection, checkable=True)
        self.viewport_XY_action = QAction(QIcon(":images/axis.png"), "XY Plane", self,
                                            statusTip="Transform to XY plane",
                                            triggered=self.changeViewPort_XY)
        self.viewport_YZ_action = QAction(QIcon(":images/axis.png"), "YZ Plane", self,
                                          statusTip="Transform to XZ plane",
                                          triggered=self.changeViewPort_YZ)
        self.viewport_XZ_action = QAction(QIcon(":images/axis.png"), "XZ Plane", self,
                                          statusTip="Transform to XZ plane",
                                          triggered=self.changeViewPort_XZ)
        #WireFrame mode
        self.changeWireFrameMode_action = QAction(QIcon(":images/wireFrame.png"), "WireFrame Mode", self,
                                               statusTip="Switch on WireFrame Mode",
                                               triggered=self.changeWireFrameMode, checkable=True)
    def createDrawActions(self):
        self.deleteItem_action = QAction(QIcon(":images/delete.png"), "Delete a selection", self,
                                      statusTip="Delete an item",
                                      triggered=self.deleteItem)
        self.addBezierCurve = QAction(QIcon(":images/bezier.png"),"Add Bezier Curve", self,
                                      statusTip="Add a cubic Bezier curve",
                                      triggered=self.drawBezierCurve)
        self.addBSplineCurve = QAction(QIcon(":images/spline.png"),"Add B Spline Curve", self,
                                       statusTip="Add a B Spline curve",
                                       triggered=self.drawBSpline)
        self.addNurbs = QAction(QIcon(":images/nurbs.png"),"Add a NURB", self,
                                       statusTip="Add a Nurb curve",
                                       triggered=self.drawNurbs)

        self.addBezierPatch = QAction(QIcon(":images/bezier_patch.png"),"Add Bezier patch", self,
                                      statusTip="Add a cubic Bezier patch",
                                      triggered=self.drawBezierPatch)
        self.addNurbsPatch = QAction(QIcon(":images/nurbs_patch.png"), "Add a NURB patch", self,
                                statusTip="Add a Nurb patch",
                                triggered=self.drawNurbsPatch)
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)


        self.viewMenu = self.menuBar().addMenu("&View")
        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        # Common action tool bar
        self.commonToolBar=self.addToolBar("Common commands")
        self.commonToolBar.addAction(self.deleteItem_action)
        # Projection tool bar
        self.viewToolBar = self.addToolBar("Projection & View")
        self.viewToolBar.addAction(self.changeProjection_action)
        self.viewToolBar.addAction(self.viewport_XY_action)
        self.viewToolBar.addAction(self.viewport_YZ_action)
        self.viewToolBar.addAction(self.viewport_XZ_action)
        self.viewToolBar.addSeparator()
        self.viewToolBar.addAction(self.changeWireFrameMode_action)
        #Beizer curve tool bar
        self.curveToolBar=QToolBar("Curve")
        self.curveToolBar.setOrientation(Qt.Vertical)
        self.curveToolBar.addAction(self.addBezierCurve)
        self.curveToolBar.addAction(self.addBSplineCurve)
        self.curveToolBar.addAction(self.addNurbs)
        #Surface tool bar
        self.surfaceToolBar=QToolBar("Surface")
        self.surfaceToolBar.setOrientation(Qt.Vertical)
        self.surfaceToolBar.addAction(self.addBezierPatch)
        self.surfaceToolBar.addAction(self.addNurbsPatch)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWindows(self):
        sceneDock = QDockWidget("Scene", self)
        sceneDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.sceneWidget =SceneDockWidget(sceneDock)
        #create sceneWidget
        sceneDock.setWidget(self.sceneWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, sceneDock)
        #create propertyWidget
        propertyDock = QDockWidget("Property", self)
        propertyDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.propertyWidget = PropertyDockWidget(propertyDock)
        propertyDock.setWidget(self.propertyWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, propertyDock)
        #create toolWidget
        toolDock = QDockWidget("Tool", self)
        toolDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        #set two vertical toolbar in the tool widget
        layout=QHBoxLayout()
        toolBarContainer=QWidget()
        layout.addWidget(self.curveToolBar)
        layout.addWidget(self.surfaceToolBar)
        toolBarContainer.setLayout(layout)
        toolDock.setWidget(toolBarContainer)
        self.addDockWidget(Qt.LeftDockWidgetArea, toolDock)

    #-----------------------------For model operation-----------------------------------#
    def deleteItem(self):
        if self.model.sceneNodes:
            currentIndex = self.sceneWidget.currentRow()
            selection = self.model.sceneNodes[currentIndex]
            self.model.deleteNode(selection)
    def drawBezierCurve(self):
        item = Bezier(None, "Beizer", [QVector3D(-1, -0.5, -0.5), QVector3D(-1, 1, -0.5), QVector3D(0, 1, -0.5),QVector3D(-1, 0.1, 0.2), QVector3D(-1, 0.4, 0.2)])
        self.model.addNode(item)
        self.sceneWidget.setCurrentItem(item)
        self.glWindow.addToScene(self.model.sceneNodes)
    def drawBSpline(self):
        item = Nurbs(None, "B Spline",[QVector3D(-1, -0.5, -0.5), QVector3D(-1, 1, -0.5), QVector3D(0, 1, -0.5),QVector3D(-1, 0.1, 0.2), QVector3D(-1, 0.4, 0.2)])
        self.model.addNode(item)
        self.sceneWidget.setCurrentItem(item)
        self.glWindow.addToScene(self.model.sceneNodes)
    def drawNurbs(self):
        item = Nurbs(None, "nurb",
                     [QVector3D(-1, -0.5, -0.5), QVector3D(-1, 1, -0.5), QVector3D(0, 1, -0.5), QVector3D(1, -1, -0.5),
                      QVector3D(-1, -0.2, -0.2), QVector3D(-1, 0.7, -0.2), QVector3D(0, 0.7, -0.2),
                      QVector3D(1, -1.3, -0.2)])
        self.model.addNode(item)
        self.sceneWidget.setCurrentItem(item)
        self.glWindow.addToScene(self.model.sceneNodes)
    def drawBezierPatch(self):
        item = BezierPatch(None, "BeizerPatch", [QVector3D(-1, -0.5, -0.5),QVector3D(-1, 1, -0.5),QVector3D(0, 1, -0.5),QVector3D(1, -1, -0.5),
                                            QVector3D(-1, -0.2, -0.2),QVector3D(-1, 0.7, -0.2),QVector3D(0, 0.7, -0.2),QVector3D(1, -1.3, -0.2),
                                            QVector3D(-1, 0.1, 0.2),QVector3D(-1, 0.4, 0.2),QVector3D(0, 0.4, 0.2),QVector3D(1, -1.6, 0.2),
                                            QVector3D(-1, -0.2, 0.5),QVector3D(-1, 0.1, 0.5),QVector3D(0, 0.1, 0.5),QVector3D(1, -1.8, 0.5)])
        self.model.addNode(item)
        self.sceneWidget.setCurrentItem(item)
        self.glWindow.addToScene(self.model.sceneNodes)
    def drawNurbsPatch(self):
        item = NurbsPatch(None, "NurbsPatch",
                           [QVector3D(-1, -0.5, -0.5), QVector3D(-1, 1, -0.5), QVector3D(0, 1, -0.5),
                            QVector3D(1, -1, -0.5),
                            QVector3D(-1, -0.2, -0.2), QVector3D(-1, 0.7, -0.2), QVector3D(0, 0.7, -0.2),
                            QVector3D(1, -1.3, -0.2),
                            QVector3D(-1, 0.1, 0.2), QVector3D(-1, 0.4, 0.2), QVector3D(0, 0.4, 0.2),
                            QVector3D(1, -1.6, 0.2),
                            QVector3D(-1, -0.2, 0.5), QVector3D(-1, 0.1, 0.5), QVector3D(0, 0.1, 0.5),
                            QVector3D(1, -1.8, 0.5)])
        self.model.addNode(item)
        self.sceneWidget.setCurrentItem(item)
        self.glWindow.addToScene(self.model.sceneNodes)

    # -----------------------------For projection operation-----------------------------------#
    def changeProjection(self,state:bool):
        self.glWindow.PerspectiveToOrtho(state)
    def changeViewPort_XY(self):
        self.glWindow.changeViewPlane(self.glWindow.VIEWPORT_XY_PLANE)
    def changeViewPort_YZ(self):
        self.glWindow.changeViewPlane(self.glWindow.VIEWPORT_YZ_PLANE)
    def changeViewPort_XZ(self):
        self.glWindow.changeViewPlane(self.glWindow.VIEWPORT_XZ_PLANE)
    def changeWireFrameMode(self,state:bool):
        for node in self.model.sceneNodes:
            node.m_showWireframe=state
    #-----------------------------For view operation-----------------------------------#
    def updateSceneNode(self,item:QTableWidgetItem):
        try:
            row=self.propertyWidget.coordinateForm.table.rowCount()
            column=self.propertyWidget.coordinateForm.table.columnCount()
            new_node=[]
            for i in range(row):
                node=QVector3D(float(self.propertyWidget.coordinateForm.table.item(i, 0).text()),
                               float(self.propertyWidget.coordinateForm.table.item(i, 1).text()),
                               float(self.propertyWidget.coordinateForm.table.item(i, 2).text()))
                new_node.append(node)
            currentIndex=self.sceneWidget.currentRow()
            self.sceneWidget.setCurrentRow(currentIndex)
            self.model.sceneNodes[currentIndex].modifyVertices(new_node)
            #if item type is Nurbs or Nurbs patch, update knots and weights as well
            if (type(self.model.sceneNodes[currentIndex])==Nurbs):
                #Number of control points
                n=len(self.model.sceneNodes[currentIndex].data(Qt.UserRole))
                k=self.model.sceneNodes[currentIndex].order
                clamped=self.model.sceneNodes[currentIndex].clamped
                self.model.sceneNodes[currentIndex].knots=self.model.sceneNodes[currentIndex].generateKnots(n,k,clamped)
                self.model.sceneNodes[currentIndex].weights=self.model.sceneNodes[currentIndex].generateWeights(n)
                #update splineWidget
                self.propertyWidget.splineWidget.updateView( self.model.sceneNodes[currentIndex])
            self.sceneWidget.setCurrentItem(self.model.sceneNodes[currentIndex])
        except Exception as e:
            print(e)
    def addControlPoint(self,item):
        self.updateSceneNode(item)
    def addItemToWidget(self,item):
        #scene widget update view
        self.sceneWidget.addItem(item)
        self.sceneWidget.setCurrentItem(item)
        #subwidget: coordinate form
        self.propertyWidget.coordinateForm.displayTable(item)
        #subwidget: spline widget
        if (type(item) == Nurbs or type(item) == NurbsPatch):
            self.propertyWidget.splineWidget.updateView(item)
        #subwidget: transform widget
        self.propertyWidget.transformWidget.setLineEdit(item.transform)
        #subwidget: color widget
        self.propertyWidget.colorWidget.setColor(item)

        self.sceneWidget.setCurrentItem(item)
    def removeItemFromWidget(self,item):
        self.sceneWidget.takeItem(self.sceneWidget.currentRow())
        self.glWindow.removeFromScene(item)
    def onItemDoubleClick(self, item: QTableWidgetItem):
        print("Table item modified", item.row(), item.column(), self.propertyWidget.coordinateForm.table.item(item.row(), item.column()).text())

    def itemClick(self,item):
        self.sceneWidget.setCurrentItem(item)
        self.propertyWidget.coordinateForm.displayTable(item)
        if (type(item) == Nurbs or type(item) == NurbsPatch):
            self.propertyWidget.splineWidget.updateView(item)
        self.propertyWidget.transformWidget.setLineEdit(item.transform)
        self.propertyWidget.colorWidget.setColor(item)
        self.sceneWidget.setCurrentItem(item)
    #mouse button event
    def keyPressEvent(self, a0: QKeyEvent) -> None:
        super(MainWindow, self).keyPressEvent(a0)
        self.glWindow.keyPressEvent(a0)
    #Transform widget lineEdit slots
    def changeTransform(self):
        currentIndex = self.sceneWidget.currentRow()
        x=self.propertyWidget.transformWidget.xEdit.text()
        y = self.propertyWidget.transformWidget.yEdit.text()
        z = self.propertyWidget.transformWidget.zEdit.text()
        try:
            x=float(x)
            y=float(y)
            z=float(z)
            self.model.sceneNodes[currentIndex].modifyTransform(x, y, z)
        except Exception as e:
            print(e)
    #Color widget slots
    def changeColor(self):
        currentIndex = self.sceneWidget.currentRow()
        #normalize color to 0-1 to fit in OPENGL color format
        def QColorToQVector3D(color:QColor):
            r,g,b=color.red(),color.green(),color.blue()
            return QVector3D(r/255.0,g/255.0,b/255.0)
        verticesColor=QColorToQVector3D(self.propertyWidget.colorWidget.verticesColor)
        polygonColor=QColorToQVector3D(self.propertyWidget.colorWidget.polygonColor)
        color=QColorToQVector3D(self.propertyWidget.colorWidget.color)
        self.model.sceneNodes[currentIndex].modifyColor(verticesColor,polygonColor,color)
    #Spline widget slots
    def changeCurve_Degree(self,new_degree:int):
        try:
            currentIndex = self.sceneWidget.currentRow()
            if (type(self.model.sceneNodes[currentIndex])==Nurbs or type(self.model.sceneNodes[currentIndex])==NurbsPatch):
                nControlPoints = len(self.model.sceneNodes[currentIndex].data(Qt.UserRole))
                clamped = self.model.sceneNodes[currentIndex].clamped
                # update nurb model
                self.model.sceneNodes[currentIndex].changeOrder(new_degree)
                self.model.sceneNodes[currentIndex].knots = self.model.sceneNodes[currentIndex].generateKnots(nControlPoints,new_degree, clamped)
                # update widget view
                self.propertyWidget.splineWidget.updateView(self.model.sceneNodes[currentIndex])
        except Exception as e:
            print(e)
    def changeCurve_Resolution(self, new_resolution: int):
        currentIndex = self.sceneWidget.currentRow()
        self.model.sceneNodes[currentIndex].changeResolution(new_resolution)

    def changeCurve_Clamped(self,new_type:int):
        try:
            currentIndex = self.sceneWidget.currentRow()
            # if the curve endpoint type is changed, its weights and knots need to be changed too!!
            if (type(self.model.sceneNodes[currentIndex])==Nurbs or type(self.model.sceneNodes[currentIndex])==NurbsPatch):
                nControlPoints=self.model.sceneNodes[currentIndex].verticesCount
                degree=self.model.sceneNodes[currentIndex].order
                new_type=bool(new_type)
                self.model.sceneNodes[currentIndex].changeEndPointType(new_type)
                self.model.sceneNodes[currentIndex].knots=self.model.sceneNodes[currentIndex].generateKnots(nControlPoints,degree,new_type)
                self.model.sceneNodes[currentIndex].weights=self.model.sceneNodes[currentIndex].generateWeights(nControlPoints)
                # update widget view
                self.propertyWidget.splineWidget.updateView(self.model.sceneNodes[currentIndex])
        except Exception as e:
            print(e)
    def changeCurve_Knots(self,item:QTableWidgetItem):
        try:
            row=self.propertyWidget.splineWidget.knotsTable.currentRow()
            column=self.propertyWidget.splineWidget.knotsTable.currentColumn()
            currentIndex = self.sceneWidget.currentRow()
            if (type(self.model.sceneNodes[currentIndex])==Nurbs or type(self.model.sceneNodes[currentIndex])==NurbsPatch):
                new_knot_value=float(item.text())
                if type(new_knot_value) is float:
                    self.model.sceneNodes[currentIndex].changeKnots(row,new_knot_value)
        except Exception as e:
            print(e)

    def changeCurve_Weights(self,item:QTableWidgetItem):
        try:
            row=self.propertyWidget.splineWidget.weightsTable.currentRow()
            column=self.propertyWidget.splineWidget.weightsTable.currentColumn()
            currentIndex = self.sceneWidget.currentRow()
            if (type(self.model.sceneNodes[currentIndex])==Nurbs or type(self.model.sceneNodes[currentIndex])==NurbsPatch):
                new_knot_value=float(item.text())
                if type(new_knot_value) is float:
                    self.model.sceneNodes[currentIndex].changeWeights(row,new_knot_value)
        except Exception as e:
            print(e)

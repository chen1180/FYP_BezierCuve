from PyQt5.QtCore import QDate, QFile, Qt, QTextStream
from PyQt5.QtGui import (QFont, QIcon, QKeySequence, QTextCharFormat,QKeyEvent,
        QTextCursor, QTextTableFormat,QVector3D,QColor)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import *
from curve_modernGL.view.GLWindow import *
from curve_modernGL.view.SceneDockWidget import SceneDockWidget
from curve_modernGL.view.PropertyDockWidget import PropertyDockWidget
from curve_modernGL.model.triangle import Triangle
from curve_modernGL.model.bezier import Bezier
from curve_modernGL.model.nurb import Nurbs
from curve_modernGL.model.bezierPatch import BezierPatch
from curve_modernGL.controller import SceneManager,GLWindowController,PropertyWidgetController,SceneWidgetController
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.glWindow =OpenGLWindow(self)
        self.setCentralWidget(self.glWindow)

        self.createActions()
        self.createDrawActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()

        self.setWindowTitle("Curve and Surface")

        #Model for rendering and manipulation
        self.model=SceneManager.SceneObjects()
        #Model signal and slots
        self.model.sceneNodeAdded.connect(self.addItemToWidget)
        # self.model.sceneNodeChanged.connect(self.updateWidgetStatus)  # Model update will changes the content in sceneDockWidget
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
    def createDrawActions(self):
        self.addBezierCurve = QAction(QIcon(":images/bezier.png"),"Add Bezier Curve", self,
                                      statusTip="Add a cubic Bezier curve",
                                      triggered=self.drawBezierCurve)
        self.addBSplineCurve = QAction(QIcon(":images/spline.png"),"Add B Spline Curve", self,
                                       statusTip="Add a B Spline curve",
                                       triggered=self.drawBSpline)
        self.addNurbs = QAction(QIcon(":images/nurbs.png"),"Add a NURB", self,
                                       statusTip="Add a Nurb curve",
                                       triggered=self.drawNurbs)

        self.addBezierPatch = QAction(QIcon(":images/bezier_patch.png"),"Add Bezier Patch", self,
                                      statusTip="Add a cubic Bezier Patch",
                                      triggered=self.drawBezierPatch)
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
        #Beizer curve tool bar
        self.curveToolBar=QToolBar("Curve")
        self.curveToolBar.setOrientation(Qt.Vertical)
        self.curveToolBar.addAction(self.addBezierCurve)
        self.curveToolBar.addAction(self.addBSplineCurve)
        self.curveToolBar.addAction(self.addNurbs)
        self.surfaceToolBar=QToolBar("Surface")
        self.surfaceToolBar.setOrientation(Qt.Vertical)
        self.surfaceToolBar.addAction(self.addBezierPatch)
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

    def drawBezierCurve(self):
        item = Bezier(None, "Beizer", [QVector3D(0,-1,0),QVector3D(0.5,0,0),QVector3D(1.0,0,0),QVector3D(1,0.5,0),QVector3D(0.5,0.5,0)])
        self.model.addNode(item)
        self.sceneWidget.setCurrentItem(item)
        self.glWindow.addToScene(self.model.sceneNodes)
    def drawBSpline(self):
        item = Nurbs(None, "B Spline",
                     [QVector3D(-1, -0.5, -0.5), QVector3D(-1, 1, -0.5), QVector3D(0, 1, -0.5), QVector3D(1, -1, -0.5),
                      QVector3D(-1, -0.2, -0.2)])
        self.model.addNode(item)
        self.sceneWidget.setCurrentItem(item)
        self.glWindow.addToScene(self.model.sceneNodes)
    def drawNurbs(self):
        item = Nurbs(None, "nurb",
                     [QVector3D(-1, -0.5, -0.5), QVector3D(-1, 1, -0.5), QVector3D(0, 1, -0.5), QVector3D(1, -1, -0.5),
                      QVector3D(-1, -0.2, -0.2), QVector3D(-1, 0.7, -0.2), QVector3D(0, 0.7, -0.2),
                      QVector3D(1, -1.3, -0.2),
                      QVector3D(-1, 0.1, 0.2), QVector3D(-1, 0.4, 0.2), QVector3D(0, 0.4, 0.2), QVector3D(1, -1.6, 0.2),
                      QVector3D(-1, -0.2, 0.5), QVector3D(-1, 0.1, 0.5), QVector3D(0, 0.1, 0.5),
                      QVector3D(1, -1.8, 0.5)])
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
            self.sceneWidget.setCurrentItem(self.model.sceneNodes[currentIndex])
        except Exception as e:
            print(e)
    def updateWidgetStatus(self,position,item):
        #check current TableWidget item
        row = self.propertyWidget.coordinateForm.table.rowCount()
        column = self.propertyWidget.coordinateForm.table.columnCount()
        new_node = []
        for i in range(row):
            node = QVector3D(float(self.propertyWidget.coordinateForm.table.item(i, 0).text()),
                             float(self.propertyWidget.coordinateForm.table.item(i, 1).text()),
                             float(self.propertyWidget.coordinateForm.table.item(i, 2).text()))
            new_node.append(node)
        currentIndex = self.sceneWidget.currentRow()
        self.model.sceneNodes[currentIndex].modifyVertices(new_node)
        new_Item=self.model.sceneNodes[currentIndex]
        self.sceneWidget.setCurrentItem(new_Item)
        print("new item",new_Item.data(Qt.UserRole))
        print(self.sceneWidget.currentItem().data(Qt.UserRole))
    def addItemToWidget(self,item):
        #scene widget update view
        self.sceneWidget.addItem(item)
        self.sceneWidget.setCurrentItem(item)
        #subwidget: coordinate form
        self.propertyWidget.coordinateForm.displayTable(item)
        #subwidget: spline widget
        self.propertyWidget.splineWidget.updateView(item)
        #subwidget: transform widget
        self.propertyWidget.transformWidget.setLineEdit(item.transform)
        #subwidget: color widget
        self.propertyWidget.colorWidget.setColor(item)

        self.sceneWidget.setCurrentItem(item)

    def onItemDoubleClick(self, item: QTableWidgetItem):
        # TODO: enable table widget to modify item such as item vertices
        print("Table item modified", item.row(), item.column(), self.propertyWidget.coordinateForm.table.item(item.row(), item.column()).text())

    def updateTable(self, item: QTableWidgetItem):
        new_data = list()
        currentIndex = self.sceneWidget.currentRow()
        for row in range(self.propertyWidget.coordinateForm.table.rowCount()):
            vector = QVector3D(float(self.propertyWidget.coordinateForm.table.item(row, 0).text()),
                               float(self.propertyWidget.coordinateForm.table.item(row, 1).text()),
                               float(self.propertyWidget.coordinateForm.table.item(row, 2).text()), )
            new_data.append(vector)
        self.model.sceneNodes[currentIndex].modifyVertices(new_data)
    def itemClick(self,item):
        self.sceneWidget.setCurrentItem(item)
        self.propertyWidget.coordinateForm.displayTable(item)
        self.propertyWidget.transformWidget.setLineEdit(item.transform)
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
        currentIndex = self.sceneWidget.currentRow()
        nControlPoints = len(self.model.sceneNodes[currentIndex].data(Qt.UserRole))
        clamped = self.model.sceneNodes[currentIndex].clamped
        # update nurb model
        self.model.sceneNodes[currentIndex].changeOrder(new_degree)
        self.model.sceneNodes[currentIndex].knots = self.model.sceneNodes[currentIndex].generateKnots(nControlPoints,new_degree, clamped)
        # update widget view
        self.propertyWidget.splineWidget.updateView(self.model.sceneNodes[currentIndex])
    def changeCurve_Resolution(self, new_resolution: int):
        currentIndex = self.sceneWidget.currentRow()
        self.model.sceneNodes[currentIndex].changeResolution(new_resolution)

    def changeCurve_Clamped(self,new_type:int):
        currentIndex = self.sceneWidget.currentRow()
        # if the curve endpoint type is changed, its weights and knots need to be changed too!!
        nControlPoints=len(self.model.sceneNodes[currentIndex].data(Qt.UserRole))
        degree=self.model.sceneNodes[currentIndex].order
        new_type=bool(new_type)
        self.model.sceneNodes[currentIndex].changeEndPointType(new_type)
        self.model.sceneNodes[currentIndex].knots=self.model.sceneNodes[currentIndex].generateKnots(nControlPoints,degree,new_type)
        self.model.sceneNodes[currentIndex].weights=self.model.sceneNodes[currentIndex].generateWeights(nControlPoints)
        # update widget view
        self.propertyWidget.splineWidget.updateView(self.model.sceneNodes[currentIndex])
    def changeCurve_Knots(self,item:QTableWidgetItem):
        try:
            row=self.propertyWidget.splineWidget.knotsTable.currentRow()
            column=self.propertyWidget.splineWidget.knotsTable.currentColumn()
            new_knot_value=float(item.text())
            if type(new_knot_value) is float:
                currentIndex=self.sceneWidget.currentRow()
                self.model.sceneNodes[currentIndex].changeKnots(row,new_knot_value)
        except Exception as e:
            print(e)

    def changeCurve_Weights(self,item:QTableWidgetItem):
        try:
            row=self.propertyWidget.splineWidget.weightsTable.currentRow()
            column=self.propertyWidget.splineWidget.weightsTable.currentColumn()
            new_knot_value=float(item.text())
            if type(new_knot_value) is float:
                currentIndex=self.sceneWidget.currentRow()
                self.model.sceneNodes[currentIndex].changeWeights(row,new_knot_value)
        except Exception as e:
            print(e)

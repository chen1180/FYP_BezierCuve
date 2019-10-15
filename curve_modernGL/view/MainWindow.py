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
        self.addBezierCurve=QAction("Add Bezier Curve", self,
                statusTip="Add a cubic Bezier curve",
                triggered=self.drawBezierCurve)
        self.addBezierPatch = QAction("Add Bezier Patch", self,
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
        self.bezierToolBar=self.addToolBar("add Bezier curve")
        self.bezierToolBar.addAction(self.addBezierCurve)
        self.bezierPatchToolBar = self.addToolBar("add Bezier patch")
        self.bezierToolBar.addAction(self.addBezierPatch)
    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWindows(self):
        sceneDock = QDockWidget("Scene", self)
        sceneDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.sceneWidget =SceneDockWidget(sceneDock)
        #create sceneWidget
        sceneDock.setWidget(self.sceneWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, sceneDock)
        propertyDock = QDockWidget("Property", self)
        propertyDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.propertyWidget = PropertyDockWidget(propertyDock)
        propertyDock.setWidget(self.propertyWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, propertyDock)
        toolDock = QDockWidget("Tool", self)
        toolDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        toolDock.setWidget(self.bezierToolBar)
        self.addDockWidget(Qt.LeftDockWidgetArea, toolDock)

    #-----------------------------For model operation-----------------------------------#

    def drawBezierCurve(self):
        # item = Bezier(None, "Beizer", [QVector3D(0,-1,0),QVector3D(0.5,0,0),QVector3D(1.0,0,0),QVector3D(1,0.5,0),QVector3D(0.5,0.5,0)])
        item = Nurbs(None, "Nurbs",[QVector3D(0, 0, 0), QVector3D(0.5, 0, 0), QVector3D(1.0, 0, 0), QVector3D(1, 0.5, 0), QVector3D(1, 1.5, 0), QVector3D(1.5, 0.5, 0)])
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
        self.sceneWidget.addItem(item)
        self.sceneWidget.setCurrentItem(item)
        self.propertyWidget.coordinateForm.displayTable(item)
        self.propertyWidget.transformWidget.setLineEdit(item.transform)
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
            # msg = QMessageBox()
            # msg.setIcon(QMessageBox.Warning)
            # msg.setText(str(e))
            # msg.setInformativeText("Please enter valid number!")
            # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # msg.exec_()
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



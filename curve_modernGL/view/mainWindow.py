from PyQt5.QtCore import QDate, QFile, Qt, QTextStream
from PyQt5.QtGui import (QFont, QIcon, QKeySequence, QTextCharFormat,QKeyEvent,
        QTextCursor, QTextTableFormat,QVector3D)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import *
import glWindow
from curve_modernGL.view.sceneDockWidget import sceneDockWidget
from curve_modernGL.view.propertyDockWidget import propertyDockWidget
from curve_modernGL.model.triangle import Triangle
from curve_modernGL.model.sceneNode import sceneNode
from curve_modernGL.model.bezier import Bezier
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.glWindow =glWindow.openGLWindow(self)
        self.setCentralWidget(self.glWindow)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()

        self.setWindowTitle("Curve and Surface")

        #Model for rendering and manipulation
        self.model=sceneNode()
        #Model signal and slots
        self.model.sceneNodeAdded.connect(self.addItemToWidget)
        # self.model.sceneNodeChanged.connect(self.updateWidgetStatus)  # Model update will changes the content in sceneDockWidget
        self.model.sceneNodeDraw.connect(self.glWindow.drawScene)
        #sceneDockWidget view signal and slots
        self.sceneWidget.itemClicked.connect(self.itemClick)
        # propertyDockWidget view signal and slots
        self.propertyWidget.vertexCoordinateWidget.vertTable.itemChanged.connect(self.updateSceneNode)
        # Signal and custom slots
        self.propertyWidget.vertexCoordinateWidget.vertTable.itemDoubleClicked.connect(self.onItemDoubleClick)
        # self.propertyWidget.vertexCoordinateWidget.vertTable.currentItemChanged.connect(self.updateTable)

    def about(self):
        QMessageBox.about(self, "About FYP",
                "Under construction")

    def createActions(self):

        self.quitAct = QAction("&Quit", self, shortcut="Ctrl+Q",
                statusTip="Quit the application", triggered=self.close)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QApplication.instance().aboutQt)
        self.addBezierCurve=QAction("Add", self,
                statusTip="Add a cubic Bezier curve",
                triggered=self.drawBezierCurve)
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)


        self.viewMenu = self.menuBar().addMenu("&View")
        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        #Beizer curve tool bar
        self.bezierToolBar=self.addToolBar("add Bezier curve")
        self.bezierToolBar.addAction(self.addBezierCurve)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWindows(self):
        sceneDock = QDockWidget("Scene", self)
        sceneDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.sceneWidget =sceneDockWidget(sceneDock)
        #create sceneWidget
        sceneDock.setWidget(self.sceneWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, sceneDock)
        propertyDock = QDockWidget("Property", self)
        propertyDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.propertyWidget = propertyDockWidget(propertyDock)
        propertyDock.setWidget(self.propertyWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, propertyDock)
        toolDock = QDockWidget("Tool", self)
        toolDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        toolDock.setWidget(self.bezierToolBar)
        self.addDockWidget(Qt.LeftDockWidgetArea, toolDock)

    #-----------------------------For model operation-----------------------------------#

    def drawBezierCurve(self):
        item = Bezier(None, "Beizer", [QVector3D(-0.5,0,0),QVector3D(0.5,0,0),QVector3D(0,0.5,0),QVector3D(1,0.5,0)])
        self.model.addNode(item)
        self.sceneWidget.setCurrentItem(item)
        self.glWindow.drawScene(self.model.sceneNodes)
    #-----------------------------For view operation-----------------------------------#
    def updateSceneNode(self,item:QTableWidgetItem):
        try:
            row=self.propertyWidget.vertexCoordinateWidget.vertTable.rowCount()
            column=self.propertyWidget.vertexCoordinateWidget.vertTable.columnCount()
            new_node=[]
            for i in range(row):
                node=QVector3D(float(self.propertyWidget.vertexCoordinateWidget.vertTable.item(i,0).text()),
                               float(self.propertyWidget.vertexCoordinateWidget.vertTable.item(i,1).text()),
                               float(self.propertyWidget.vertexCoordinateWidget.vertTable.item(i,2).text()))
                new_node.append(node)
            currentIndex=self.sceneWidget.currentRow()
            self.sceneWidget.setCurrentRow(currentIndex)
            self.model.sceneNodes[currentIndex].modifyInputData(new_node)
            self.sceneWidget.setCurrentItem(self.model.sceneNodes[currentIndex])
            #For debugging
            # print("current data",self.sceneWidget.currentItem().data(Qt.UserRole))
            # print("scene node", new_node)
            # print("scene node item", self.model.sceneNodes[currentIndex].data(Qt.UserRole))
            # print(self.sceneWidget.currentItem().data(Qt.UserRole))
        except Exception as e:
            print(e)
    def updateWidgetStatus(self,position,item):
        #check current TableWidget item
        row = self.propertyWidget.vertexCoordinateWidget.vertTable.rowCount()
        column = self.propertyWidget.vertexCoordinateWidget.vertTable.columnCount()
        new_node = []
        for i in range(row):
            node = QVector3D(float(self.propertyWidget.vertexCoordinateWidget.vertTable.item(i, 0).text()),
                             float(self.propertyWidget.vertexCoordinateWidget.vertTable.item(i, 1).text()),
                             float(self.propertyWidget.vertexCoordinateWidget.vertTable.item(i, 2).text()))
            new_node.append(node)
        currentIndex = self.sceneWidget.currentRow()
        self.model.sceneNodes[currentIndex].modifyInputData(new_node)
        new_Item=self.model.sceneNodes[currentIndex]
        self.sceneWidget.setCurrentItem(new_Item)
        print("new item",new_Item.data(Qt.UserRole))
        print(self.sceneWidget.currentItem().data(Qt.UserRole))
    def addItemToWidget(self,item):
        self.sceneWidget.addItem(item)
        self.sceneWidget.setCurrentItem(item)
        self.propertyWidget.vertexCoordinateWidget.displayTable(item)
        self.sceneWidget.setCurrentItem(item)

    def onItemDoubleClick(self, item: QTableWidgetItem):
        # TODO: enable table widget to modify item such as item vertices
        print("Table item modified", item.row(), item.column(),  self.propertyWidget.vertexCoordinateWidget.vertTable.item(item.row(), item.column()).text())

    def updateTable(self, item: QTableWidgetItem):
        new_data = list()
        currentIndex = self.sceneWidget.currentRow()
        for row in range( self.propertyWidget.vertexCoordinateWidget.vertTable.rowCount()):
            vector = QVector3D(float( self.propertyWidget.vertexCoordinateWidget.vertTable.item(row, 0).text()),
                               float( self.propertyWidget.vertexCoordinateWidget.vertTable.item(row, 1).text()),
                               float( self.propertyWidget.vertexCoordinateWidget.vertTable.item(row, 2).text()), )
            new_data.append(vector)
        self.model.sceneNodes[currentIndex].modifyInputData(new_data)
    def itemClick(self,item):
        self.sceneWidget.setCurrentItem(item)
        self.propertyWidget.vertexCoordinateWidget.displayTable(item)
        self.sceneWidget.setCurrentItem(item)
    #mouse button event
    def keyPressEvent(self, a0: QKeyEvent) -> None:
        super(MainWindow, self).keyPressEvent(a0)
        self.glWindow.keyPressEvent(a0)

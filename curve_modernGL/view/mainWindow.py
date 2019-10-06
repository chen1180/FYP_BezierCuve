from PyQt5.QtCore import QDate, QFile, Qt, QTextStream
from PyQt5.QtGui import (QFont, QIcon, QKeySequence, QTextCharFormat,
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
        self.model.sceneNodeChanged.connect(self.updateSceneDockWidget) # Model update will changes the content in sceneDockWidget
        self.model.sceneNodeChanged.connect(self.updatePropertyDockWidget)# Model update will changes the content in propertyDockWidget
        #sceneDockWidget view signal and slots
        self.sceneWidget.itemClicked.connect(self.updatePropertyDockWidget)
        # propertyDockWidget view signal and slots
        self.propertyWidget.vertexCoordinateWidget.vertTable.itemChanged.connect(self.updateSceneNode)
    def print_(self):
        document = self.textEdit.document()
        printer = QPrinter()
        dlg = QPrintDialog(printer, self)
        if dlg.exec_() != QDialog.Accepted:
            return

        document.print_(printer)

        self.statusBar().showMessage("Ready", 2000)

    def save(self):
        filename, _ = QFileDialog.getSaveFileName(self,
                "Choose a file name", '.', "HTML (*.html *.htm)")
        if not filename:
            return

        file = QFile(filename)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Dock Widgets",
                    "Cannot write file %s:\n%s." % (filename, file.errorString()))
            return

        out = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        out << self.textEdit.toHtml()
        QApplication.restoreOverrideCursor()

        self.statusBar().showMessage("Saved '%s'" % filename, 2000)

    def undo(self):
        document = self.textEdit.document()
        document.undo()

    def insertCustomer(self, customer):
        if not customer:
            return
        customerList = customer.split(', ')
        document = self.textEdit.document()
        cursor = document.find('NAME')
        if not cursor.isNull():
            cursor.beginEditBlock()
            cursor.insertText(customerList[0])
            oldcursor = cursor
            cursor = document.find('ADDRESS')
            if not cursor.isNull():
                for i in customerList[1:]:
                    cursor.insertBlock()
                    cursor.insertText(i)
                cursor.endEditBlock()
            else:
                oldcursor.endEditBlock()

    def addParagraph(self, paragraph):
        if not paragraph:
            return
        document = self.textEdit.document()
        cursor = document.find("Yours sincerely,")
        if cursor.isNull():
            return
        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor,
                2)
        cursor.insertBlock()
        cursor.insertText(paragraph)
        cursor.insertBlock()
        cursor.endEditBlock()

    def about(self):
        QMessageBox.about(self, "About FYP",
                "Under construction")

    def createActions(self):
        # self.newLetterAct = QAction(QIcon(':/images/new.png'), "&New Letter",
        #         self, shortcut=QKeySequence.New,
        #         statusTip="Create a new form letter", triggered=None)

        self.saveAct = QAction(QIcon(':/images/save.png'), "&Save...", self,
                shortcut=QKeySequence.Save,
                statusTip="Save the current form letter", triggered=self.save)

        self.printAct = QAction(QIcon(':/images/print.png'), "&Print...", self,
                shortcut=QKeySequence.Print,
                statusTip="Print the current form letter",
                triggered=self.print_)

        self.undoAct = QAction(QIcon(':/images/undo.png'), "&Undo", self,
                shortcut=QKeySequence.Undo,
                statusTip="Undo the last editing action", triggered=self.undo)

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
        # self.fileMenu.addAction(self.newLetterAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)

        self.viewMenu = self.menuBar().addMenu("&View")

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        # self.fileToolBar.addAction(self.newLetterAct)
        self.fileToolBar.addAction(self.saveAct)
        self.fileToolBar.addAction(self.printAct)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.undoAct)
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
        # self.glWindow.createScene(item1)
        self.addDockWidget(Qt.RightDockWidgetArea, sceneDock)
        propertyDock = QDockWidget("Property", self)
        propertyDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.propertyWidget = propertyDockWidget(propertyDock)
        propertyDock.setWidget(self.propertyWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, propertyDock)
        # self.viewMenu.addAction(dock.toggleViewAction())
        # self.customerList.currentTextChanged.connect(self.insertCustomer)
        # self.paragraphsList.currentTextChanged.connect(self.addParagraph)
        toolDock = QDockWidget("Tool", self)
        toolDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        toolDock.setWidget(self.bezierToolBar)
        self.addDockWidget(Qt.LeftDockWidgetArea, toolDock)

    #-----------------------------For model operation-----------------------------------#

    def drawBezierCurve(self):
        item = Bezier(None, "Beizer", [QVector3D(-0.5,0,0),QVector3D(0.5,0,0),QVector3D(0,0.5,0),QVector3D(1,0.5,0)])
        self.model.addNode(item)
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
            print(self.sceneWidget.currentRow())#return the current selected row of sceneWidget
            currentIndex=self.sceneWidget.currentRow()
            self.model.sceneNodes[currentIndex].modifyInputData(new_node)
            self.glWindow.drawScene(self.model.sceneNodes)
        except Exception as e:
            print(e)
    def updateSceneDockWidget(self,item):
        self.sceneWidget.addItem(item)
    def updatePropertyDockWidget(self,item):
        self.propertyWidget.updateItems(item)


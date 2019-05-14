from PyQt5 import QtCore,QtGui,QtWidgets
class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setGeometry(200,200,1200,600)
        scene=QtWidgets.QGraphicsScene()
        scene.addItem(QtWidgets.QGraphicsRectItem(600,300,1000,400))
        view=QtWidgets.QGraphicsView()
        view.setScene(scene)
        self.setCentralWidget(view)

        exitAction=QtWidgets.QAction(QtGui.QIcon('Icons/exit.png'),'exit',self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menuBar=self.menuBar()
        fileMenu=menuBar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolBar=self.addToolBar('Exit')
        toolBar.addAction(exitAction)

        self.show()
if __name__ == '__main__':
    app=QtWidgets.QApplication([])
    window=mainWindow()
    app.exec_()
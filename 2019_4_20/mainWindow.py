from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from testPackage import *
class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.setSceneRect(-100, -100, 200, 200)
        self.points=[]
        self.opt=""
    def setOption(self,opt):
        self.opt=opt
    def mousePressEvent(self, event):
        pen = QPen(QtCore.Qt.black)
        brush = QBrush(QtCore.Qt.black)
        point=event.scenePos()
        if self.opt=="Draw Point":
            self.addEllipse(point.x(),point.y(), 4, 4, pen, brush)
        elif self.opt=="Draw Line":
            self.points.append(point)
            if len(self.points)==2:
                line=QLineF(self.points[0],self.points[1])
                self.addLine(line)
                self.points.clear()
        elif self.opt=="Draw Curve":
            self.points.append(point)
            if len(self.points)==1:
                self.addEllipse(point.x(), point.y(), 4, 4, pen, brush)
            if len(self.points)==2:
                line = QLineF(self.points[0], self.points[1])
                self.addLine(line)
        elif self.opt=="Clear Drawing":
            self.clear()
            self.update()

class Point(QtWidgets.QGraphicsItem):
    def __init__(self,x,y):
        super(Point, self).__init__()
        self.setFlag(self.ItemIsMovable)
        self.x=x
        self.y=y
    def boundingRect(self) -> QtCore.QRectF:
        penWidth=5.0
        return QtCore.QRectF(-10 - penWidth / 2, -10 - penWidth / 2,
                      20 + penWidth, 20 + penWidth)
    def paint(self, painter: QtGui.QPainter,pos:QtCore.QPoint,option=None, widget=None) -> None:
        radius=5.0
        painter.setBrush(QBrush(Qt.black))
        painter.drawEllipse(self.x,self.y,radius,radius)

class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.saved_scene=[]
        self.setupUI()
    def setupUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.graphicsView.setMouseTracking(True)
        self.mousePos = None

        self.scene = GraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        #push button signal
        self.ui.push_button_drawPoint.clicked.connect(self.drawPoint)
        self.ui.push_button_drawLine.clicked.connect(self.drawLine)
        self.ui.push_button_clearDrawing.clicked.connect(self.clearDrawing)
    def drawPoint(self):
        self.scene.setOption(self.ui.push_button_drawPoint.text())
    def drawLine(self):
        self.scene.setOption(self.ui.push_button_drawLine.text())
    def clearDrawing(self):
        self.scene.setOption(self.ui.push_button_clearDrawing.text())
if __name__ == '__main__':
    app=QtWidgets.QApplication([])
    window=mainWindow()
    window.show()
    app.exec_()
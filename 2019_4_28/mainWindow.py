from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from testPackage import *


class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.setSceneRect(-250, -250, 500, 500)
        self.lastPoint = None
        self.isDrawing = False
        self.opt = ""
        self.currentItem = None

    def setOption(self, opt):
        self.opt = opt

    def mousePressEvent(self, event):
        point = event.scenePos()
        if self.isDrawing == False:
            if event.button() == Qt.LeftButton:
                self.isDrawing = True
                if self.opt == "Draw Curve":
                    p = Curve(parent=self)
                    self.addItem(p)
                    p.addPoint(point)
                    self.currentItem = p
                else:
                    self.isDrawing = False
            elif event.button() == Qt.RightButton:
                print("Remove item")
                itemToremove = self.items(event.scenePos())
                if itemToremove:
                    self.removeItem(itemToremove[0])
        else:
            if self.currentItem.isDrawingComplete:
                self.isDrawing = False
                self.currentItem = None
            else:
                self.currentItem.addPoint(point)
        self.update()

    def resetData(self):
        self.opt = ""
        self.lastPoint = None

    def mouseMoveEvent(self, event):
        for item in self.selectedItems():
            item.setPos(event.scenePos())
        self.lastPoint = event.scenePos()
        self.update()

    def mouseReleaseEvent(self, event):
        if self.selectedItems():
            for item in self.selectedItems():
                item.setSelected(False)
        self.update()

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
        items = self.items(event.scenePos())
        if items:
            for item in items:
                item.setSelected(True)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            print("escaped")
            self.opt = ""
            print(self.selectedItems())


class Curve(QtWidgets.QGraphicsItem):
    def __init__(self, rect=(0, 0, 250, 250), tooltip='No tip here', parent=None):
        super(QGraphicsItem, self).__init__()
        self.points = []
        self.isDrawingComplete = False
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setAcceptHoverEvents(True)

        self.parent = parent
        self.pen = QPen(Qt.blue, 1)
        pw = self.pen.widthF()
        self.brush = QBrush(Qt.blue)
        self.setToolTip(tooltip)
        self.rect = QRectF(rect[0], rect[1], rect[2], rect[3])
        self.focusrect = QRectF(rect[0] - pw / 2, rect[1] - pw / 2, rect[2] + pw, rect[3] + pw)

    def addPoint(self, point):
        self.points.append(point)

    def get_points_size(self):
        return len(self.points)

    def boundingRect(self) -> QtCore.QRectF:
        return self.rect

    def paint(self, painter: QtGui.QPainter, option=None, widget=None) -> None:
        path = QPainterPath()
        painter.setRenderHints(QPainter.Antialiasing)
        if self.get_points_size() == 0:
            painter.setPen(QPen(Qt.green, 5))
            painter.drawPoint(self.parent.lastPoint)
        elif self.get_points_size() == 1:
            painter.setPen(QPen(Qt.green, 5))
            painter.drawPoint(self.points[0])
            painter.drawPoint(self.parent.lastPoint)
            painter.setPen(QPen(Qt.red, Qt.DashLine, 3))
            painter.drawLine(QLineF(self.points[0], self.parent.lastPoint))
        elif self.get_points_size() == 2:
            painter.setPen(QPen(Qt.green, 5))
            painter.drawPoint(self.points[0])
            painter.drawPoint(self.points[1])
            painter.drawPoint(self.parent.lastPoint)
            painter.setPen(QPen(Qt.red, Qt.DashLine, 3))
            painter.drawLine(QLineF(self.points[0], self.parent.lastPoint))
            painter.drawLine(QLineF(self.points[0], self.points[1]))
            painter.drawLine(QLineF(self.points[1], self.parent.lastPoint))
            painter.setPen(QPen(Qt.black, 1))
            path.moveTo(self.points[0])
            path.quadTo(self.parent.lastPoint, self.points[1])
            painter.drawPath(path)
        elif self.get_points_size() == 3:
            painter.setPen(QPen(Qt.black, 1))
            path.moveTo(self.points[0])
            path.quadTo(self.points[2], self.points[1])
            painter.drawPath(path)
            self.isDrawingComplete = True
            self.rect = path.boundingRect()
            self.focusrect = path.boundingRect()
        if self.isSelected():
            self.drawFocusRect(painter)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        print("enter")
        self.pen.setStyle(QtCore.Qt.DotLine)

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        print("leave")
        self.pen.setStyle(QtCore.Qt.SolidLine)

    def drawFocusRect(self, painter):
        self.focusbrush = QtGui.QBrush()
        self.focuspen = QtGui.QPen(QtCore.Qt.DotLine)
        self.focuspen.setColor(QtCore.Qt.black)
        self.focuspen.setWidthF(1.5)
        painter.setBrush(self.focusbrush)
        painter.setPen(self.focuspen)
        painter.drawRect(self.focusrect)


class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.graphicsView.setMouseTracking(True)
        self.mousePos = None

        self.scene = GraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        # push button signal
        self.ui.push_button_drawPoint.clicked.connect(self.drawPoint)
        self.ui.push_button_drawLine.clicked.connect(self.drawLine)
        self.ui.push_button_drawCurve.clicked.connect(self.drawCurve)
        self.ui.push_button_clearDrawing.clicked.connect(self.clearDrawing)

    def drawPoint(self):
        self.scene.setOption(self.ui.push_button_drawPoint.text())
        self.scene.update()

    def drawLine(self):
        self.scene.setOption(self.ui.push_button_drawLine.text())
        self.scene.update()

    def drawCurve(self):
        self.scene.setOption(self.ui.push_button_drawCurve.text())

    def clearDrawing(self):
        self.scene.resetData()
        self.scene.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = mainWindow()
    window.show()
    app.exec_()

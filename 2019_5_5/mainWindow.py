from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from testPackage import *


class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.setSceneRect(0, 0, 1000, 1000)
        self.lastPoint = None
        self.isDrawing = False
        self.opt = ""
        self.currentItem = None

    def setOption(self, opt):
        self.opt = opt

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        point = event.scenePos()
        if self.isDrawing == False:
            if event.button() == Qt.LeftButton :
                if self.opt=="QuadBezier" or self.opt== "CubicBezier" or self.opt=="MultiBezier":
                    self.isDrawing = True
                    p = Curve(parent=self)
                    self.addItem(p)
                    self.currentItem = p
                elif self.opt=="Select":
                    print("Select")
                    pass
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
        super().mouseMoveEvent(event)
        self.lastPoint = event.scenePos()
        self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.update()

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Escape:
            print("scene Esc")


class Curve(QtWidgets.QGraphicsItem):
    def __init__(self, rect=(0, 0, 250, 250), tooltip='No tip here', parent=None):
        super(QGraphicsItem, self).__init__()
        #saved data
        self.points = []
        self.selected_Point = None
        #default setting
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        #status
        self.isDrawingComplete = False
        self.isHover=False
        #painting method
        self.parent = parent
        self.opt = self.parent.opt
        self.pen_point = QPen(Qt.green, 5)
        self.pen_line = QPen(Qt.gray, Qt.DotLine, 5)
        self.pen_curve = QPen(Qt.black, 2, Qt.SolidLine)
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
        self.BezierCurve(painter, path)
        if self.isSelected():
            self.drawFocusRect(painter)

    def BezierCurve(self, painter, path):
        painter.setPen(self.pen_point)
        if self.isDrawingComplete==False :
            painter.drawPoint(self.parent.lastPoint)
            for point in self.points:
                painter.drawPoint(point)
            painter.setPen(self.pen_line)
            for index in range(len(self.points) - 1):
                painter.drawLine(QLineF(self.points[index], self.points[index + 1]))
        else:
            if self.isHover == True or self.isSelected():
                for point in self.points:
                    painter.drawPoint(point)
                painter.setPen(self.pen_line)
                for index in range(len(self.points) - 1):
                    painter.drawLine(QLineF(self.points[index], self.points[index + 1]))
        if self.get_points_size() == 3 and self.opt == "QuadBezier":
            path.moveTo(self.points[0])
            path.quadTo(self.points[1], self.points[2])
            painter.setPen(self.pen_curve)
            painter.drawPath(path)
            self.isDrawingComplete = True
            self.rect = path.boundingRect()
            self.focusrect = path.boundingRect()
        elif self.get_points_size() == 4 and self.opt == "CubicBezier":
            path.moveTo(self.points[0])
            path.cubicTo(self.points[1], self.points[2], self.points[3])
            painter.setPen(self.pen_curve)
            painter.drawPath(path)
            self.isDrawingComplete = True
            self.rect = path.boundingRect()
            self.focusrect = path.boundingRect()
        elif self.get_points_size() >= 3 and self.opt == "MultiBezier":
            path.moveTo(self.points[0])
            for index in range(1, len(self.points) - 2):
                start_point = self.points[index]
                ctrl_point = self.points[index + 1]
                end_point = QPointF((self.points[index + 1] + self.points[index + 2]) / 2.0)
                path.quadTo(ctrl_point, end_point)
                path.moveTo(end_point)
                index = index + 2
            painter.setPen(self.pen_curve)
            painter.drawPath(path)
            self.rect = path.boundingRect()
            self.focusrect = path.boundingRect()

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mouseMoveEvent(event)
        if self.selected_Point:
            print(self.selected_Point)
            self.selected_Point=QPointF(0,0)
        self.update()

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mousePressEvent(event)
        print("press")
        if event.button() == Qt.LeftButton:
            if self.isSelected():
                print("selected")
                self.selected_Point=self.points[0]
        self.update()

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mouseReleaseEvent(event)
        print("release")

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.setSelected(True)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.isHover=True
        print("hover")

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.isHover=False
        print("leave")

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Escape:
            print("Esc")

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
        self.ui.graphicsView.setBackgroundBrush(QBrush(Qt.white))
        # push button signal
        self.ui.push_button_bezier_quad.clicked.connect(
            lambda state, button_text=self.ui.push_button_bezier_quad.text(): self.drawCurve(button_text))
        self.ui.push_button_bezier_cubic.clicked.connect(
            lambda state, button_text=self.ui.push_button_bezier_cubic.text(): self.drawCurve(button_text))
        self.ui.push_button_bezier_multi.clicked.connect(
            lambda state, button_text=self.ui.push_button_bezier_multi.text(): self.drawCurve(button_text))
        self.ui.actionClear.triggered.connect(self.clearDrawing)
        self.ui.actionSelect.triggered.connect(
            lambda state, button_text=self.ui.actionSelect.text(): self.drawCurve(button_text))

    def drawCurve(self, button_text):
        self.scene.setOption(button_text)

    def clearDrawing(self):
        self.scene.resetData()
        self.scene.clear()
        self.scene.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = mainWindow()
    window.show()
    app.exec_()

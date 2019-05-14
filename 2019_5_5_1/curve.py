from PyQt5.QtWidgets import *
from PyQt5 import QtCore,QtGui
class Curve(QGraphicsItem):
    def __init__(self, rect=(0, 0, 250, 250), tooltip='No tip here', parent=None):
        super(Curve, self).__init__()
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
        self.pen_point = QtGui.QPen(QtCore.Qt.green, 5)
        self.pen_line = QtGui.QPen(QtCore.Qt.gray, QtCore.Qt.DotLine, 5)
        self.pen_curve = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        self.pen = QtGui.QPen(QtCore.Qt.blue, 1)
        pw = self.pen.widthF()
        self.brush = QtGui.QBrush(QtCore.Qt.blue)
        self.setToolTip(tooltip)
        self.rect = QtCore.QRectF(rect[0], rect[1], rect[2], rect[3])
        self.focusrect = QtCore.QRectF(rect[0] - pw / 2, rect[1] - pw / 2, rect[2] + pw, rect[3] + pw)

    def addPoint(self, point):
        self.points.append(point)

    def get_points_size(self):
        return len(self.points)

    def boundingRect(self) -> QtCore.QRectF:
        return self.rect

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mouseMoveEvent(event)
        if self.selected_Point:
            print(self.selected_Point)
            self.selected_Point=QtCore.QPointF(0,0)
        self.update()

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mousePressEvent(event)
        print("press")
        if event.button() == QtCore.Qt.LeftButton:
            if self.isSelected():
                print("selected")
                self.selected_Point=self.points[0]
        self.update()

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mouseReleaseEvent(event)
        print("release")

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.isHover=True
        print("hover")

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.isHover=False
        print("leave")

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Escape:
            print("Esc")

    def drawFocusRect(self, painter):
        self.focusbrush = QtGui.QBrush()
        self.focuspen = QtGui.QPen(QtCore.Qt.DotLine)
        self.focuspen.setColor(QtCore.Qt.black)
        self.focuspen.setWidthF(1.5)
        painter.setBrush(self.focusbrush)
        painter.setPen(self.focuspen)
        painter.drawRect(self.focusrect)

class QuadBezierCurve(Curve):
    def __init__(self,parent=None):
        super(QuadBezierCurve, self).__init__(parent=parent)
    def paint(self, painter: QtGui.QPainter, option=None, widget=None) -> None:
        path = QtGui.QPainterPath()
        painter.setRenderHints(QtGui.QPainter.Antialiasing)
        self.drawQuadBeizerCuve(painter, path)
        if self.isSelected():
            self.drawFocusRect(painter)
    def drawQuadBeizerCuve(self,painter,path):
        painter.setPen(self.pen_point)
        if self.isDrawingComplete == False:
            print(self.parent)
            painter.drawPoint(self.parent.lastPoint)
            for point in self.points:
                painter.drawPoint(point)
            painter.setPen(self.pen_line)
            for index in range(len(self.points) - 1):
                painter.drawLine(QtCore.QLineF(self.points[index], self.points[index + 1]))
        if self.get_points_size() == 3 and self.opt == "QuadBezier":
            path.moveTo(self.points[0])
            path.quadTo(self.points[1], self.points[2])
            painter.setPen(self.pen_curve)
            painter.drawPath(path)
            self.isDrawingComplete = True
            self.rect = path.boundingRect()
            self.focusrect = path.boundingRect()
class CubicBeizerCurve(Curve):
    def __init__(self,parent=None):
        super(CubicBeizerCurve, self).__init__(parent=parent)
    def paint(self, painter: QtGui.QPainter, option=None, widget=None) -> None:
        path = QtGui.QPainterPath()
        painter.setRenderHints(QtGui.QPainter.Antialiasing)
        self.drawCubicBeizerCuve(painter, path)
        if self.isSelected():
            self.drawFocusRect(painter)

    def drawCubicBeizerCuve(self, painter, path):
        painter.setPen(self.pen_point)
        if self.isDrawingComplete == False:
            print(self.parent)
            painter.drawPoint(self.parent.lastPoint)
            for point in self.points:
                painter.drawPoint(point)
            painter.setPen(self.pen_line)
            for index in range(len(self.points) - 1):
                painter.drawLine(QtCore.QLineF(self.points[index], self.points[index + 1]))
        if self.get_points_size() == 4 and self.opt == "CubicBezier":
            path.moveTo(self.points[0])
            path.cubicTo(self.points[1], self.points[2], self.points[3])
            painter.setPen(self.pen_curve)
            painter.drawPath(path)
            self.isDrawingComplete = True
            self.rect = path.boundingRect()
            self.focusrect = path.boundingRect()
class MultiBeizerCurve(Curve):
    def __init__(self,parent=None):
        super(MultiBeizerCurve, self).__init__(parent=parent)
        self.editMode=False
    def paint(self, painter: QtGui.QPainter, option=None, widget=None) -> None:
        path = QtGui.QPainterPath()
        painter.setRenderHints(QtGui.QPainter.Antialiasing)
        self.drawMultiBeizerCuve(painter, path)
        if self.isSelected():
            self.drawFocusRect(painter)
    def drawMultiBeizerCuve(self, painter, path):
        painter.setPen(self.pen_point)
        if self.isDrawingComplete == False:
            print(self.parent)
            painter.drawPoint(self.parent.lastPoint)
            for point in self.points:
                painter.drawPoint(point)
            painter.setPen(self.pen_line)
            for index in range(len(self.points) - 1):
                painter.drawLine(QtCore.QLineF(self.points[index], self.points[index + 1]))
        if self.get_points_size() >= 3 and self.opt == "MultiBezier":
            path.moveTo(self.points[0])
            for index in range(1, len(self.points) - 2):
                start_point = self.points[index]
                ctrl_point = self.points[index + 1]
                end_point = QtCore.QPointF((self.points[index + 1] + self.points[index + 2]) / 2.0)
                path.quadTo(ctrl_point, end_point)
                path.moveTo(end_point)
                index = index + 2
            painter.setPen(self.pen_curve)
            painter.drawPath(path)
            self.rect = path.boundingRect()
            self.focusrect = path.boundingRect()
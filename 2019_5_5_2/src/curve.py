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
        self.isEditing=False
        #painting method
        self.parent = parent
        self.pen_point = QtGui.QPen(QtCore.Qt.blue, 5)
        self.pen_line = QtGui.QPen(QtCore.Qt.blue, 2,QtCore.Qt.SolidLine)
        self.pen_curve = QtGui.QPen(QtCore.Qt.red,3, QtCore.Qt.SolidLine)
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
    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget: None) -> None:
        painter.setRenderHints(QtGui.QPainter.Antialiasing)
        painter.setPen(self.pen_point)
        if self.isDrawingComplete==False or self.isHover==True or self.isSelected():
            #painter.drawPoint(self.parent.lastPoint)
            for point in self.points:
                painter.drawPoint(point)
            painter.setPen(self.pen_line)
            for index in range(len(self.points) - 1):
                painter.drawLine(QtCore.QLineF(self.points[index], self.points[index + 1]))
        if self.isSelected():
            self.drawFocusRect(painter)
    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        #super().mouseMoveEvent(event)
        if self.isEditing==True:
            print(self.selected_Point)
            self.points[self.selected_Point]=event.scenePos()
        self.update()

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        #super(Curve, self).mousePressEvent(event)
        self.update()
    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        #super().mouseReleaseEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            if self.isEditing == True:
                self.points[self.selected_Point] = event.scenePos()
                self.isEditing=False
    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        #super(Curve, self).mouseDoubleClickEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            for idx, point in enumerate(self.points):
                if (QtCore.QLineF(point, event.scenePos()).length() < 20.0):
                    self.selected_Point = idx
                    print("yes")
                    self.isEditing = True
                    break
    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.isHover=True

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.isHover=False

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
        super(QuadBezierCurve, self).paint(painter,option,widget)
        path = QtGui.QPainterPath()
        self.drawQuadBeizerCuve(painter, path)
    def drawQuadBeizerCuve(self,painter,path):
        if self.get_points_size() == 3:
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
        super(CubicBeizerCurve, self).paint(painter,option,widget)
        path = QtGui.QPainterPath()
        self.drawCubicBeizerCuve(painter, path)
    def drawCubicBeizerCuve(self, painter, path):
        if self.get_points_size() == 4:
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
        super(MultiBeizerCurve, self).paint(painter,option,widget)
        path = QtGui.QPainterPath()
        self.drawMultiBeizerCuve(painter, path)
    def drawMultiBeizerCuve(self, painter, path):
        if self.get_points_size() >= 3:
            path.moveTo(self.points[0])
            for index in range(1, len(self.points) - 2):
                start_point = self.points[index]
                ctrl_point = self.points[index + 1]
                end_point = QtCore.QPointF((start_point + ctrl_point) / 2.0)
                path.quadTo(start_point, end_point)
                path.moveTo(end_point)
            path.quadTo(self.points[-2],self.points[-1])
            painter.setPen(self.pen_curve)
            painter.drawPath(path)
            self.rect = path.boundingRect()
            self.focusrect = path.boundingRect()
    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Escape:
            print("Esc2")
            self.editMode=False
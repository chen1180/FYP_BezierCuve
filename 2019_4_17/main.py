from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np


class Bezier_Curve(QtWidgets.QMainWindow):
    DELTA = 10
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setGeometry(300, 300, 1080, 768)
        self.setAutoFillBackground(True)
        self.setWindowTitle("Bezier curve")
        self.show()
        self.pos = None
        self.setFixedSize(self.size())
        self.points = QtGui.QPolygon()
        self.draggin_idx = -1

    def distance_between_points(self, p1, p2):
        return ((p1.x() - p2.x()) ** 2 + (p1.y() + p2.y()) ** 2) ** 0.5

    def mousePressEvent(self, event) -> None:
        if (len(self.points) < 3):
            self.points.append(event.pos())
            self.update()
        if event.button() == QtCore.Qt.RightButton and self.draggin_idx == -1 and len(self.points) == 3:
            for index, point in enumerate(self.points):
                if self.distance_between_points(event.pos(), point) < self.DELTA:
                    self.draggin_idx = index

    def mouseMoveEvent(self, event) -> None:
        self.pos = event.pos()
        self.update()
        if self.draggin_idx != -1:
            self.points.setPoint(self.draggin_idx, event.pos().x(), event.pos().y())
            self.update()

    def mouseReleaseEvent(self,  event) -> None:
        if event.button() == QtCore.Qt.RightButton and self.draggin_idx != -1 and len(self.points) == 3:
            self.points.setPoint(self.draggin_idx, event.pos().x(), event.pos().y())
            self.draggin_idx = -1
            self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        if (len(self.points) == 1):
            qp.setPen(QtGui.QPen(QtCore.Qt.green, 3, QtCore.Qt.DotLine))
            qp.drawLine(self.points[0].x(), self.points[0].y(), self.pos.x(), self.pos.y())
        if (len(self.points) == 2):
            qp.setPen(QtGui.QPen(QtCore.Qt.green, 3, QtCore.Qt.DotLine))
            qp.drawLine(self.points[0].x(), self.points[0].y(), self.points[1].x(), self.points[1].y())
            qp.drawLine(self.points[0].x(), self.points[0].y(), self.pos.x(), self.pos.y())
            qp.drawLine(self.points[1].x(), self.points[1].y(), self.pos.x(), self.pos.y())
            qp.setPen(QtGui.QPen(QtCore.Qt.black, 3, QtCore.Qt.SolidLine))
            self.drawQuadBezierCurve(qp, self.points, self.pos)
        if (len(self.points) == 3):
            qp.setPen(QtGui.QPen(QtCore.Qt.green, 3, QtCore.Qt.DotLine))
            qp.drawLine(self.points[0].x(), self.points[0].y(), self.points[1].x(), self.points[1].y())
            qp.drawLine(self.points[0].x(), self.points[0].y(), self.points[2].x(), self.points[2].y())
            qp.drawLine(self.points[1].x(), self.points[1].y(), self.points[2].x(), self.points[2].y())
            qp.setPen(QtGui.QPen(QtCore.Qt.black, 3, QtCore.Qt.SolidLine))
            self.drawQuadBezierCurve(qp, self.points, self.points[-1])
        qp.setPen(QtGui.QPen(QtCore.Qt.red, 5, QtCore.Qt.DotLine))
        for point in self.points:
            qp.drawPoint(point.x(), point.y())
            qp.drawText(point.x(), point.y(), "({},{})".format(point.x(), point.y()))
        qp.end()

    def drawQuadBezierCurve(self, qp, endPoints, controlPoints):
        path = QtGui.QPainterPath()
        points_x = []
        points_y = []
        for t in np.linspace(0, 1, 100, dtype='float'):
            points_x.append(
                (1 - t) ** 2 * endPoints[0].x() + 2 * (1 - t) * t * controlPoints.x() + t ** 2 * endPoints[1].x())
            points_y.append(
                (1 - t) ** 2 * endPoints[0].y() + 2 * (1 - t) * t * controlPoints.y() + t ** 2 * endPoints[1].y())
        path.moveTo(endPoints[0].x(), endPoints[0].y())
        for index in range(len(points_x)):
            path.lineTo(points_x[index], points_y[index])
            qp.drawPath(path)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    ex = Bezier_Curve()
    app.exec_()
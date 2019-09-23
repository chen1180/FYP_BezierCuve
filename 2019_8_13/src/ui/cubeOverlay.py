import sys
import math, random

from PyQt5.QtCore import (QPoint, QPointF, QRect, QRectF, QSize, Qt, QTime,
        QTimer)
from PyQt5.QtGui import (QBrush, QColor, QFontMetrics, QImage, QPainter,
        QRadialGradient, QSurfaceFormat,QPaintEvent)
from PyQt5.QtWidgets import QApplication, QGraphicsView,QGraphicsScene

import OpenGL.GL as gl

class cubeRotator(QGraphicsView):
    def __init__(self):
        super(cubeRotator, self).__init__()
        self.setWindowTitle("Rotate")
        self.scene=QGraphicsScene()
        self.setScene(self.scene)
        self.scene.addSimpleText("Asd")

    def drawBubble(self, painter:QPainter):
        painter.save()
        radius=20
        backgroundRect=QRect(0,0,100,100)
        painter.drawRect(0,0,150,150)
        painter.drawEllipse(100, 50, radius, radius)
        painter.drawEllipse(150, 100, radius, radius)
        painter.drawEllipse(100, 150 ,radius, radius)
        painter.drawEllipse(50, 100, radius, radius)
        painter.restore()

    def rect(self):
        return QRectF(self.position.x() - self.radius,
                self.position.y() - self.radius, 2 * self.radius,
                2 * self.radius)

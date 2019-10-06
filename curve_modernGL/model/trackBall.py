from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import math
class Trackball(QObject):
    def __init__(self,cameraPos:QVector3D,center:QVector3D,WorldUp:QVector3D):
        self.cameraPos=cameraPos
        self.center=center
        self.WorldUp=WorldUp
        #camera state
        self.m_pressed=False
        self.m_rotation=QQuaternion()
        self.m_lastPos=QPointF()
    def updateCamera(self):
        pass
    def pushMiddleButton(self,p:QPointF):
        self.m_pressed=True
        self.m_lastPos=p
    def moveMiddleButton(self,p:QPointF):
        if self.m_pressed==False:
            return
        lastPos3D=QVector3D(self.m_lastPos.x(),self.m_lastPos.y(),0)
        sqrZ=1-QVector3D.dotProduct(lastPos3D,lastPos3D)
        if sqrZ>0:
            lastPos3D.setZ(math.sqrt(sqrZ))
        else:
            lastPos3D.normalize()
        currentPos3D = QVector3D(p.x(), p.y(), 0)
        sqrZ = 1 - QVector3D.dotProduct(currentPos3D, currentPos3D)
        if sqrZ > 0:
            currentPos3D.setZ(math.sqrt(sqrZ))
        else:
            currentPos3D.normalize()
        axis=QVector3D.crossProduct(lastPos3D,currentPos3D)
        angle=math.degrees(math.asin(axis.length()))
        axis.normalize()
        self.m_rotation=QQuaternion.fromAxisAndAngle(axis,angle)*self.m_rotation
        self.m_lastPos=p
    def releaseMiddleButton(self):
        self.m_pressed=False



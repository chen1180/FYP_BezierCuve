from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import math
class Trackball(QObject):
    def __init__(self,cameraPos:QVector3D,center:QVector3D,WorldUp:QVector3D):
        self.cameraPos=cameraPos
        self.center=center
        self.WorldUp=WorldUp
        self.zoomFactor=1.0
        #camera state
        self.m_rotationTrigger=False
        self.m_panningTrigger=False
        self.m_rotation=QQuaternion()
        self.m_lastPos=QPointF()
    def updateCamera(self):
        pass
    # camera rotation
    def pushMiddleButton(self,p:QPointF):
        self.m_rotationTrigger=True
        self.m_lastPos=p
    def moveMiddleButton(self,p:QPointF):
        if self.m_rotationTrigger==False:
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
        #update camera position
        self.cameraPos=self.m_rotation.vector()+self.center
    def releaseMiddleButton(self):
        self.m_rotationTrigger=False
    #camera panning
    def pushRightButton(self,p:QPointF):
        self.m_panningTrigger = True
        self.m_lastPos = p
    def moveRightButton(self,p:QPointF):
        if self.m_panningTrigger==False:
            return
        oldCenter3D = QVector3D(self.m_lastPos.x(), self.m_lastPos.y(), 0)
        sqrZ = 1 - QVector3D.dotProduct(oldCenter3D, oldCenter3D)
        if sqrZ > 0:
            oldCenter3D.setZ(math.sqrt(sqrZ))
        else:
            oldCenter3D.normalize()
        newCenter3D = QVector3D(p.x(), p.y(), 0)
        sqrZ = 1 - QVector3D.dotProduct(newCenter3D, newCenter3D)
        if sqrZ > 0:
            newCenter3D.setZ(math.sqrt(sqrZ))
        else:
            newCenter3D.normalize()
        transVec=newCenter3D-oldCenter3D
        # self.cameraPos+=transVec*0.01
        self.center+=transVec.normalized()
        self.m_lastPos = p
    def releaseRightButton(self):
        self.m_panningTrigger=False


    #camere zooming
    def moveMiddleScroller(self,angleDelta):
        numStep=angleDelta/1200
        self.zoomFactor +=numStep
        if self.zoomFactor>=5:
            self.zoomFactor=5
        if self.zoomFactor<=0.5:
            self.zoomFactor=0.5
        delta=(self.cameraPos-self.center).normalized()
        self.cameraPos=self.zoomFactor*delta







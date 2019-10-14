from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import math
class Trackball(QObject):
    def __init__(self,cameraPos:QVector3D,targetPos:QVector3D,WorldUp:QVector3D):
        self.cameraPos=cameraPos
        self.targetPos=targetPos
        self.cameraUp=WorldUp
        self.radius=(self.cameraPos-self.targetPos).length()
        #camera state
        self.m_rotationTrigger=False
        self.m_panningTrigger=False
        self.m_rotation=QQuaternion()
        self.m_lastPos=QPointF()
        self.sensitivity=2.5

    def updateCamera(self,rotation):
        RotationMatrix = QMatrix4x4()
        RotationMatrix.rotate(rotation)
        '''
                        RightX      RightY      RightZ      0
                        UpX         UpY         UpZ         0
                        LookX       LookY       LookZ       0
                        PosX        PosY        PosZ        1
        '''
        ViewMatrix = RotationMatrix.data()
        viewDir = QVector3D(ViewMatrix[8], ViewMatrix[9], ViewMatrix[10])
        #update camera position
        self.cameraPos = viewDir * self.radius + self.targetPos
        self.cameraUp = QVector3D(ViewMatrix[4], ViewMatrix[5], ViewMatrix[6])

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
        if lastPos3D!= currentPos3D:

            axis=QVector3D.crossProduct(lastPos3D,currentPos3D).normalized()
            angle=math.degrees(math.acos(QVector3D.dotProduct(lastPos3D,currentPos3D)))

            for i in range(10):
                previousRotation=self.m_rotation
                nextRotation=QQuaternion.fromAxisAndAngle(axis,angle*self.sensitivity)*self.m_rotation
                rotation=QQuaternion.slerp(previousRotation,nextRotation,i/9)
                self.updateCamera(rotation)
            self.m_rotation=QQuaternion.fromAxisAndAngle(axis,angle*self.sensitivity)*self.m_rotation
            self.m_lastPos = p


    def releaseMiddleButton(self,p:QPointF):
        self.m_rotationTrigger=False

    #camera panning
    def pushRightButton(self,p:QPointF):
        self.m_panningTrigger = True
        self.m_lastPos = p
    def moveRightButton(self,p:QPointF):
        if self.m_panningTrigger==False:
            return
        dx = (p - self.m_lastPos).x()
        dy = (p - self.m_lastPos).y()
        look = self.cameraPos-self.targetPos
        right = QVector3D.crossProduct(look, self.cameraUp).normalized()
        up = QVector3D.crossProduct(look, right).normalized()
        # self.cameraPos+=transVec
        self.targetPos+= (right * dx + up * dy)
        self.m_lastPos = p
        self.updateCamera(self.m_rotation)
    def releaseRightButton(self):
        self.m_panningTrigger=False

    #camere zooming
    def moveMiddleScroller(self,angleDelta):
        if angleDelta>0:
            self.radius+=1
        else:
            self.radius-=1
        if self.radius<=0.5:
            self.radius=0.5
        if self.radius>=20:
            self.radius=20
        self.updateCamera(self.m_rotation)






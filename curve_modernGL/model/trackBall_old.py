from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import math
class Trackball(QObject):
    def __init__(self,target:QVector3D,radius:float,theta:float,phi:float):
        self.m_target=target
        self.m_radius=radius
        self.m_theta=theta
        self.m_phi=phi
        self.m_position = self.ToCartesian()
        #camera state
        self.m_rotationTrigger=False
        self.m_panningTrigger=False
        self.m_lastPos=QPointF()
    # camera rotation
    def pushRightButton(self,p:QPointF):
        self.m_rotationTrigger=True
        self.m_lastPos=p
    def moveRightButton(self,p:QPointF):
        if self.m_rotationTrigger==False:
            return
        dPhi = (self.m_lastPos.y() - p.y())
        dTheta =( p.x()-self.m_lastPos.x())
        self.m_phi+=dPhi
        self.m_theta+=dTheta
        self.m_position=self.ToCartesian()
        self.m_lastPos=p
    def releaseRightButton(self):
        self.m_rotationTrigger=False
    #camera panning
    def pushMiddleButton(self,p:QPointF):
        self.m_panningTrigger = True
        self.m_lastPos = p
    def moveMiddleButton(self,p:QPointF):
        if self.m_panningTrigger==False:
            return
        dx=(p-self.m_lastPos).x()
        dy=(p-self.m_lastPos).y()

        look=self.ToCartesian().normalized()
        wordUp=QVector3D(0,1,0)
        right=QVector3D.crossProduct(look,wordUp)
        up=QVector3D.crossProduct(look,right)
        self.m_target+=right*dx+up*dy
        self.m_lastPos = p
    def releaseMiddleButton(self):
        self.m_panningTrigger=False

    #camere zooming
    def moveMiddleScroller(self,angleDelta):
        numStep=angleDelta/1200
        if self.m_radius>=5:
            self.m_radius=5
        if self.m_radius<=1:
            self.m_radius=1
        self.m_radius+=numStep
        self.ToCartesian()
        print(self.m_radius)

    def ToCartesian(self):
        x = self.m_radius * math.sin(self.m_phi) * math.sin(self.m_theta)
        y = self.m_radius *  math.cos(self.m_phi)
        z = self.m_radius * math.sin(self.m_phi) * math.cos(self.m_theta)
        return QVector3D(x,y,z)





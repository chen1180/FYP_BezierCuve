from geometry import point
from OpenGL.GLU import gluLookAt,gluPerspective,gluOrtho2D
from numpy import cos,sin,radians,cross
class Camera:
    def __init__(self,_targetPos=point(0,0,0),_up=1.0,_theta=90,_phi=45,radius=1.0,_fov=45):
        self.targetPos=_targetPos
        self.up=_up
        self.radius=radius
        self.theta=_theta
        self.phi=_phi
        self.viewNeedUpdate=False
        self.fov=_fov
    def updateViewMatrix(self):
        gluLookAt(self.getCameraPosition().x, self.getCameraPosition().y, self.getCameraPosition().z,self.targetPos.x, self.targetPos.y, self.targetPos.z,0, self.up, 0)
    def updatePerspectiveMatrix(self,width,height,znear=0.1,zfar=100):
        gluPerspective(self.fov,width/height,znear,zfar )
    def updateOrthoMatrix(self,width,height):
        gluOrtho2D(0,width,0,height)
    def getView(self):
        if self.viewNeedUpdate:
            self.updateViewMatrix()
            self.viewNeedUpdate=False
    def pan(self,dx,dy):
        self.viewNeedUpdate = True
        look = self.normalize(self.targetPos-self.getCameraPosition())
        right = self.cross(look, point(0.0,self.up,0.0))
        up = self.cross(look, right)
        self.targetPos += right * dx * 0.01 + up * dy * 0.01
    def rotate(self,dTheta,dPhi):
        self.viewNeedUpdate = True
        if self.up>0:
            self.theta+=dTheta
        else:
            self.theta-=dTheta
        self.phi+=dPhi
        if self.phi>89:
            self.phi=89
        elif self.phi<-89:
            self.phi=-89
        if (self.phi>0 and self.phi<180) or (self.phi<-180 and self.phi>-360):
            self.up=1.0
        else:
            self.up=-1.0
    def zoom(self,distance):
        self.viewNeedUpdate = True
        self.radius-=distance
        if self.radius<=0:
            self.radius=2
            look = self.normalize(self.targetPos-self.getCameraPosition())
            self.targetPos+=look*self.radius
    def getCameraPosition(self):
        return self.toCardesian()+self.targetPos
    def toCardesian(self):
        x=self.radius*sin(radians(self.phi))*cos(radians(self.theta))
        y=self.radius*cos(radians(self.theta))
        z=self.radius*sin(radians(self.phi))*sin(radians(self.theta))
        return point(x,y,z)
    def normalize(self,p):
        length = (p[0] ** 2 + p[1] ** 2 + p[2] ** 2) ** 0.5
        return p*(1/length)
    def cross(self,p1,p2):
        p=cross(p1.components(),p2.components())
        return point.with_components(p)



from geometry import point
from OpenGL.GLU import gluLookAt,gluPerspective,gluOrtho2D
from OpenGL.GL import *
from numpy import cos,sin,radians,cross,sqrt,pi,arccos
import math
class Arcball:
    def __init__(self):
        self.lastPos=point(0,0,0)
        self.curPos=point(0,0,0)
        self.lookatCenter=point(0,0,0)
        self.scale=1.0
        self.angle=0
        self.axis=point(0,1,0)
        self.trackingMouse=False
        self.scrollMouse=False
        self.pan=False
        self.redrawContinue=False

    def cross(self, p1, p2):
        p = cross(p1.components(), p2.components())
        return point.with_components(p)
    def screenToSpherical(self,x,y,width,height):
        xPos=(2*x-width)/width
        yPos=(height-2*y)/height
        d=(xPos**2+yPos**2)**0.5
        zPos=cos(pi/2*(d if d<1 else 1))
        normalLength=1.0/(xPos**2+yPos**2+zPos**2)**0.5
        return point(xPos,yPos,zPos)*normalLength
    def startPan(self,x,y,width,height):
        self.pan=True
        self.lastPos=self.screenToSpherical(x,y,width,height)
        print("pan start")
    def stopPan(self,x,y,width,height):
        self.pan=False
        print("pan stop")
    def mousePan(self,x,y,width,height,dx,dy):
        if self.pan:
            self.curPos = self.screenToSpherical(x, y, width, height)
            look = self.normalize(self.curPos - self.lookatCenter)
            right = self.cross(look, point(0.0, 1.0, 0.0))
            up = self.cross(look, right)
            self.lookatCenter += right *0.01*dx + up *0.01*dy
    def mouseMotion(self,x,y,width,height):
        if self.trackingMouse:
            m_magic_number=1.1# this number is used to avoid the case p1-p2=0 where math value erro may occur in ratateAngle
            self.curPos=self.screenToSpherical(m_magic_number*x,m_magic_number*y,width,height)
            p1=self.normalize(self.lastPos-self.lookatCenter)
            p2=self.normalize(self.curPos-self.lookatCenter)
            rotateAxis=point.cross(p1,p2)
            rotateAngle=math.acos(point.dot(p1,p2))*0.5
            self.angle=rotateAngle
            self.axis=rotateAxis
    def mouseScroll(self,y):
        if y:
            self.scrollMouse=True
            self.scale+=y*0.001
            if self.scale<0.1:
                self.scale<0.1
    def startMotion(self,x,y,winWidth,winHeight):
        self.trackingMouse=True
        self.redrawContinue=False
        self.lastPos=self.screenToSpherical(x,y,winWidth,winHeight)
    def stopMotion(self,x,y,winWidth,winHeight):
        self.trackingMouse=False
        if self.lastPos.x!=x and self.lastPos.y!=y:
            self.redrawContinue=True
        else:
            self.angle=0
            self.redrawContinue=False
    def cameraUpdate(self):
        m = glGetFloatv(GL_MODELVIEW_MATRIX)
        glLoadIdentity()
        if self.pan:
            glTranslatef(self.lookatCenter.x,self.lookatCenter.y,self.lookatCenter.z)
            self.lookatCenter=point(0,0,0)
        if self.scrollMouse:
            glScalef(self.scale, self.scale, self.scale)
            self.scrollMouse=False
            self.scale=1.0
        if self.trackingMouse:
            glRotatef(self.angle,self.axis.x,self.axis.y,self.axis.z)
        glMultMatrixf(m)
    def normalize(self, p):
        length = (p[0] ** 2 + p[1] ** 2 + p[2] ** 2) ** 0.5
        return p * (1 / length)

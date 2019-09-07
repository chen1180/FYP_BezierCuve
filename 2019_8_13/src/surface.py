from curve import BezierCurve,BSpline
from OpenGL.GL import *
import numpy as np
from geometry import surface,point
class BeizerSurface(BezierCurve):
    def __init__(self,controlPoints=[],divs=100,showPolygon=False):
        self.controlPoints=controlPoints.copy()
        self.dlbPatch=None
        self.showPolygon=showPolygon
        self.divs=divs
        self.texture=0
    def genBezierSurface(self):
        drawList=glGenLists(1)
        last=[None]*(self.divs+1)
        if self.dlbPatch:
            glDeleteLists(self.dlbPatch,1)
        temp=[row[3] for row in self.controlPoints]
        for v in range(self.divs+1):
            px=v/self.divs
            last[v]=self.deCasteljauCubic(temp[0],temp[1],temp[2],temp[3],px)
        glNewList(drawList,GL_COMPILE)
        glBindTexture(GL_TEXTURE_2D,self.texture)
        for u in range(1,self.divs+1):
            py=u/self.divs
            pyold=(u-1)/self.divs
            temp[0]=self.deCasteljauCubic(self.controlPoints[0][3],self.controlPoints[0][2],self.controlPoints[0][1],self.controlPoints[0][0],py)
            temp[1] = self.deCasteljauCubic(self.controlPoints[1][3],self.controlPoints[1][2],self.controlPoints[1][1],self.controlPoints[1][0],py)
            temp[2] = self.deCasteljauCubic(self.controlPoints[2][3],self.controlPoints[2][2],self.controlPoints[2][1],self.controlPoints[2][0],py)
            temp[3] = self.deCasteljauCubic(self.controlPoints[3][3],self.controlPoints[3][2],self.controlPoints[3][1],self.controlPoints[3][0],py)
            glColor3f(0,0.5,0.5)
            glBegin(GL_TRIANGLE_STRIP)
            for v in range(self.divs+1):
                px = v / self.divs
                glTexCoord2f(pyold,px)
                glVertex3f(last[v].x,last[v].y,last[v].z)
                last[v]=self.deCasteljauCubic(temp[0],temp[1],temp[2],temp[3],px)
                glTexCoord2f(py,px)
                glVertex3f(last[v].x,last[v].y,last[v].z)
            glEnd()
        glEndList()
        del last
        return drawList
    def genMesh(self):
        if self.showPolygon==True:
            glDisable(GL_TEXTURE_2D)
            for i in range(0,4):
                glColor3f(1.0, 1.0, 1.0)
                glBegin(GL_LINE_STRIP)
                for j in range(0,4):
                    glVertex3f(self.controlPoints[i][j].x,self.controlPoints[i][j].y,self.controlPoints[i][j].z)
                glEnd()
            for i in range(0,4):
                glBegin(GL_LINE_STRIP)
                for j in range(0,4):
                    glVertex3f(self.controlPoints[j][i].x,self.controlPoints[j][i].y,self.controlPoints[j][i].z)
                glEnd()
            glEnable(GL_TEXTURE_2D)
    def changeDivs(self,new_divs):
        self.divs=new_divs
    @classmethod
    def drawBeizerSurface(cls):
        glMatrixMode(GL_MODELVIEW)
        glColor3f(0.5, 0.5, 0.5)
        glPushMatrix()
        control_points = [[[-0.25, 0.0, -0.5], [0, 0, 0.0], [0.25, -0.2, 0.0], [0.5, 0.2, 0.0]],
                          [[-0.5, -0.5, 0.0], [0, -0.9, 0.0], [0.25, -0.2, 2.0], [0.5, -0.6, 0.0]]]
        glMap2f(GL_MAP2_VERTEX_3, 0, 1, 0, 1, control_points)
        glEnable(GL_MAP2_VERTEX_3)
        # glMapGrid2f(50, 0, 1, 50, 0, 1)
        # glEvalMesh2(GL_LINE, 0, 50, 0, 50)
        glPointSize(5)
        glColor3f(1, 1, 1)
        glBegin(GL_POINTS)
        for line in control_points:
            for point in line:
                glVertex3f(point[0], point[1], point[2])
        glEnd()
        glPopMatrix()
class BSplineSurface(BSpline):
    def __init__(self,controlPoints=[],divs=100,showPolygon=False):
        self.controlPoints=controlPoints.copy()
        self.divs=divs
        self.dlbPatch = None
        self.showPolygon=showPolygon
        self.texture=0
    def genBSplineSurface(self):
        drawList=glGenLists(1)
        if self.dlbPatch:
            glDeleteLists(self.dlbPatch,1)
        last=[None]*(self.divs)
        temp=[row[0] for row in self.controlPoints]
        order=3
        tmin = 0
        tmax = order
        self.uKnots=self.createClampedUniformKnots(5,order)
        self.vKnots = self.createClampedUniformKnots(5, order)
        steps = float((tmax - tmin) / (self.divs - 1))
        for v in range(self.divs):
            px=tmin+v*steps
            last[v]=self.getBSplinePoint(px,temp,order,self.vKnots)
        glNewList(drawList,GL_COMPILE)
        glBindTexture(GL_TEXTURE_2D,self.texture)
        for u in range(1,self.divs):
            py=tmin+u*steps
            pyold=tmin+(u-1)*steps
            for i,row in enumerate(self.controlPoints):
                temp[i]=self.getBSplinePoint(py,row,order,self.uKnots)
            glColor3f(0,py/tmax,0)
            glBegin(GL_LINE_STRIP)
            for v in range(self.divs):
                px =tmin+v*steps
                glTexCoord2f(pyold,px)
                glVertex3f(last[v].x,last[v].y,last[v].z)
                last[v]=self.getBSplinePoint(px,temp,order,self.vKnots)
                glColor3f(px/ tmax, 0, 0)
                glTexCoord2f(py,px)
                glVertex3f(last[v].x,last[v].y,last[v].z)
            glEnd()
            break
        glEndList()
        del last
        return drawList
    def genMesh(self):
        if self.showPolygon==True:
            glDisable(GL_TEXTURE_2D)
            for i in range(0,4):
                glColor3f(1.0, 1.0, 1.0)
                glBegin(GL_LINE_STRIP)
                for j in range(0,4):
                    glVertex3f(self.controlPoints[i][j].x,self.controlPoints[i][j].y,self.controlPoints[i][j].z)
                glEnd()
            for i in range(0,4):
                glBegin(GL_LINE_STRIP)
                for j in range(0,4):
                    glVertex3f(self.controlPoints[j][i].x,self.controlPoints[j][i].y,self.controlPoints[j][i].z)
                glEnd()
            glEnable(GL_TEXTURE_2D)
    def genPolygon(self):
        print(self.columns)

if __name__ == '__main__':
    a=BSplineSurface(surface.convertListToPoint(
            [[[-0.75, -0.75, -0.50], [-0.25, -0.75, 0.00], [0.25, -0.75, 0.00], [0.75, -0.75, -0.50]],
             [[-0.75, -0.25, -0.75], [-0.25, -0.25, 0.50], [0.25, -0.25, 0.50], [0.75, -0.25, -0.75]],
             [[-0.75, 0.25, 0.00], [-0.25, 0.25, -0.50], [0.25, 0.25, -0.50], [0.75, 0.25, 0.00]],
             [[-0.75, 0.75, -0.50], [-0.25, 0.75, -1.00], [0.25, 0.75, -1.00], [0.75, 0.75, -0.50]]]))
    a.genBSplineSurface()
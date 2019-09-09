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
        drawList = glGenLists(1)
        last = [None] * (self.divs+1)
        if self.dlbPatch:
            glDeleteLists(self.dlbPatch, 1)
        temp = [row[0] for row in self.controlPoints]
        for v in range(self.divs+1):
            px = v / self.divs
            last[v] = self.bersteinPolynomial(px,temp)
        glNewList(drawList, GL_COMPILE)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        for u in range(1, self.divs+1 ):
            py = u / self.divs
            pyold = (u - 1) / self.divs
            for idx,row in enumerate(self.controlPoints):
                temp[idx]=self.bersteinPolynomial(py,row)
            glColor3f(0, 0.5, 0.5)
            glBegin(GL_TRIANGLE_STRIP)
            for v in range(self.divs+1):
                px = v / self.divs
                glTexCoord2f(pyold, px)
                glVertex3f(last[v].x, last[v].y, last[v].z)
                last[v] = self.bersteinPolynomial(px,temp)
                glTexCoord2f(py, px)
                glVertex3f(last[v].x, last[v].y, last[v].z)
            glEnd()
        glEndList()
        del last
        return drawList
    def genMesh(self):
        if self.showPolygon == True:
            glDisable(GL_TEXTURE_2D)
            for i in range(len(self.controlPoints)):
                glColor3f(1.0, 1.0, 1.0)
                glBegin(GL_LINE_STRIP)
                for j in range(len(self.controlPoints[0])):
                    glVertex3f(self.controlPoints[i][j].x, self.controlPoints[i][j].y, self.controlPoints[i][j].z)
                glEnd()
            for i in range(len(self.controlPoints[0])):
                glBegin(GL_LINE_STRIP)
                for j in range(len(self.controlPoints)):
                    glVertex3f(self.controlPoints[j][i].x, self.controlPoints[j][i].y, self.controlPoints[j][i].z)
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
    def __init__(self,controlPoints,order,divs=100,knotsType="Clamped",showPolygon=False):
        self.controlPoints=controlPoints.copy()
        self.divs=divs
        self.dlbPatch = None
        self.showPolygon=showPolygon
        self.texture=0
        self.knotsType=knotsType
        self.order=order
    def genKnotsTypeSurface(self):
        if self.knotsType=="Clamped":
            self.dlbPatch= self.genClampedBSplineSurface()
        elif  self.knotsType=="Open":
            self.dlbPatch=self.genOpenBSplineSurface()
        elif  self.knotsType=="Closed":
            self.dlbPatch=self.genClosedBSplineSurface()
    def genClampedBSplineSurface(self):
        drawList=glGenLists(1)
        if self.dlbPatch:
            glDeleteLists(self.dlbPatch,1)
        last=[None]*(self.divs)
        temp=[row[0] for row in self.controlPoints]
        self.uKnots = self.createClampedUniformKnots(len(self.controlPoints[0]), self.order)
        self.vKnots = self.createClampedUniformKnots(len(self.controlPoints), self.order)
        vmin = self.vKnots[self.order]
        vmax = self.vKnots[len(self.controlPoints)]
        vsteps = float((vmax - vmin) / (self.divs - 1))
        umin = self.uKnots[self.order]
        umax = self.uKnots[len(self.controlPoints[0])]
        usteps = float((umax - umin) / (self.divs - 1))
        for v in range(self.divs):
            px=vmin+v*vsteps
            coeff = self.computeClampedCofficient(len(temp), self.order, px, self.vKnots)
            last[v] = self.getBSplinePoint(coeff, temp)
        glColor3f(0,1,1)
        glNewList(drawList,GL_COMPILE)
        glBindTexture(GL_TEXTURE_2D,self.texture)
        for u in range(1,self.divs):
            py=umin+u*usteps
            pyold=umin+(u-1)*usteps
            for i,row in enumerate(self.controlPoints):
                coeff = self.computeClampedCofficient(len(row), self.order, py, self.uKnots)
                temp[i]=self.getBSplinePoint(coeff,row)
            glBegin(GL_TRIANGLE_STRIP)
            for v in range(self.divs):
                px =vmin+v*vsteps
                glTexCoord2f(pyold,px)
                glVertex3f(last[v].x,last[v].y,last[v].z)
                coeff = self.computeClampedCofficient(len(temp), self.order, px, self.vKnots)
                last[v]=self.getBSplinePoint(coeff,temp)
                glColor3f(px/ vmax, py/ vmax, 0)
                glTexCoord2f(py,px)
                glVertex3f(last[v].x,last[v].y,last[v].z)
            glEnd()
        glEndList()
        del last
        return drawList
    def genOpenBSplineSurface(self):
        drawList = glGenLists(1)
        if self.dlbPatch:
            glDeleteLists(self.dlbPatch, 1)
        last = [None] * (self.divs)
        temp = [row[0] for row in self.controlPoints]
        self.uKnots = self.createOpenUniformKnots(len(self.controlPoints[0]), self.order)
        self.vKnots = self.createOpenUniformKnots(len(self.controlPoints), self.order)
        vmin = self.vKnots[self.order]
        vmax = self.vKnots[len(self.controlPoints)]
        vsteps = float((vmax - vmin) / (self.divs - 1))
        umin = self.uKnots[self.order]
        umax = self.uKnots[len(self.controlPoints[0])]
        usteps = float((umax - umin) / (self.divs - 1))
        for v in range(self.divs):
            px = vmin + v * vsteps
            coeff = self.computeOpenCofficient(len(temp), self.order, px, self.vKnots)
            last[v] = self.getBSplinePoint(coeff, temp)
        glColor3f(0, 1, 1)
        glNewList(drawList, GL_COMPILE)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        for u in range(1, self.divs):
            py = umin + u * usteps
            pyold = umin + (u - 1) * usteps
            for i, row in enumerate(self.controlPoints):
                coeff = self.computeOpenCofficient(len(row), self.order, py, self.uKnots)
                temp[i] = self.getBSplinePoint(coeff, row)
            glBegin(GL_TRIANGLE_STRIP)
            for v in range(self.divs):
                px = vmin + v * vsteps
                glTexCoord2f(pyold, px)
                glVertex3f(last[v].x, last[v].y, last[v].z)
                coeff = self.computeOpenCofficient(len(temp), self.order, px, self.vKnots)
                last[v] = self.getBSplinePoint(coeff, temp)
                glColor3f(px / vmax, py / vmax, 0)
                glTexCoord2f(py, px)
                glVertex3f(last[v].x, last[v].y, last[v].z)
            glEnd()
        glEndList()
        del last
        return drawList

    def genClosedBSplineSurface(self):
        drawList = glGenLists(1)
        if self.dlbPatch:
            glDeleteLists(self.dlbPatch, 1)
        last = [None] * (self.divs)
        print("before")
        for row in self.controlPoints:
            print(row)
        for i in range(self.order):
                self.controlPoints.append(self.controlPoints[i])
        print("after")
        for row in self.controlPoints:
            print(row)
        temp = [row[0] for row in self.controlPoints]
        self.uKnots = self.createClosedUniformKnots(len(self.controlPoints[0]), self.order)
        self.vKnots = self.createClosedUniformKnots(len(self.controlPoints), self.order)
        vmin = self.vKnots[self.order]
        vmax = self.vKnots[len(self.controlPoints)]
        vsteps = float((vmax - vmin) / (self.divs - 1))
        umin = self.uKnots[self.order]
        umax = self.uKnots[len(self.controlPoints[0])]
        usteps = float((umax - umin) / (self.divs - 1))
        for v in range(self.divs):
            px = vmin + v * vsteps
            coeff = self.computeOpenCofficient(len(temp), self.order, px, self.vKnots)
            last[v] = self.getBSplinePoint(coeff, temp)
        glColor3f(0, 1, 1)
        glNewList(drawList, GL_COMPILE)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        for u in range(1, self.divs):
            py = umin + u * usteps
            pyold = umin + (u - 1) * usteps
            for i, row in enumerate(self.controlPoints):
                coeff = self.computeOpenCofficient(len(row), self.order, py, self.uKnots)
                temp[i] = self.getBSplinePoint(coeff, row)
            glBegin(GL_TRIANGLE_STRIP)
            for v in range(self.divs):
                px = vmin + v * vsteps
                glTexCoord2f(pyold, px)
                glVertex3f(last[v].x, last[v].y, last[v].z)
                coeff = self.computeOpenCofficient(len(temp), self.order, px, self.vKnots)
                last[v] = self.getBSplinePoint(coeff, temp)
                glColor3f(px / vmax, py / vmax, 0)
                glTexCoord2f(py, px)
                glVertex3f(last[v].x, last[v].y, last[v].z)
            glEnd()
        glEndList()
        del last
        return drawList
    def genMesh(self):
        if self.showPolygon==True:
            glDisable(GL_TEXTURE_2D)
            for i in range(len(self.controlPoints)):
                glColor3f(1.0, 1.0, 1.0)
                glBegin(GL_LINE_STRIP)
                for j in range(len(self.controlPoints[0])):
                    glVertex3f(self.controlPoints[i][j].x,self.controlPoints[i][j].y,self.controlPoints[i][j].z)
                glEnd()
            for i in range(len(self.controlPoints[0])):
                glBegin(GL_LINE_STRIP)
                for j in range(len(self.controlPoints)):
                    glVertex3f(self.controlPoints[j][i].x,self.controlPoints[j][i].y,self.controlPoints[j][i].z)
                glEnd()
            glEnable(GL_TEXTURE_2D)

if __name__ == '__main__':
    a=BSplineSurface(surface.convertListToPoint(
            [[[-0.75, -0.75, -0.50], [-0.25, -0.75, 0.00], [0.25, -0.75, 0.00], [0.75, -0.75, -0.50]],
             [[-0.75, -0.25, -0.75], [-0.25, -0.25, 0.50], [0.25, -0.25, 0.50], [0.75, -0.25, -0.75]],
             [[-0.75, 0.25, 0.00], [-0.25, 0.25, -0.50], [0.25, 0.25, -0.50], [0.75, 0.25, 0.00]],
             [[-0.75, 0.75, -0.50], [-0.25, 0.75, -1.00], [0.25, 0.75, -1.00], [0.75, 0.75, -0.50]]]))
    a.genBSplineSurface()
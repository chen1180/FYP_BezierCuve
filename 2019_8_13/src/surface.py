from curve import BezierCurve,BSpline
from OpenGL.GL import *
from geometry import surface,point
from PyQt5 import QtGui,QtWidgets,QtCore
import numpy as np
from PIL import Image

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
    def __init__(self,controlPoints,order,divs=100,knotsType="Clamped",texturePath=None,showTexture=False):
        self.controlPoints=controlPoints.copy()
        self.divs=divs
        self.showTexture=showTexture
        self.knotsType=knotsType
        self.order=order
        self.curvePoints=[]
        self.dlbPatch =self.getBSplineSurfacePoints()
        self.texture = None
        self.texturePath=texturePath
    def readTexture(self,path):
        img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(list(img.getdata()), np.uint8)
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        # Texture parameters are part of the texture object, so you need to
        # specify them only once for a given texture object.
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glBindTexture(GL_TEXTURE_2D, 0)
        return texture
    def genClampedBSplineSurface(self):
        drawList=glGenLists(1)
        if self.dlbPatch:
            glDeleteLists(self.dlbPatch,1)
        glNewList(drawList, GL_COMPILE)
        if self.showTexture and self.texturePath:
            if self.texture is None:
                self.texture = self.readTexture(self.texturePath)
                self.drawTexture()
        glDisable(GL_TEXTURE_2D)
        for i in range(len(self.curvePoints)):
            glColor3f(1.0, 1.0, 1.0)
            glBegin(GL_LINE_STRIP)
            for j in range(len(self.curvePoints[0])):
                glVertex3f(self.curvePoints[i][j].x, self.curvePoints[i][j].y, self.curvePoints[i][j].z)
            glEnd()
        for i in range(len(self.curvePoints[0])):
            glBegin(GL_LINE_STRIP)
            for j in range(len(self.curvePoints)):
                glVertex3f(self.curvePoints[j][i].x, self.curvePoints[j][i].y, self.curvePoints[j][i].z)
            glEnd()
        glEnable(GL_TEXTURE_2D)
        glEndList()

        return drawList
    def getBSplineSurfacePoints(self):
        print("original row")
        for row in self.controlPoints:
            print(row)
        last = [None] * (self.divs)
        temp = [row[0] for row in self.controlPoints]
        if self.knotsType=="Clamped":
            self.uKnots = self.createClampedUniformKnots(len(self.controlPoints[0]), self.order)
            self.vKnots = self.createClampedUniformKnots(len(self.controlPoints), self.order)
        elif self.knotsType=="Closed":
            try:
                for row in range(len(self.controlPoints)):
                    for i in range(self.order):
                        self.controlPoints[row].append(self.controlPoints[row][i])
                print("closed loop row")
                for row in self.controlPoints:
                    print(row)
                self.uKnots = self.createOpenUniformKnots(len(self.controlPoints[0]), self.order)
                self.vKnots = self.createClampedUniformKnots(len(self.controlPoints), self.order)
            except Exception as e:
                print(e)
        vmin = self.vKnots[self.order]
        vmax = self.vKnots[len(self.controlPoints)]
        vsteps = float((vmax - vmin) / (self.divs - 1))
        umin = self.uKnots[self.order]
        umax = self.uKnots[len(self.controlPoints[0])]
        usteps = float((umax - umin) / (self.divs - 1))
        print(umin,umax,usteps,vmin,vmax,vsteps)
        for u in range(0,self.divs):
            py=umin+u*usteps
            for i,row in enumerate(self.controlPoints):
                if self.knotsType == "Clamped":
                    coeff = self.computeClampedCofficient(len(row), self.order, py, self.uKnots)
                elif self.knotsType == "Closed":
                    coeff = self.computeOpenCofficient(len(row), self.order, py, self.uKnots)
                temp[i]=self.getBSplinePoint(coeff,row)
            for v in range(self.divs):
                px = vmin + v * vsteps
                if self.knotsType == "Clamped":
                    coeff = self.computeClampedCofficient(len(temp), self.order, px, self.vKnots)
                elif self.knotsType == "Closed":
                    coeff = self.computeClampedCofficient(len(temp), self.order, px, self.vKnots)
                last[v] = self.getBSplinePoint(coeff, temp)
            self.curvePoints.append(last.copy())
    def drawTexture(self):
        last = [None] * (self.divs)
        temp = [row[0] for row in self.controlPoints]
        if self.knotsType == "Clamped":
            self.uKnots = self.createClampedUniformKnots(len(self.controlPoints[0]), self.order)
            self.vKnots = self.createClampedUniformKnots(len(self.controlPoints), self.order)
        elif self.knotsType == "Closed":
            try:
                for row in range(len(self.controlPoints)):
                    for i in range(self.order):
                        self.controlPoints[row].append(self.controlPoints[row][i])
                print("closed loop row")
                for row in self.controlPoints:
                    print(row)
                self.uKnots = self.createOpenUniformKnots(len(self.controlPoints[0]), self.order)
                self.vKnots = self.createClampedUniformKnots(len(self.controlPoints), self.order)
            except Exception as e:
                print(e)
        vmin = self.vKnots[self.order]
        vmax = self.vKnots[len(self.controlPoints)]
        vsteps = float((vmax - vmin) / (self.divs - 1))
        umin = self.uKnots[self.order]
        umax = self.uKnots[len(self.controlPoints[0])]
        usteps = float((umax - umin) / (self.divs - 1))
        glColor3f(1, 1, 1)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        for v in range(self.divs):
            px=vmin+v*vsteps
            coeff = self.computeClampedCofficient(len(temp), self.order, px, self.vKnots)
            last[v] = self.getBSplinePoint(coeff, temp)
        for u in range(1, self.divs):
            py = umin + u * usteps
            pyold = umin + (u - 1) * usteps
            for i, row in enumerate(self.controlPoints):
                if self.knotsType == "Clamped":
                    coeff = self.computeClampedCofficient(len(row), self.order, py, self.uKnots)
                elif self.knotsType == "Closed":
                    coeff = self.computeOpenCofficient(len(row), self.order, py, self.uKnots)
                temp[i] = self.getBSplinePoint(coeff, row)
            glBegin(GL_TRIANGLE_STRIP)
            for v in range(self.divs):
                px = vmin + v * vsteps
                glTexCoord2f(pyold / umax, px / vmax)
                glVertex3f(last[v].x, last[v].y, last[v].z)
                if self.knotsType == "Clamped":
                    coeff = self.computeClampedCofficient(len(temp), self.order, px, self.vKnots)
                elif self.knotsType == "Closed":
                    coeff = self.computeClampedCofficient(len(temp), self.order, px, self.vKnots)
                last[v] = self.getBSplinePoint(coeff, temp)
                glTexCoord2f(py / umax, px / vmax)
                glVertex3f(last[v].x, last[v].y, last[v].z)
            glEnd()
        del last
if __name__ == '__main__':
    data = QtGui.QPixmap("./teapotCGA.bpt")
    print(data.width())
from curve import BezierCurve,BSpline,NURBS
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from geometry import surface,point,curve
from PyQt5 import QtGui,QtWidgets,QtCore
import numpy as np
from PIL import Image
import math
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
        self.texture = None
        self.texturePath = texturePath
        self.dlbPatch =self.getBSplineSurfacePoints()

    def readTexture(self,path):
        # m_texture=QtGui.QOpenGLTexture(QtGui.QImage(path).mirrored())
        # m_texture.setMinificationFilter(QtGui.QOpenGLTexture.LinearMipMapLinear)
        # m_texture.setMagnificationFilter(QtGui.QOpenGLTexture.Linear)
        # m_texture.setFormat(QtGui.QOpenGLTexture.RGBFormat)
        # m_texture.bind()

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
        else:
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
        glEndList()
        return drawList
    def getBSplineSurfacePoints(self):
        # print("original row")
        # for row in self.controlPoints:
        #     print(row)
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
                # print("closed loop row")
                # for row in self.controlPoints:
                #     print(row)
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
        # print(umin,umax,usteps,vmin,vmax,vsteps)
        for u in range(self.divs):
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
        # for row in self.curvePoints:
        #     print(row)
    def drawTexture(self):
        if self.knotsType == "Clamped":
            self.uKnots = self.createClampedUniformKnots(len(self.controlPoints[0]), self.order)
            self.vKnots = self.createClampedUniformKnots(len(self.controlPoints), self.order)
        elif self.knotsType == "Closed":
            try:
                for row in range(len(self.controlPoints)):
                    for i in range(self.order):
                        self.controlPoints[row].append(self.controlPoints[row][i])
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
        for u in range(0, self.divs-1):
            py = umin + u * usteps
            py_next = umin + (u+1) * usteps
            glBegin(GL_TRIANGLE_STRIP)
            for v in range(self.divs):
                px = vmin + v * vsteps
                glTexCoord2f( px / vmax,py / umax)
                glVertex3f(self.curvePoints[v][u][0],self.curvePoints[v][u][1],self.curvePoints[v][u][2])
                glTexCoord2f( px / vmax,py_next / umax)
                glVertex3f(self.curvePoints[v][u+1][0],self.curvePoints[v][u+1][1],self.curvePoints[v][u+1][2])
                # print("texture coordinate:",(self.curvePoints[v][u],self.curvePoints[v][u+1]))
            glEnd()
        glDisable(GL_TEXTURE_2D)
class NurbsSurface(NURBS):
    def __init__(self):
        self.result=[]
        self.shape=[]
    def drawNURBS_BilinearSurface(self):
        result = []
        bilinear = surface.convertListToPoint(
            [[[0.0, 1.0, -0.50], [1.0, 1.0, 0.00]], [ [0, 0, 0.00],[1, 0, 0.00]]])
        uWeight = [1,1,1,1]
        knotsType = "Clamped"
        uKnots = [0, 0, 1, 1]
        uOrder = 1

        vKnots = [0, 0, 1, 1]
        vWeight = [1, 1, 1, 1]
        vOrder = 1
        divs = 10

        vmin = vKnots[0]
        vmax = vKnots[-1]
        vsteps = float((vmax - vmin) / (divs - 1))
        umin = uKnots[0]
        umax = uKnots[-1]
        usteps = float((umax - umin) / (divs - 1))

        for u in range(divs):
            py = umin + u * usteps
            Nu = self.computeCofficient(len(bilinear), uOrder, py, uKnots, knotsType)
            tmp=[]
            for v in range(divs):
                px=vmin+v*vsteps
                Nv=self.computeCofficient(len(bilinear), vOrder, px, vKnots, knotsType)
                nwp=point(0,0,0)
                for row in range(2):
                    for column in range(2):
                        nwp+=Nv[row]*Nu[column]*bilinear[row][column]
                tmp.append(nwp)
            result.append(tmp)
        glColor3f(0.0, 1.0, 0.0)
        glLineWidth(3.0)
        for i in range(len(result)):
            glColor3f(1.0, 1.0, 1.0)
            glBegin(GL_LINE_STRIP)
            for j in range(len(result[0])):
                glVertex3f(result[i][j].x, result[i][j].y, result[i][j].z)
            glEnd()
        for i in range(len(result[0])):
            glBegin(GL_LINE_STRIP)
            for j in range(len(result)):
                glVertex3f(result[j][i].x, result[j][i].y, result[j][i].z)
            glEnd()
    #create NURBS cylinder
    #TODO: This function is not complete, the input should be set to a curve and extrude normal vector with length.
    def drawNURBS_Cylinder(self):
        result=[]
        circles =curve.listToPoint([[0.0, 1.0, 0.00], [1.0, 1.0, 0.00], [1, 0, 0.00], [1.0, -1, 0.00], [0, -1, 0.00], [-1, -1, 0.00],
             [-1, 0, 0.00], [-1, 1, 0.00], [0.0, 1.0, 0.00]])
        uWeight = [1, 2 ** 0.5 / 2, 1, 2 ** 0.5 / 2, 1, 2 ** 0.5 / 2, 1, 2 ** 0.5 / 2, 1]
        knotsType = "Circle"
        uKnots= [0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4]
        uOrder = 2

        vKNots=[0,0,1,1]
        vWeight=[1, 2 ** 0.5 / 2, 1, 2 ** 0.5 / 2, 1, 2 ** 0.5 / 2, 1, 2 ** 0.5 / 2, 1]
        W=point(0,0,1)
        length=2
        vOrder=1
        divs=100
        displaced_circles=[p+length*W for p in circles]

        vmin = vKNots[0]
        vmax = vKNots[-1]
        vsteps = float((vmax - vmin) / (divs - 1))
        umin = uKnots[uOrder]
        umax = uKnots[len(circles)]
        usteps = float((umax - umin) / (divs - 1))

        for u in range(divs):
            py = umin + u * usteps
            coe = self.computeCofficient(len(circles), uOrder, py, uKnots,knotsType)
            nwp = point(0, 0, 0)
            nw = 0
            for n, w, p in zip(coe, uWeight, circles):
                nwp +=  p*(n*w)
                nw += n * w
            try:
                C1 = nwp * (1 / nw)
            except Exception as e:
                # messengeBox=QMessageBox.warning(None,"Warning",e.args[0],QMessageBox.Yes|QMessageBox.No)
                print("NURBS CURVE ERROR", e)
            for n, w, p in zip(coe, uWeight, displaced_circles):
                nwp += n * w * p
                nw += n * w
            try:
                C2 = nwp * (1 / nw)
            except Exception as e:
                # messengeBox=QMessageBox.warning(None,"Warning",e.args[0],QMessageBox.Yes|QMessageBox.No)
                print("NURBS CURVE ERROR", e)
            result.append([C1,C2])
        glColor3f(0.0, 1.0, 0.0)
        glLineWidth(3.0)
        glBegin(GL_LINE_STRIP)
        for p1,p2 in result:
            p1.glVertex3()
        glEnd()
        for p1,p2 in result:
            glBegin(GL_LINES)
            p1.glVertex3()
            p2.glVertex3()
            glEnd()
        glBegin(GL_LINE_STRIP)
        for p1, p2 in result:
            p2.glVertex3()
        glEnd()
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(1)
        glBegin(GL_LINE_STRIP)
        for p in circles:
            p.glVertex3()
        glEnd()
    #create NURBS surface of revolution
    def getNURBS_SurfaceRevolution(self,S,T,theta,P,W,knotsType="Clamped",order=2,divs=20):
        '''Input: S: The axis is specified by a point
                  T: a unit length vector
                  theta: Angle of revolution
                  P: control points that define the curve for revolution
                  W: weights of the curve
            Output: U: knots vector
        '''
        U=[]
        if theta<=90:
            narcs=1
        elif theta<=180:
            narcs=2
            U+=[0.5,0.5]
        elif theta<=270:
            narcs=3
            U+=[1/3,1/3,2/3,2/3]
        else:
            narcs = 4
            U+=[1/4,1/4,2/4,2/4,3/4,3/4]
        dtheta = theta / narcs
        j = 3 + 2 * (narcs - 1)
        for i in range(3):
            U.insert(i,0)
            U.insert(j,1)
            j+=1
        print(U)
        wm=math.cos(math.radians(dtheta/2.0))
        angle=0.0
        cosines=[0]*(narcs+1)
        sines=[0]*(narcs+1)
        n = 2 * narcs
        Pij=[[point(0,0,0)]*len(P) for i in range(n) ]
        Pij.insert(0,P)
        Wij=[[0]*len(P)  for i in range(n)]
        Wij.insert(0,W)
        for i in range(1,narcs+1):
            angle+=dtheta
            cosines[i]=np.cos(math.radians(angle))
            sines[i]=np.sin(math.radians(angle))
        print(cosines,sines)
        for j in range(len(P)): #iterate row of control points
            O=self.PointToLine(S,T,P[j])
            X=(P[j]-O)
            Y=point.cross(T,X)
            r=X.normalize().getLength()
            Pij[0][j]=P[j]
            P0=P[j]
            Wij[0][j]=W[j]
            T0,index,angle=Y,0,0
            for i in range(1,narcs+1): #compute u row
                P2=O+X*r*cosines[i]+Y*r*sines[i]
                Pij[index + 2][j] = P2
                Wij[index + 2][j] = W[j]
                T2 = -sines[i] * X + cosines[i] * Y
                Pij[index + 1][j]=self.Intersect3DLines(P0, T0, P2, T2)
                Wij[index + 1][j] = wm * W[j]
                index+= 2
                if i < narcs:
                    P0,T0=P2,T2
        print("Pij")
        for row in Pij:
            print(row)
        print("Wij")
        for row in Wij:
            print(row)
        ###render####
        vOrder = 2
        vKnots = U
        vmin = vKnots[vOrder]
        vmax = vKnots[len(Pij)]
        vsteps = float((vmax - vmin) / (divs - 1))
        vWeight=[ Wij[row][0] for row in range(len(Wij))]

        uOrder = order
        uKnots = self.setKnots(knotsType,len(Pij[0]), uOrder)
        umin = uKnots[uOrder]
        umax = uKnots[len(Pij[0])]
        usteps = float((umax - umin) / (divs - 1))

        tmp = [None] * len(Pij)
        for u in range(divs):
            py = umin + u * usteps
            for i, row in enumerate(Pij):
                Nu = self.computeCofficient(len(row), uOrder, py, uKnots, knotsType)
                nwp1 = point(0, 0, 0)
                nw1 = 0
                for n1, w1, p1 in zip(Nu, Wij[i], row):
                    nwp1 += n1 * w1 * p1
                    nw1 += n1 * w1
                try:
                    p1 = nwp1 * (1 / nw1)
                    tmp[i] = p1
                except Exception as e:
                    print("NURBS Surface U: direction error", e)
            tmp_row=[]
            for v in range(divs):
                px = vmin + v * vsteps
                Nv = self.computeCofficient(len(tmp), vOrder, px, vKnots, "Circle")
                nwp2 = point(0, 0, 0)
                nw2=0
                for n2, w2, p2 in zip(Nv, vWeight, tmp):
                    nwp2 += n2 * w2 * p2
                    nw2 += n2 * w2
                try:
                    p2 = nwp2 * (1 / nw2)
                    tmp_row.append(p2)
                except Exception as e:
                    print("NURBS Surface V: direction error", e)
            self.result.append(tmp_row.copy())
        self.shape=Pij
    def getNURBS_Torus(self,S,T,theta,P,W,knotsType="Clamped",order=2,divs=20):
        '''Input: S: The axis is specified by a point
                  T: a unit length vector
                  theta: Angle of revolution
                  P: control points that define the curve for revolution
                  W: weights of the curve
            Output: U: knots vector
        '''
        U=[]
        if theta<=90:
            narcs=1
        elif theta<=180:
            narcs=2
            U+=[0.5,0.5]
        elif theta<=270:
            narcs=3
            U+=[1/3,1/3,2/3,2/3]
        else:
            narcs = 4
            U+=[1/4,1/4,2/4,2/4,3/4,3/4]
        dtheta = theta / narcs
        j = 3 + 2 * (narcs - 1)
        for i in range(3):
            U.insert(i,0)
            U.insert(j,1)
            j+=1
        print(U)
        wm=math.cos(math.radians(dtheta/2.0))
        angle=0.0
        cosines=[0]*(narcs+1)
        sines=[0]*(narcs+1)
        n = 2 * narcs
        Pij=[[point(0,0,0)]*len(P) for i in range(n) ]
        Pij.insert(0,P)
        Wij=[[0]*len(P)  for i in range(n)]
        Wij.insert(0,W)
        for i in range(1,narcs+1):
            angle+=dtheta
            cosines[i]=np.cos(math.radians(angle))
            sines[i]=np.sin(math.radians(angle))
        print(cosines,sines)
        for j in range(len(P)): #iterate row of control points
            O=self.PointToLine(S,T,P[j])
            X=P[j]-O
            Y=point.cross(T,X)
            r=X.normalize().getLength()
            Pij[0][j]=P[j]
            Wij[0][j]=W[j]
            P0,T0,index,angle=P[j],Y,0,0
            print("{}th point:\n O:{}\n X:{}\n Y:{}\n P:{}".format(j,O,X,Y,P[j]))
            for i in range(1,narcs+1): #compute u row
                P2=O+X*r*cosines[i]+Y*r*sines[i]
                Pij[index + 2][j] = P2
                Wij[index + 2][j] = W[j]
                T2 = -sines[i] * X + cosines[i] * Y
                Pij[index + 1][j]=self.Intersect3DLines(P0, T0, P2, T2)
                Wij[index + 1][j] = wm * W[j]
                print("{}th row:\n P2:{}\n T2:{}\n Pij:{}".format(i, P2, T2,  Pij[index + 1][j]))
                index+= 2
                if i < narcs:
                    P0,T0=P2,T2
        print("Pij")
        for row in Pij:
            print(row)
        print("Wij")
        for row in Wij:
            print(row)
        ###render####
        vOrder = 2
        vKnots = U
        vmin = vKnots[vOrder]
        vmax = vKnots[len(Pij)]
        vsteps = float((vmax - vmin) / (divs - 1))
        vWeight=[ Wij[row][0] for row in range(len(Wij))]
        uOrder = order
        uKnots = self.setKnots(knotsType,len(Pij[0]), uOrder)
        umin = uKnots[uOrder]
        umax = uKnots[len(Pij[0])]
        usteps = float((umax - umin) / (divs - 1))

        tmp = [None] * len(Pij)
        for u in range(divs):
            py = umin + u * usteps
            for i, row in enumerate(Pij):
                Nu = self.computeCofficient(len(row), uOrder, py, uKnots, knotsType)
                nwp1 = point(0, 0, 0)
                nw1 = 0
                for n1, w1, p1 in zip(Nu, Wij[i], row):
                    nwp1 += n1 * w1 * p1
                    nw1 += n1 * w1
                try:
                    p1 = nwp1 * (1 / nw1)
                    tmp[i] = p1
                except Exception as e:
                    print("NURBS Surface U: direction error", e)
            tmp_row=[]
            for v in range(divs):
                px = vmin + v * vsteps
                Nv = self.computeCofficient(len(tmp), vOrder, px, vKnots, "Circle")
                nwp2 = point(0, 0, 0)
                nw2=0
                for n2, w2, p2 in zip(Nv, vWeight, tmp):
                    nwp2 += n2 * w2 * p2
                    nw2 += n2 * w2
                try:
                    p2 = nwp2 * (1 / nw2)
                    tmp_row.append(p2)
                except Exception as e:
                    print("NURBS Surface V: direction error", e)
            self.result.append(tmp_row.copy())
        self.shape=Pij
    def drawNURBS_SurfaceRevolution(self,result):
        glColor3f(0.0, 1.0, 0.0)
        glLineWidth(3.0)
        try:
            for i in range(len(result)):
                glBegin(GL_LINE_STRIP)
                for j in range(len(result[0])):
                    glVertex3f(result[i][j].x, result[i][j].y, result[i][j].z)
                glEnd()
        except Exception as e:
            print("U direction drawing error encountered")
        try:
            for i in range(len(result[0])):
                glBegin(GL_LINE_STRIP)
                for j in range(len(result)):
                    glVertex3f(result[j][i].x, result[j][i].y, result[j][i].z)
                glEnd()
        except Exception as e:
            print("V direction drawing error encountered")
        glColor3f(1, 1, 1)
        glPushAttrib(GL_ENABLE_BIT)
        glLineStipple(1, 0XAAAA)
        glLineWidth(0.5)
        glEnable(GL_LINE_STIPPLE)
        for row in range(len(self.shape[0])):
            glBegin(GL_LINE_STRIP)
            for column in range(len(self.shape)):
                self.shape[column][row].glVertex3()
            glEnd()
        for row in range(len(self.shape)):
            glBegin(GL_LINE_STRIP)
            for column in range(len(self.shape[0])):
                self.shape[row][column].glVertex3()
            glEnd()
        glPopAttrib()

        glPointSize(3)
        glBegin(GL_POINTS)
        for row in self.shape:
            for p in row:
                p.glVertex3()
        glEnd()

    def PointToLine(self,S,T,P):#https://www.qc.edu.hk/math/Advanced%20Level/Point_to_line.htm
        st=T-S
        sp=P-S
        try:
            result=point.dot(st,sp)/point.dot(st,st)*st
        except Exception as e:
            print(e)
            result=point(0,0,0)
        return result
    def Intersect3DLines(self,P0, T0, P2, T2):
        #https://math.stackexchange.com/questions/3176543/intersection-point-of-2-lines-defined-by-2-points-each
        return (P0+T0)
if __name__ == '__main__':
    b=NurbsSurface()
    b.getNURBS_Torus(point(-2,0,0),point(0,1,0),90, curve.listToPoint(
                [[0.0, 1.0, 0.00], [1.0, 1.0, 0.00], [1, 0, 0.00], [1.0, -1, 0.00], [0, -1, 0.00], [-1, -1, 0.00],
                 [-1, 0, 0.00], [-1, 1, 0.00], [0.0, 1.0, 0.00]]),[1,2**0.5/2,1,2**0.5/2,1,2**0.5/2,1,2**0.5/2,1],knotsType="Circle",order=2,divs=20)
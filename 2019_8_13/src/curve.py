from OpenGL.GL import *
import numpy as np
from geometry import point,surface,curve
from PyQt5.QtWidgets import QMessageBox
import math
class BezierCurve:
    def __init__(self,controlPoints,type,divs=10):
        self.controlPoints=controlPoints
        self.divs=divs
        self.type=type
    @classmethod
    def combination(cls,n,r):
        return math.factorial(n)/math.factorial(n-r)/math.factorial(r)
    @classmethod
    def deCasteljauCubic(cls,p1,p2,p3,p4,t):
        p12=(1 - t) * p1 + t * p2
        p23 = (1 - t) * p2 + t * p3
        p34 = (1 - t) * p3 + t * p4
        p1223 = (1 - t) * p12 + t * p23
        p2334 = (1 - t) * p23 + t * p34
        return (1-t)*p1223+t*p2334
    @classmethod
    def deCasteljauQuad(cls,p1,p2,p3,t):
        p12=(1 - t) * p1 + t * p2
        p23 = (1 - t) * p2 + t * p3
        return (1 - t) * p12 + t * p23
    @classmethod
    def deCasteljauSplit(cls,p1,p2,p3,p4,t):
        p12 = (1 - t) * p1 + t * p2
        p23 = (1 - t) * p2 + t * p3
        p34 = (1 - t) * p3 + t * p4
        p1223 = (1 - t) * p12 + t * p23
        p2334 = (1 - t) * p23 + t * p34
        p=(1-t)*p1223+t*p2334
        return [p1,p12,p1223,p],[p,p2334,p34,p4]
    def bersteinPolynomial(self,t,controlPoints):
        c=point(0,0,0)
        n=len(controlPoints)-1
        for r in range(len(controlPoints)):
            c+=self.combination(n,r)*((1-t)**(n-r))*(t**r)*controlPoints[r]
        return c
    def drawCurve(self, c_color=(1, 1, 1)):
        glColor3f(c_color[0], c_color[1], c_color[2])
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for i, p in enumerate(self.controlPoints):
            p.glVertex3()
        glEnd()
        if self.type=="Quadratic":
            for i in range(0,len(self.controlPoints)-3,3):
                glBegin(GL_LINE_STRIP)
                for t in np.linspace(0, 1, self.divs):
                    p = self.deCasteljauQuad(self.controlPoints[i],self.controlPoints[i+1],self.controlPoints[i+2],t)
                    p.glVertex3()
                glEnd()
        elif self.type=="Cubic":
            for i in range(0, len(self.controlPoints) - 4, 4):
                glBegin(GL_LINE_STRIP)
                for t in np.linspace(0, 1, self.divs):
                    p = self.deCasteljauCubic(self.controlPoints[i], self.controlPoints[i + 1],
                                             self.controlPoints[i + 2],self.controlPoints[i + 3], t)
                    p.glVertex3()
                glEnd()
        else:
            glBegin(GL_LINE_STRIP)
            for t in np.linspace(0, 1, self.divs):
                p = self.bersteinPolynomial(t,self.controlPoints)
                p.glVertex3()
            glEnd()
    def splitCurve(self,t=0.2,c1_color=(1,0,0),c2_color=(0,0,1)):
        curve1, curve2 = self.deCasteljauSplit(self.controlPoints[0],
                                                self.controlPoints[1],
                                                self.controlPoints[2],
                                                self.controlPoints[3],
                                                t)
        glColor3f(c1_color[0], c1_color[1], c1_color[2])
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for point in curve1:
            point.glVertex3()
        glEnd()
        glColor3f(c2_color[0], c2_color[1], c2_color[2])
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for point in curve2:
            point.glVertex3()
        glEnd()
        self.drawCurve(self.controlPoints,c_color=c1_color)
        self.drawCurve(self.controlPoints, c_color=c2_color)
        glFlush()
    def drawMultiBeizerCurve(self):
        glColor3f(1, 1, 1)
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for i, p in enumerate(self.controlPoints):
            p.glVertex3()
        glEnd()
        glColor3f(0, 1, 0)
        if self.type=="Quadratic":
            glBegin(GL_LINE_STRIP)
            start_point = self.controlPoints[0]
            ctrl_point = self.controlPoints[1]
            end_point = (self.controlPoints[1] + self.controlPoints[2]) * 0.5
            for t in np.linspace(0, 1, self.divs):
                p = self.deCasteljauQuad(start_point, ctrl_point, end_point, t)
                p.glVertex3()
            for index in range(1, len(self.controlPoints) - 3):
                start_point = (self.controlPoints[index] + self.controlPoints[index+1]) * 0.5
                ctrl_point = self.controlPoints[index+1]
                end_point = (self.controlPoints[index+1] + self.controlPoints[index+2]) * 0.5
                for t in np.linspace(0, 1,self.divs):
                    p = self.deCasteljauQuad(start_point, ctrl_point, end_point, t)
                    p.glVertex3()
                if index==len(self.controlPoints) - 4:
                    start_point = end_point
                    ctrl_point = self.controlPoints[index + 2]
                    end_point = self.controlPoints[index + 3]
                    for t in np.linspace(0, 1, self.divs):
                        p = self.deCasteljauQuad(start_point, ctrl_point, end_point, t)
                        p.glVertex3()
            glEnd()
        elif self.type=="Cubic":
            glBegin(GL_LINE_STRIP)
            start_point = self.controlPoints[0]
            c1 = self.controlPoints[1]
            c2=self.controlPoints[2]
            end_point = (self.controlPoints[2] + self.controlPoints[3]) * 0.5
            for t in np.linspace(0, 1, self.divs):
                p = self.deCasteljauCubic(start_point, c1,c2, end_point, t)
                p.glVertex3()
            for index in range(2, len(self.controlPoints) - 5,2):
                start_point = (self.controlPoints[index] + self.controlPoints[index + 1]) * 0.5
                c1 = self.controlPoints[index + 1]
                c2 = self.controlPoints[index + 2]
                end_point = (self.controlPoints[index + 2] + self.controlPoints[index + 3]) * 0.5
                for t in np.linspace(0, 1, self.divs):
                    p = self.deCasteljauCubic(start_point, c1,c2, end_point, t)
                    p.glVertex3()
                if index==len(self.controlPoints) - 6:
                    start_point = end_point
                    c1 = self.controlPoints[index+3]
                    c2 = self.controlPoints[index+4]
                    end_point = self.controlPoints[index + 5]
                    for t in np.linspace(0, 1, self.divs):
                        p = self.deCasteljauCubic(start_point, c1,c2, end_point, t)
                        p.glVertex3()

            glEnd()

    def drawBezierCircle(self,center=point(0.0,0,0.0),radius=0.5):
        #Bezier curve approximation constant
        #reference: https://www.jianshu.com/p/5198d8aa80c1
        C_MAGIC_NUMNER= 0.552284749831
        difference=C_MAGIC_NUMNER*radius
        c_x=center[0]
        c_y=center[1]
        c_z=center[2]
        p0=point(c_x,c_y+radius, c_z)
        c1 = point(c_x+difference,c_y+radius,c_z)
        c2 = point(c_x+radius, c_y+difference, c_z)
        p1=point(c_x+radius,c_y,c_z)
        c3 = point(c_x+radius,c_y-difference,c_z)
        c4 =point(c_x+difference,c_y-radius,c_z)
        p2=point(c_x,c_y-radius, c_z)
        c5 = point(c_x-difference,c_y-radius, c_z)
        c6 = point(c_x-radius,c_y-difference, c_z)
        p3=point(c_x-radius,c_y, c_z)
        c7=point(c_x-radius,c_y+difference, c_z)
        c8 = point(c_x-difference,c_y+radius, c_z)
        self.drawCurve([p0,c1,c2,p1])
        self.drawCurve([p1, c3, c4, p2])
        self.drawCurve([p2, c5, c6, p3])
        self.drawCurve([p3, c7, c8, p0])
    def degreeElevationBezier(self):
        n=len(self.controlPoints)
        print("Number of control points: {}".format(n))
        print("Degree: {}".format(n-1))
        print(self.controlPoints)
        glColor3f(1.0,1.0,1.0)
        glBegin(GL_LINE_STRIP)
        for p in self.controlPoints:
            p.glVertex3()
        glEnd()
        Q=[]
        Q.append(self.controlPoints[0])
        for i in range(1,n):
            q=i/n*self.controlPoints[i-1]+(1.0-i/n)*self.controlPoints[i]
            Q.append(q)
        Q.append(self.controlPoints[-1])
        print("Number of new control points: {}".format(len(Q)))
        print("New degree: {}".format(len(Q)-1))
        print(Q)
        del self.controlPoints
        self.controlPoints=Q

class BSpline:
    def __init__(self,controlPoints,order,knotsType="Clamped",divs=100):
        self.controlPoints=controlPoints[:]
        self.order=order
        self.divs=divs
        self.knotsType=knotsType
        self.knots=self.setKnots()
        self.coeff=self.getCoefficent()
    def computeClampedCofficient(self,n,p,u,knots):
        #for clamped B-Spline
        #reference https://pages.mtu.edu/~shene/COURSES/cs3621/NOTES/spline/B-spline/bspline-curve-coef.html
        N=[0]*(n)
        k=0
        for idx in range(len(knots)-1):
            if u>=knots[idx] and u<knots[idx+1]:
                k=idx
                break
        if u==knots[0]:
            N[0]=1.0
            return N
        elif u==knots[-1]:
            N[-1]=1.0
            return N
        try:
            N[k]=1.0
        except Exception as e:
            print("Got error {}".format(e))
        for d in range(1,p+1):
            N[k-d]=(knots[k+1]-u)/(knots[k+1]-knots[(k-d)+1])*N[(k-d)+1]
            for i in range(k-d+1,k):
                N[i]=(u-knots[i])/(knots[i+d]-knots[i])*N[i]+(knots[i+d+1]-u)/(knots[i+d+1]-knots[i+1])*N[i+1]
            N[k]=(u-knots[k])/(knots[k+d]-knots[k])*N[k]
        return N
    def computeOpenCofficient(self,n,p,u,knots):
        # for Open B-Spline
        N = [0] * (n+p+1)
        k = 0
        for idx in range(len(knots) - 1):
            if u >= knots[idx] and u < knots[idx + 1]:
                k = idx
                break
        try:
            N[k] = 1.0
            for d in range(1, p + 1):
                N[k - d] = (knots[k + 1] - u) / (knots[k + 1] - knots[(k - d) + 1]) * N[(k - d) + 1]
                for i in range(k - d + 1, k):
                    N[i] = (u - knots[i]) / (knots[i + d] - knots[i]) * N[i] + (knots[i + d + 1] - u) / (
                                knots[i + d + 1] - knots[i + 1]) * N[i + 1]
                N[k] = (u - knots[k]) / (knots[k + d] - knots[k]) * N[k]
        except Exception as e:
            print("Got error {}".format(e))
        N=N[0:n]
        return N
    def getCoefficent(self):
        tmin = self.knots[self.order]
        tmax = self.knots[len(self.controlPoints)]
        steps = float((tmax - tmin) / (self.divs-1))
        Nik = []
        for i in range(self.divs):
            t = tmin + i * steps
            if self.knotsType=="Clamped":
                coe=self.computeClampedCofficient(len(self.controlPoints),self.order,t,self.knots)
            elif self.knotsType=="Open":
                coe = self.computeOpenCofficient(len(self.controlPoints), self.order, t, self.knots)
            elif self.knotsType=="Closed":
                coe = self.computeOpenCofficient(len(self.controlPoints), self.order, t, self.knots)
            Nik.append(coe)
        # for row in Nik:
        #       print(row)
        # print(len(Nik))
        return Nik
    #https://www.cnblogs.com/nobodyzhou/p/5451528.html
    def createOpenUniformKnots(self,n,k):
        #For open B-spline curves, the domain is [uk, um-k]. p is the degree,m is n+k+1
        nKnots = n + k + 1
        knots = [None] * nKnots
        for i in range(nKnots):
            knots[i] = i
        print(knots)
        return knots

    def createClampedUniformKnots(self, n, k):
        nKnots=n+k+1
        knots=[0]*(k+1)
        knots+=[i for i in range(1,n-k)]
        knots+=[n-k]*(nKnots-n)
        print(knots)
        return knots
    # def createBezierKnots(self, n, k):
    #     #Boehm's Algorithm
    #     #http://web.archive.org/web/20120227050519/http://tom.cs.byu.edu/~455/bs.pdf
    #     if ((n - 1) // k) % 2 == 0:
    #         knots = [0] * (k + 1)
    #         knots += [i for i in range(1, k + 1)]
    #         knots += [k + 2] * (k + 1)
    #     print(knots)
    #     return knots
    def setKnots(self):
        knots=[]
        if self.knotsType=="Clamped":
            knots = self.createClampedUniformKnots(len(self.controlPoints),self.order)
        elif self.knotsType=="Open":
            knots = self.createOpenUniformKnots(len(self.controlPoints), self.order)
        elif self.knotsType=="Closed":
            print(self.controlPoints)
            for i in range(self.order):
                self.controlPoints.append(self.controlPoints[i])
            print(self.controlPoints)
            knots = self.createOpenUniformKnots(len(self.controlPoints), self.order)
            print(knots)
        # elif self.knotsType=="Bezier":
        #     knots=self.createBezierKnots(len(self.controlPoints),self.order)
        return knots
    def getBSplinePoint(self,N,controlPoints):
        c=point(0,0,0)
        for a,b in zip(N,controlPoints):
            c+=a*b
        return c
    def drawBSplineCurve(self):
        glColor3f(1.0,1.0,0.0)
        glLineWidth(3.0)
        glBegin(GL_LINE_STRIP)
        for step in self.getCoefficent():
            p=point(0,0,0)
            for i,coeff in enumerate(step):
                p+=coeff*self.controlPoints[i]
            p.glVertex3()
        glEnd()
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(1)
        glBegin(GL_LINE_STRIP)
        for p in self.controlPoints:
            p.glVertex3()
        glEnd()

    def deBoor_Cox(self, i, k, t, knots):
        if k == 0:
            if (t >= knots[i] and t < knots[i + 1]) or (t==knots[i+1] and knots[i+1]==knots[-1]):
                return 1.0
            else:
                return 0.0
        else:
            den1 = knots[i + k] - knots[i]
            den2 = knots[i + k + 1] - knots[i + 1]
            if den1 == 0:
                den1 = 1
            if den2 == 0:
                den2 = 1
            a = (t - knots[i]) / den1
            b = (knots[i + k + 1] - t) / den2
            return a * self.deBoor_Cox(i, k - 1, t, knots) + b * self.deBoor_Cox(i + 1, k - 1, t, knots)
class NURBS:
    def __init__(self,controlPoints,weights,order,knotsType="Clamped",divs=100):
        self.controlPoints=controlPoints.copy()
        self.order=order
        self.divs=divs
        self.knotsType=knotsType
        self.knots=self.setKnots()
        self.weights=weights
        self.curvePoints=self.getNURBSPoints()
    def computeCofficient(self,n,p,u,knots):
        #for clamped B-Spline
        #reference https://pages.mtu.edu/~shene/COURSES/cs3621/NOTES/spline/B-spline/bspline-curve-coef.html
        N=[0]*(n)
        k=0
        for idx in range(len(knots)-1):
            if u>=knots[idx] and u<knots[idx+1]:
                k=idx
                break
        if self.knotsType=="Clamped" or self.knotsType=="Circle":
            if u==knots[0]:
                N[0]=1.0
                return N
            elif u==knots[-1]:
                N[-1]=1.0
                return N
        try:
            N[k]=1.0
            for d in range(1,p+1):
                N[k-d]=(knots[k+1]-u)/(knots[k+1]-knots[(k-d)+1])*N[(k-d)+1]
                for i in range(k-d+1,k):
                    N[i]=(u-knots[i])/(knots[i+d]-knots[i])*N[i]+(knots[i+d+1]-u)/(knots[i+d+1]-knots[i+1])*N[i+1]
                N[k]=(u-knots[k])/(knots[k+d]-knots[k])*N[k]
        except Exception as e:
            print("Array:",N)
            print(e)
        return N
    def getNURBSPoints(self):
        tmin = self.knots[self.order]
        tmax = self.knots[len(self.controlPoints)]
        steps = float((tmax - tmin) / (self.divs-1))
        curve = []
        for i in range(self.divs):
            t = tmin + i * steps
            coe=self.computeCofficient(len(self.controlPoints),self.order,t,self.knots)
            nwp=point(0,0,0)
            nw=0
            for n,w,p in zip(coe,self.weights,self.controlPoints):
                nwp+=n*w*p
                nw+=n*w
            try:
                p=nwp*(1/nw)
                curve.append(p)
            except Exception as e:
                messengeBox=QMessageBox.warning(None,"Warning",e.args[0],QMessageBox.Yes|QMessageBox.No)
        # for row in Nik:
        #       print(row)
        # print(len(Nik))
        return curve
    def createClampedUniformKnots(self, n, k):
        nKnots=n+k+1
        knots=[0]*(k+1)
        knots+=[i for i in range(1,n-k)]
        knots+=[n-k]*(nKnots-n)
        print(knots)
        return knots
    def createOpenUniformKnots(self,n,k):
        #For open B-spline curves, the domain is [uk, um-k]. p is the degree,m is n+k+1
        nKnots = n + k + 1
        knots = [None] * nKnots
        for i in range(nKnots):
            knots[i] = i
        print(knots)
        return knots
    def setWeights(self,w):
        weights=[w]*(len(self.controlPoints))
        return weights

    def setKnots(self):
        knots = []
        if self.knotsType == "Clamped":
            knots = self.createClampedUniformKnots(len(self.controlPoints), self.order)
        elif self.knotsType == "Open":
            knots = self.createOpenUniformKnots(len(self.controlPoints), self.order)
        elif self.knotsType == "Closed":
            for i in range(self.order):
                self.controlPoints.append(self.controlPoints[i])
            knots = self.createClosedUniformKnots(len(self.controlPoints), self.order)
        elif self.knotsType=="Circle":
            knots = [0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4]
        # elif self.knotsType=="Bezier":
        #     knots=self.createBezierKnots(len(self.controlPoints),self.order)
        return knots
    def drawNURBS(self):
        glColor3f(0.0,1.0,0.0)
        glLineWidth(3.0)
        glBegin(GL_LINE_STRIP)
        for p in self.curvePoints:
            p.glVertex3()
        glEnd()
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(1)
        glBegin(GL_LINE_STRIP)
        for p in self.controlPoints:
            p.glVertex3()
        glEnd()

if __name__ == '__main__':
    # surface_controlPoints=BeizerSurface(surface.convertListToPoint([[[-0.25, 0.0, -0.5], [0, 0, 0.0], [0.25, -0.2, 0.0], [0.5, 0.2, 0.0]],
    #                                              [[-0.5, -0.5, 0.0], [0, -0.2, 0.0], [0.15, -0.1, 2.0], [0.5, -0.6, 0.0]],
    #                                              [[-0.7, -0.7, 0.0], [-0.2, -0.5, 0.0], [0.1, -0.3, 2.0], [0.4, -0.7, 0.0]],
    #                                              [[-0.8, -0.7, 0.0], [0.3, -0.5, 0.0], [-0.2, -0.3, 2.0], [0.4, -0.9, 0.0]]]))
    # print("row")
    # for row in surface_controlPoints.row:
    #     print(row)
    # print("column")
    # for column in surface_controlPoints.column:
    #     print(column)
    #
    # print(BezierCurve.combination(3,0),BezierCurve.combination(3,1),BezierCurve.combination(3,2),BezierCurve.combination(3,3))
    b=BSpline(curve.listToPoint([[-0.75, -0.75, -0.50], [-0.25, -0.5, 0.00],[-0.5, -0.5, 0.0], [0, -0.2, 0.0], [0.15, -0.1, 2.0]]),order=3)
    knots=[0, 1, 2, 3, 4, 5, 6, 7, 8]
    divs=5
    tmin=0
    tmax=2
    print(knots)
    step=float(tmax-tmin)/(divs-1)
    for j in range(divs):
        t=tmin+j*step
        print(t)
        print(b.de_boors(t, knots, b.controlPoints, 3))




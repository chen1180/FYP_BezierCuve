from OpenGL.GL import *
import numpy as np
from geometry import point,surface,curve
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
    def bersteinPolynomial(self,t):
        c=point(0,0,0)
        n=len(self.controlPoints)-1
        for r in range(len(self.controlPoints)):
            c+=self.combination(n,r)*((1-t)**(n-r))*(t**r)*self.controlPoints[r]
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
                p = self.bersteinPolynomial(t)
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
        self.controlPoints=list(controlPoints)
        self.order=order
        self.divs=divs
        self.knotsType=knotsType
        self.knots=self.setKnots()
        self.coeff=self.getCoefficent()
    def getCoefficent(self):
        tmin = self.knots[self.order]
        tmax = self.knots[len(self.controlPoints)]
        steps = float((tmax - tmin) / (self.divs-1))
        Nik = []
        for i in range(self.divs):
            t = tmin + i * steps
            coe=[]
            for j, c_p in enumerate(self.controlPoints):
                nik = self.deBoor_Cox(j, self.order, t, self.knots)
                if (self.knotsType=="Clamped" or self.knotsType=="Bezier") and j==len(self.controlPoints)-1 and t==tmax:
                    nik=1.0
                coe.append(nik)
            Nik.append(coe)
        # for row in Nik:
        #       print(row)
        # print(len(Nik))
        return Nik
    # def deBoor_Cox(self, i, k, t, knots):
    #     if k == 0:
    #         if t >= knots[i] and t < knots[i + 1]:
    #             return 1.0
    #         else:
    #             return 0.0
    #     else:
    #         den1 = knots[i + k] - knots[i]
    #         den2 = knots[i + k + 1] - knots[i + 1]
    #         if den1 == 0:
    #             den1 = 1
    #         if den2 == 0:
    #             den2 = 1
    #         a = (t - knots[i]) / den1
    #         b = (knots[i + k + 1] - t) / den2
    #         return a * self.deBoor_Cox(i, k - 1, t, knots) + b * self.deBoor_Cox(i + 1, k - 1, t, knots)
    def deBoor_Cox(self, i, k, t, knots):
        if k == 0:
            if t >= knots[i] and t < knots[i + 1]:
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

    #https://www.cnblogs.com/nobodyzhou/p/5451528.html
    def createOpenUniformKnots(self,n,k):
        nKnots = n + k + 1
        knots = [None] * nKnots
        for i in range(nKnots):
            knots[i] = i
        return knots

    def createClampedUniformKnots(self, n, k):
        knots=[0]*(k+1)
        knots+=[i for i in range(1,n-k)]
        knots+=[n-k]*(k+1)
        print(knots)
        return knots
    def createClosedUniformKnots(self, n, k):
        nKnots = n + k + 1
        knots = [None] * nKnots
        for i in range(n):
            knots[i]=i
        for i in range(k+1):
            knots[n+i]=knots[i]
        return knots
    def createBezierKnots(self, n, k):
        if ((n-1)//k)%2==0:
            knots = [0] * (k+1)
            knots += [i for i in range(1,k+1)]
            knots+=[k+2]*(k+1)
        return knots
    def setKnots(self):
        knots=[]
        if self.knotsType=="Clamped":
            print(self.controlPoints)
            knots = self.createClampedUniformKnots(len(self.controlPoints),self.order)
        elif self.knotsType=="Open":
            print(self.controlPoints)
            knots = self.createOpenUniformKnots(len(self.controlPoints), self.order)
        elif self.knotsType=="Closed":
            self.controlPoints.append(self.controlPoints[0])
            self.controlPoints.append(self.controlPoints[1])
            self.controlPoints.append(self.controlPoints[2])
            print(self.controlPoints)
            knots = self.createOpenUniformKnots(len(self.controlPoints), self.order)
        elif self.knotsType=="Bezier":
            knots=self.createBezierKnots(len(self.controlPoints),self.order)
        return knots
    def getBSplinePoint(self,t,controlPoints,order,knots):
        bsplinePoint=point(0,0,0)
        for i,p in enumerate(controlPoints):
            nik = self.deBoor_Cox(i, order, t, knots)
            bsplinePoint+=nik*p
        return bsplinePoint
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
    b=BSpline(curve.listToPoint([[-0.75, -0.75, -0.50], [-0.25, -0.5, 0.00]]),order=2)
    print( b.getBSplinePoint([0.5,0.5],b.controlPoints))




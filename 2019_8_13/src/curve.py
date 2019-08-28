from OpenGL.GL import *
import numpy as np
from geometry import point,surface
class BezierCurve:
    def __init__(self,controlPoints):
        self.controlPoints=controlPoints
    @classmethod
    def decasteljauCubic(cls,p1,p2,p3,p4,t):
        p12=(1 - t) * p1 + t * p2
        p23 = (1 - t) * p2 + t * p3
        p34 = (1 - t) * p3 + t * p4
        p1223 = (1 - t) * p12 + t * p23
        p2334 = (1 - t) * p23 + t * p34
        return (1-t)*p1223+t*p2334
    @classmethod
    def decasteljauQuad(cls,p1,p2,p3,t):
        p12=(1 - t) * p1 + t * p2
        p23 = (1 - t) * p2 + t * p3
        return (1 - t) * p12 + t * p23
    @classmethod
    def decasteljau_split(cls,p1,p2,p3,p4,t):
        p12 = (1 - t) * p1 + t * p2
        p23 = (1 - t) * p2 + t * p3
        p34 = (1 - t) * p3 + t * p4
        p1223 = (1 - t) * p12 + t * p23
        p2334 = (1 - t) * p23 + t * p34
        p=(1-t)*p1223+t*p2334
        return [p1,p12,p1223,p],[p,p2334,p34,p4]
    def drawCurve(self,controlPoints, c_color=(1, 1, 1)):
        glColor3f(c_color[0], c_color[1], c_color[2])
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for i, p in enumerate(controlPoints):
            p.glVertex3()
        glEnd()
        glBegin(GL_LINE_STRIP)
        for t in np.linspace(0, 1, 10):
            p = self.decasteljauCubic(controlPoints[0], controlPoints[1], controlPoints[2], controlPoints[3], t)
            p.glVertex3()
        glEnd()
    def splitCurve(self,t=0.2,c1_color=(1,0,0),c2_color=(0,0,1)):
        curve1, curve2 = self.decasteljau_split(self.controlPoints[0],
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
        for t in np.linspace(0, 1, 10):
            p = self.decasteljauQuad(start_point, ctrl_point, end_point, t)
            p.glVertex3()
        for index in range(1, len(self.controlPoints) - 3):
            start_point = (self.controlPoints[index] + self.controlPoints[index+1]) * 0.5
            ctrl_point = self.controlPoints[index+1]
            end_point = (self.controlPoints[index+1] + self.controlPoints[index+2]) * 0.5
            for t in np.linspace(0, 1, 10):
                p = self.decasteljauQuad(start_point, ctrl_point, end_point, t)
                p.glVertex3()
            if index==len(self.controlPoints) - 4:
                start_point = end_point
                ctrl_point = self.controlPoints[index + 2]
                end_point = self.controlPoints[index + 3]
                for t in np.linspace(0, 1, 10):
                    p = self.decasteljauQuad(start_point, ctrl_point, end_point, t)
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
class BeizerSurface(BezierCurve):
    def __init__(self,controlPoints):
        self.controlPoints=controlPoints
        self.row,self.column=self.BezierSurfaceEvaluator()
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
    def BezierSurfaceEvaluator(self):
        curveInRow=[]
        curveInColumn=[]
        for u in np.linspace(0,1,10):
            p=[]
            for v in np.linspace(0,1,10):
                q = []
                for row in self.controlPoints:
                    q_i = self.decasteljauCubic(row[0], row[1], row[2], row[3], v)
                    q.append(q_i)
                curveInRow.append(q)
                p_u_v=self.decasteljauCubic(q[0],q[1],q[2],q[3],u)
                p.append(p_u_v)
            curveInColumn.append(p)
        return curveInRow,curveInColumn
    def drawBezierSurface_DelCasteljau(self):
        #https://pages.mtu.edu/~shene/COURSES/cs3621/NOTES/surface/bezier-de-casteljau.html
        for row in self.row:
            glBegin(GL_LINE_STRIP)
            for u in row:
                u.glVertex3()
            glEnd()
        for column in self.column:
            glBegin(GL_LINE_STRIP)
            for v in column:
                v.glVertex3()
            glEnd()
        glBegin(GL_LINE_STRIP)
        self.controlPoints[0][0].glVertex3()
        self.controlPoints[1][0].glVertex3()
        self.controlPoints[2][0].glVertex3()
        self.controlPoints[3][0].glVertex3()

        glEnd()

class BSpline:
    def __init__(self):
        pass
    @classmethod
    def deBoor_Cox(cls, i, k, t, knots):
        if k == 0:
            if t >= knots[i] and t < knots[i + 1]:
                return 1.0
            else:
                return 0.0
        den1 = knots[i + k] - knots[i]
        den2 = knots[i + k + 1] - knots[i + 1]
        a = 0
        b = 0
        if den1 == 0 and den2 == 0:
            a, b = 1, 1
        elif den1 != 0 and den2 == 0:
            a = (t - knots[i]) / den1
            b = 1
        elif den1 == 0 and den2 != 0:
            a = 1
            b = knots[i + k + 1] - t
        else:
            a = (t - knots[i]) / den1
            b = (knots[i + k + 1] - t) / den2
        return a * cls.deBoor_Cox(i, k - 1, t, knots) + b * cls.deBoor_Cox(i + 1, k - 1, t, knots)

    @classmethod
    #https://www.cnblogs.com/nobodyzhou/p/5451528.html
    def createOpenUniformKnots(cls,n,k):
        nKnots = n + k + 1
        knots = [None] * nKnots
        for i in range(nKnots):
            knots[i] = i
        return knots

    @classmethod
    def createClampedUniformKnots(cls, n, k):
        nKnots = n + k+1
        knots = [None] * nKnots
        for i in range(nKnots):
            if i < k+1:
                knots[i] = 0
            elif i < nKnots - k:
                knots[i] = knots[i - 1] + 1
            else:
                knots[i] = knots[i - 1]
        return knots
    @classmethod
    def createClosedUniformKnots(cls, n, k):
        nKnots = n + k + 1
        knots = [None] * nKnots
        for i in range(nKnots):
            knots[i]=i+1
        return knots

    @classmethod
    def createBezierKnots(cls, n, k):
        nKnots=(n+k+1)
        knots = [0] * (k+1)
        knots+=[1]*(k+1)
        return knots
    @classmethod
    def drawBSplineCurve(cls,controlPoints=[],order=2,knots_type="clamped"):
        glColor3f(1.0,1.0,0.0)
        glLineWidth(3.0)
        glBegin(GL_LINE_STRIP)
        if knots_type=="Clamped":
            knots = cls.createClampedUniformKnots(len(controlPoints),order)
        elif knots_type=="Open":
            knots = cls.createOpenUniformKnots(len(controlPoints), order)
        elif knots_type=="Closed":
            knots=cls.createClosedUniformKnots(len(controlPoints),order)
        elif knots_type=="Bezier":
            order=len(controlPoints)-1
            knots=cls.createBezierKnots(len(controlPoints),order)
        print(knots)
        tmin=knots[order]
        tmax=knots[len(controlPoints)]
        insertNum = 100
        steps=(tmax-tmin)/(insertNum)
        for i in range(insertNum):
            t=tmin+i*steps
            p=point(0,0,0)
            for j,c_p in enumerate(controlPoints):
                Nik=cls.deBoor_Cox(j,order,t,knots)
                p+=Nik*c_p
            if i==insertNum-1 and knots_type!="Open":
                p=controlPoints[-1]
            glVertex3f(p.x,p.y,p.z)
        glEnd()
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(1)
        glBegin(GL_LINE_STRIP)
        for p in controlPoints:
            p.glVertex3()
        glEnd()
if __name__ == '__main__':
    surface_controlPoints=BeizerSurface(surface.convertListToPoint([[[-0.25, 0.0, -0.5], [0, 0, 0.0], [0.25, -0.2, 0.0], [0.5, 0.2, 0.0]],
                                                 [[-0.5, -0.5, 0.0], [0, -0.2, 0.0], [0.15, -0.1, 2.0], [0.5, -0.6, 0.0]],
                                                 [[-0.7, -0.7, 0.0], [-0.2, -0.5, 0.0], [0.1, -0.3, 2.0], [0.4, -0.7, 0.0]],
                                                 [[-0.8, -0.7, 0.0], [0.3, -0.5, 0.0], [-0.2, -0.3, 2.0], [0.4, -0.9, 0.0]]]))
    print("row")
    for row in surface_controlPoints.row:
        print(row)
    print("column")
    for column in surface_controlPoints.column:
        print(column)






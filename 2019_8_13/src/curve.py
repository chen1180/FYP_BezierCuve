from OpenGL.GL import *
import numpy as np
from geometry import point
class BezierCurve:
    def __init__(self):
        pass
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
    @classmethod
    def drawCurve(cls, control_points, c_color=(1, 1, 1)):
        glColor3f(c_color[0], c_color[1], c_color[2])
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for i, p in enumerate(control_points):
            p.glVertex3()
        glEnd()
        glBegin(GL_LINE_STRIP)
        for t in np.linspace(0, 1, 10):
            p = cls.decasteljauCubic(control_points[0], control_points[1], control_points[2], control_points[3], t)
            p.glVertex3()
        glEnd()
    @classmethod
    def splitCurve(cls,control_points,t=0.2,c1_color=(1,0,0),c2_color=(0,0,1)):
        curve1, curve2 = cls.decasteljau_split(control_points[0],
                                                control_points[1],
                                                control_points[2],
                                                control_points[3],
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
        cls.drawCurve(curve1, c_color=c1_color)
        cls.drawCurve(curve2, c_color=c2_color)
        glFlush()
    @classmethod
    def drawMultiBeizerCurve(cls,control_points):
        glColor3f(1, 1, 1)
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for i, p in enumerate(control_points):
            p.glVertex3()
        glEnd()
        glColor3f(0, 1, 0)
        glBegin(GL_LINE_STRIP)
        start_point = control_points[0]
        ctrl_point = control_points[1]
        end_point = (control_points[1] + control_points[2]) * 0.5
        for t in np.linspace(0, 1, 10):
            p = cls.decasteljauQuad(start_point, ctrl_point, end_point, t)
            p.glVertex3()
        for index in range(1, len(control_points) - 2):
            start_point = (control_points[index] + control_points[index+1]) * 0.5
            ctrl_point = control_points[index+1]
            end_point = (control_points[index+1] + control_points[index+2]) * 0.5
            for t in np.linspace(0, 1, 10):
                p = cls.decasteljauQuad(start_point, ctrl_point, end_point, t)
                p.glVertex3()
        control_points[-1].glVertex3()
        glEnd()
    @classmethod
    def drawBeizerSurface(cls):
        glMatrixMode(GL_MODELVIEW)
        glColor3f(0.5, 0.5, 0.5)
        glPushMatrix()
        # glRotatef(45.0,-10.0,1.0,-10.0)
        control_points = [[[-0.25, 0.0, -0.5], [0, 0, 0.0], [0.25, -0.2, 0.0], [0.5, 0.2, 0.0]],
                          [[-0.5, -0.5, 0.0], [0, -0.9, 0.0], [0.25, -0.2, 2.0], [0.5, -0.6, 0.0]]]
        glMap2f(GL_MAP2_VERTEX_3, 0, 1, 0, 1, control_points)
        glEnable(GL_MAP2_VERTEX_3)
        glMapGrid2f(50, 0, 1, 50, 0, 1)
        glEvalMesh2(GL_LINE, 0, 50, 0, 50)
        glPointSize(5)
        glColor3f(1, 1, 1)
        glBegin(GL_POINTS)
        for line in control_points:
            for point in line:
                glVertex3f(point[0], point[1], point[2])
        glEnd()
        glPopMatrix()
    @classmethod
    def drawBezierCircle(cls,center=point(0.0,0,0.0),radius=0.5):
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
        cls.drawCurve([p0,c1,c2,p1])
        cls.drawCurve([p1, c3, c4, p2])
        cls.drawCurve([p2, c5, c6, p3])
        cls.drawCurve([p3, c7, c8, p0])
class BSpline:
    def __init__(self):
        pass
    @classmethod
    # B样条基函数
    # i: 控制点计数
    # k: 次数
    # t: 节点
    # knots: 节点向量，用来分段
    def deBoor_Cox(cls,j,k,i,t,controlPoints,knots):
        if j==0:
            return controlPoints[i]
        else:
            param=(t-knots[i])/(knots[i+k-j]-knots[i])

            return (1-param)*cls.deBoor_Cox(j-1,k,i-1,t,controlPoints,knots)+(1-param)*cls.deBoor_Cox(j-1,k,i,t,controlPoints,knots)

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
        nKnots = n + k
        knots = [None] * nKnots
        for i in range(nKnots):
            if i < k:
                knots[i] = 0
            elif i < nKnots - k+1:
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
    def getBSpline(cls,detail,controlPoints,order=-1):
        points=[]
        if (order == -1 or order < 4):
            order =len(controlPoints)-1 if len(controlPoints) <= 4 else 4
        # generate knots
        knots=cls.createClampedUniformKnots(len(controlPoints), order)
        # 根据[k - 1, n + 1)这个区间长度和采样的线段点detail个数生成t的增量
        tJump = (knots[len(knots) - order] - knots[order - 1]) / (detail - 1);
        for i in range(0,detail):
            if i==detail-1:
                point=controlPoints[-1]
            else:
                t = knots[order - 1] + i * tJump
                tInt=cls.whichInterval(t,knots)
                if tInt>=len(controlPoints):
                    continue
                point=cls.deBoor_Cox(order-1,order,tInt,t,controlPoints,knots)
            points.append(point)
        return points

    @classmethod
    def whichInterval(cls,t,knots):
        for i in range(1,len(knots)-1):
            if t<knots[i]:
                return i-1
            elif t==knots[-2]:
                return -2
        return -1
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
        print(knots)
        tmin=knots[0]
        tmax=knots[-1]
        insertNum = 100
        steps=(tmax-tmin)/(insertNum-1)
        for i in range(insertNum):
            t=tmin+i*steps
            p=point(0,0,0)
            for j,c_p in enumerate(controlPoints):
                Nik=cls.deBoor_Cox(j,order,t,knots)
                p+=Nik*c_p
            glVertex3f(p.x,p.y,p.z)
        glEnd()
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(1)
        glBegin(GL_LINE_STRIP)
        for p in controlPoints:
            p.glVertex3()
        glEnd()





from OpenGL.GL import *
import numpy as np
import math
class point:
    def __init__(self,_x,_y,_z):
        self.x=_x
        self.y=_y
        self.z=_z
    @classmethod
    def with_components(cls,cs):
        return point(cs[0],cs[1],cs[2])
    @classmethod
    def cross(cls,p1,p2):
        p = np.cross(p1.components(), p2.components())
        return point.with_components(p)
    @classmethod
    def dot(cls, p1, p2):
        return p1.x*p2.x+p1.y*p2.y+p1.z*p2.z
    def components(self):
        return [self.x,self.y,self.z]
    def glVertex3(self):
        glVertex3f(self.x,self.y,self.z)
    def getLength(self):
        return (self.x**2+self.y**2+self.z**2)**0.5
    def plus(self,offset):
        return point(self.x+offset.x,self.y+offset.y,self.z+offset.z)
    def minus(self, other):
        return point(self.x - other.x, self.y - other.y, self.z - other.z)
    def mul(self,num):
        return point(num*self.x,num*self.y,num*self.z)
    def rmul(self,num):
        return self.mul(num)
    def dist2(self, other):
        return (self - other).norm2()

    def dist(self, other):
        return (self - other).norm()

    def combo(self, scalar, other):
        return self.plus(other.minus(self).scale(scalar))

    #
    # Special methods, hooks into Python syntax.
    #
    __add__=plus
    __sub__=minus
    __mul__=mul
    __rmul__=rmul
    def __str__(self):
        return "({},{},{})".format(self.x,self.y,self.z)
    __repr__=__str__
    def __getitem__(self, item):
        return (self.components())[item]
class curve:
    def __init__(self):
        pass
    @classmethod
    def generateMatrix(cls,range=[-1,1],dim=[6,3]):
        mat=np.random.uniform(range[0],range[1],[dim[0],3])
        controlPoints=[]
        for row in mat:
            controlPoints.append(point.with_components(row))
        #print(controlPoints)
        return controlPoints

    @classmethod
    def listToPoint(cls,list):
        curve=[]
        for p in list:
            curve.append(point.with_components(p))
        return curve
class surface:
    def __init__(self):
        pass
    @classmethod
    def generateRandomMatrix(cls,range=[-1,1],dim=[4,4]):
        mat=np.random.uniform(range[0],range[1],[dim[0],dim[1],3])
        controlPoints=[]
        for row in mat:
            controlPointsRow=[]
            for column in row:
                controlPointsRow.append(point.with_components(column))
            controlPoints.append(controlPointsRow)
        print(controlPoints)
        return controlPoints

    @classmethod
    def convertListToPoint(self,mat):
        controlPoints = []
        for row in mat:
            controlPointsRow = []
            for column in row:
                controlPointsRow.append(point.with_components(column))
            controlPoints.append(controlPointsRow)
        return controlPoints
if __name__ == '__main__':
    test=point(0,1,2)
    test2=point(3,4,5)
    print(type(test))
    print(test+test2)


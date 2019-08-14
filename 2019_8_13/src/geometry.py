from random import random
from math import sqrt,pi,sin,cos,acos
from OpenGL.GL import *

class point:
    def __init__(self,_x,_y,_z):
        self.x=_x
        self.y=_y
        self.z=_z
    @classmethod
    def with_components(cls,cs):
        return point(cs[0],cs[1],cs[2])
    def components(self):
        return [self.x,self.y,self.z]
    def glVertex3(self):
        glVertex3f(self.x,self.y,self.z)
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

if __name__ == '__main__':
    test=point(0,1,2)
    test2=point(3,4,5)
    print(test)
    print(test+test2)


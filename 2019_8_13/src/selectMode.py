from OpenGL.GL import *
class SelectionEngine:
    def __init__(self):
        self.mDrawSquare=False
    def drawSelectSquare(self,x1,y1,z1,x2,y2,z2):
        if self.mDrawSquare:
            glColor3f(0,0,1)
            glBegin(GL_QUADS)
            glVertex3f(x1,y1,z1)
            glVertex3f(x2,y1,z2)
            glVertex3f(x2,y2,z2)
            glVertex3f(x1,y2,z1)
            glEnd()
    def changeDrawSquare(self,status):
        self.mDrawSquare=status
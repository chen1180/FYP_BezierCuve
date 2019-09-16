from curve import BezierCurve,BSpline
from OpenGL.GL import *
from geometry import surface,point
from surface import BSplineSurface
import re
class Model:
    def __init__(self,path):
        self.patchList=self.parseFile_bpt(path)
        self.glList=[]
    def parseFile_bpt(self,path):
        patchesList=[]
        with open(path,'r') as infile:
            patch=[]
            row=[]
            patchCount=0
            rowCount=0
            for line in infile.readlines():
                n=re.findall(r'(\S+)',line)
                if n and len(n)==3:
                    p=point(float(n[0]),float(n[1]),float(n[2]))
                    print(p)
                    row.append(p)
                    rowCount+=1
                    patchCount+=1
                    if rowCount==4:
                        patch.append(row.copy())
                        row.clear()
                        rowCount=0
                    if patchCount==16:
                        patchCount=0
                        patchesList.append(patch.copy())
                        patch.clear()
        return patchesList
    def loadModel(self):
        for list in self.patchList:
            splineSurface = BSplineSurface(list, 3, 5, "Clamped", True)
            splineSurface.getBSplineSurfacePoints()
            splineSurface.dlbPatch = splineSurface.genClampedBSplineSurface()
            self.glList.append(splineSurface.dlbPatch)
    def renderModel(self):
        for i,list in enumerate(self.glList):
            glCallList(list)
if __name__ == '__main__':
    a=Model("./teapotCGA.bpt")

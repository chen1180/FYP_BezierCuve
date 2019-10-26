from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from OpenGL.GL import *
from PyQt5.QtGui import *
import sys
class PickingEffect(QObject):
    def __init__(self):
        self.m_drawIndexLocation=0
        self.m_WVPLocation=0
        self.m_objectIndexLocation=0

    def Init(self):
        self.program = QOpenGLShaderProgram()
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex, ":CommonShader/picking.vert")
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, ":CommonShader/picking.frag")
        self.program.link()
    def SetMVP(self,MVP):
        self.program.setUniformValue("gWVP",MVP)
    def DrawStartCB(self,DrawIndex):
        self.program.setUniformValue("gDrawIndex",  DrawIndex)
    def SetObjectIndex(self,ObjectIndex):
        self.program.setUniformValue("gObjectIndex", ObjectIndex)
    def Enable(self):
        self.program.bind()
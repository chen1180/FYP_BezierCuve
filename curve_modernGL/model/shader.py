from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from OpenGL.GL import *
from PyQt5.QtGui import *
import sys
class Shader(object):
    def __init__(self):
        self.vao=0
        self.vbo=0

    def Init(self,vertShader,fragShader,tescShader=None,teseShader=None,geomShader=None):
        self.program = QOpenGLShaderProgram()
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex, vertShader)
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, fragShader)
        if tescShader:
            self.program.addShaderFromSourceFile(QOpenGLShader.TessellationControl, tescShader)
        if teseShader:
            self.program.addShaderFromSourceFile(QOpenGLShader.TessellationEvaluation, teseShader)
        if geomShader:
            self.program.addShaderFromSourceFile(QOpenGLShader.Geometry, geomShader)
        self.program.link()
        if self.program.log():
            qDebug(self.program.log())
            return False
        return True

    def bindShader(self):
        self.program.bind()

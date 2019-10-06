from OpenGL.GL import *
from PyQt5.QtWidgets import QApplication,QOpenGLWidget
from PyQt5.QtGui import QSurfaceFormat,QVector3D
import sys
from curve_modernGL.model.triangle import Bezier
class openGLWindow(QOpenGLWidget):
    def __init__(self,parent=None):
        super(openGLWindow, self).__init__(parent)
    def getFileContent(self,filename):
        return open(filename,"r").read()
    def initializeGL(self) -> None:
        QOpenGLWidget.initializeGL(self)
        self.bezier=Bezier(None,"Beizer1",[QVector3D(-0.5,0,0),QVector3D(0.5,0,0),QVector3D(0,0.5,0)])
        self.bezier.create()
    def paintGL(self) -> None:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        self.bezier.draw()
        self.update()




sys._excepthook = sys.excepthook
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = my_exception_hook
if __name__ == '__main__':
    application=QApplication([])
    # The follow format can set up the OPENGL context
    format=QSurfaceFormat()
    format.setDepthBufferSize(24)
    format.setStencilBufferSize(8)
    format.setVersion(4,4)
    format.setProfile(QSurfaceFormat.CoreProfile)
    QSurfaceFormat.setDefaultFormat(format) #it must be called before OpenGL window, set OPENGL format globally
    window = openGLWindow() #Opengl window creation
    window.show()
    application.exec_()


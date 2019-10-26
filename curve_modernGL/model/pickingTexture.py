from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from OpenGL.GL import *
from PyQt5.QtGui import *
import sys
class PickingTexture(QObject):
    def __init__(self):
        self.m_fbo=None
        self.m_pickingTexture=None
        self.m_depthTexture=None
    def Init(self,WindowWidth,WindowHeight):
        #Create the FBO
        self.origin_fbo=glGetIntegerv(GL_FRAMEBUFFER_BINDING)
        self.m_fbo=glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER,self.m_fbo)
        #Create the texture object for the primitive information buffer
        self.m_pickingTexture=glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.m_pickingTexture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB32F, WindowWidth, WindowHeight, 0, GL_RGB, GL_FLOAT, None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.m_pickingTexture, 0)
        #Create the texture object for the depth buffer
        self.m_depthTexture=glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.m_depthTexture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, WindowWidth, WindowHeight, 0, GL_DEPTH_COMPONENT, GL_FLOAT,None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.m_depthTexture, 0)

        glReadBuffer(GL_NONE)
        glDrawBuffer(GL_COLOR_ATTACHMENT0)
        #Verify that the FBO is correct
        Status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if (Status != GL_FRAMEBUFFER_COMPLETE):
            qDebug("B error, status:{}".format(Status))
            return False
        #Restore the default framebuffer
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        return True
    def EnableWriting(self):
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, self.m_fbo)
    def DisableWriting(self):
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)

    def ReadPixel(self,x,y):
        glBindFramebuffer(GL_READ_FRAMEBUFFER, self.m_fbo)
        glReadBuffer(GL_COLOR_ATTACHMENT0)

        Pixel=(GLuint*1)(1)
        glReadPixels(x, y, 1, 1, GL_RGB, GL_FLOAT, Pixel)
        glReadBuffer(GL_NONE)

        glBindFramebuffer(GL_READ_FRAMEBUFFER, 0)
        return Pixel


#For debug purpose
if __name__ == '__main__':
    sys._excepthook = sys.excepthook
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
    sys.excepthook = my_exception_hook
    application=QApplication([])
    # The follow format can set up the OPENGL context
    window = SceneDockWidget() #Opengl window creation
    window.addItem(Bezier(window,"asd",[QVector3D(0,0,0),QVector3D(0,0,2)]))
    window.show()
    application.exec_()
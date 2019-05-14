from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow,QGraphicsItem,QGraphicsScene,QGraphicsView
from Ui_mainWindow import *
import curve
from mixin import MainMixin
class GraphicView(QGraphicsView):
    def __init__(self,parent=None):
        super(GraphicView, self).__init__(parent)
class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.setSceneRect(0, 0, 1000, 1000)
        self.lastPoint = None
        self.isDrawing = False
        self.opt = ""
        self.currentItem = None

    def setOption(self, opt):
        self.opt = opt

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.isDrawing == False:
            if event.button() == Qt.LeftButton:
                if self.opt == "QuadBezier":
                    self.isDrawing = True
                    p = curve.QuadBezierCurve(parent=self)
                    self.addItem(p)
                    self.currentItem = p
                elif self.opt == "CubicBezier":
                    self.isDrawing = True
                    p = curve.CubicBeizerCurve(parent=self)
                    self.addItem(p)
                    self.currentItem = p
                elif self.opt == "MultiBezier":
                    self.isDrawing = True
                    p = curve.MultiBeizerCurve(parent=self)
                    self.addItem(p)
                    self.currentItem = p
                elif self.opt == "Select":
                    pass
            elif event.button() == Qt.RightButton:
                print("Remove item")
                itemToremove = self.items(event.scenePos())
                if itemToremove:
                    self.removeItem(itemToremove[0])
        else:
            if self.currentItem.isDrawingComplete:
                self.resetData()
        self.update()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.lastPoint = event.scenePos()
        self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.isDrawing and self.currentItem.isDrawingComplete == False:
            self.currentItem.addPoint(event.scenePos())
        self.update()

    def resetData(self):
        self.opt = ""
        self.lastPoint = None
        self.isDrawing = False
        self.currentItem = None

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Escape:
            print("scene Esc")


class MainWindow(QMainWindow,MainMixin):
    name = 'Curve System GUI'
    org='NTU FYP'
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        MainMixin.__init__(self)
        #self.setWindowIcon()
        self.setupUI()

    def setupUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.graphicsView.setMouseTracking(True)
        self.mousePos = None

        self.scene = GraphicsScene()

        #customize QgraphicView UI
        self.ui.horizontalLayout.removeWidget(self.ui.graphicsView)
        self.ui.graphicsView.close()
        self.ui.graphicsView=GraphicView(self.ui.centralwidget)
        self.ui.horizontalLayout.addWidget(self.ui.graphicsView)
        self.ui.horizontalLayout.update()

        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.setBackgroundBrush(QBrush(Qt.white))
        # push button signal
        self.ui.push_button_bezier_quad.clicked.connect(
            lambda state, button_text=self.ui.push_button_bezier_quad.text(): self.drawCurve(button_text))
        self.ui.push_button_bezier_cubic.clicked.connect(
            lambda state, button_text=self.ui.push_button_bezier_cubic.text(): self.drawCurve(button_text))
        self.ui.push_button_bezier_multi.clicked.connect(
            lambda state, button_text=self.ui.push_button_bezier_multi.text(): self.drawCurve(button_text))
        self.ui.actionClear.triggered.connect(self.clearDrawing)
        self.ui.actionSelect.triggered.connect(
            lambda state, button_text=self.ui.actionSelect.text(): self.drawCurve(button_text))

    def drawCurve(self, button_text):
        self.scene.setOption(button_text)

    def clearDrawing(self):
        self.scene.resetData()
        self.scene.clear()
        self.scene.update()


if __name__ == '__main__':
    pass

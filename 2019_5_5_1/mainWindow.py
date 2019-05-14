from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from testPackage import *
import curve

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
        point = event.scenePos()
        if self.isDrawing == False:
            if event.button() == Qt.LeftButton :
                if self.opt=="QuadBezier":
                    self.isDrawing = True
                    p = curve.QuadBezierCurve(parent=self)
                    self.addItem(p)
                    self.currentItem = p
                elif self.opt=="CubicBezier":
                    self.isDrawing = True
                    p = curve.CubicBeizerCurve(parent=self)
                    self.addItem(p)
                    self.currentItem = p
                elif self.opt=="MultiBezier":
                    self.isDrawing = True
                    p = curve.MultiBeizerCurve(parent=self)
                    self.addItem(p)
                    self.currentItem = p
                elif self.opt=="Select":
                    print("Select")
            elif event.button() == Qt.RightButton:
                print("Remove item")
                itemToremove = self.items(event.scenePos())
                if itemToremove:
                    self.removeItem(itemToremove[0])
        else:
            if self.currentItem.isDrawingComplete:
                self.isDrawing = False
                self.currentItem = None
            else:
                self.currentItem.addPoint(point)
        self.update()

    def resetData(self):
        self.opt = ""
        self.lastPoint = None

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.lastPoint = event.scenePos()
        self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.update()

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Escape:
            print("scene Esc")

class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.graphicsView.setMouseTracking(True)
        self.mousePos = None

        self.scene = GraphicsScene()
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
    app = QtWidgets.QApplication([])
    window = mainWindow()
    window.show()
    app.exec_()

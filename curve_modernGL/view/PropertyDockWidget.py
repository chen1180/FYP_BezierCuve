from PyQt5.QtWidgets import *
from PyQt5.QtGui import QVector3D,QPalette,QColor
from PyQt5.QtCore import Qt,QEvent,pyqtSignal
from curve_modernGL.model.SceneNode import *
class PropertyDockWidget(QTabWidget):
    def __init__(self,parent=None,item:QListWidgetItem=None):
        super(PropertyDockWidget, self).__init__(parent)
        self.setTabPosition(QTabWidget.West)
        self.coordinateForm=VerticiesProperty(None)
        self.transformWidget=TransformationProperty(None)
        self.colorWidget = ColorProperty(None)
        self.insertTab(0, self.coordinateForm, "Vertices")
        self.insertTab(1, self.transformWidget, "Transform")
        self.insertTab(2,self.colorWidget,"Color")
class VerticiesProperty(QTabWidget):
    dataChanged=pyqtSignal(QVector3D)
    def __init__(self,parent=None):
        super(VerticiesProperty, self).__init__(parent)
        self.setWindowTitle("Property")

        gridLayout=QGridLayout()
        gridLayout.setSpacing(10)

        vertLabel=QLabel("Coordinates")
        #setup table to display vertices coordinate
        self.table=QTableWidget()
        self.table.setColumnCount(3)
        self.table.setColumnWidth(0, 2)
        self.table.setColumnWidth(1, 2)
        self.table.setColumnWidth(2, 2)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("x"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("y"))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("z"))
        gridLayout.addWidget(vertLabel, 1, 0)
        gridLayout.addWidget(self.table, 2, 0)
        self.setLayout(gridLayout)
        self.setGeometry(300, 300, 350, 300)
    def displayTable(self,item):
        try:
            vertices = item.data(Qt.UserRole)
            size = len(vertices)
            self.table.setRowCount(size)
            for i, data in enumerate(vertices):
                self.table.setItem(i, 0, QTableWidgetItem(str(data.x())))
                self.table.setItem(i, 1, QTableWidgetItem(str(data.y())))
                self.table.setItem(i, 2, QTableWidgetItem(str(data.z())))
        except Exception as e:
            print(e, "Table data doesn't exist")
class TransformationProperty(QTabWidget):
    lineEditFinished=pyqtSignal()
    def __init__(self,parent=None):
        super(TransformationProperty, self).__init__(parent)
        self.setWindowTitle("Transform")
        formLayout = QFormLayout()

        self.xEdit=QLineEdit()
        self.yEdit = QLineEdit()
        self.zEdit = QLineEdit()
        self.xEdit.editingFinished.connect(self.sendSignal)
        self.yEdit.editingFinished.connect(self.sendSignal)
        self.zEdit.editingFinished.connect(self.sendSignal)
        formLayout.addRow("X", self.xEdit)
        formLayout.addRow("Y", self.yEdit)
        formLayout.addRow("Z", self.zEdit)
        self.setLayout(formLayout)
    def setLineEdit(self,transform:QVector3D):
        self.xEdit.setText(str(transform.x()))
        self.yEdit.setText(str(transform.y()))
        self.zEdit.setText(str(transform.z()))
    def sendSignal(self):
        self.lineEditFinished.emit()
class ColorProperty(QTableWidget):
    VERTICES_COLOR=0
    POLYGON_COLOR=1
    COLOR=2
    colorChanged=pyqtSignal()
    def __init__(self,parent=None):
        super(ColorProperty, self).__init__(parent)
        #property
        self.verticesColor=QColor()
        self.polygonColor=QColor()
        self.color=QColor()

        formLayout=QFormLayout()
        #1st row: vertices color
        self.verticesColorButton=QPushButton()
        self.verticesColorButton.clicked.connect(lambda state,color=self.VERTICES_COLOR: self.colorPicker(color))

        formLayout.addRow("Point color",self.verticesColorButton)
        #2nd row: polygon color
        self.polygonColorButton = QPushButton()
        self.polygonColorButton.clicked.connect(lambda state,color=self.POLYGON_COLOR: self.colorPicker(color))
        formLayout.addRow("Polygon color", self.polygonColorButton)
        #3rd row: item color
        self.colorButton = QPushButton()
        self.colorButton.clicked.connect(lambda state,color=self.COLOR: self.colorPicker(color))
        formLayout.addRow("color", self.colorButton)
        self.updatePushButtonColor()
        self.setLayout(formLayout)

        self.setWindowTitle("Color")
    def setColor(self, item:AbstractSceneNode):
        #convert Qvector3D in item to Qcolor
        self.verticesColor=self.QVector3DtoQcolor(item.verticesColor)
        self.polygonColor=self.QVector3DtoQcolor(item.polygonColor)
        self.color=self.QVector3DtoQcolor(item.color)
        self.updatePushButtonColor()
    def QVector3DtoQcolor(self,vector:QVector3D):
        x=vector.x()
        y=vector.y()
        z=vector.z()
        return QColor(x*255,y*255,z*255)
    def colorPicker(self,colorType:int):
        colorDialog = QColorDialog.getColor(Qt.white, self)
        msg = "r:{},g:{},b:{}".format(colorDialog.red(), colorDialog.green(), colorDialog.blue())
        # QMessageBox.information(None, "Selected color", msg)
        chosenColor=QColor(colorDialog.red(), colorDialog.green(), colorDialog.blue())
        if colorType==self.VERTICES_COLOR:
            self.verticesColor=chosenColor
        elif colorType==self.POLYGON_COLOR:
            self.polygonColor=chosenColor
        elif colorType==self.COLOR:
            self.color=chosenColor
        self.colorChanged.emit()
        self.updatePushButtonColor()
    def setPushButtonBackground(self,pushButton:QPushButton,color:QColor):
        pal = pushButton.palette()
        # if the same color on the color palette is chosen, no change and return
        if color==pal.color(QPalette.Button):
            return
        pal.setColor(QPalette.Button, color)
        pushButton.setAutoFillBackground(True)
        pushButton.setFlat(True)
        pushButton.setPalette(pal)
        pushButton.update()
    def updatePushButtonColor(self):
        self.setPushButtonBackground(self.verticesColorButton, self.verticesColor)
        self.setPushButtonBackground(self.polygonColorButton,self.polygonColor)
        self.setPushButtonBackground(self.colorButton,self.color)
if __name__ == '__main__':
    import sys
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
    item = QListWidgetItem("Asd")
    item.setData(Qt.UserRole, [QVector3D(0, 1, 2), QVector3D()])
    window = PropertyDockWidget(None, item) #Opengl window creation
    window.show()
    application.exec_()
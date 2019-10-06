from PyQt5.QtWidgets import QTabWidget,QApplication,QListWidgetItem,QGridLayout,QLabel,QTableWidget,QTableWidgetItem
from PyQt5.QtGui import QVector3D
from PyQt5.QtCore import Qt,QEvent,pyqtSignal
class propertyDockWidget(QTabWidget):
    def __init__(self,parent=None,item:QListWidgetItem=None):
        super(propertyDockWidget, self).__init__(parent)
        self.setTabPosition(QTabWidget.West)
        self.vertexCoordinateWidget=curveProperty(None)
        self.insertTab(0,self.vertexCoordinateWidget,"Coordinates")
    def updateItems(self,item):
        self.vertexCoordinateWidget.displayItems(item)
class curveProperty(QTabWidget):
    dataChanged=pyqtSignal(QVector3D)
    def __init__(self,parent=None):
        super(curveProperty, self).__init__(parent)
        self.setWindowTitle("Property")

        gridLayout=QGridLayout()
        gridLayout.setSpacing(10)

        vertLabel=QLabel("Vertices")
        #setup table to display vertices coordinate
        self.vertTable=QTableWidget()
        self.vertTable.setColumnCount(3)
        self.vertTable.setColumnWidth(0, 2)
        self.vertTable.setColumnWidth(1, 2)
        self.vertTable.setColumnWidth(2, 2)
        self.vertTable.setHorizontalHeaderItem(0,QTableWidgetItem("x"))
        self.vertTable.setHorizontalHeaderItem(1,QTableWidgetItem("y"))
        self.vertTable.setHorizontalHeaderItem(2,QTableWidgetItem("z"))
        gridLayout.addWidget(vertLabel, 1, 0)
        gridLayout.addWidget(self.vertTable, 2, 0)
        self.setLayout(gridLayout)
        self.setGeometry(300, 300, 350, 300)
        #Signal and custom slots
        self.vertTable.itemDoubleClicked.connect(self.onItemDoubleClick)
        self.vertTable.currentItemChanged.connect(self.updateTable)
        self.sceneItem=None
    def displayItems(self,item:QListWidgetItem):
        self.sceneItem = item
        try:
            vertices=item.data(Qt.UserRole)
            size=len(vertices)
            self.vertTable.setRowCount(size)
            for i,data in enumerate(vertices):
                self.vertTable.setItem(i,0,QTableWidgetItem(str(data.x())))
                self.vertTable.setItem(i,1, QTableWidgetItem(str(data.y())))
                self.vertTable.setItem(i,2, QTableWidgetItem(str(data.z())))
        except Exception as e:
            print(e,"item data doesn't exist")
    def onItemDoubleClick(self,item:QTableWidgetItem):
        #TODO: enable table widget to modify item such as item vertices
        print("Table item modified",item.row(),item.column(),self.vertTable.item(item.row(),item.column()).text())
    def updateTable(self,item:QTableWidgetItem):
        print("item changed")
        new_data=list()
        for row in range(self.vertTable.rowCount()):
            vector=QVector3D(float(self.vertTable.item(row,0).text()),
                             float(self.vertTable.item(row,1).text()),
                             float(self.vertTable.item(row,2).text()),)
            new_data.append(vector)
        self.sceneItem.setData(Qt.UserRole,new_data)
        print(self.sceneItem.data(Qt.UserRole))
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
    window = propertyManager(None,item) #Opengl window creation
    window.show()
    application.exec_()
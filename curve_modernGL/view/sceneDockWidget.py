from PyQt5.QtWidgets import QListWidget,QApplication,QPushButton,QVBoxLayout
from PyQt5.QtCore import QAbstractListModel,QModelIndex,pyqtSignal,QObject
import sys
class sceneDockWidget(QListWidget):
    currentItemSelected=pyqtSignal(QObject)
    def __init__(self,parent=None):
        super(sceneDockWidget, self).__init__(None)
        self.setWindowTitle("Scene")
        self.dragEnabled()
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
    window = sceneDockWidget() #Opengl window creation
    window.show()
    application.exec_()
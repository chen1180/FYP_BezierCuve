from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from curve_modernGL.view.mainWindow import MainWindow
import sys
sys._excepthook = sys.excepthook
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = my_exception_hook

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling,True)
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.showMaximized()
    sys.exit(app.exec_())
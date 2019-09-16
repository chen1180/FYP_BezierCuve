from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QResizeEvent
from PyQt5.QtCore import QStringListModel,Qt,QSize,pyqtSignal
import sys
import os
class textureFileDialog(QWidget):
    resized=pyqtSignal()
    def __init__(self,parent=None):
        super(textureFileDialog, self).__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle("Select textures")
        self.setGeometry(200, 200, 600, 400)

        self.le = QLabel("Preview")
        self.le.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        self.le.setGeometry(200,200,self.width(),self.height())
        layout.addWidget(self.le)

        self.btn = QPushButton("Choose textures from files")
        layout.addWidget(self.btn)
        self.btn.clicked.connect(self.getfile)
        self.resized.connect(self.pixmapResize)
        self.img=None
    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',os.getcwd(), "Image files (*.jpg *.gif)")
        self.img=QPixmap(fname[0])
        img=self.img.scaled(self.le.width(),self.le.height(),Qt.KeepAspectRatio)
        self.le.setScaledContents(True)
        self.le.setPixmap(img)
    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.resized.emit()
        return super(textureFileDialog, self).resizeEvent(a0)
    def pixmapResize(self):
        if self.img:
            img = self.img.scaled(self.le.width(), self.le.height(), Qt.KeepAspectRatio)
            self.le.setPixmap(img)

def main():
    app = QApplication(sys.argv)
    ex = textureFileDialog()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
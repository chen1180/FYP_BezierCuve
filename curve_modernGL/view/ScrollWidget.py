from PyQt5 import QtCore, QtGui, QtWidgets
class ExpandWidget(QtWidgets.QWidget):
    def __init__(self,title=""):
        super(ExpandWidget, self).__init__()
        mainLayout=QtWidgets.QGridLayout()
        self.toggleButton=QtWidgets.QToolButton(self)
        headerLine=QtWidgets.QFrame()
        self.toggleAnimation=QtCore.QParallelAnimationGroup()
        self.contentArea=QtWidgets.QScrollArea()
        self.animationDuration=300

        self.toggleButton.setStyleSheet("QToolButton { border: none; }")
        self.toggleButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toggleButton.setArrowType(QtCore.Qt.ArrowType.RightArrow)
        self.toggleButton.setText(title)
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked(False)

        headerLine.setFrameShape(QtWidgets.QFrame.HLine)
        headerLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        headerLine.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)

        self.contentArea.setStyleSheet("QScrollArea { background-color: white; border: none; }")
        self.contentArea.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.contentArea.setMaximumHeight(0)
        self.contentArea.setMinimumHeight(0)
        self.toggleAnimation.addAnimation(QtCore.QPropertyAnimation(self))
        self.toggleAnimation.addAnimation(QtCore.QPropertyAnimation(self))
        self.toggleAnimation.addAnimation(QtCore.QPropertyAnimation(self.contentArea))

        mainLayout.setVerticalSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        row = 0
        mainLayout.addWidget( self.toggleButton, row, 0, 1, 1, QtCore.Qt.AlignLeft)
        mainLayout.addWidget( headerLine, row, 2, 1, 1)
        mainLayout.addWidget( self.contentArea, row, 0, 1, 3)
        self.setLayout( mainLayout)
        self.toggleButton.clicked.connect(self.toggle)
    def toggle(self,checked):
        self.toggleButton.setArrowType(QtCore.Qt.ArrowType.DownArrow if checked else QtCore.Qt.ArrowType.RightArrow)
        self.toggleAnimation.setDirection(QtCore.QAbstractAnimation.Forward if checked else QtCore.QAbstractAnimation.Backward)
        self.toggleAnimation.start()
    def setContentLayout(self,contentLayout:QtWidgets.QLayout):

        self.contentArea.setLayout(contentLayout)
        self.contentArea.show()
        collapsedHeight = self.sizeHint().height() - self.contentArea.maximumHeight()
        contentHeight = contentLayout.sizeHint().height()
        for i in range(self.toggleAnimation.animationCount()-1):
            spoilerAnimation = QtCore.QPropertyAnimation(self.toggleAnimation.animationAt(i))
            spoilerAnimation.setDuration(self.animationDuration)
            spoilerAnimation.setStartValue(collapsedHeight)
            spoilerAnimation.setEndValue(collapsedHeight + contentHeight)
        contentAnimation = QtCore.QPropertyAnimation(self.toggleAnimation.animationAt(self.toggleAnimation.animationCount()-1))
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)
    #For debug purpose
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
    application= QtWidgets.QApplication([])
    # The follow format can set up the OPENGL context
    layout=QtWidgets.QVBoxLayout()
    layout.addWidget(QtWidgets.QLabel("Asdasd"))
    layout.addWidget(QtWidgets.QPushButton("sadaszxc"))
    window = ExpandWidget() #Opengl window creation
    window.setLayout(layout)
    window.setContentLayout(layout)
    window.show()
    application.exec_()
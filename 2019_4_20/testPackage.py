# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 603)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 801, 561))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.gridLayoutWidget)
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.setAutoFillBackground(True)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.graphicsView.setBackgroundBrush(brush)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.push_button_drawPoint = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.push_button_drawPoint.setMaximumSize(QtCore.QSize(16777215, 100))
        self.push_button_drawPoint.setObjectName("push_button_drawPoint")
        self.verticalLayout.addWidget(self.push_button_drawPoint)
        self.push_button_drawLine = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.push_button_drawLine.setMaximumSize(QtCore.QSize(16777215, 100))
        self.push_button_drawLine.setObjectName("push_button_drawLine")
        self.verticalLayout.addWidget(self.push_button_drawLine)
        self.push_button_drawCurve = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.push_button_drawCurve.setMaximumSize(QtCore.QSize(16777215, 100))
        self.push_button_drawCurve.setObjectName("push_button_drawCurve")
        self.verticalLayout.addWidget(self.push_button_drawCurve)
        self.push_button_clearDrawing = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.push_button_clearDrawing.setMaximumSize(QtCore.QSize(16777215, 100))
        self.push_button_clearDrawing.setObjectName("push_button_clearDrawing")
        self.verticalLayout.addWidget(self.push_button_clearDrawing)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuStart = QtWidgets.QMenu(self.menubar)
        self.menuStart.setObjectName("menuStart")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuStart.menuAction())

        self.retranslateUi(MainWindow)
        self.push_button_drawPoint.clicked.connect(self.graphicsView.invalidateScene)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.push_button_drawPoint.setText(_translate("MainWindow", "Draw Point"))
        self.push_button_drawLine.setText(_translate("MainWindow", "Draw Line"))
        self.push_button_drawCurve.setText(_translate("MainWindow", "Draw Curve"))
        self.push_button_clearDrawing.setText(_translate("MainWindow", "Clear Drawing"))
        self.menuStart.setTitle(_translate("MainWindow", "Start"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

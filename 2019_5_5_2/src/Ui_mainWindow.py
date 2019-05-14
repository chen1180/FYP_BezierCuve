# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1001, 686)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setObjectName("tabWidget")
        self.curve_tab = QtWidgets.QWidget()
        self.curve_tab.setMinimumSize(QtCore.QSize(0, 598))
        self.curve_tab.setObjectName("curve_tab")
        self.formLayout = QtWidgets.QFormLayout(self.curve_tab)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.curve_tab)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.push_button_bezier_quad = QtWidgets.QPushButton(self.curve_tab)
        self.push_button_bezier_quad.setObjectName("push_button_bezier_quad")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.push_button_bezier_quad)
        self.push_button_bezier_cubic = QtWidgets.QPushButton(self.curve_tab)
        self.push_button_bezier_cubic.setObjectName("push_button_bezier_cubic")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.push_button_bezier_cubic)
        self.push_button_bezier_multi = QtWidgets.QPushButton(self.curve_tab)
        self.push_button_bezier_multi.setObjectName("push_button_bezier_multi")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.push_button_bezier_multi)
        self.pushButton_2 = QtWidgets.QPushButton(self.curve_tab)
        self.pushButton_2.setObjectName("pushButton_2")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.pushButton_2)
        self.label_2 = QtWidgets.QLabel(self.curve_tab)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.curve_tab)
        self.pushButton_3.setObjectName("pushButton_3")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.pushButton_3)
        self.tabWidget.addTab(self.curve_tab, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.horizontalLayout.setStretch(1, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1001, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSelect = QtWidgets.QAction(MainWindow)
        self.actionSelect.setObjectName("actionSelect")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionMove = QtWidgets.QAction(MainWindow)
        self.actionMove.setObjectName("actionMove")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Bezier:"))
        self.push_button_bezier_quad.setText(_translate("MainWindow", "QuadBezier"))
        self.push_button_bezier_cubic.setText(_translate("MainWindow", "CubicBezier"))
        self.push_button_bezier_multi.setText(_translate("MainWindow", "MultiBezier"))
        self.pushButton_2.setText(_translate("MainWindow", "Circle"))
        self.label_2.setText(_translate("MainWindow", "Nurbs:"))
        self.pushButton_3.setText(_translate("MainWindow", "Nurbs Curve"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.curve_tab), _translate("MainWindow", "Curve"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))
        self.actionClear.setToolTip(_translate("MainWindow", "Clear the palatte"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSelect.setText(_translate("MainWindow", "Select"))
        self.actionSelect.setToolTip(_translate("MainWindow", "Select an item"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionMove.setText(_translate("MainWindow", "Move"))
        self.actionMove.setToolTip(_translate("MainWindow", "Move an item"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

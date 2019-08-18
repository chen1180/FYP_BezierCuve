# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tmp.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(878, 584)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.drawWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.drawWidget.setObjectName("drawWidget")
        self.BezierCurve = QtWidgets.QWidget()
        self.BezierCurve.setObjectName("BezierCurve")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.BezierCurve)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.drawBtn = QtWidgets.QPushButton(self.BezierCurve)
        self.drawBtn.setObjectName("drawBtn")
        self.verticalLayout_3.addWidget(self.drawBtn)
        self.clearBtn = QtWidgets.QPushButton(self.BezierCurve)
        self.clearBtn.setObjectName("clearBtn")
        self.verticalLayout_3.addWidget(self.clearBtn)
        self.splitBtn = QtWidgets.QPushButton(self.BezierCurve)
        self.splitBtn.setObjectName("splitBtn")
        self.verticalLayout_3.addWidget(self.splitBtn)
        self.drawSurfaceBtn = QtWidgets.QPushButton(self.BezierCurve)
        self.drawSurfaceBtn.setObjectName("drawSurfaceBtn")
        self.verticalLayout_3.addWidget(self.drawSurfaceBtn)
        self.pushButton = QtWidgets.QPushButton(self.BezierCurve)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton)
        self.drawWidget.addTab(self.BezierCurve, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.drawWidget.addTab(self.tab, "")
        self.horizontalLayout_3.addWidget(self.drawWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.openGLWidget = QtWidgets.QOpenGLWidget(self.centralwidget)
        self.openGLWidget.setObjectName("openGLWidget")
        self.horizontalLayout_2.addWidget(self.openGLWidget)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout_3.addLayout(self.formLayout)
        self.horizontalLayout_3.setStretch(1, 6)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 878, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSelect_mode = QtWidgets.QAction(MainWindow)
        self.actionSelect_mode.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Icons/mouse-pointer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSelect_mode.setIcon(icon)
        self.actionSelect_mode.setObjectName("actionSelect_mode")
        self.toolBar.addAction(self.actionSelect_mode)

        self.retranslateUi(MainWindow)
        self.drawWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.drawBtn.setText(_translate("MainWindow", "Draw curve"))
        self.clearBtn.setText(_translate("MainWindow", "Clear"))
        self.splitBtn.setText(_translate("MainWindow", "Split curve"))
        self.drawSurfaceBtn.setText(_translate("MainWindow", "Bezier surface"))
        self.pushButton.setText(_translate("MainWindow", "Bezier circle"))
        self.drawWidget.setTabText(self.drawWidget.indexOf(self.BezierCurve), _translate("MainWindow", "Bezier"))
        self.drawWidget.setTabText(self.drawWidget.indexOf(self.tab), _translate("MainWindow", "B-Spline"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionSelect_mode.setText(_translate("MainWindow", "Select mode"))

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
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.drawBtn = QtWidgets.QPushButton(self.centralwidget)
        self.drawBtn.setObjectName("drawBtn")
        self.verticalLayout_3.addWidget(self.drawBtn)
        self.clearBtn = QtWidgets.QPushButton(self.centralwidget)
        self.clearBtn.setObjectName("clearBtn")
        self.verticalLayout_3.addWidget(self.clearBtn)
        self.splitBtn = QtWidgets.QPushButton(self.centralwidget)
        self.splitBtn.setObjectName("splitBtn")
        self.verticalLayout_3.addWidget(self.splitBtn)
        self.drawSurfaceBtn = QtWidgets.QPushButton(self.centralwidget)
        self.drawSurfaceBtn.setObjectName("drawSurfaceBtn")
        self.verticalLayout_3.addWidget(self.drawSurfaceBtn)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.openGLWidget = QtWidgets.QOpenGLWidget(self.centralwidget)
        self.openGLWidget.setObjectName("openGLWidget")
        self.horizontalLayout_2.addWidget(self.openGLWidget)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 6)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.drawBtn.setText(_translate("MainWindow", "Draw curve"))
        self.clearBtn.setText(_translate("MainWindow", "Clear"))
        self.splitBtn.setText(_translate("MainWindow", "Split curve"))
        self.drawSurfaceBtn.setText(_translate("MainWindow", "Bezier surface"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))

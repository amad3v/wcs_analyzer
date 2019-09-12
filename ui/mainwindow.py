# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtGui, QtWidgets, QtCore


class Ui_mwWCS(object):
    def setupUi(self, mwWCS):
        mwWCS.setObjectName("mwWCS")
        mwWCS.resize(340, 268)
        mwWCS.setMaximumSize(QtCore.QSize(340, 268))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("wcs.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mwWCS.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(mwWCS)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 322, 244))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblInput = QtWidgets.QLabel(self.layoutWidget)
        self.lblInput.setObjectName("lblInput")
        self.verticalLayout.addWidget(self.lblInput)
        self.lstInput = QtWidgets.QListWidget(self.layoutWidget)
        self.lstInput.setObjectName("lstInput")
        self.verticalLayout.addWidget(self.lstInput)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pbAdd = QtWidgets.QPushButton(self.layoutWidget)
        self.pbAdd.setObjectName("pbAdd")
        self.horizontalLayout.addWidget(self.pbAdd)
        self.pbSave = QtWidgets.QPushButton(self.layoutWidget)
        self.pbSave.setObjectName("pbSave")
        self.horizontalLayout.addWidget(self.pbSave)
        self.pbClearList = QtWidgets.QPushButton(self.layoutWidget)
        self.pbClearList.setObjectName("pbClearList")
        self.horizontalLayout.addWidget(self.pbClearList)
        self.pbExit = QtWidgets.QPushButton(self.layoutWidget)
        self.pbExit.setObjectName("pbExit")
        self.horizontalLayout.addWidget(self.pbExit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        mwWCS.setCentralWidget(self.centralwidget)

        self.retranslateUi(mwWCS)
        self.pbClearList.clicked.connect(self.lstInput.clear)
        self.pbExit.clicked.connect(mwWCS.close)
        QtCore.QMetaObject.connectSlotsByName(mwWCS)

    def retranslateUi(self, mwWCS):
        _translate = QtCore.QCoreApplication.translate
        mwWCS.setWindowTitle(_translate("mwWCS", "WCS Analyzer"))
        self.lblInput.setText(_translate("mwWCS", "Input files:"))
        self.pbAdd.setText(_translate("mwWCS", "&Add files"))
        self.pbSave.setText(_translate("mwWCS", "&Save"))
        self.pbClearList.setText(_translate("mwWCS", "&Clear List"))
        self.pbExit.setText(_translate("mwWCS", "&Exit"))

# -*- coding: utf-8 -*-

# Resource object code
#
# Created by: The Resource Compiler for PyQt5 (Qt v5.13.0)
#
# WARNING! All changes made in this file will be lost!

from ui import mainwindow_rc
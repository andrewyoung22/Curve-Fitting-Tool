"""
此代码为designer界面设计后生成的StartupInterfaceUI.ui文件直接转换为Python代码而来
实现了软件的开始界面
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_startup(QMainWindow):
    def setupUi(self, startup):
        startup.setObjectName("startup")
        startup.resize(400, 371)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        startup.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(startup)
        self.label.setGeometry(QtCore.QRect(125, 40, 150, 141))
        self.label.setText("")
        self.label.setObjectName("label")
        self.name = QtWidgets.QLabel(startup)
        self.name.setGeometry(QtCore.QRect(60, 180, 281, 41))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB Demi")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.start_btn = QtWidgets.QPushButton(startup)
        self.start_btn.setGeometry(QtCore.QRect(110, 230, 181, 41))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.start_btn.setFont(font)
        self.start_btn.setObjectName("start_btn")
        self.help_btn = QtWidgets.QPushButton(startup)
        self.help_btn.setGeometry(QtCore.QRect(110, 280, 181, 41))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.help_btn.setFont(font)
        self.help_btn.setObjectName("help_btn")

        self.retranslateUi(startup)
        QtCore.QMetaObject.connectSlotsByName(startup)

    def retranslateUi(self, startup):
        _translate = QtCore.QCoreApplication.translate
        startup.setWindowTitle(_translate("startup", "Curve Fitiing Tool"))
        self.name.setText(_translate("startup", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">Curve Fitting Tool</span></p></body></html>"))
        self.start_btn.setText(_translate("startup", "启动"))
        self.help_btn.setText(_translate("startup", "帮助"))

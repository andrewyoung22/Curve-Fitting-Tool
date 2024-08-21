"""
此代码为designer界面设计后生成的HelpUI.ui文件直接转换为Python代码而来
实现了软件的帮助界面
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices


class Ui_Help(object):
    def setupUi(self, Help):
        Help.setObjectName("Help")
        Help.resize(338, 203)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Help.setWindowIcon(icon)
        self.verticalLayoutWidget = QtWidgets.QWidget(Help)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 271, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cmd_btn1 = QtWidgets.QCommandLinkButton(self.verticalLayoutWidget)
        self.cmd_btn1.setObjectName("cmd_btn1")
        self.verticalLayout.addWidget(self.cmd_btn1, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.cmd_btn2 = QtWidgets.QCommandLinkButton(self.verticalLayoutWidget)
        self.cmd_btn2.setObjectName("cmd_btn2")
        self.verticalLayout.addWidget(self.cmd_btn2, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.cmd_btn3 = QtWidgets.QCommandLinkButton(self.verticalLayoutWidget)
        self.cmd_btn3.setObjectName("cmd_btn3")
        self.verticalLayout.addWidget(self.cmd_btn3, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

        self.cmd_btn1.clicked.connect(self.lagrange_help)
        self.cmd_btn2.clicked.connect(self.cubicspline_help)
        self.cmd_btn3.clicked.connect(self.leastsquares_help)

        self.retranslateUi(Help)
        QtCore.QMetaObject.connectSlotsByName(Help)

    def retranslateUi(self, Help):
        _translate = QtCore.QCoreApplication.translate
        Help.setWindowTitle(_translate("Help", "Curve Fitting Tool Help"))
        self.cmd_btn1.setText(_translate("Help", "了解什么是拉格朗日插值"))
        self.cmd_btn2.setText(_translate("Help", "了解什么是三次样条插值"))
        self.cmd_btn3.setText(_translate("Help", "了解什么是最小二乘拟合"))

    def lagrange_help(self):
        QDesktopServices.openUrl(
            QUrl("https://zh.wikipedia.org/wiki/%E6%8B%89%E6%A0%BC%E6%9C%97%E6%97%A5%E6%8F%92%E5%80%BC%E6%B3%95"))

    def cubicspline_help(self):
        QDesktopServices.openUrl(
            QUrl('https://zh.wikipedia.org/wiki/%E6%A0%B7%E6%9D%A1%E6%8F%92%E5%80%BC?wprov=srpw1_1'))

    def leastsquares_help(self):
        QDesktopServices.openUrl(QUrl('https://zh.wikipedia.org/wiki/%E6%9C%80%E5%B0%8F%E4%BA%8C%E4%B9%98'))

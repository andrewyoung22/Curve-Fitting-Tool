"""
程序入口
主要完成了开始界面的相关功能完善
实现了开始界面窗口和其他窗口的关联与调用
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from StartupInterfaceUI import Ui_startup


class UI_startup(Ui_startup):
    def setupUi(self, startup):
        super().setupUi(startup)
        self.startup = startup
        # 开始界面放置logo图
        self.label.setPixmap(QPixmap('icon.jpg'))
        # 点击“启动”按钮，调用startup_MainWindow函数
        self.start_btn.clicked.connect(self.startup_MainWindow)
        # 点击“帮助”按钮，调用help函数
        self.help_btn.clicked.connect(self.help)

    def startup_MainWindow(self):
        from MainWindow import UI_MainWindow
        # 创建UI_MainWindow类的实例
        self.ui_mainwindow = UI_MainWindow()
        self.MainWindow = QMainWindow()
        self.ui_mainwindow.setupUi(self.MainWindow)
        # 开始界面
        self.MainWindow.show()
        # 关闭开始界面
        self.startup.close()

    def help(self):
        from HelpUI import Ui_Help
        # 创建Ui_Help类的实例
        self.ui_help = Ui_Help()
        self.HelpWindow = QMainWindow()
        self.ui_help.setupUi(self.HelpWindow)
        # 帮助界面
        self.HelpWindow.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("windowsvista")
    startup = QMainWindow()
    ui = UI_startup()
    ui.setupUi(startup)
    startup.show()
    sys.exit(app.exec_())

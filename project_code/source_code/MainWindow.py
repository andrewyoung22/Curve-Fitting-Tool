"""
功能界面（软件主窗口）的相关元素丰富，信号函数搭建
"""
import numpy as np
from PyQt5.QtWidgets import *
import sympy as sym
from MainWindowUI import Ui_MainWindow
from Fitting import CurveFitting


class UI_MainWindow(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.func = sym.Integer(0)
        self.data_process = 0
        self.data_x = np.array([])

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        # 设置控件的初始状态
        self.degree_label.setEnabled(False)
        self.degree_spb.setEnabled(False)
        self.squaremethod.setEnabled(False)
        self.splinemethod.setEnabled(False)
        self.nature1.setEnabled(False)
        self.nature2.setEnabled(False)
        self.value1.setEnabled(False)
        self.value2.setEnabled(False)
        self.value1.setText('0')
        self.value2.setText('0')
        self.clamped1.setVisible(False)
        self.clamped2.setVisible(False)
        self.precision_spb.setValue(3)

        # 信号函数（响应函数）设置，根据用操作执行相应的函数
        self.poly_btn.toggled.connect(self.enable)
        self.cubic_btn.toggled.connect(self.enable)
        self.start_btn.clicked.connect(self.start_fitting)
        self.open_btn.clicked.connect(self.getFile)
        self.calculatebutton.clicked.connect(self.calculate)
        self.splinemethod.currentIndexChanged.connect(self.splinechoose)
        self.squaremethod.currentIndexChanged.connect(self.squarechoose)
        self.extre_btn.clicked.connect(self.extreme_value)

    # 主要实现三次样条下属控件以及最小二乘下属控件的使能状态激活与转换
    def enable(self):
        if self.poly_btn.isChecked():
            self.degree_label.setEnabled(True)
            self.degree_spb.setEnabled(True)
            self.squaremethod.setEnabled(True)
            self.splinemethod.setEnabled(False)
            self.nature1.setEnabled(False)
            self.nature2.setEnabled(False)
        elif self.cubic_btn.isChecked():
            self.degree_label.setEnabled(False)
            self.degree_spb.setEnabled(False)
            self.squaremethod.setEnabled(False)
            self.splinemethod.setEnabled(True)
            self.nature1.setEnabled(True)
            self.nature2.setEnabled(True)
        else:
            self.degree_label.setEnabled(False)
            self.degree_spb.setEnabled(False)
            self.squaremethod.setEnabled(False)
            self.splinemethod.setEnabled(False)
            self.nature1.setEnabled(False)
            self.nature2.setEnabled(False)

    # 实现文件读取，并将其路径写入软件对应位置文本框中
    def getFile(self):
        file = QFileDialog()
        if file.exec_():
            filename = file.selectedFiles()[0]
            self.lineEdit.setText(filename)

    # 点击软件界面“开始拟合”按钮后触发函数，判断所选拟合方法并调用相应的函数
    def start_fitting(self):
        # 如果此时还没选择文件，将会提示用户
        if len(self.lineEdit.text()) == 0:
            QMessageBox.warning(self.MainWindow, "提示", "请先选择文件！")
            return
        # 调用拉格朗日插值算法
        elif self.lagrange_btn.isChecked():
            self.lagrange()
        # 调用三次样条插值算法
        elif self.cubic_btn.isChecked():
            self.cubic_spline()
        # 调用最小二乘拟合算法，并将阶数n传入
        elif self.poly_btn.isChecked():
            n = self.degree_spb.value()
            self.least_squares(n)
        # 如果此时还没选择方法，将会提示用户
        else:
            QMessageBox.warning(self.MainWindow, "提示", "请选择方法！")

    # 拉格朗日插值
    def lagrange(self):
        filename = self.lineEdit.text()
        # 创建CurveFitting类的实例，并传入文件
        curve_fitting = CurveFitting(filename)
        # 调用类下的拉格朗日插值算法，绘制图像，并得到返回值
        self.func, self.data_x = curve_fitting.lagrange()
        # 同时将左右端点写入左右区间文本框
        self.leftvalue.setText(str(self.data_x[0]))
        self.rightvalue.setText(str(self.data_x[-1]))
        # 调用show_expression函数展示表达式
        self.show_expression()
        # 调用extreme_value函数获得最值
        self.extreme_value()

    # 三次样条插值
    def cubic_spline(self):
        filename = self.lineEdit.text()
        # 创建CurveFitting类的实例，并传入文件，处理方法选择以及一阶导数值
        curve_fitting = CurveFitting(filename)
        method = self.splinechoose()
        derivative_a = np.float64(self.value1.text())
        derivative_b = np.float64(self.value2.text())
        # 调用类下的三次样条插值算法，绘制图像，并得到返回值
        self.func, self.data_x = curve_fitting.cubic_spline(method, derivative_a, derivative_b)
        # 同时将左右端点写入左右区间文本框
        self.leftvalue.setText(str(self.data_x[0]))
        self.rightvalue.setText(str(self.data_x[-1]))
        # 调用show_expression函数展示表达式
        self.show_expression()
        # 调用extreme_value函数获得最值
        self.extreme_value()

    # 根据选择选择自然三次样条还是紧压三次样条，控制相关控件的可视与否
    def splinechoose(self):
        if self.splinemethod.currentIndex() == 0:
            self.nature1.setVisible(True)
            self.nature2.setVisible(True)
            self.value1.setEnabled(False)
            self.value2.setEnabled(False)
            self.value1.setText('0')
            self.value2.setText('0')
            self.clamped1.setVisible(False)
            self.clamped2.setVisible(False)
            return 0
        elif self.splinemethod.currentIndex() == 1:
            self.nature1.setVisible(False)
            self.nature2.setVisible(False)
            self.value1.setEnabled(True)
            self.value2.setEnabled(True)
            self.clamped1.setVisible(True)
            self.clamped2.setVisible(True)
            return 1

    # 最小二乘拟合算法
    def least_squares(self, n):
        filename = self.lineEdit.text()
        # 创建CurveFitting类的实例，并传入文件，处理方式
        curve_fitting = CurveFitting(filename)
        # 调用类下的最小二乘拟合算法，绘制图像，并得到返回值
        self.func, self.data_x = curve_fitting.least_squares(n, data_process=self.data_process)
        # 同时将左右端点写入左右区间文本框
        self.leftvalue.setText(str(self.data_x[0]))
        self.rightvalue.setText(str(self.data_x[-1]))
        # 调用show_expression函数展示表达式
        self.show_expression()
        # 调用extreme_value函数获得最值
        self.extreme_value()

    # 根据不同的处理方法，决定阶数选择控件是否使能，并将记录处理方法
    def squarechoose(self):
        if self.squaremethod.currentIndex() == 0:
            self.degree_spb.setEnabled(True)
            self.data_process = 0
        elif self.squaremethod.currentIndex() == 1:
            self.degree_spb.setValue(1)
            self.degree_spb.setEnabled(False)
            self.data_process = 1
        elif self.squaremethod.currentIndex() == 2:
            self.degree_spb.setValue(1)
            self.degree_spb.setEnabled(False)
            self.data_process = 2

    # 表达式展示
    def show_expression(self):
        # 首先将展示文本框清空
        self.textEdit.clear()
        # 根据保留位数确定展示的表达式中的数值的保留位数
        precision = self.precision_spb.value()
        # 对表达式中数值进行小数位数保留处理，由于样条插值有多段函数，此处需要判断是否为样条插值
        if self.cubic_btn.isChecked():
            i = 1
            for func in self.func:
                func = func.xreplace({n: round(n, precision) for n in func.atoms(sym.Number)})
                self.textEdit.append('S{0}:'.format(i) + str(func).replace('**', '^'))
                i += 1
        else:
            func = self.func.xreplace({n: round(n, precision) for n in self.func.atoms(sym.Number)})
            self.textEdit.setText(str(func).replace('**', '^'))

    # 根据拟合函数的表达式计算用户希望计算的x对应的y值
    def calculate(self):
        if len(self.predictinputdata.text()) == 0:
            QMessageBox.warning(self.MainWindow, "提示", "请先输入x值！")
            return
        input_x = float(self.predictinputdata.text())
        precision = self.precision_spb.value()
        x = sym.Symbol('x')
        # 由于样条插值有多段函数，此处仍需要判断是否为样条插值
        if self.cubic_btn.isChecked():
            if input_x < self.data_x[0] or input_x >= self.data_x[-1]:
                QMessageBox.warning(self.MainWindow, "提示", "对于三次样条，您输入的x值应在原数据区间内！")
            else:
                idx = np.where(self.data_x > input_x)[0][0]
                output_y = round(self.func[idx - 1].evalf(subs={x: input_x}), precision)
                self.predictoutputdata.setText(str(output_y))
        else:
            output_y = round(self.func.evalf(subs={x: input_x}), precision)
            self.predictoutputdata.setText(str(output_y))

    # 区间最值计算
    def extreme_value(self):
        # 首先判断两个文本框中均有数字
        if self.leftvalue.text() != '' and self.rightvalue.text() != '':
            left = np.float64(self.leftvalue.text())
            right = np.float64(self.rightvalue.text())
            # 左端点值不能小于右端点值
            if left < right:
                x = sym.Symbol('x')
                interval = np.float64(0.001)
                x_ = np.arange(left, right, interval)
                # 此处仍需对样条插值和非样条插值分开考虑
                if self.cubic_btn.isChecked():
                    if left < self.data_x[0] or right > self.data_x[-1]:
                        QMessageBox.warning(self.MainWindow, "提示", "对于三次样条，您的区间应包含在原数据区间中！")
                    else:
                        indx = np.where(self.data_x > left)[0][0]
                        maximum = minimum = [x_[0], self.func[indx - 1].evalf(subs={x: x_[0]})]
                        idx = indx
                        for xi in x_:
                            if xi > self.data_x[idx]:
                                idx += 1
                            value = self.func[idx - 1].evalf(subs={x: xi})
                            # 如果此处计算值小于保留的最小值，更新最小值的x和y
                            if value < minimum[1]:
                                minimum = [xi, value]
                            # 如果此处计算值大于保留的最大值，更新最大值的x和y
                            if value > maximum[1]:
                                maximum = [xi, value]
                        self.maxxvalue.setText(str(round(maximum[0], 2)))
                        self.maxyvalue.setText(str(round(maximum[1], 2)))
                        self.minxvalue.setText(str(round(minimum[0], 2)))
                        self.minyvalue.setText(str(round(minimum[1], 2)))
                else:
                    maximum = minimum = [x_[0], self.func.evalf(subs={x: x_[0]})]
                    for xi in x_:
                        value = self.func.evalf(subs={x: xi})
                        # 如果此处计算值小于保留的最小值，更新最小值的x和y
                        if value < minimum[1]:
                            minimum = [xi, value]
                        # 如果此处计算值大于保留的最大值，更新最大值的x和y
                        if value > maximum[1]:
                            maximum = [xi, value]
                    self.maxxvalue.setText(str(round(maximum[0], 2)))
                    self.maxyvalue.setText(str(round(maximum[1], 2)))
                    self.minxvalue.setText(str(round(minimum[0], 2)))
                    self.minyvalue.setText(str(round(minimum[1], 2)))
            else:
                QMessageBox.warning(self.MainWindow, "提示", "左端点值必须小于右端点值！")

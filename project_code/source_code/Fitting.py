"""
拟合算法实现
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import sympy as sym


class CurveFitting:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.data_process()
        self.data_x = self.data[0]
        self.data_y = self.data[1]

    # 数据处理
    def data_process(self):
        filename = self.filename
        data = pd.read_excel(filename)
        # 默认header=None，即没有表头
        header = None
        # 判断是否存在表头
        for element in data.columns:
            if type(element) == str:
                header = 0
                break
        # 将读入的数据处理，将数据按x值大小排列
        data = np.array((pd.read_excel(filename, header=header))).T
        data = data[:, data[0, :].argsort()]
        return data

    # 拉格朗日插值算法
    def lagrange(self):
        data_x = self.data_x
        data_y = self.data_y
        x = sym.Symbol('x')
        # f为最终曲线表达式，现赋初值0
        f = sym.Integer(0)
        # 遍历数据获得拉格朗日插值函数
        for k, x_k in enumerate(data_x):
            Lk = 1
            for x_i in data_x:
                if x_i != x_k:
                    Lk *= (x - x_i) / (x_k - x_i)
            f += Lk * data_y[k]
        # 简化表达式
        f = sym.simplify(f)

        # 在数据区间均匀取1000个点作图
        interval = (self.data_x[-1] - self.data_x[0]) / 1000
        curve_x = np.arange(data_x[0], data_x[-1], interval)
        curve_y = np.array([])
        # 根据所取的x值代入表达式进行计算
        for i in curve_x:
            curve_y = np.append(curve_y, f.evalf(subs={x: i}))

        # 绘制图像
        plt.plot(data_x, data_y, 'bo', markersize=4)
        plt.plot(curve_x, curve_y, 'r-', linewidth=2)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()

        return f, self.data_x

    # 三次样条插值算法
    # method=0为选择使用自然样条，method=1为选择使用紧压样条
    # derivative_a、derivative_b为端点一阶导数，用于紧压样条
    def cubic_spline(self, method, derivative_a, derivative_b):
        data_x = self.data_x
        data_y = self.data_y
        h = data_x[1:] - data_x[:-1]
        A = np.array([])
        # 构建自然样条的矩阵A
        if method == 0:
            A_diag = np.insert(np.append((2 * (h[1:] + h[:-1])), 2*h[-1]), 0, 2*h[0])
            A_triu = A_tril = h
            A = np.diag(A_diag) + np.diag(A_tril, -1) + np.diag(A_triu, 1)
        # 构建紧压样条的矩阵A
        elif method == 1:
            A_diag = np.insert(np.append((2 * (h[1:] + h[:-1])), 1), 0, 1)
            A_triu = np.insert(h[1:], 0, 0)
            A_tril = np.append(h[:-1], 0)
            A = np.diag(A_diag) + np.diag(A_tril, -1) + np.diag(A_triu, 1)
        a_diff = data_y[1:] - data_y[:-1]
        u_first = 0
        u_last = 0
        # 构建紧压样条的向量u
        if method == 1:
            u_l = 3 * a_diff[1:] / h[1:]
            u_r = 3 * a_diff[:-1] / h[:-1]
            u_first = u_r[0] - 3 * derivative_a
            u_last = 3 * derivative_b - u_l[-1]
        u = np.insert(np.append(3 * (a_diff[1:] / h[1:] - a_diff[:-1] / h[:-1]), u_last), 0, u_first)

        # a,b,c,d为系数向量
        a = data_y[:-1]
        # 通过解线性方程矩阵，求得系数向量c
        c = np.linalg.solve(A, u)
        b = a_diff / h - h * (2 * c[:-1] + c[1:]) / 3
        d = (c[1:] - c[:-1]) / (3 * h)

        # 由于样条插值为一系列曲线，故使用列表存储各样条表达式
        func = []
        plt.plot(data_x, data_y, 'bo', markersize=4)
        x = sym.Symbol('x')
        for i in range(len(data_x) - 1):
            # 在每一段区间以0.005为间隔取点
            curve_x = np.arange(data_x[i], data_x[i + 1], 0.005)
            curve_y = np.array([])
            f = a[i] + b[i] * (x - data_x[i]) + c[i] * (x - data_x[i]) ** 2 + d[i] * (x - data_x[i]) ** 3
            f = sym.simplify(f)
            func.append(f)
            for j in curve_x:
                value = f.evalf(subs={x: j})
                curve_y = np.append(curve_y, value)
            # 绘制图像
            plt.plot(curve_x, curve_y, 'r-', linewidth=2)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()

        return func, self.data_x

    # 最小二乘拟合算法
    # n为阶数选择
    # data_process为数据处理方式，=0为常规，=1为指数化处理，=2为对数化处理
    def least_squares(self, n, data_process=0):
        data_x = self.data_x
        if data_process == 1:
            # 将x值指数化
            data_x = np.exp(self.data_x)
        if data_process == 2:
            # 将x值对数化
            data_x = np.log(self.data_x)
        data_y = self.data_y

        # 构建计算所使用矩阵
        s = np.array([])
        b = np.array([])
        tmp = np.ones(len(data_x))
        for _ in np.arange(n + 1):
            s = np.append(s, np.sum(tmp))
            b = np.append(b, np.sum(data_y * tmp))
            tmp = data_x * tmp
        for _ in np.arange(n + 1, 2 * n + 1):
            s = np.append(s, np.sum(tmp))
            tmp = data_x * tmp
        M = np.array([])
        for i in np.arange(n + 1):
            M = np.append(M, s[i: i + n + 1])
        M = M.reshape(n + 1, -1)

        # 通过解线性方程矩阵，求得系数向量a
        a = np.linalg.solve(M, b)

        plt.plot(self.data_x, self.data_y, 'bo', markersize=4)
        x = sym.Symbol('x')
        f = sym.Integer(0)

        # 根据数据处理方式记录f的表达式
        if data_process == 0:
            for i, a_i in enumerate(a):
                f = a_i * x ** i + f
        elif data_process == 1:
            for i, a_i in enumerate(a):
                f = a_i * sym.exp(x) ** i + f
        elif data_process == 2:
            for i, a_i in enumerate(a):
                f = a_i * sym.log(x) ** i + f

        f = sym.simplify(f)

        # 在数据区间均匀取1000个点作图
        interval = (self.data_x[-1] - self.data_x[0]) / 1000
        curve_x = np.arange(self.data_x[0], self.data_x[-1], interval)
        curve_y = np.array([])
        for j in curve_x:
            curve_y = np.append(curve_y, f.evalf(subs={x: j}))

        # 绘制图像
        plt.plot(curve_x, curve_y, 'r-', linewidth=2)
        plt.show()

        return f, self.data_x

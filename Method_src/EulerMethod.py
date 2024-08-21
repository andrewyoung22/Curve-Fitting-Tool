import numpy as np
import sympy as sym

a = np.float64(input('输入左端点t值：'))
_t = a
_y = np.float64(input('输入左端点y值：'))
b = np.float64(input('输入右端点t值：'))
h = np.float64(input('输入间隔h：'))
n = int((b - a) / h)
f = sym.sympify(input('输入函数：'))
t = sym.Symbol('t')
y = sym.Symbol('y')

for _ in range(n):
    _y = _y + h * f.evalf(subs={t: _t, y: _y})
    _t += h
    print(_y)

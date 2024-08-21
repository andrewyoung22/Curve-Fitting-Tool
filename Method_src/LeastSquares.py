import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sympy as sym


# def round_expr(expr, num_digits):
#     return expr.xreplace({n: round(n, num_digits) for n in expr.atoms(Number)})


file_name = '../test.xlsx'
data = np.array((pd.read_excel(file_name, header=None))).T
data = data[:, data[0, :].argsort()]
data_x, data_y = data[0], data[1]

n = int(input("Input Approximation Degree: "))

s = np.array([])
b = np.array([])
tmp = np.ones(len(data_x))
for _ in np.arange(n+1):
    s = np.append(s, np.sum(tmp))
    b = np.append(b, np.sum(data_y * tmp))
    tmp = data_x * tmp
for _ in np.arange(n+1, 2*n+1):
    s = np.append(s, np.sum(tmp))
    tmp = data_x * tmp

M = np.array([])
for i in np.arange(n+1):
    M = np.append(M, s[i: i+n+1])
M = M.reshape(n+1, -1)
a = np.linalg.solve(M, b)

plt.plot(data_x, data_y, 'bo', markersize=4)
x = sym.Symbol('x')
f = x - x
for i, a_i in enumerate(a):
    f = a_i * x**i + f
# func = sym.Poly(f, x)
print(f)

func = f.xreplace({n: round(n, 3) for n in f.atoms(sym.Number)})
print(func)


loss = 0
for i, x_i in enumerate(data_x):
    value = f.evalf(subs={x: x_i})
    loss += (data_y[i] - value) ** 2
print(loss)

curve_x = np.arange(data_x[0], data_x[-1], 0.005)
curve_y = np.array([])
for j in curve_x:
    curve_y = np.append(curve_y, f.evalf(subs={x: j}))
plt.plot(curve_x, curve_y, 'r-', linewidth=2)
plt.show()

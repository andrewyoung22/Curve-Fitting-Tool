import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sympy as sym

file_name = '../test.xlsx'
data = np.array((pd.read_excel(file_name, header=None))).T
data = data[:, data[0, :].argsort()]
data_x, data_y = data[0], data[1]
h = data_x[1:] - data_x[:-1]
A_diag = np.insert(np.append((2 * (h[1:] + h[:-1])), 1), 0, 1)
A_triu = np.insert(h[1:], 0, 0)
A_tril = np.append(h[:-1], 0)
A = np.diag(A_diag) + np.diag(A_tril, -1) + np.diag(A_triu, 1)
a_diff = data_y[1:] - data_y[:-1]
# u = np.insert(np.append(3 * (a_diff[1:] / h[1:] - a_diff[:-1] / h[:-1]), 1), 0, 1)
u_l = 3 * a_diff[1:] / h[1:]
u_r = 3 * a_diff[:-1] / h[:-1]
u_first = u_r[0] - 3
u_last = 3 - u_l[-1]
u = np.insert(np.append(u_l - u_r, u_last), 0, u_first)
print(A)
print(u)

a = data_y[:-1]
c = np.linalg.solve(A, u)
b = a_diff / h - h * (2 * c[:-1] + c[1:]) / 3
d = (c[1:] - c[:-1]) / (3 * h)

plt.plot(data_x, data_y, 'bo', markersize=4)
x = sym.Symbol('x')
minimum = [data_x[0], data_y[0]]
curve_x = np.array([])
curve_y = np.array([])

for i in range(len(data_x)-1):
    curve_x = np.arange(data_x[i], data_x[i+1], 0.005)
    curve_y = np.array([])
    f = a[i] + b[i] * (x - data_x[i]) + c[i] * (x - data_x[i]) ** 2 + d[i] * (x - data_x[i]) ** 3
    print(sym.simplify(f))
    for j in curve_x:
        value = f.evalf(subs={x: j})
        if value < minimum[1]:
            minimum = [j, value]
        curve_y = np.append(curve_y, value)
    plt.plot(curve_x, curve_y, 'r-', linewidth=2)
plt.plot(minimum[0], minimum[1], 'ro', markersize=6)
plt.show()
# print(curve_x)
# print(curve_y)

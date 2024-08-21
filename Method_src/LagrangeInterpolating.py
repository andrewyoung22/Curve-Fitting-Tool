import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sympy as sym

file_name = '../test.xlsx'
data = np.array((pd.read_excel(file_name, header=None))).T
data = data[:, data[0, :].argsort()]
data_x, data_y = data[0], data[1]

x = sym.Symbol('x')
f = x - x
for k, x_k in enumerate(data_x):
    Lk = 1
    for x_i in data_x:
        if x_i != x_k:
            Lk *= (x - x_i) / (x_k - x_i)
    f += Lk * data_y[k]

print(sym.simplify(f))
curve_x = np.arange(data_x[0], data_x[-1], 0.01)
curve_y = np.array([])
for i in curve_x:
    curve_y = np.append(curve_y, f.evalf(subs={x: i}))

plt.plot(data_x, data_y, 'bo', markersize=4)
plt.plot(curve_x, curve_y, 'r-', linewidth=2)
plt.xlabel('x')
plt.ylabel('y')
plt.show()

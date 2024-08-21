import numpy as np
import sympy as sym

# upper = 2 * np.e
# lower = np.e
upper = np.float64(input('输入积分上限：'))
lower = np.float64(input('输入积分下限：'))
N = int(int(input('输入精度阶数（偶数）：'))/2)
f = sym.sympify(input('输入被积函数：'))

R = np.zeros((N, N))
x = sym.Symbol('x')
f_low = f.evalf(subs={x: lower})
f_up = f.evalf(subs={x: upper})

for i in np.arange(0, N):
    n = 2**i
    h = (upper - lower) / n
    M = np.array([f.evalf(subs={x: i}) for i in np.linspace(lower, upper, n+1)]) * 2
    R[i][0] = h/2 * (np.sum(M) - f_low - f_up)

start = 1
for j in np.arange(start, N):
    for k in np.arange(start, N):
        R[k][j] = R[k][j-1] + (R[k][j-1] - R[k-1][j-1]) / (4**j - 1)
    start += 1

print(R)
print(sym.integrate(f, (x, lower, upper)))

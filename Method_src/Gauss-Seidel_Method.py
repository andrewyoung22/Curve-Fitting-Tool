import numpy as np

N = int(input("Matrix Size N:"))
a, b = [], []
for i in range(1, N+1):
    a.append(list(map(np.float32, input(f"Input Row{i} Elements of Matrix:").rstrip().split(" "))))
    b.append(np.float32(input(f"Input b[{i}] Element:")))
a, b = np.array(a), np.array(b)

if 0 in np.diag(a):
    print("Cannot Use Jacobi Method !")
    exit(1)

D = np.diag(np.diag(a))
L = -np.tril(a, -1)
U = -np.triu(a, 1)

DL_inv  = np.linalg.inv(D-L)
TOL = np.float16(input("Input TOL:"))
X = np.zeros(N)
_X = np.full(N, TOL+1)

while np.max(np.abs(X-_X)) > TOL:
    _X = X
    X = DL_inv @ U @ X + DL_inv @ b
    print(X)
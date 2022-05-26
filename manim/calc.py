import numpy as np

p0 = [(-2, 0, 0), (0, 2, 0)]
p1 = [(1, 0.75, 3), (-0.25, -1, 3)]

A = []
B = []
for i in range(2):
    x0, y0, z0 = p0[i]
    x1, y1, z1 = p1[i]
    l, m, n = x1 - x0, y1 - y0, z1 - z0
    A.append([m, -l, 0])
    B.append(-(l * y0 - m * x0))
    A.append([0, n, -m])
    B.append(-(m * z0 - n * y0))
    A.append([n, 0, -l])
    B.append(-(l * z0 - n * x0))
A = np.matrix(A)
A = A.reshape((-1, 3))
B = np.matrix(B)
B = B.reshape((-1, 1))
X = (A.T * A).I * A.T * B
print(X)
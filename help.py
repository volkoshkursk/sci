import numpy as np

f = np.loadtxt('lambda')

for i in range(671):
    print(sum(f[:, i]))

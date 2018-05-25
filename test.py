import cmath
import numpy as np
import matplotlib.pyplot as plt


w = np.linspace(-1000000, 1000000, 10000000)
w = np.insert(w, 0, -np.inf)
w = np.append(w, np.inf)
print(w)
#z = w ** 2 + 2 / w * 1j
#z = w * 1j / (1 + w * 1j)
z = (3 + w * 1j) * (4 + w * 1j) / ((1 + w * 1j) * (10 + w * 1j) * (2 + w * 1j))

plt.plot(z.real, z.imag)
plt.show()

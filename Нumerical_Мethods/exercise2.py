import numpy as np
import math
import matplotlib.pyplot as plt

x_values = np.linspace(-1, 1, 1000)

def p1(x):
    return (x-9)**9

def p2(x):
    return x**9 - 18*x**8 + 144*x**7 - 672*x**6 + 2016*x**5 - 4032*x**4 + 5376*x**3 - 4608*x**2 + 2304*x - 512

plt.plot(x_values, p1(x_values), x_values, p2(x_values))
plt.legend(['p1(x)', 'p2(x)'])
plt.show()

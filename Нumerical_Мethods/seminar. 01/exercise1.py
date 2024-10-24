import numpy as np
import math
import matplotlib.pyplot as plt

x_value = np.linspace(-0.5, 0.5, 1000)

def f(x):
    return (math.e)**x

def g(x):
    return  1 + x + 0.5*x**2 + 0.1667*x**3

plt.plot(x_value, f(x_value), x_value, g(x_value))
plt.legend(["f(x)", "g(x)"])
plt.show()

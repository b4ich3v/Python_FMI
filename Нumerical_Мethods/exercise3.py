import numpy as np
import math
import matplotlib.pyplot as plt

x_values = [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990]
y_values = [106.46, 123.08, 132.12, 152.27, 180.67, 205.05, 227.23, 249.46]

def function(x, x_values, y_values):
    result = 0
    for i in range(len(x_values)):
        term = y_values[i]
        for j in range(len(x_values)):
            if i != j:
                term *= (x - x_values[j]) / (x_values[i] - x_values[j])
            result += term
        return result

x_axis = np.linspace(1920,1990,1000000)
plt.plot(x_axis, function(x_axis, x_values, y_values), x_values, y_values)
plt.legend(["function(x)", "real(x)"])
plt.show()

import numpy as np
import math
import matplotlib.pyplot as plt

x_values = [1, 2, 4, 6]
y_values = [2, 9, 41, 97]

def function(x, x_values, y_values):
    result = 0
    for i in range(len(x_values)):
        term = y_values[i]
        for j in range(len(x_values)):
            if i != j:
                term *= (x - x_values[j]) / (x_values[i] - x_values[j])
            result += term
        return result

x_axis = np.linspace(-1,1,1000000)
plt.plot(x_axis, function(x_axis, x_values, y_values))
plt.legend(["function(x)"])
plt.show()

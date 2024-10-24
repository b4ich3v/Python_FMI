import math
import numpy as np
import matplotlib.pyplot as plt

x_values = [0, math.pi / 6, math.pi / 3, math.pi / 2]
y_values = []

for current in x_values:
    y_values.append(math.sin(current))

def function(x_values, y_values, x):
    result = 0
    for i in range(len(x_values)):
        term = y_values[i]
        for j in range(len(x_values)):
            if i != j:
                term *= (x - x_values[j]) / (x_values[i] - x_values[j])
        result += term
    return result

x_target = math.pi / 5
approx_value = function(x_values, y_values, x_target)
exact_value = math.sin(x_target)
error = abs(exact_value - approx_value)

print(approx_value)
print(exact_value)
print(error)

x_plot = np.linspace(0, math.pi / 2, 100)
y_plot_exact = np.sin(x_plot)
y_plot_approx = [function(x_values, y_values, x) for x in x_plot]

plt.plot(x_plot, y_plot_exact, label = "sin(x)", color = "blue")
plt.plot(x_plot, y_plot_approx, linestyle = "--", color = "red")
plt.scatter(x_values, y_values, color = "green", zorder = 5)
plt.legend()
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.show()

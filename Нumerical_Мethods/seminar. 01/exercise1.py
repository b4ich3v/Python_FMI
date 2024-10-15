import math
import numpy as np
import matplotlib.pyplot as plt

x_values = [0, math.pi / 6, math.pi / 3, math.pi / 2]
y_values = []

for current in x_values:
    y_values.append(math.sin(current))

def func(x, x_values, y_values):
    result = 0
    for i in range(len(x_values)):
        term = y_values[i]
        for j in range(len(x_values)):
            if i != j:
                term *= (x - x_values[j]) / (x_values[i] - x_values[j])
        result += term
    return result

x = math.pi / 5
result = func(x, x_values, y_values)
print(result)

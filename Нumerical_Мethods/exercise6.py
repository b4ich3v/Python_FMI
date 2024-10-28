import numpy as np
import matplotlib.pyplot as plt
import math

def f(x):
    return 1 / (1 + x)

x_values = [0, 1]
y_values = [f(current) for current in x_values]

def interpolation(x, x_values, y_values):
    result = 0
    for i in range(len(x_values)):
        term = y_values[i]
        for j in range(len(x_values)):
            if i != j:
                term *= (x - x_values[j]) / (x_values[i] - x_values[j])
        result += term
    return result

real = f(0.75)
apr = interpolation(0.75, x_values, y_values)
error = abs(real - apr)
print(real, apr, error)

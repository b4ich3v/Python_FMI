import numpy as np
import math
import matplotlib.pyplot as plt

x_values = [0, 1]
y_values = [1, 0.5]

def f(x):
    return x / (x + 1)

def function(x, x_values, y_values):
    result = 0
    for i in range(len(x_values)):
        term = y_values[i]
        for j in range(len(x_values)):
            if i != j:
                term *= (x - x_values[j]) / (x_values[i] - x_values[j])
            result += term
        return result

target = 0.75
apr = function(target, x_values, y_values)
real = f(target)
error = abs(real - apr)
print(apr, error)

import math
import numpy as np
import matplotlib.pyplot as plt

def lagrange_poly(f, nodes, x):
    n = len(nodes)
    result = 0
    for i in range(n):
        term = f(nodes[i])
        for j in range(n):
            if i != j:
                term *= (x - nodes[j]) / (nodes[i] - nodes[j])
        result += term
    return result

nodes = [0, math.pi / 6, math.pi / 3, math.pi / 2]
x = math.pi / 4
result = lagrange_poly(math.sin, nodes, x)
print(result)

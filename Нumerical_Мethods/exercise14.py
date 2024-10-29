import numpy as np
import sympy as sp


def divided_difference(nodes, values):
    n = len(nodes)
    coeffs = np.zeros((n, n))
    coeffs[:, 0] = values

    for j in range(1, n):
        for i in range(n - j):
            coeffs[i][j] = (coeffs[i + 1][j - 1] - coeffs[i][j - 1]) / (nodes[i + j] - nodes[i])

    return coeffs[0]  # Връща коефициентите на полинома


def newton_poly(nodes, values):
    x = sp.Symbol("x")
    coeffs = divided_difference(nodes, values)

    result = coeffs[0]
    product = 1

    for i in range(1, len(nodes)):
        product *= (x - nodes[i - 1])
        result += coeffs[i] * product

    return result

nodes = [0.163928, 0.53282, 3.00007, 11.2078, 26.7487, 47.3297, 76.8061]
values = [10, 20, 50, 100, 150, 200, 250]

res_pol = newton_poly(nodes, values)
target = 30
result = res_pol.subs("x", target)
print(result)

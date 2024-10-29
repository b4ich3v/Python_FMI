import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

def chebyshev_nodes(n):
    return [np.cos((2*k - 1) / (2*n) * np.pi) for k in range(1, n + 1)]

def runge(x):
    return 1 / (1 + 25 * x**2)

def diff(nodes, values):
    if len(nodes) == 1:
        return values[0]
    den = nodes[-1] - nodes[0]
    return (diff(nodes[1:], values[1:]) - diff(nodes[:-1], values[:-1])) / den

def newton_poly(nodes, values):
    x = sp.Symbol("x")
    product = 1
    result = values[0]
    for i in range(1, len(nodes)):
        coeff = diff(nodes[:i + 1], values[:i + 1])
        product *= (x - nodes[i - 1])
        result += coeff * product
    return result

n = 10
nodes = chebyshev_nodes(n)
values = [runge(current) for current in nodes]

res_pol = newton_poly(nodes, values)  
res_pol_simplified = res_pol.simplify()  

nodes_real = np.linspace(-1, 1, 100)
values_real = [runge(current) for current in nodes_real]
values_appr = [res_pol_simplified.subs("x", current) for current in nodes_real]

error = np.abs(np.array(values_real) - np.array(values_appr))

plt.plot(nodes_real, error)
plt.show()

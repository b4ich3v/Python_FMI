import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

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

x_nodes1 = np.linspace(-1, 1, 10)
y_values1 = [runge(current) for current in x_nodes1]

x_nodes2 = np.linspace(-1, 1, 4)
y_values2 = [runge(current) for current in x_nodes2]

res_pol1 = newton_poly(x_nodes1, y_values1)
res_pol2 = newton_poly(x_nodes2, y_values2)

apr_values1 = [res_pol1.subs("x", current) for current in x_nodes1]
apr_values2 = [res_pol2.subs("x", current) for current in x_nodes2]

plt.plot(x_nodes1, apr_values1, label='pol1')
plt.plot(x_nodes2, apr_values2, label='pol2')
plt.show()

import sympy as sp

def diff(nodes, values):
    if len(nodes) == 1:
        return values[0]
    den = nodes[-1] - nodes[0]
    return (diff(nodes[1:], values[1:]) - diff(nodes[:-1], values[:-1])) / den

def newton_poly(nodes, values):
    x = sp.Symbol("x")
    result = values[0]
    product = 1
    for i in range(1, len(nodes)):
        coeff = diff(nodes[:i + 1], values[:i + 1])
        product *= (x - nodes[i - 1])
        result += coeff * product
    return result

nodes = [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990]
values = [106.46, 123.08, 132.12, 152.27, 180.67, 205.05, 227.23, 249.46]
res_pol = newton_poly(nodes, values)
res_pol.simplify()

x_targets = [1952, 1974, 2000]
x_values = [res_pol.subs("x", current) for current in x_targets]

print(x_values)

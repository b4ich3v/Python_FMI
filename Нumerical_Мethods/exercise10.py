def diff(nodes, values):
    if len(nodes) == 1:
        return values[0]
    den = nodes[-1] - nodes[0]
    return (diff(nodes[1:], values[1:]) - diff(nodes[:-1], values[:-1])) / den
    
def newton_poly(nodes, values, x):
    result = values[0]
    product = 1
    for i in range(1, len(nodes)):
        coeff = diff(nodes[:i + 1], values[:i + 1])
        product *= (x - nodes[i - 1])
        result += coeff * product
    return result

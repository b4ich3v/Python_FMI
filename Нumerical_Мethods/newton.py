import numpy as np
import sympy
import sympy as sp

def diff(nodes, values):
    if len(nodes) == 1:
        return values[0]
    return diff(nodes[1:], values[1:]) - diff(nodes[:-1], values[:-1]) / (nodes[-1] - nodes[0])

def newton_pol_ve1(nodes, values, x):
    result = values[0]
    product = 1
    for i in range(1, len(nodes)):
        coeff = diff(nodes[:i + 1], values[:i + 1])
        product *= (x - nodes[i - 1])
        result += coeff * product
    return result

def newton_pol_ve2(nodes, values):
    x = sympy.Symbol("x")
    result = values[0]
    product = 1
    for i in range(1, len(nodes)):
        coeff = diff(nodes[:i + 1], values[:i + 1])
        product *= (x - nodes[i - 1])
        result += coeff * product
    return result

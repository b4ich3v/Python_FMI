import numpy as np
import sympy as sp

def lagrange_pol_ve1(nodes, values, x):
    result = 0
    for i in range(len(nodes)):
        term = values[i]
        for j in range(len(nodes)):
            if i != j:
                term *= (x - nodes[j]) / (nodes[i] - nodes[j])
        result += term
    return result

def lagrange_pol_ve2(nodes, values):
    x = sympy.Symbol("x")
    result = 0
    for i in range(len(nodes)):
        term = values[i]
        for j in range(len(nodes)):
            if i != j:
                term *= (x - nodes[j]) / (nodes[i] - nodes[j])
        result += term
    return result

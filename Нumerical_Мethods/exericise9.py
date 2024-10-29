def divided_difference(nodes, values):
    if len(nodes) == 1:
        return values[0]
    den = nodes[-1] - nodes[0]
    return (divided_difference(nodes[1:], values[1:]) - divided_difference(nodes[:-1], values[:-1])) / den

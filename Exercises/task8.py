def reverse_string(string):
    ls_string = list(string)
    ls_reversed_string = []
    for i in range(len(ls_string) - 1 ,-1, -1):
        ls_reversed_string.append(ls_string[i])
    reversed_string = ""
    for current in ls_reversed_string:
        reversed_string += current
    return reversed_string

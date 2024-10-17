def is_palindrome(string):
    ls_string = list(string)
    ls_reversed_string = []
    for i in range(len(ls_string) - 1, -1, -1):
        ls_reversed_string.append(ls_string[i])
    return ls_string == ls_reversed_string

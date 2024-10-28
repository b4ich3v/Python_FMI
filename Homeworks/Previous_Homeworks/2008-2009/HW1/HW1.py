def fizzbuzz(n):
    if not isinstance(n, int):
        print("Tup")
        return None
    else:
        result = []
        for i in range(1, n + 1, 1):
            if i % 3 == 0 and not i % 5 == 0:
                result.append("Fizz")
            elif i % 5 == 0 and not i % 3 == 0:
                result.append("Buzz")
            elif i % 3 == 0 and i % 5 == 0:
                result.append("FizzBuzz")
            else:
                result.append(i)
        return result

def find_index_max(ls_input):
    max = ls_input[0]
    for current in ls_input:
        if current >= max:
            max = current
    return max

def find_index_min(ls_input):
    min = ls_input[0]
    for current in ls_input:
        if current <= min:
            min = current
    return min

def find_index_close_mid(ls_input, target):
    eps = abs(target - ls_input[0])
    index = ls_input[0]
    for i in range(len(ls_input)):
        current_eps = abs(target - ls_input[i])
        if current_eps <= eps:
            eps = current_eps
            index = ls_input[i]
    return index

def minmaxmean(input_dic):
    if not isinstance(input_dic, dict):
        print("Tup")
        return None
    else:
        ls_values = []
        for key, value in input_dic.items():
            ls_values.append(value)
        max = find_index_max(ls_values)
        min = find_index_min(ls_values)
        middle = find_index_close_mid(ls_values, (max + min) / 2)
        first , second, third= "", "", ""
        for key, value in input_dic.items():
            if value == min:
                first = key
            elif value == max:
                second = key
            elif value == middle:
                third = key
            else:
                continue
        return (first, second, third)

def is_anagram(word1, word2):
    if not isinstance(word1, str) or not isinstance(word2, str):
        return False
    return sorted(word1.lower()) == sorted(word2.lower())

def anagrams(ls_strings):
    if not isinstance(ls_strings, list):
        return None
    else:
        result = []
        used_indexes = set()
        for i in range(len(ls_strings)):
            if i in used_indexes:
                continue
            current = [ls_strings[i]]
            used_indexes.add(i)
            for j in range(i + 1, len(ls_strings)):
                if j not in used_indexes and is_anagram(ls_strings[i], ls_strings[j]):
                    current.append(ls_strings[j])
                    used_indexes.add(j)
            if len(current) > 1:
                result.append(current)
        return result


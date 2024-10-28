def make_multiset(input_list):
    if not isinstance(input_list, list):
        print("Tup")
    else:
        helper = set(current_arg for current_arg in input_list)
        result = {}
        for element in helper:
            counter = 0
            for current_arg in input_list:
                if element == current_arg:
                    counter += 1
                result[element] = counter
        return result

def bubble_sort(items):
    size = len(items)
    for i in range(size):
        for j in range(size - i - 1):
            if items[j][0] > items[j + 1][0]:
                items[j], items[j + 1] = items[j + 1], items[j]

def ordered_dict(input_dict):
    if not isinstance(input_dict, dict):
        print("Tup")
    else:
        items = list(input_dict.items())
        bubble_sort(items)
        sorted_dict = dict(items)
        return sorted_dict

def reversed_dict(input_dict):
    if not isinstance(input_dict, dict):
        print("Tup")
    else:
        reversed_dict = {}
        for key, value in input_dict.items():
            reversed_dict[value] = key
        return reversed_dict

def unique_objects(input_list):
    if not isinstance(input_list, list):
        print("Tup")
        return 0
    else:
        counter = 0
        for item in input_list:
            if isinstance(item, list):
                counter += unique_objects(item)
            elif isinstance(item, int):
                counter += 1
        return counter

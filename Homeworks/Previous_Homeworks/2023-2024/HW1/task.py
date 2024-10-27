def calculate_remainder(word):
    return len(word) % 3

def beginning(word):
    if not isinstance(word, str):
        print("Tup")
    else:
        remainder = calculate_remainder(word)
        if remainder == 0 or remainder == 1:
            index = len(word) // 3
            result = ""
            for i in range(index):
                result += word[i]
            return result
        else:
            index = len(word) // 3
            result = ""
            for i in range(index + 1):
                result += word[i]
            return result

def middle(word):
    if not isinstance(word, str):
        print("Tup")
    else:
        remainder = calculate_remainder(word)
        if remainder == 0:
            index = len(word) // 3
            result = ""
            for i in range(index, len(word) - index, 1):
                result += word[i]
            return result
        elif remainder == 1:
            index = len(word) // 3
            result = ""
            for i in range(index, len(word) - index, 1):
                result += word[i]
            return result
        else:
            index = len(word) // 3
            result = ""
            for i in range(index + 1, len(word) - index - 1, 1):
                result += word[i]
            return result

def end(word):
    if not isinstance(word, str):
        print("Tup")
    else:
        size = len(word)
        start_part = beginning(word)
        middle_part = middle(word)
        index = len(start_part) + len(middle_part)
        result = ""
        for i in range(index, size, 1):
            result += word[i]
        return result

def split_sentence(sentence):
    if not isinstance(sentence, str):
        print("Tup")
    else:
        result = []
        ls_sentence = sentence.split()
        for current in ls_sentence:
            start_part = beginning(current)
            middle_part = middle(current)
            end_part = end(current)
            current_element = (start_part, middle_part, end_part)
            result.append(current_element)
        return result

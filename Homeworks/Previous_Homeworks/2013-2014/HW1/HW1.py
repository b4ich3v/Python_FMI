def wow_such_much(start, end):
    if not (isinstance(start, int) and isinstance(end, int)):
        print("Tup")
    else:
        result = []
        for i in range(start, end, 1):
            if i % 3 == 0 and not i % 5 ==0:
                result.append("such")
            elif i % 5 == 0 and not i % 3 ==0:
                result.append("much")
            elif i % 3 == 0 and i % 5 == 0:
                result.append("suchmuch")
            else:
                result.append(i)
        return result

def count_doge_words(sentence):
    if not isinstance(sentence, str):
        print("Tup")
    else:
        counter = 0
        str_sentence = sentence.split()
        for current_word in str_sentence:
            if current_word == "wow" or current_word == "lol" or current_word == "so" or current_word == "such" or current_word == "much" or current_word == "very":
                counter += 1
        return counter

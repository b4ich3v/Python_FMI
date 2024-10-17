def count_vowels(string):
    vowels = "аъоуеиАЪОУЕИ"
    return sum(1 for char in string if char in vowels)

import unittest
from unittest.mock import mock_open, patch
from secret import validate_recipe, RuinedNikuldenDinnerError

def simple_cache(func):
    data = {}

    def wrapper(*args):
        if args in data:
            return data[args]
        result = func(*args)
        data[args] = result
        return result

    return wrapper

@simple_cache
def generate_all_variations(word):
    size = len(word)
    result = []
    for i in range(1 << size):  
        current = []
        for j in range(size):
            if i & (1 << j):  
                current.append(word[j].upper())
            else:
                current.append(word[j].lower())
        result.append(''.join(current))
    return result

@simple_cache
def generate_all_insertions_for_keyword(word, special_word):
    return [word[:i] + special_word + word[i:] for i in range(len(word) + 1)]

@simple_cache
def generate_all_insertions_for_random(word, special_word):
    return [special_word[:i] + word + special_word[i:] for i in range(len(special_word) + 1)]

class TestNikuldenValidator(unittest.TestCase):

    def setUp(self):
        self.keywords = ["риба", "рибена", "шаран", "сьонга"]
        self.special_word = "рок"
        self.valid_keywords = set()
        self.invalid_keywords = set()
        self.some_edge_cases = ["", "\t", "\n", "123"]

        self.templates = [
            "Днес ще ям {keyword}, защото е Никулден ;Д.",
            "Тази рецепта включва {keyword}.",
            "{keyword} е подходящо ястие за Никулден.",
            "Нямам против да приготвя {keyword}, знаейки че иначе ще бъде жена ми ;(.",
            "{keyword} е доста екзотично и полезно ястие."
        ]

        for current_keyword in self.keywords:
            variations = generate_all_variations(current_keyword)
            self.valid_keywords.update(variations)

    def test_valid_recipe(self):
        valid_contents = [
            template.format(keyword=current_keyword)
            for current_keyword in self.valid_keywords
            for template in self.templates
        ]

        for content in valid_contents:
            with self.subTest(content=content):
                m = mock_open(read_data=content)
                with patch("builtins.open", m):
                    result = validate_recipe("dummy_path.txt")
                    self.assertTrue(result, f"Expected True for content: {content}")

    def test_invalid_recipe(self):
        for current_keyword in self.valid_keywords:
            variations_keyword = generate_all_insertions_for_keyword(current_keyword, self.special_word)
            variations_random = generate_all_insertions_for_random(current_keyword, self.special_word)
            self.invalid_keywords.update(variations_keyword)
            self.invalid_keywords.update(variations_random)

        invalid_contents = self.some_edge_cases.copy()

        invalid_contents.extend(
            template.format(keyword=current_keyword)
            for current_keyword in self.invalid_keywords
            for template in self.templates
        )

        for content in invalid_contents:
            with self.subTest(content=content):
                m = mock_open(read_data=content)
                with patch("builtins.open", m):
                    result = validate_recipe("dummy_path.txt")
                    self.assertFalse(result, f"Expected False for content: {content}")

    def test_bad_recipe_file(self):
        error_cases = [OSError, IOError]

        for error in error_cases:
            with self.subTest(error=error):
                with patch("builtins.open", side_effect=error):
                    with self.assertRaises(RuinedNikuldenDinnerError):
                        validate_recipe("missing_file.txt")

if __name__ == "__main__":
    unittest.main()

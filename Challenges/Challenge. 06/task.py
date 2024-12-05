import unittest
from unittest.mock import mock_open, patch
from secret import validate_recipe, RuinedNikuldenDinnerError

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

def generate_all_insertions_for_keyword(word, special_word):
    variations = []
    for i in range(len(word) + 1):
        new_word = word[:i] + special_word + word[i:]
        variations.append(new_word)
    return variations

def generate_all_insertions_for_random(word, special_word):
    variations = []
    for i in range(len(special_word) + 1):
        new_word = special_word[:i] + word + special_word[i:]
        variations.append(new_word)
    return variations

class TestNikuldenValidator(unittest.TestCase):

    def setUp(self):
        self.keywords = ["риба", "рибена", "шаран", "сьонга"]
        self.special_word = "рок"
        self.valid_keywords = set()
        self.invalid_keywords = set()
        self.some_edge_cases = ["", "\t", "\n"]

        for current_keyword in self.keywords:
            variations = generate_all_variations(current_keyword)
            self.valid_keywords.update(variations)

    def test_valid_recipe(self):
        valid_contents = []
        for current_keyword in self.valid_keywords:
            valid_contents.extend([
                f"Днес ще ям {current_keyword}, защото е Никулден ;Д.",
                f"Тази рецепта включва {current_keyword}.",
                f"{current_keyword} е подходящо ястие за Никулден.",
                f"Нямам против да приготвя {current_keyword}, знаейки че иначе ще бъде жена ми ;(.",
                f"{current_keyword} е доста екзотично и полезно ястие."
            ])
       
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

        for current_keyword in self.invalid_keywords:
            invalid_contents.extend([
                f"Днес ще ям {current_keyword}, защото е Никулден ;Д.",
                f"Тази рецепта включва {current_keyword}.",
                f"{current_keyword} е подходящо ястие за Никулден.",
                f"Нямам против да приготвя {current_keyword}, знаейки че иначе ще бъде жена ми ;(.",
                f"{current_keyword} е доста екзотично и полезно ястие."
            ])

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

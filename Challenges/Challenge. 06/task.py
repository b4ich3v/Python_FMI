import unittest
from unittest.mock import mock_open, patch
from secret import validate_recipe, RuinedNikuldenDinnerError

def generate_all_variations(word):
    n = len(word)
    variations = []
    for i in range(1 << n):  
        variation = []
        for j in range(n):
            if i & (1 << j):  
                variation.append(word[j].upper())
            else:
                variation.append(word[j].lower())
        variations.append(''.join(variation))
    return variations


class TestNikuldenValidator(unittest.TestCase):

    def test_valid_recipe(self):
        keywords = ['риба', 'рибена', 'шаран', 'сьонга']

        valid_keywords = []
        for current_keyword in keywords:
            valid_keywords.extend(generate_all_variations(current_keyword))

        valid_contents = []
        for current_keyword in valid_keywords:
            self.valid_contents.append(f"Днес ще ям {current_keyword}, защото е Никулден ;Д")
            self.valid_contents.append(f"Тази рецепта включва {current_keyword}.")
            self.valid_contents.append(f"{current_keyword} е идеална за Никулден.")
            self.valid_contents.append(f"Нямам против да приготвя {current_keyword} тази година.")
            self.valid_contents.append(f"{current_keyword} и още нещо вкусно.")
           
        for content in valid_contents:
            with self.subTest(content=content):
                m = mock_open(read_data=content)
                with patch('builtins.open', m):
                    result = validate_recipe("dummy_path.txt")
                    self.assertTrue(result, f"Рецептата '{content}' трябва да е валидна.")

    def test_invalid_recipe(self):
        invalid_contents = [
            "",            
            " ",           
            "\n",          
            "картофи",     
            "месо",        
            "12345",       
            "randomtext",  
            "плодове и зеленчуци"  
        ]

        for content in invalid_contents:
            with self.subTest(content=content):
                m = mock_open(read_data=content)
                with patch('builtins.open', m):
                    result = validate_recipe("dummy_path.txt")
                    self.assertFalse(result, f"Рецептата '{content}' не трябва да е валидна.")

    def test_bad_recipe_file(self):
        error_cases = [OSError, IOError]

        for error in error_cases:
            with self.subTest(error=error):
                with patch("builtins.open", side_effect=error):
                    with self.assertRaises(RuinedNikuldenDinnerError):
                        validate_recipe("missing_file.txt")


if __name__ == "__main__":
    unittest.main()

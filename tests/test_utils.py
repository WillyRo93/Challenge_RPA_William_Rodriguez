import os
import sys
from datetime import datetime
import unittest

# Agregar el directorio del proyecto al path de Python
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)

# Importar las funciones a probar
from news_browser.utils import (
    format_current_date,
    convert_date_to_mm_aaaa,
    word_counter,
    does_it_contain_money
)


class TestUtils(unittest.TestCase):
    def test_convert_date_to_mm_aaaa(self):
        # In some cases when the new is literally new, they put it like :3 min ago
        # So, we need also to try such "excepcions"
        date_str = "3 hours ago"
        expected_result = format_current_date()
        self.assertEqual(convert_date_to_mm_aaaa(date_str), expected_result)

        date_str = "May 26, 2024"
        expected_result = "05-2024"
        self.assertEqual(convert_date_to_mm_aaaa(date_str), expected_result)

        date_str = "1 min ago"
        expected_result = format_current_date()
        self.assertEqual(convert_date_to_mm_aaaa(date_str), expected_result)

        date_str = "48 minutes ago"
        expected_result = format_current_date()
        self.assertEqual(convert_date_to_mm_aaaa(date_str), expected_result)

        date_str = "1 hour ago"
        expected_result = format_current_date()
        self.assertEqual(convert_date_to_mm_aaaa(date_str), expected_result)

        date_str = "2 seconds ago"
        expected_result = format_current_date()
        self.assertEqual(convert_date_to_mm_aaaa(date_str), expected_result)

    def test_word_counter(self):
        text_to_match = "This is a test sentence for testing."
        search_phrase = "test"
        expected_result = 2
        self.assertEqual(word_counter(text_to_match, search_phrase), expected_result)

        text_to_match = "Venezuelan culture is very rich. Many Venezuelans live in Venezuela."
        search_phrase = "venezuela"
        expected_result = 3
        self.assertEqual(word_counter(text_to_match, search_phrase), expected_result)

        text_to_match = "Trump’s resilience gives California GOP dreams of payback in a state that has long been blue."
        search_phrase = "trump"
        expected_result = 1
        self.assertEqual(word_counter(text_to_match, search_phrase), expected_result)

        text_to_match = "Column: Don’t cancel those summer plans yet. Who knows if the presidential debates will come off."
        search_phrase = "column"
        expected_result = 1
        self.assertEqual(word_counter(text_to_match, search_phrase), expected_result)

    def test_does_it_contain_money(self):
        # Testing with both $ sign and € sign
        text_to_match = "The price is $20.50 and €30."
        self.assertTrue(does_it_contain_money(text_to_match))

        # Testing without $ sign but € alone instead
        text_without_money = "The price is €30."
        self.assertFalse(does_it_contain_money(text_without_money))

if __name__ == "__main__":
    unittest.main()

# Standard Python library imports
from datetime import datetime, timedelta
import os
import sys
import unittest

# Taking the correct directory to import the files
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)

# Local module imports
from news_browser.utils import (
    format_current_date,
    convert_date_to_mm_aaaa,
    word_counter,
    does_it_contain_money,
    calculate_months_to_consider,
    clean_text,
    validate_input
)


class TestUtils(unittest.TestCase):
    def test_format_current_date(self):
        current_date = datetime.now().strftime("%m-%Y")
        self.assertEqual(format_current_date(), current_date)

    def test_convert_date_to_mm_aaaa(self):
        self.assertEqual(convert_date_to_mm_aaaa("Jan. 1, 2020"), "01-2020")
        self.assertEqual(convert_date_to_mm_aaaa("5 seconds ago"), (datetime.now() - timedelta(seconds=5)).strftime("%m-%Y"))
        self.assertEqual(convert_date_to_mm_aaaa("3 hours ago"), (datetime.now() - timedelta(seconds=5)).strftime("%m-%Y"))
        self.assertEqual(convert_date_to_mm_aaaa("48 minutes ago"), (datetime.now() - timedelta(seconds=5)).strftime("%m-%Y"))

    def test_word_counter(self):
        self.assertEqual(word_counter("hello world", "hello"), 1)
        self.assertEqual(word_counter("hello hello world", "hello"), 2)
        self.assertEqual(word_counter("Venezuelan culture is very rich. Many Venezuelans live in Venezuela.", "venezuela"), 3)
        self.assertEqual(word_counter("this is a test", "is"), 2)
        self.assertEqual(word_counter("no match here", "test"), 0)
        self.assertEqual(word_counter("Trump’s resilience gives California GOP dreams of payback in a state that has long been blue.", "trump"), 1)
        self.assertEqual(word_counter("This is a test sentence for testing.", "test"), 2)
        self.assertEqual(word_counter("Column: Don’t cancel those summer plans yet. Who knows if the presidential debates will come off.", "column"), 1)
        self.assertEqual(word_counter("This is a test sentence for testing.", "test"), 2)

    def test_does_it_contain_money(self):
        self.assertTrue(does_it_contain_money("The price is $100."))
        self.assertTrue(does_it_contain_money("It costs $100,00 USD."))
        self.assertTrue(does_it_contain_money("The price is $20.50 and €30."))
        self.assertFalse(does_it_contain_money("The price is €30."))
        self.assertFalse(does_it_contain_money("No money here."))

    def test_calculate_months_to_consider(self):
        self.assertEqual(len(calculate_months_to_consider(0)), 1)
        self.assertEqual(len(calculate_months_to_consider(1)), 1)
        self.assertEqual(len(calculate_months_to_consider(5)), 5)
        self.assertRaises(ValueError, calculate_months_to_consider, -1)

    def test_clean_text(self):
        self.assertEqual(clean_text("Hello, World!"), "HelloWorld")
        self.assertEqual(clean_text("No $%&special !!!char=?¡=)((//s"), "Nospecialchars")
        self.assertEqual(clean_text("T%&/(/%his is a test."), "Thisisatest")
        self.assertEqual(clean_text("i$&% a/(&(m hu=)/(=)(ngry."), "iamhungry")
        self.assertEqual(clean_text("No special chars"), "Nospecialchars")

    def test_validate_input(self):
        self.assertTrue(validate_input({"num_months": 5}))
        self.assertFalse(validate_input({"num_months": -1}))
        self.assertFalse(validate_input({"num_months": "five"}))

if __name__ == '__main__':
    unittest.main()

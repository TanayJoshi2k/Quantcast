import unittest
import tempfile
import os
from unittest.mock import patch
from most_active_cookie import find_most_active_cookie

class Test(unittest.TestCase):

    def setUp(self):
        # Define file paths and test data
        self.valid_file_name = "./cookie_log.csv"
        self.invalid_file_path = "./Downloads/cookies.csv"
        self.invalid_file_format = "./cookies.json"
        self.missing_date = "2018-12-"
        self.missing_month = "2018--09"
        self.missing_year = "-12-09"
        self.invalid_date_type = 11

        # Create a named temporary empty file for testing
        self.empty_file = tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix='.csv')

        # Create a named header-only temporary empty file for testing
        self.header_only_file = tempfile.NamedTemporaryFile(
            mode='w', delete=False)
        self.header_only_file.write("cookie,timestamp")
        self.header_only_file.flush()

    def tearDown(self):
        # Clean up temporary files after each test
        self.empty_file.close()
        os.remove(self.empty_file.name)
        self.header_only_file.close()
        os.remove(self.header_only_file.name)

    # Test cases for handling file not found error
    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            find_most_active_cookie(self.invalid_file_path, '2018-12-09')

    # Test cases for handling invalid file format error
    def test_invalid_file_format(self):
        with self.assertRaises(ValueError):
            find_most_active_cookie(self.invalid_file_format, '2018-12-09')

    # Test cases for handling empty file
    def test_empty_file(self):
        with patch('builtins.open', return_value=open(self.empty_file.name, 'r')) as mock_open:
            self.assertEqual(find_most_active_cookie(self.empty_file.name, '2018-12-09'), [])

    # Test cases for handling invalid date format
    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            find_most_active_cookie(self.valid_file_name, "")
        with self.assertRaises(ValueError):
            find_most_active_cookie(self.valid_file_name, self.missing_date)
        with self.assertRaises(ValueError):
            find_most_active_cookie(self.valid_file_name, self.missing_month)
        with self.assertRaises(ValueError):
            find_most_active_cookie(self.valid_file_name, self.missing_year)
        with self.assertRaises(TypeError):
            find_most_active_cookie(self.valid_file_name, self.invalid_date_type)

    # Test cases for handling header-only file
    def test_header_only_file(self):
        with patch('builtins.open', return_value=open(self.header_only_file.name, 'r')) as mock_open:
            self.assertEqual(find_most_active_cookie(self.valid_file_name, '2018-12-08'), [])
                
    # Test cases for finding most active cookies
    def test_find_most_active_cookie(self):
        self.assertEqual(find_most_active_cookie(
            self.valid_file_name, '2018-12-08'), ['SAZuXPGUrfbcn5UA', '4sMM2LxV07bPJzwf', 'fbcn5UAVanZf6UtG'])
        self.assertEqual(find_most_active_cookie(
            self.valid_file_name, '2018-12-09'), ["AtY0laUfhglK3lC7"])
        self.assertEqual(find_most_active_cookie(
            self.valid_file_name, '2018-12-11'), [])

if __name__ == "__main__":
    unittest.main()
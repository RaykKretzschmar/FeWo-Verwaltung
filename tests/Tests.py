import unittest
import datetime
import re

class Tests(unittest.TestCase):
    def test_date_strings_format(self):
        # RegEx pattern to match the date format DD.MM.YYYY
        date_pattern = re.compile(r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.\d{4}$')
        
        # Define a list of date strings to test
        test_dates = {
            "01.01.2023" : "01.01.2023",   # Correct format with leading zeros
            "1.9.2023" : "01.09.2023",     # Incorrect format without leading zeros
            "02.2.2023" : "02.02.2023",   # Correct format with leading zero only on day
            "5.02.2023" : "05.02.2023",   # Correct format with leading zero only on month
        }

        date_format = "%d.%m.%Y"

        # Check if each date string matches the correct format
        for date_str in test_dates.items():
            date_date = datetime.datetime.strptime(date_str[0], date_format)
            self.assertTrue(date_str[1] == date_date.strftime(date_format), f"{date_str} is NOT in the correct format.")

if __name__ == '__main__':
    unittest.main()

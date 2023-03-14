"""
Module Name: test_extract_csv
Description: This module contains unit tests for processing CSV files.

Dependencies:
    - sys
    - unittest
    - requests
    - extract (from ../Extract)

Usage:
    To run the unit tests, execute `python test_process_csv.py`

"""

import sys
import unittest
import requests
#pylint: disable=wrong-import-position
sys.path.append("pipeline/Extract")
import extract
#pylint: disable=wrong-import-position

class TestExtractCSV(unittest.TestCase):

    """
    Class Name: TestExtractCSV
    Description: This class contains unit tests for processing CSV files.
    """

    def test_initial_page_success(self):
        """
        Method Name: test_initial_page_success
        Description: This method tests the initial page response for success.
        """
        session = requests.Session()
        assert session is not None
        response = extract.initial_page(session)
        assert response is not None

    def test_get_airport_csv_smoke(self):
        """
        Method Name: test_get_airport_csv_smoke
        Description: This method tests the smoke test for retrieving airport CSV data.
        """
        session = requests.Session()
        assert session is not None
        result = extract.get_airport_csv(session)
        assert result is None

if __name__ == '__main__':
    unittest.main()

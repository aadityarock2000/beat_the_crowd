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
import os
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
        flag = True
        session = requests.Session()
        assert session is not None
        try:
            response = extract.initial_page(session)
            assert response is not None
        except requests.exceptions.ConnectTimeout:
            assert self.assertTrue(flag)
        finally:
            session.close()

    def test_get_airport_csv_smoke(self):
        """
        Method Name: test_get_airport_csv_smoke
        Description: This method tests the smoke test for retrieving airport CSV data.
        """
        session = requests.Session()
        assert session is not None
        result = extract.get_airport_csv(session)
        assert result is None

    def test_query_aspx_smoke(self):
        """
        Method Name: test_query_aspx_smoke
        Description: This method tests the smoke test for retrieving airport CSV data for 
        all airlines.
        """
        session = requests.Session()
        flag = True
        try:
            extract.initial_page(session)
            path = 'data/pipeline_data'
            extract.query_aspx('BFI', path,session)
            assert session is not None
            is_exist = os.path.exists(path+'/BFI.csv')
            assert is_exist
        except requests.exceptions.ConnectTimeout:
            assert self.assertTrue(flag)
        finally:
            session.close()
        


if __name__ == '__main__':
    unittest.main()

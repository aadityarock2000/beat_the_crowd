"""
This module contains a set of tests for functions that provide the necesary 
input to the streamlit app for selection.
"""
import unittest
import sys
sys.path.append("../website_utils")
from departure_input_data import airport_list, carrier_list, file_types # pylint: disable=wrong-import-position, import-error

class TestAirportList(unittest.TestCase):
    """
    This class contains test cases for the airport_list() function.

    Methods:

    - test_smoke(self)
        A smoke test to check if the function returns a list of airports when given a 
        valid path to a CSV file.

    - test_edge(self)
        An edge test to check if the function returns ['All'] when given an empty CSV file.

    - test_airport_list_contains_all(self)
        A test to check if the list of airports returned by the function contains 'All' 
        as one of its elements.

    """
    def test_smoke(self):
        """
        A smoke test to check if the function returns a list of 
        airports when given a valid path to a CSV file.
        """
        # Smoke test
        path = '../website_utils/reference_data/airport_codes_reference.csv'
        airports = airport_list(path)
        self.assertIsInstance(airports, list)
        self.assertTrue(len(airports) > 0)

    def test_edge(self):
        """
        An edge test to check if the function returns ['All'] 
        when given an empty CSV file.
        """
        path = '../website_utils/reference_data/empty_file.csv'
        airports = airport_list(path)
        self.assertEqual(airports, ['All'])

    def test_airport_list_contains_all(self):
        """
        A test to check if the list of airports returned by the function 
        contains 'All' as one of its elements.
        """
        self.assertIn('All', airport_list(
            '../website_utils/reference_data/airport_codes_reference.csv'))


class TestCarrierList(unittest.TestCase):
    """
    This class contains test cases for the carrier_list() function.

    Methods:

    - test_smoke_1(self)
        A smoke test to check if the function returns a list of carriers when given a 
        valid path to a CSV file.

    - test_edge_1(self)
        An edge test to check if the function returns ['All'] when given an empty CSV 
        file.

    - test_edge_2(self)
        An edge test to check if the function raises a FileNotFoundError when given a 
        nonexistent file path.

    """
    def test_smoke_1(self):
        """
        A smoke test to check if the function returns a list of 
        carriers when given a valid path to a CSV file.
        """
        file = '../website_utils/reference_data/airport_carrier_codes_reference.csv'
        carriers = carrier_list(file)
        self.assertIsInstance(carriers, list)
        self.assertTrue(len(carriers) > 0)

    def test_edge_1(self):
        """
        An edge test to check if the function returns ['All'] when given an empty CSV file."""
        # Edge test 1
        file = '../website_utils/reference_data/empty_file.csv'
        carriers = carrier_list(file)
        self.assertEqual(carriers, ['All'])
    def test_edge_2(self):
        # Edge test 2
        """
        An edge test to check if the function raises a `FileNotFoundError` when 
        given a nonexistent file path.
        """
        file = 'nonexistent_file.csv'
        with self.assertRaises(FileNotFoundError):
            carriers = carrier_list(file) # pylint: disable=unused-variable

class TestFileTypes(unittest.TestCase):
    """
    This class contains test cases for the file_types() function.

    Methods:

    - test_file_types_type(self)
        A test to check if the function returns a list.

    - test_file_types_length(self)
        A test to check if the list returned by the function has a length of 3.

    - test_file_types_contains_excel(self)
        A test to check if the list returned by the function contains 'Excel' as one 
        of its elements.
    """
    def test_file_types_type(self):
        """
        A test to check if the function returns a list.
        """
        self.assertIsInstance(file_types(), list)

    def test_file_types_length(self):
        """
        A test to check if the list returned by the function has a length of 3.
        """
        self.assertEqual(len(file_types()), 3)

    def test_file_types_contains_excel(self):
        """
        A test to check if the list returned by the function contains 'Excel' as one 
        of its elements.
        """
        self.assertIn('Excel', file_types())

if __name__ == '__main__':
    unittest.main()

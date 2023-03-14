'''
This module contains a set of tests for functions that parse SQL queries in the context of a data 
pipeline.

The tests aim to confirm that the functions perform as expected, given specific inputs. 
Specifically, the tests check if the functions can successfully retrieve information from reference 
data files to populate SQL queries.

'''
import unittest
import datetime
import sys
import pyodbc
sys.path.append("./SmoothFly/website_utils")
from website_utils.sql_parsing import fetch_airport_code, fetch_carrier_code, input_preparation # pylint: disable=wrong-import-position, import-error
from website_utils.sql_parsing import create_query_string, connect_sql_server # pylint: disable=wrong-import-position, import-error

class TestFetchFunctions(unittest.TestCase):
    '''
    Test class for the fetch functions used by the SQL parsing script.
    '''
    def test_fetch_airport_code_smoke(self):
        '''
        Test if the function `fetch_airport_code` correctly retrieves airport codes 
        given airport names.
        '''
        path = 'website_utils/reference_data/airport_codes_reference.csv'
        self.\
        assertEqual(
            fetch_airport_code("Los Angeles, CA: Los Angeles International (LAX)", path), 'LAX')

    def test_fetch_airport_code_one_shot(self):
        '''
        Test if the function `fetch_airport_code` correctly retrieves airport codes 
        given airport names.
        '''
        path = 'website_utils/reference_data/airport_codes_reference.csv'
        self.assertEqual(fetch_airport_code
                         ("Chicago, IL: Chicago O 'Hare International (ORD)", path), 'ORD')
    def test_fetch_airport_code_edge_empty_input(self):
        '''
        Test if the function `fetch_airport_code` raises an error when passed an empty 
        string as an argument.
        '''
        path = 'website_utils/reference_data/airport_codes_reference.csv'
        with self.assertRaises(ValueError):
            fetch_airport_code('', path)

    def test_fetch_airport_code_edge_not_found(self):
        '''
        Test if the function `fetch_airport_code` raises an error when passed a 
        nonexistent airport name.
        '''
        path = 'website_utils/reference_data/airport_codes_reference.csv'
        with self.assertRaises(ValueError):
            fetch_airport_code('Nonexistent Airport', path)

    def test_fetch_airport_code_edge_empty_file(self):
        '''
        Test if the function `fetch_airport_code` raises an error when passed an 
        empty reference data file.
        '''
        path = 'website_utils/reference_data/empty_file.csv'
        with self.assertRaises(ValueError):
            fetch_airport_code('Chicago O\'Hare International Airport', path)

    def test_fetch_carrier_code_smoke(self):
        '''
        Test if the function `fetch_carrier_code` correctly retrieves carrier codes 
        given carrier names.
        '''
        path = 'website_utils/reference_data/airport_carrier_codes_reference.csv'
        self.assertEqual(fetch_carrier_code('Delta Airlines Inc. (DL)', path), 'DL')

    def test_fetch_carrier_code_one_shot(self):
        '''
        Test if the function `fetch_carrier_code` correctly retrieves carrier codes 
        given carrier names.
        '''
        path = 'website_utils/reference_data/airport_carrier_codes_reference.csv'
        self.assertEqual(fetch_carrier_code('Southwest Airlines Co. (WN)', path), 'WN')

    def test_fetch_carrier_code_edge_empty_input(self):
        '''
        Test if the function `fetch_carrier_code` raises an error when passed an 
        empty string as an argument.
        '''
        path = 'website_utils/reference_data/airport_carrier_codes_reference.csv'
        with self.assertRaises(ValueError):
            fetch_carrier_code('', path)

    def test_fetch_carrier_code_edge_not_found(self):
        '''
        Test if the function `fetch_carrier_code` raises an error when passed a 
        nonexistent carrier name.
        '''
        path = 'website_utils/reference_data/airport_carrier_codes_reference.csv'
        with self.assertRaises(ValueError):
            fetch_carrier_code('Nonexistent Carrier', path)

    def test_fetch_carrier_code_edge_empty_file(self):
        """Test fetch_carrier_code() function edge case: empty reference data file.    
        This test checks the behavior of the 
        fetch_carrier_code() function when it's called with an empty
        reference data file. The function should raise a ValueError exception, 
        because it can't find the requested carrier in an empty file."""
        # Edge Test 3: empty reference data file
        path = 'website_utils/reference_data/empty_file.csv'
        with self.assertRaises(ValueError):
            fetch_carrier_code('Delta Air Lines, Inc.', path)

class TestInputPreparation(unittest.TestCase):
    """
    This class tests the input_preparation function to ensure it correctly processes input data
    for the flight search web application.

    Each test case checks if the function returns the expected output given specific input 
    conditions.
    """
    def test_input_preparation(self):
        """
        Test input_preparation function for normal input conditions. 
        
        Sets up input data for a flight search request, invokes input_preparation, and compares
        the returned output with the expected output. 
        
        Raises an AssertionError if the returned output does not match the expected output.
        """
        path='website_utils/reference_data/airport_codes_reference.csv'
        car_path='website_utils/reference_data/airport_carrier_codes_reference.csv'
        inputs = {
            'source_airport': ['Los Angeles, CA: Los Angeles International (LAX)'],
            'destination_airport': ["Chicago, IL: Chicago O 'Hare International (ORD)"],
            'carrier': ['Delta Airlines Inc. (DL)'],
            'from_date': '2022-01-01',
            'to_date': '2022-01-05',
            'file_format': 'csv'
        }
        expected_output = {
            'source_airport': ['LAX'],
            'destination_airport': ['ORD'],
            'carrier': ['DL'],
            'from_date': '2022-01-01',
            'to_date': '2022-01-05',
            'file_format': 'csv'
        }
        self.assertEqual(input_preparation(inputs,path,car_path), expected_output)
    def test_input_preparation_all(self):
        """
        Test input_preparation function for "All" input conditions. 
        
        Sets up input data for a flight search request with "All" values for all fields,
        invokes input_preparation, and compares the returned output with the expected output. 
        
        Raises an AssertionError if the returned output does not match the expected output.
        """
        path='website_utils/reference_data/airport_codes_reference.csv'
        car_path='website_utils/reference_data/airport_carrier_codes_reference.csv'
        inputs = {
            'source_airport': ['All'],
            'destination_airport': ['All'],
            'carrier': ['All'],
            'from_date': '2022-01-01',
            'to_date': '2022-01-05',
            'file_format': 'csv'
        }
        expected_output = {
            'source_airport': ['All'],
            'destination_airport': ['All'],
            'carrier': ['All'],
            'from_date': '2022-01-01',
            'to_date': '2022-01-05',
            'file_format': 'csv'
        }
        self.assertEqual(input_preparation(inputs,path,car_path), expected_output)

    def test_input_preparation_empty(self):
        """
        Test input_preparation function for empty input conditions. 
        
        Sets up input data for a flight search request with empty values for all fields,
        invokes input_preparation, and raises a ValueError because empty inputs are invalid.
        """
        path='website_utils/reference_data/airport_codes_reference.csv'
        car_path='website_utils/reference_data/airport_carrier_codes_reference.csv'
        inputs = {
            'source_airport': [],
            'destination_airport': [],
            'carrier': [],
            'from_date': '',
            'to_date': '',
            'file_format': ''
        }
        with self.assertRaises(ValueError):
            input_preparation(inputs,path,car_path)

class TestCreateQueryString(unittest.TestCase):
    """
    A unittest test case class for testing the create_query_string function.

    Methods:
    - test_one_shot: Test function to verify that create_query_string produces the correct SQL 
    query and file format for a single search request.
    - test_edge: Test function to verify that create_query_string produces the correct SQL 
    query and file format for the edge case of searching for all airports, all carriers, 
    and all destinations.
    - test_smoke: Test function to verify that create_query_string produces non-null output
     for a typical search request."""

    def test_one_shot(self):
        '''
        Test function to verify that create_query_string produces the correct SQL query and 
        file format for a single search request.
        '''
        inputs = {
            'source_airport': ['SFO'],
            'destination_airport': ['LAX'],
            'carrier': ['AA'],
            'from_date': datetime.date(2022, 1, 1),
            'to_date': datetime.date(2022, 1, 31),
            'file_format': 'csv'
        }
        expected_query = '''SELECT * FROM airline_stats WHERE source in ('SFO') AND destination in ('LAX') AND carrier in ('AA') AND date BETWEEN '2022-01-01' AND '2022-01-31';''' # pylint: disable=line-too-long
        expected_file_format = 'csv'
        actual_query, actual_file_format = create_query_string(inputs)
        self.assertEqual(actual_query, expected_query)
        self.assertEqual(actual_file_format, expected_file_format)

    def test_edge(self):
        '''
        Test function to verify that create_query_string produces the correct 
        SQL query and file format for the edge case of searching for all 
        airports, all carriers, and all destinations.
        '''
        inputs = {
            'source_airport': ['All'],
            'destination_airport': ['All'],
            'carrier': ['All'],
            'from_date': datetime.date(2022, 1, 1),
            'to_date': datetime.date(2022, 1, 31),
            'file_format': 'csv'
        }
        expected_query = """SELECT * FROM airline_stats WHERE date BETWEEN '2022-01-01' AND '2022-01-31';""" # pylint: disable=line-too-long
        expected_file_format = 'csv'
        actual_query, actual_file_format = create_query_string(inputs)
        self.assertEqual(actual_query, expected_query)
        self.assertEqual(actual_file_format, expected_file_format)

    def test_smoke(self):
        '''
        Test function to verify that create_query_string produces non-null output 
        for a typical search request.
        '''
        inputs = {
            'source_airport': ['SFO', 'LAX'],
            'destination_airport': ['JFK'],
            'carrier': ['DL'],
            'from_date': datetime.date.today(),
            'to_date': datetime.date.today() + datetime.timedelta(days=7),
            'file_format': 'csv'
        }
        actual_query, actual_file_format = create_query_string(inputs)
        self.assertIsNotNone(actual_query)
        self.assertIsNotNone(actual_file_format)

class TestConnectSqlServer(unittest.TestCase):
    '''
    A unittest class for testing connection to SQL Server.
    Methods
    -------
    test_connection_string()
        Test that the connection string is created properly and that a pyodbc Connection 
        object is returned.
    test_cursor()
        Test that a pyodbc Cursor object is returned by the connection.
    '''
    def test_connection_string(self):
        """
        Test that the connection string is created properly and that a pyodbc 
        Connection object is returned.
        """
        cnxn = connect_sql_server()
        self.assertIsInstance(cnxn, pyodbc.Connection)

    def test_cursor(self):
        """
        Test that a pyodbc Cursor object is returned by the connection.
        """
        cnxn = connect_sql_server()
        cursor = cnxn.cursor()
        self.assertIsInstance(cursor, pyodbc.Cursor)


if __name__ == '__main__':
    unittest.main()

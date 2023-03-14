import unittest
import datetime
import sys
sys.path.append("../website_utils")
import pandas as pd
from sql_parsing import fetch_airport_code, fetch_carrier_code, input_preparation 
from sql_parsing import create_query_string


class TestFetchFunctions(unittest.TestCase):

    def test_fetch_airport_code_smoke(self):
        # Smoke Test
        path = '../website_utils/reference_data/airport_codes_reference.csv'
        self.assertEqual(fetch_airport_code("Los Angeles, CA: Los Angeles International (LAX)", path), 'LAX')

    def test_fetch_airport_code_one_shot(self):
        # One Shot Test
        path = '../website_utils/reference_data/airport_codes_reference.csv'
        self.assertEqual(fetch_airport_code("Chicago, IL: Chicago O 'Hare International (ORD)", path), 'ORD')
    
    def test_fetch_airport_code_edge_empty_input(self):
        # Edge Test 1: empty input
        path = '../website_utils/reference_data/airport_codes_reference.csv'
        with self.assertRaises(ValueError):
            fetch_airport_code('', path)

    def test_fetch_airport_code_edge_not_found(self):
        # Edge Test 2: airport not found
        path = '../website_utils/reference_data/airport_codes_reference.csv'
        with self.assertRaises(ValueError):
            fetch_airport_code('Nonexistent Airport', path)

    def test_fetch_airport_code_edge_empty_file(self):
        # Edge Test 3: empty reference data file
        path = '../website_utils/reference_data/empty_file.csv'
        with self.assertRaises(ValueError):
            fetch_airport_code('Chicago O\'Hare International Airport', path)

    def test_fetch_carrier_code_smoke(self):
        # Smoke Test
        path = '../website_utils/reference_data/airport_carrier_codes_reference.csv'
        self.assertEqual(fetch_carrier_code('Delta Airlines Inc. (DL)', path), 'DL')

    def test_fetch_carrier_code_one_shot(self):
        # One Shot Test
        path = '../website_utils/reference_data/airport_carrier_codes_reference.csv'
        self.assertEqual(fetch_carrier_code('Southwest Airlines Co. (WN)', path), 'WN')

    def test_fetch_carrier_code_edge_empty_input(self):
        # Edge Test 1: empty input
        path = '../website_utils/reference_data/airport_carrier_codes_reference.csv'
        with self.assertRaises(ValueError):
            fetch_carrier_code('', path)

    def test_fetch_carrier_code_edge_not_found(self):
        # Edge Test 2: carrier not found
        path = '../website_utils/reference_data/airport_carrier_codes_reference.csv'
        with self.assertRaises(ValueError):
            fetch_carrier_code('Nonexistent Carrier', path)

    def test_fetch_carrier_code_edge_empty_file(self):
        # Edge Test 3: empty reference data file
        path = '../website_utils/reference_data/empty_file.csv'
        with self.assertRaises(ValueError):
            fetch_carrier_code('Delta Air Lines, Inc.', path)

class TestInputPreparation(unittest.TestCase):
    def test_input_preparation(self):
        path='../website_utils/reference_data/airport_codes_reference.csv'
        car_path='../website_utils/reference_data/airport_carrier_codes_reference.csv'
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
        path='../website_utils/reference_data/airport_codes_reference.csv'
        car_path='../website_utils/reference_data/airport_carrier_codes_reference.csv'
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
        path='../website_utils/reference_data/airport_codes_reference.csv'
        car_path='../website_utils/reference_data/airport_carrier_codes_reference.csv'
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

    def test_one_shot(self):
        inputs = {
            'source_airport': ['SFO'],
            'destination_airport': ['LAX'],
            'carrier': ['AA'],
            'from_date': datetime.date(2022, 1, 1),
            'to_date': datetime.date(2022, 1, 31),
            'file_format': 'csv'
        }
        expected_query = "SELECT * FROM airline_stats WHERE source in ('SFO') AND destination in ('LAX') AND carrier in ('AA') AND date BETWEEN '2022-01-01' AND '2022-01-31';"
        expected_file_format = 'csv'
        actual_query, actual_file_format = create_query_string(inputs)
        self.assertEqual(actual_query, expected_query)
        self.assertEqual(actual_file_format, expected_file_format)

    def test_edge(self):
        inputs = {
            'source_airport': ['All'],
            'destination_airport': ['All'],
            'carrier': ['All'],
            'from_date': datetime.date(2022, 1, 1),
            'to_date': datetime.date(2022, 1, 31),
            'file_format': 'json'
        }
        expected_query = "SELECT * FROM airline_stats WHERE date BETWEEN '2022-01-01' AND '2022-01-31';"
        expected_file_format = 'json'
        actual_query, actual_file_format = create_query_string(inputs)
        self.assertEqual(actual_query, expected_query)
        self.assertEqual(actual_file_format, expected_file_format)

    def test_smoke(self):
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

if __name__ == '__main__':
    unittest.main()

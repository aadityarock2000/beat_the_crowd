import unittest
import sys
sys.path.append("../website_utils")
import pandas as pd
from departure_input_data import airport_list, carrier_list, file_types

class TestAirportList(unittest.TestCase):
    def test_airport_list_type(self):
        self.assertIsInstance(airport_list(), list)
        
    def test_airport_list_contains_all(self):
        self.assertIn('All', airport_list())
        
    def test_airport_list_contains_reference(self):
        airport_code_reference=pd.read_csv('../website_utils/reference_data/airport_codes_reference.csv')
        self.assertCountEqual(list(airport_code_reference['Airport_name']), airport_list()[1:])
        
# class TestCarrierList(unittest.TestCase):
#     def test_carrier_list_type(self):
#         self.assertIsInstance(carrier_list(), list)
        
#     def test_carrier_list_contains_all(self):
#         self.assertIn('All', carrier_list())
        
#     def test_carrier_list_contains_reference(self):
#         airport_carrier_codes_reference=pd.read_csv('website_utils/reference_data/airport_carrier_codes_reference.csv')
#         self.assertCountEqual(list(airport_carrier_codes_reference['Carrier_name']), carrier_list()[1:])
        
class TestFileTypes(unittest.TestCase):
    def test_file_types_type(self):
        self.assertIsInstance(file_types(), list)
        
    def test_file_types_length(self):
        self.assertEqual(len(file_types()), 3)
        
    def test_file_types_contains_excel(self):
        self.assertIn('Excel', file_types())

if __name__ == '__main__':
    unittest.main()
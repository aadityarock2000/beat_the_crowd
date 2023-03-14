import unittest
import sys
sys.path.append("../website_utils")
import pandas as pd
from departure_input_data import airport_list, carrier_list, file_types

class TestAirportList(unittest.TestCase):
    def test_smoke(self):
        # Smoke test
        path = '../website_utils/reference_data/airport_codes_reference.csv'
        airports = airport_list(path)
        self.assertIsInstance(airports, list)
        self.assertTrue(len(airports) > 0)
    
    def test_edge(self):
        # Edge test
        path = '../website_utils/reference_data/empty_file.csv'
        airports = airport_list(path)
        self.assertEqual(airports, ['All'])
        
    def test_airport_list_contains_all(self):
        self.assertIn('All', airport_list('../website_utils/reference_data/airport_codes_reference.csv'))
        
        
class TestCarrierList(unittest.TestCase):
    def test_smoke_1(self):
        # Smoke test 1
        file = '../website_utils/reference_data/airport_carrier_codes_reference.csv'
        carriers = carrier_list(file)
        self.assertIsInstance(carriers, list)
        self.assertTrue(len(carriers) > 0)
     
    def test_edge_1(self):
        # Edge test 1
        file = '../website_utils/reference_data/empty_file.csv'
        carriers = carrier_list(file)
        self.assertEqual(carriers, ['All'])
    
    def test_edge_2(self):
        # Edge test 2
        file = 'nonexistent_file.csv'
        with self.assertRaises(FileNotFoundError):
            carriers = carrier_list(file)

class TestFileTypes(unittest.TestCase):
    def test_file_types_type(self):
        self.assertIsInstance(file_types(), list)
        
    def test_file_types_length(self):
        self.assertEqual(len(file_types()), 3)
        
    def test_file_types_contains_excel(self):
        self.assertIn('Excel', file_types())

if __name__ == '__main__':
    unittest.main()
import unittest
import sys
sys.path.append('../src')
# importing the hello
from example_visualization_denied_boarding import first_plot

import numbers
import numpy as np 
import pandas as pd 


# Define a class in which the tests will run
class TestDeniedBoarding(unittest.TestCase):      
    # Smoke Test
    def test_plot_smoke(self):
        first_plot()
        self.assertTrue(True) 
            
if __name__ == '__main__':
    unittest.main()
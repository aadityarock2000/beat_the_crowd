# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 21:14:51 2023

@author: mdbla
"""

import unittest
import sys
sys.path.append('../create_visualizations')
# importing the hello
import fares

# Define a class in which the tests will run
class TestFares(unittest.TestCase):      
    # Smoke Test
            
    def test_plot_smoke1(self):
        fares.avg_lh_sh_fares()
        self.assertTrue(True)
        
    def test_plot_smoke2(self):
        fares.prem_disc_by_year()
        self.assertTrue(True)
    
    def test_plot_smoke3(self):
        fares.avg_fare_by_city()
        self.assertTrue(True)

    def test_plot_smoke4(self):
        fares.pct_by_avg_fare()
        self.assertTrue(True)  
        
           
  
if __name__ == '__main__':
    unittest.main()

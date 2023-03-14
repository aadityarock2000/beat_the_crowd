# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 21:14:51 2023

@author: mdbla
"""

import unittest
import sys
sys.path.append('../create_visualizations')
# importing the hello
import delays

# Define a class in which the tests will run
class TestDelays(unittest.TestCase):      
    # Smoke Test
            
    def test_plot_smoke(self):
        delays.creat_delay_ranking()
        self.assertTrue(True)
        
    def test_plot_smoke2(self):
        delays.create_delay_ct_breakdown()
        self.assertTrue(True)
    
    def test_plot_smoke3(self):
        delays.create_delay_min_breakdown()
        self.assertTrue(True)

    def test_plot_smoke4(self):
        delays.pct_delays_by_carrier()
        self.assertTrue(True)  
        
           
  
if __name__ == '__main__':
    unittest.main()

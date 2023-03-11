import unittest
import sys
sys.path.append('../create_visualizations')
# importing the hello
import denied_boarding 

# Define a class in which the tests will run
class TestDeniedBoarding(unittest.TestCase):      
    # Smoke Test
            
    def test_plot_smoke(self):
        denied_boarding.db_plot_comp_voluntary_by_carrier()
        self.assertTrue(True)
        
    def test_plot_smoke(self):
        denied_boarding.db_plot_perc_denied_over_time()
        self.assertTrue(True)
    
    def test_plot_smoke(self):
        denied_boarding.db_plot_perc_denied_by_carrier()
        self.assertTrue(True)

    def test_plot_smoke(self):
        denied_boarding.db_plot_total_denied_by_carrier()
        self.assertTrue(True)  
        
    def test_plot_smoke(self):
        denied_boarding.db_plot_denial_type_by_carrier()
        self.assertTrue(True)
        
    def test_plot_smoke(self):
        denied_boarding.db_plot_denied_compensation_reason()
        self.assertTrue(True)

           
  
if __name__ == '__main__':
    unittest.main()
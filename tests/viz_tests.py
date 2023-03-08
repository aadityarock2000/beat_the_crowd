import unittest

# The below is to import the function that will produce our figures when we write it
# from ..src.delays_visualizations import fig_function

# This is to perform unit testing on our visualizations 

class UnitTests(unittest.TestCase):
    # This class will be for us to test our visualizations
	def smoke_test(self):
		# smoke test to test if our function creates the figure
		# "plotly" %in% fig_function()
    

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
    _ = unittest.TextTestRunner().run(suite)
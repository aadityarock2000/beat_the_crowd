import unittest

# The below is to import the function that will produce our figures when we write it
# from ..src.delays_visualizations import 

# This is to perform unit testing on our visualizations 

class UnitTests(unittest.TestCase):
    # This class will be for us to test our visualizations
    

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
    _ = unittest.TextTestRunner().run(suite)
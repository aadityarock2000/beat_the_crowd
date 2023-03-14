# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 08:11:07 2023

@author: mdbla
"""

import unittest
import sys
import plotly.graph_objs._figure
sys.path.append('analysis/create_visualizations')
import fares # pylint: disable=wrong-import-position


# Define a class in which the tests will run
class TestFares(unittest.TestCase):
    """
    Test denied boarding functions.
    
    ...
    Attributes
    ----------
    Inherited from unittest -- https://docs.python.org/3/library/unittest.html
    Methods
    -------
    test_fares_not_none(): Perform non none test on denied boarding functions.
    test_fares_plotly_fig(): Perform plotly figure test on denied boarding functions.
    """
    def test_fares_not_none(self):
        """Return the result of test for return value of none of denied boarding functions."""
        test_cases = [
            fares.avg_lh_sh_fares(),
            fares.prem_disc_by_year(),
            fares.avg_fare_by_city(),
            fares.pct_by_avg_fare()
        ]
        def test(fig):
            self.assertIsNotNone(fig)
        for fig in test_cases:
            test(fig)

    def test_fares_plotly_fig(self):
        """Return the result of plotly figure test of denied boarding functions."""
        test_cases = [
            fares.avg_lh_sh_fares(),
            fares.prem_disc_by_year(),
            fares.avg_fare_by_city(),
            fares.pct_by_avg_fare()
        ]
        def test(fig):
            self.assertIsInstance(fig, plotly.graph_objs._figure.Figure) #pylint: disable=protected-access
        for fig in test_cases:
            test(fig)

if __name__ == '__main__':
    unittest.main()
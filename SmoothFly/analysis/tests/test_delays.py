# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 08:07:00 2023

@author: mdbla
"""

import unittest
import sys
import plotly.graph_objs._figure
sys.path.append('analysis/create_visualizations')
import delays # pylint: disable=wrong-import-position


# Define a class in which the tests will run
class TestDelays(unittest.TestCase):
    """
    Test delays functions.
    
    ...
    Attributes
    ----------
    Inherited from unittest -- https://docs.python.org/3/library/unittest.html
    Methods
    -------
    test_delays_not_none(): Perform non none test on delays functions.
    test_delays_plotly_fig(): Perform plotly figure test on delays functions.
    """
    def test_delays_not_none(self):
        """Return the result of test for return value of none of delays functions."""
        test_cases = [
            delays.create_delay_ranking(),
            delays.create_delay_ct_breakdown(),
            delays.create_delay_min_breakdown(),
            delays.pct_delays_by_carrier()
        ]
        def test(fig):
            self.assertIsNotNone(fig)
        for fig in test_cases:
            test(fig)

    def test_delays_plotly_fig(self):
        """Return the result of plotly figure test of delays functions."""
        test_cases = [
            delays.create_delay_ranking(),
            delays.create_delay_ct_breakdown(),
            delays.create_delay_min_breakdown(),
            delays.pct_delays_by_carrier()
        ]
        def test(fig):
            self.assertIsInstance(fig, plotly.graph_objs._figure.Figure) #pylint: disable=protected-access
        for fig in test_cases:
            test(fig)

if __name__ == '__main__':
    unittest.main()
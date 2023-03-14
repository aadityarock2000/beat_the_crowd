"""
Denied Boarding Unit Tests: Test denied boarding visualizations.
Classes
-------
TestDeniedBoarding -- Unit Test class to test denied boarding visualization functions.
"""
import unittest
import sys
import plotly.graph_objs._figure
sys.path.append('analysis/create_visualizations')
import denied_boarding # pylint: disable=wrong-import-position


# Define a class in which the tests will run
class TestDeniedBoarding(unittest.TestCase):
    """
    Test denied boarding functions.
    
    ...
    Attributes
    ----------
    Inherited from unittest -- https://docs.python.org/3/library/unittest.html
    Methods
    -------
    test_denied_boarding_not_none(): Perform non none test on denied boarding functions.
    test_denied_boarding_plotly_fig(): Perform plotly figure test on denied boarding functions.
    """
    def test_denied_boarding_not_none(self):
        """Return the result of test for return value of none of denied boarding functions."""
        test_cases = [
            denied_boarding.db_plot_perc_denied_over_time(),
            denied_boarding.db_plot_perc_denied_by_carrier(),
            denied_boarding.db_plot_total_denied_by_carrier(),
            denied_boarding.db_plot_denial_type_by_carrier(),
            denied_boarding.db_plot_denied_compensation_reason(),
            denied_boarding.db_plot_comp_voluntary_by_carrier()
        ]
        def test(fig):
            self.assertIsNotNone(fig)
        for fig in test_cases:
            test(fig)

    def test_denied_boarding_plotly_fig(self):
        """Return the result of plotly figure test of denied boarding functions."""
        test_cases = [
            denied_boarding.db_plot_perc_denied_over_time(),
            denied_boarding.db_plot_perc_denied_by_carrier(),
            denied_boarding.db_plot_total_denied_by_carrier(),
            denied_boarding.db_plot_denial_type_by_carrier(),
            denied_boarding.db_plot_denied_compensation_reason(),
            denied_boarding.db_plot_comp_voluntary_by_carrier()
        ]
        def test(fig):
            self.assertIsInstance(fig, plotly.graph_objs._figure.Figure) #pylint: disable=protected-access
        for fig in test_cases:
            test(fig)

if __name__ == '__main__':
    unittest.main()

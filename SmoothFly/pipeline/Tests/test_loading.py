"""
This module contains unit tests for loading CSV files into a database using pyodbc.

Dependencies:
- sys
- unittest
- pytest
- pyodbc
- loading module

Classes:
- TestLoadCSV

"""
# import sys
import unittest
# import pytest
# import pyodbc

# #pylint: disable=wrong-import-position
# sys.path.append("pipeline/Load")
# import loading
# #pylint: disable=wrong-import-position

class TestLoadCSV(unittest.TestCase):

    # Will work only when there is server locally. Commenting as we do not have SQL Server on cloud
    # or accessible via github
    # """
    # Class Name: TestLoadCSV
    # Description: This class contains unit tests for Loading CSV files to DB.
    # """

    # def test_get_connection_empty_input(self):
    #     """
    #         Tests whether an error is raised when no input is provided to get_connection() method.
    #         Input:
    #             None
    #         Returns:
    #             None
    #         Raises:
    #             pyodbc.Error: If an error occurs while connecting to the database.
    #     """
    #     with pytest.raises(pyodbc.Error):
    #         loading.get_connection()

    # def test_get_connection_success(self):
    #     """
    #         Tests whether a pyodbc Connection object is returned when get_connection() is called.
    #         Input:
    #             None
    #         Returns:
    #             None
    #         Raises:
    #             AssertionError: If the object returned by get_connection() is not of 
    #             type pyodbc.Connection.
    #     """
    #     conn = loading.get_connection()
    #     assert isinstance(conn, pyodbc.Connection)

    # def test_get_connection_smoke(self):
    #     """
    #     Tests whether a non-null pyodbc Connection object is returned when get_connection() 
    #     is called.
    #     Input:
    #         None
    #     Returns:
    #         None
    #     Raises:
    #         AssertionError: If the object returned by get_connection() is None.
    #     """
    #     conn = loading.get_connection()
    #     assert conn is not None

if __name__ == '__main__':
    unittest.main()

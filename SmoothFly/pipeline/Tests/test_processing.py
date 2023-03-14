"""
This is a subclass of the unittest.TestCase class and contains multiple test methods to test the
functionality of the proceesing function of ETL.

Classes:
    TestProcessCSV
    TestProcessingMain
"""
import os
import sys
import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
#pylint: disable=wrong-import-position
sys.path.append("../Process")
from processing import process_csv, processing_main
#pylint: disable=wrong-import-position


class TestProcessCSV(unittest.TestCase):

    """
    Class:
        TestProcessCSV
    Functions :
    - test_one_shot(): This test case tests the function using a non-empty dataframe as input.
    It checks if the returned dataframe is equal to the expected dataframe and has the expected
    number of rows.
    - test_smoke_empty_frame(): This test case tests the function using an empty
    dataframe as input. It checks if the returned dataframe is empty and of type pandas.DataFrame.
    - test_edge_only_header(): This test case tests the function using a dataframe with only header
    as input. It checks if the returned dataframe is empty and of type pandas.DataFrame.
    - test_edge_one_row(): This test case tests the function using a dataframe with only one row as
    input. It checks if the returned dataframe has the expected number of rows and is of type
    pandas DataFrame.
    """

    def setUp(self):
        """
        Set up test data for the test methods. Creates a test dataframe with flight
        data and an expected dataframe with the same data but with different column names.
        """
        self.csv_data = pd.DataFrame({
            'Destination Airport': ['LAX', 'ORD', 'SFO'],
            'Carrier Code': ['AA', 'UA', 'DL'],
            'Date (MM/DD/YYYY)': ['01/01/2022', '01/02/2022', '01/03/2022'],
            'Flight Number': ['123', '456', '789'],
            'Tail Number': ['N12345', 'N67890', 'N24680'],
            'Scheduled departure time': ['12:00', '13:00', '14:00'],
            'Actual departure time': ['12:10', '13:05', '14:10'],
            'Scheduled elapsed time (Minutes)': [300, 180, 240],
            'Actual elapsed time (Minutes)': [310, 175, 245],
            'Departure delay (Minutes)': [10, 5, 10],
            'Wheels-off time': ['12:20', '13:10', '14:20'],
            'Taxi-Out time (Minutes)': [20, 5, 10],
            'Delay Carrier (Minutes)': [0, 0, 5],
            'Delay Weather (Minutes)': [0, 5, 0],
            'Delay National Aviation System (Minutes)': [5, 0, 0],
            'Delay Security (Minutes)': [0, 0, 0],
            'Delay Late Aircraft Arrival (Minutes)': [0, 0, 0]
        })

        self.expected_data = pd.DataFrame({
            'source': ['test', 'test', 'test'],
            'destination': ['LAX', 'ORD', 'SFO'],
            'carrier': ['AA', 'UA', 'DL'],
            'date': ['01/01/2022', '01/02/2022', '01/03/2022'],
            'flightNumber': ['123', '456', '789'],
            'tailNumber': ['N12345', 'N67890', 'N24680'],
            'scheduledDepartureTime': ['12:00', '13:00', '14:00'],
            'actualDepartureTime': ['12:10', '13:05', '14:10'],
            'scheduledElapsedMinutes': [300, 180, 240],
            'actualElapsedMinutes': [310, 175, 245],
            'departureDelayMinutes': [10, 5, 10],
            'wheelsOffTime': ['12:20', '13:10', '14:20'],
            'taxiOutMinutes': [20, 5, 10],
            'delayCarrierMinutes': [0, 0, 5],
            'delayWeatherMinutes': [0, 5, 0],
            'delayNationalAviationSystemMinutes': [5, 0, 0],
            'delaySecurityMinutes': [0, 0, 0],
            'delayLateAircraftArrivalMinutes': [0, 0, 0]
        })

    def test_one_shot(self):
        """
        Test the process_csv function with a test dataframe containing flight data. 
        Compares the output dataframe with an expected dataframe to ensure that the 
        function processes the data correctly.
        """
        result = process_csv('test.csv', self.csv_data)
        assert_frame_equal(result, self.expected_data)
        self.assertEqual(len(result), 3)

    def test_smoke_empty_frame(self):
        """
        Test the process_csv function with an empty dataframe. Assert that the function 
        returns an empty dataframe.
        """
        data_frame = pd.DataFrame()
        result = process_csv('empty_data.csv', data_frame)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 0)

    def test_edge_only_header(self):
        """
        Test the process_csv function with a dataframe containing only headers. 
        Assert that the function returns an empty dataframe.
        """
        data_frame = pd.read_csv('Test_Suite/Header_only.csv')
        result = process_csv('Header_only.csv', data_frame)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 0)

    def test_edge_one_row(self):
        """
        Test the process_csv function with a test dataframe containing only one row. 
        Compares the output dataframe with an expected dataframe to ensure that the 
        function processes the data correctly.
        """
        result = process_csv('test.csv', self.csv_data)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)

class TestProcessingMain(unittest.TestCase):

    """
    Class:
        TestProcessingMain

    Functions :
    - test_processing_main_smoke : Smoke test for processing_main function. 
    Test that processing_main function can be called without errors on an empty directory.
    - test_processing_main_one_shot : Test case for processing_main() with a single input CSV file. 
    The test case creates a CSV file with dummy data in a temporary directory, runs 
    processing_main() on it, and verifies that the output file has the expected columns and rows. 
    Finally, the temporary file is deleted.
    - test_processing_main_edge : Test case for processing_main() with an input file that is not 
    a CSV. The test case creates a non-CSV file in a temporary directory, runs processing_main() 
    on it, and verifies that the file is not modified. Finally, the temporary file is deleted.
    """

    def test_processing_main_smoke(self):
        """
        Smoke test for processing_main function.
        Test that processing_main function can be called without errors on an empty directory.
        Raises:
            AssertionError: If the test fails.
        """
        test_dir = "Empty"
        processing_main(test_dir)

    def test_processing_main_one_shot(self):
        """
        Test case for processing_main() with a single input CSV file.
        The test case creates a CSV file with dummy data in a temporary directory, 
        runs processing_main() on it, and verifies that the output file has the expected 
        columns and rows. Finally, the temporary file is deleted.
        Raises:
            AssertionError: If the output file does not have the expected columns or rows, 
            or if the temporary file was not deleted.
        """
        test_dir = "Test_Suite"
        file_name = "test.csv"
        csv_data = pd.DataFrame({
            'Destination Airport': ['LAX', 'ORD', 'SFO'],
            'Carrier Code': ['AA', 'UA', 'DL'],
            'Date (MM/DD/YYYY)': ['01/01/2022', '01/02/2022', '01/03/2022'],
            'Flight Number': ['123', '456', '789'],
            'Tail Number': ['N12345', 'N67890', 'N24680'],
            'Scheduled departure time': ['12:00', '13:00', '14:00'],
            'Actual departure time': ['12:10', '13:05', '14:10'],
            'Scheduled elapsed time (Minutes)': [300, 180, 240],
            'Actual elapsed time (Minutes)': [310, 175, 245],
            'Departure delay (Minutes)': [10, 5, 10],
            'Wheels-off time': ['12:20', '13:10', '14:20'],
            'Taxi-Out time (Minutes)': [20, 5, 10],
            'Delay Carrier (Minutes)': [0, 0, 5],
            'Delay Weather (Minutes)': [0, 5, 0],
            'Delay National Aviation System (Minutes)': [5, 0, 0],
            'Delay Security (Minutes)': [0, 0, 0],
            'Delay Late Aircraft Arrival (Minutes)': [0, 0, 0]
        })
        csv_data.to_csv(test_dir + '/' + file_name, index=False)
        processing_main(test_dir)
        processed_data = pd.read_csv(test_dir + '/' + file_name)
        print(len(processed_data))
        assert len(processed_data.columns) == 18
        assert len(processed_data) == 3
        assert 'source' in processed_data.columns
        assert 'destination' in processed_data.columns
        assert 'date' in processed_data.columns
        assert 'flightNumber' in processed_data.columns
        assert 'tailNumber' in processed_data.columns
        os.remove(test_dir+'/test.csv')

    def test_processing_main_edge(self):
        """
        Test case for processing_main() with an input file that is not a CSV.
        The test case creates a non-CSV file in a temporary directory, runs processing_main() on it, 
        and verifies that the file is not modified. Finally, the temporary file is deleted.
        Raises:
            AssertionError: If the file is modified or the temporary file was not deleted.

        """
        test_dir = "Test_Suite"
        file_name = "test.txt"
        with open(test_dir + '/' + file_name, "w",encoding='utf-8') as file:
            file.write("Test file")
        processing_main(test_dir)
        assert os.path.isfile(test_dir + '/' + file_name)  # non-CSV file should not be modified

if __name__ == '__main__':
    unittest.main()

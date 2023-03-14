"""
Attributes:
    None.

Methods:
    get_connection() -> pyodbc.Connection:
        Returns a pyodbc Connection object to a SQL Server database.
    
    init_table() -> None:
        Initializes a table named 'airline_stats' in the connected database.
    
    insert_data(data: pd.DataFrame) -> None:
        Inserts the data from a given pandas DataFrame into the 'airline_stats' 
        table in the connected database.
    
    loading_main(path: str) -> None:
        Reads a list of CSV files from a given path and inserts their data into the 'airline_stats' 
        table in the connected database.
"""

import os
import pandas as pd
import pyodbc

def get_connection() -> pyodbc.Connection:
    """
    Returns a pyodbc Connection object to a SQL Server database.
    No arguments needed.
    Returns:
        conn (pyodbc.Connection): A connection object to the database.
    """
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=localhost;'
                          'Database=airlines;'
                          'Trusted_Connection=yes;')
    return conn


def init_table() -> None:
    """
    Initializes a table named 'airline_stats' in the connected database.
    No arguments needed.
    Returns:
        None.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("drop table airline_stats")
    cursor.execute("""CREATE TABLE airline_stats ( source VARCHAR(255), destination VARCHAR(255),
    carrier VARCHAR(255), date DATE, flightNumber VARCHAR(255), 
    scheduledDepartureTime VARCHAR(255), actualDepartureTime VARCHAR(255), 
    scheduledElapsedMinutes VARCHAR(255), actualElapsedMinutes VARCHAR(255), 
    departureDelayMinutes VARCHAR(255), wheelsOffTime VARCHAR(255), taxiOutMinutes VARCHAR(255), 
    delayCarrierMinutes VARCHAR(255), delayWeatherMinutes VARCHAR(255), 
    delayNationalAviationSystemMinutes VARCHAR(255), delaySecurityMinutes VARCHAR(255), 
    delayLateAircraftArrivalMinutes VARCHAR(255))""")
    conn.commit()
    cursor.close()


def insert_data(data) -> None:
    """
    Inserts the data from a given pandas DataFrame into the 'airline_stats' table in the 
    connected database.
    Arguments:
        df (pd.DataFrame): The pandas DataFrame containing the data to be inserted into 
        the database.
    Returns:
        None.
    """
    conn = get_connection()
    cursor = conn.cursor()
    for row in data.itertuples():
        cursor.execute("""INSERT INTO [dbo].[airline_stats] ([source], [destination],
        [flightNumber],[carrier],[date],[scheduledDepartureTime],[actualDepartureTime],
        [scheduledElapsedMinutes],[actualElapsedMinutes],[departureDelayMinutes],[wheelsOffTime],
        [taxiOutMinutes],[delayCarrierMinutes],[delayWeatherMinutes],
        [delayNationalAviationSystemMinutes],[delaySecurityMinutes],
        [delayLateAircraftArrivalMinutes]) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        row.source, row.destination, row.flightNumber, row.carrier, row.date,
        row.scheduledDepartureTime,row.actualDepartureTime, row.scheduledElapsedMinutes,
        row.actualElapsedMinutes, row.departureDelayMinutes,row.wheelsOffTime, row.taxiOutMinutes,
        row.delayCarrierMinutes, row.delayWeatherMinutes,row.delayNationalAviationSystemMinutes,
        row.delaySecurityMinutes, row.delayLateAircraftArrivalMinutes)
    conn.commit()
    cursor.close()


def loading_main(path) -> None:
    """
    Reads a list of CSV files from a given path and inserts their data into the 'airline_stats' 
    table in the connected database.
    Arguments:
        path (str): The path where the CSV files are located.
    Returns:
        None.
    """
    file_list = os.listdir(path)
    for file in file_list:
        split_len = len(file.split('.'))

        if split_len > 1:
            ext = file.split('.')[1]
            if ext == 'csv':
                csv = pd.read_csv(path+'/'+file)
                insert_data(csv)

if __name__ == "__main__":
    PATH = '../../data/pipeline_data'
    loading_main(PATH)

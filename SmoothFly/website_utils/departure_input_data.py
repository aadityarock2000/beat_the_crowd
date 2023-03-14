'''
This module contains the utilities that the input fields for the pipeline part of website uses.

Functions:

airports_list: Returns the list of airports that are in the reference files for airports
carrier_list: Returns the list of air carriers that are in the reference files for carriers_list.txt
file_types: Returns the list of file types availiable

'''

import pandas as pd


def airport_list(path):
    '''
    Returns the list of airports that are in the reference files for airports_list.txt
    '''

    try:
        airport_code_reference = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        # Handle the edge case of reading an empty file
        return ['All']

    airports = ['All'] + list(airport_code_reference['Airport_name'])
    return airports

def carrier_list(file):
    '''
    Returns the list of air carriers that are in the reference files for carriers_list.txt
    '''
    try:
        airport_carrier_codes_reference = pd.read_csv(file)
    except pd.errors.EmptyDataError:
        return ['All']
    except FileNotFoundError as exc:
        raise FileNotFoundError("The file '" + file + "' could not be found.") from exc


    carrier_lists=['All']+list(airport_carrier_codes_reference['Carrier_name'])
    return carrier_lists

def file_types():
    '''
    Returns the list of file types availiable
    '''
    types=['Excel', 'CSV', 'MS SQL DB']
    return types

if __name__=='__main__':
    print('Hello')

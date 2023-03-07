'''
This module contains the utilities that the input fields for the pipeline part of website uses.

Functions:

airports_list: Returns the list of airports that are in the reference files for airports
carrier_list: Returns the list of air carriers that are in the reference files for carriers_list.txt
file_types: Returns the list of file types availiable

'''

import pandas as pd


def airport_list():
    '''
    Returns the list of airports that are in the reference files for airports_list.txt
    '''
    airport_code_reference=pd.read_csv('website_utils/airport_codes_reference.csv')
    airports=list(airport_code_reference['Airport_name'])
    return airports

def carrier_list():
    '''
    Returns the list of air carriers that are in the reference files for carriers_list.txt
    '''
    airport_carrier_codes_reference=pd.read_csv('website_utils/airport_carrier_codes_reference.csv')
    carriers=list(airport_carrier_codes_reference['Carrier_name'])
    return carriers

def file_types():
    '''
    Returns the list of file types availiable
    '''
    types=['Excel', 'CSV', 'MS SQL DB']
    return types

if __name__=='__main__':
    print('in the departure_input_delay function')

'''
This module provides functions that can parse the SQL database and provide the output 
in the website end

Functions:
input_preparation: Parses the input from the user in the website, and prepares it for parsing in SQL
'''
import pandas as pd

def fetch_airport_code(airport):
    '''
    Fetches the airport code for the given airport name
    '''
    airport_reference=pd.read_csv('website_utils/reference_data/airport_codes_reference.csv')
    #print(airport_reference[airport_reference['Airport_name']==airport]['Airport_code'])
    code=airport_reference[airport_reference['Airport_name']==airport]['Airport_code'].item()
    return code

def input_preparation(inputs):
    '''
    Parses the input from the user in the website, and prepares it for parsing in SQL
    '''
    print(inputs)
    source = fetch_airport_code(inputs['source_airport'])
    destination = fetch_airport_code(inputs['destination_airport'])
    return (source,destination)

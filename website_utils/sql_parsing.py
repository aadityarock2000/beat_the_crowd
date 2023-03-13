'''
This module provides functions that can parse the SQL database and provide the output 
in the website end

Functions:
fetch_airport_code: Fetches the airport code for the given airport name
fetch_carrier_code: Fetches the code for the given single carrier using the reference data
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

def fetch_carrier_code(carrier):
    '''
    Fetches the code for the given single carrier using the reference data
    '''
    file = 'website_utils/reference_data/airport_carrier_codes_reference.csv'
    carrier_reference=pd.read_csv(file)
    code=carrier_reference[carrier_reference['Carrier_name']==carrier]['Carrier_code'].item()
    return code

def input_preparation(inputs):
    '''
    Parses the input from the user in the website, and prepares it for parsing in SQL
    '''
    #print(inputs)

    source = []
    destination = []
    carrier =[]


    #parsing source and destination and carrier
    # source = fetch_airport_code(inputs['source_airport'])
    # destination = fetch_airport_code(inputs['destination_airport'])
    # carrier = fetch_airport_code(inputs['carrier'])
    #checking for the all command
    if 'All' in inputs['source_airport']:
        source = ['All']
    else:
        for airport in inputs['source_airport']:
            source.append(fetch_airport_code(airport))
    if 'All' in inputs['destination_airport']:
        destination = ['All']
    else:
        for airport in inputs['destination_airport']:
            destination.append(fetch_airport_code(airport))
    if 'All' in carrier:
        carrier = ['All']
    else:
        for car in inputs['carrier']:
            carrier.append(fetch_carrier_code(car))
    #fetching the rest of the inputs
    from_date=inputs['from_date']
    to_date=inputs['to_date']
    file_format=inputs['file_format']
    parsed_inputs={
        'source_airport':source,
        'from_date':from_date,
        'file_format':file_format,
        'destination_airport':destination,
        'to_date':to_date,
        'carrier':carrier
        }
    # print(parsed_inputs)
    # print(type(from_date)) #<class 'datetime.date'>
    return parsed_inputs

def create_query_string(parsed_inputs):
    '''
    creates the query based on the inputs given, to be used in the SQL SERVER
    '''
    table_name=''
    query = 'SELECT * FROM '+table_name+' WHERE '
    parsed_inputs={
        'source_airport':source,
        'from_date':from_date,
        'file_format':file_format,
        'destination_airport':destination,
        'to_date':to_date,
        'carrier':carrier
        }
    if parsed_inputs['source_airport'] != ['All']:
        source_string='source in '
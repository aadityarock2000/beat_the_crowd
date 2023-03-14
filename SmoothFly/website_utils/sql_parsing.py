'''
This module provides functions that can parse the SQL database and provide the output 
in the website end

Functions:
fetch_airport_code: Fetches the airport code for the given airport name
fetch_carrier_code: Fetches the code for the given single carrier using the reference data
input_preparation: Parses the input from the user in the website, and prepares it for parsing in SQL
'''
import io
import csv

import pandas as pd
import pyodbc


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
    Creates the query based on the inputs given, to be used in the SQL SERVER
    '''
    table_name='airlines'
    query = 'SELECT * FROM '+table_name+' WHERE '
    if parsed_inputs['source_airport'] != ['All']:
        string_=''
        for ele in parsed_inputs['source_airport']:
            string_+="'"+ele+"'"
            string_+=','
        string_=string_[:-1]
        source_string='source in ('+string_+') AND '
        query+=source_string
    if parsed_inputs['destination_airport'] != ['All']:
        string_=''
        for ele in parsed_inputs['destination_airport']:
            string_+="'"+ele+"'"
            string_+=','
        string_=string_[:-1]
        dest_string='destination in ('+string_+') AND '
        query+=dest_string
    if parsed_inputs['carrier'] != ['All']:
        string_=''
        for ele in parsed_inputs['carrier']:
            string_+="'"+ele+"'"
            string_+=','
        string_=string_[:-1]
        dest_string='carrier in ('+string_+') AND '
        query+=dest_string
    #adding dates to the query
    query +='date BETWEEN ? AND ?'

    return query,parsed_inputs['from_date'],parsed_inputs['to_date'],parsed_inputs['file_format']

def connect_sql_server():
    '''
    Connect to a sql server
    '''
    DRIVER_NAME = 'SQL SERVER'
    SERVER_NAME = 'Sniperwolf'
    DATABASE_NAME = 'DEMODB'
    connection_string=f"""
        DRIVER={{{DRIVER_NAME}}};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        Trust_Connection=yes;
    """
    cnxn = pyodbc.connect(connection_string)
    return cnxn

def execute_code(cnxn,query,from_date,to_date,file_format):
    '''
    Executes the code and returns the file to be downloaded
    '''
    # Execute a SQL query
    cursor = cnxn.cursor()
    cursor.execute(query, from_date, to_date)
    # Retrieve the results


    if file_format=='CSV':
        results = cursor.fetchall()
        # write the results to a StringIO buffer
        csv_buffer = io.StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow([column[0] for column in cursor.description]) # write the headers
        for row in results:
            csv_writer.writerow(row)
        # convert the buffer to a string and create a download button for the user
        csv_string = csv_buffer.getvalue()
        return csv_string
    elif file_format=='Excel':
        # execute the query and create a DataFrame
        df = pd.read_sql(query, cnxn)
        # create an Excel file from the DataFrame
        excel_file = io.BytesIO()
        writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
        excel_file.seek(0)
        return excel_file
    else:
        df = pd.read_sql(query, cnxn)
        return df
    
    cnxn.close()


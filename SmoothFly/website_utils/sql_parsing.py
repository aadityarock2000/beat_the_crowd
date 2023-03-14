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


def fetch_airport_code(airport, path):
    '''
    Fetches the airport code for the given airport name
    '''
    if not airport:
        raise ValueError("Airport name cannot be empty")
    airport_reference = pd.read_csv(path)
    airport_reference['Airport_name'] = airport_reference['Airport_name'].str.lower()
    airport_reference['Airport_code'] = airport_reference['Airport_code'].str.upper()
    code = airport_reference[airport_reference['Airport_name'] == airport.lower()]['Airport_code'].item()
    return code if code else None

def fetch_carrier_code(carrier, path):
    '''
    Fetches the code for the given single carrier using the reference data
    '''
    if not carrier:
        raise ValueError("Carrier name cannot be empty")
    carrier_reference = pd.read_csv(path)
    carrier_reference['Carrier_name'] = carrier_reference['Carrier_name'].str.lower()
    carrier_reference['Carrier_code'] = carrier_reference['Carrier_code'].str.upper()
    code = carrier_reference[carrier_reference['Carrier_name'] == carrier.lower()]['Carrier_code'].item()
    return code if code else None


    # carrier_reference=pd.read_csv(path)
    # code=carrier_reference[carrier_reference['Carrier_name']==carrier]['Carrier_code'].item()
    # return code

def input_preparation(inputs,path,car_path):
    '''
    Parses the input from the user in the website, and prepares it for parsing in SQL
    '''
    #print(inputs)
    if not inputs['source_airport'] or not inputs['destination_airport'] or not inputs['carrier'] \
            or not inputs['from_date'] or not inputs['to_date'] or not inputs['file_format']:
        raise ValueError('All fields are required.')


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
            source.append(fetch_airport_code(airport,path))
    if 'All' in inputs['destination_airport']:
        destination = ['All']
    else:
        for airport in inputs['destination_airport']:
            destination.append(fetch_airport_code(airport,path))
    if 'All' in inputs['carrier']:
        carrier = ['All']
    else:
        for car in inputs['carrier']:
            carrier.append(fetch_carrier_code(car,car_path))

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
    table_name='airline_stats'
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

    from_ = "'"+parsed_inputs['from_date'].strftime(r"%Y-%m-%d")+"'"
    to_= "'"+parsed_inputs['to_date'].strftime(r"%Y-%m-%d")+"'"
    query +='date BETWEEN '+from_+' AND '+to_+';'

    return query,parsed_inputs['file_format']

def connect_sql_server():
    '''
    Connect to a sql server
    '''
    driver_name = 'SQL SERVER'
    server_name = 'Sniperwolf'
    database_name = 'airlines'
    connection_string=f"""
        DRIVER={{{driver_name}}};
        SERVER={server_name};
        DATABASE={database_name};
        Trust_Connection=yes;
    """
    cnxn = pyodbc.connect(connection_string)
    return cnxn

def execute_code(cnxn,query,file_format):
    '''
    Executes the code and returns the file to be downloaded
    '''
    # Execute a SQL query
    cursor = cnxn.cursor()



    cursor.execute(query)
    #cursor.execute('SELECT TOP 5 * FROM airline_stats;')
    columns = [column[0] for column in cursor.description]
    # Retrieve the results
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    if file_format=='CSV':
        csv_file = io.StringIO()
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(columns)
        csv_writer.writerows(rows)
        cnxn.close()
        return csv_file

        # results = cursor.fetchall()
        # # write the results to a StringIO buffer
        # csv_buffer = io.StringIO()
        # csv_writer = csv.writer(csv_buffer)
        # csv_writer.writerow([column[0] for column in cursor.description]) # write the headers
        # for row in results:
        #     csv_writer.writerow(row)
        # # convert the buffer to a string and create a download button for the user
        # csv_string = csv_buffer.getvalue()
        # return csv_string
    elif file_format=='Excel':
        # execute the query and create a DataFrame
        data1 = pd.DataFrame(rows, columns=columns)
        data1.to_excel('output.xlsx', index=False)
        return 'output.xlsx'
    else:
        data1 = pd.read_sql(query, cnxn)
        cnxn.close()
        return data1

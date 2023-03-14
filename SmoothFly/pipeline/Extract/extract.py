"""
    The module collects data on flight departures and logs them into a file. It uses the requests and BeautifulSoup libraries for web scraping and logging library for logging.

    It defines the following global variables:

    URL: the URL of the website to be scraped.
    HEADERS: a dictionary of headers to be used for the HTTP request.
    AIRPORTS: a list of airports to be scraped.
    AIRLINES: a list of airlines to be scraped.
    DATA: a dictionary of data fields to be submitted in the HTTP request.
    It also defines the following function:

    update_state(soup): a function to update the state (aspx related) to maintain authorization.
    get_master_data(response): a function to extract list of airports and airlines from page
    initial_page(session): a function to get the initial landing page of BTS.gov
    get_airport_csv(session): a function to get downloadable CSV from BTS.gov
    query_aspx(airport, path, session): a function to query all airlines for a given airport
    extract_main(path): main function of extraction logic

"""

import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(filename='data-collection.log',
                    encoding='utf-8', level=logging.DEBUG)

URL = 'https://www.transtats.bts.gov/ontime/departures.aspx'
HEADERS = {'User-Agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50'}
AIRPORTS = []
AIRLINES = []
DATA = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': '',
    '__VIEWSTATEGENERATOR': '',
    '__EVENTVALIDATION': '',
    'chkAllStatistics': 'on',
    'chkStatistics$0': '0',
    'chkStatistics$1': '1',
    'chkStatistics$2': '2',
    'chkStatistics$3': '3',
    'chkStatistics$4': '4',
    'chkStatistics$5': '5',
    'chkStatistics$6': '6',
    'chkStatistics$7': '7',
    'cboAirport': 'ABR',
    'cboAirline': 'TZ',
    'chkAllMonths': 'on',
    'chkMonths$0': '1',
    'chkMonths$1': '2',
    'chkMonths$2': '3',
    'chkMonths$3': '4',
    'chkMonths$4': '5',
    'chkMonths$5': '6',
    'chkMonths$6': '7',
    'chkMonths$7': '8',
    'chkMonths$8': '9',
    'chkMonths$9': '10',
    'chkMonths$10': '11',
    'chkMonths$11': '12',
    'chkAllDays': 'on',
    'chkDays$0': '1',
    'chkDays$1': '2',
    'chkDays$2': '3',
    'chkDays$3': '4',
    'chkDays$4': '5',
    'chkDays$5': '6',
    'chkDays$6': '7',
    'chkDays$7': '8',
    'chkDays$8': '9',
    'chkDays$9': '10',
    'chkDays$10': '11',
    'chkDays$11': '12',
    'chkDays$12': '13',
    'chkDays$13': '14',
    'chkDays$14': '15',
    'chkDays$15': '16',
    'chkDays$16': '17',
    'chkDays$17': '18',
    'chkDays$18': '19',
    'chkDays$19': '20',
    'chkDays$20': '21',
    'chkDays$21': '22',
    'chkDays$22': '23',
    'chkDays$23': '24',
    'chkDays$24': '25',
    'chkDays$25': '26',
    'chkDays$26': '27',
    'chkDays$27': '28',
    'chkDays$28': '29',
    'chkDays$29': '30',
    'chkDays$30': '31',
    'chkAllYears': 'on',
    'chkYears$0': '1987',
    'chkYears$1': '1988',
    'chkYears$2': '1989',
    'chkYears$3': '1990',
    'chkYears$4': '1991',
    'chkYears$5': '1992',
    'chkYears$6': '1993',
    'chkYears$7': '1994',
    'chkYears$8': '1995',
    'chkYears$9': '1996',
    'chkYears$10': '1997',
    'chkYears$11': '1998',
    'chkYears$12': '1999',
    'chkYears$13': '2000',
    'chkYears$14': '2001',
    'chkYears$15': '2002',
    'chkYears$16': '2003',
    'chkYears$17': '2004',
    'chkYears$18': '2005',
    'chkYears$19': '2006',
    'chkYears$20': '2007',
    'chkYears$21': '2008',
    'chkYears$22': '2009',
    'chkYears$23': '2010',
    'chkYears$24': '2011',
    'chkYears$25': '2012',
    'chkYears$26': '2013',
    'chkYears$27': '2014',
    'chkYears$28': '2015',
    'chkYears$29': '2016',
    'chkYears$30': '2017',
    'chkYears$31': '2018',
    'chkYears$32': '2019',
    'chkYears$33': '2020',
    'chkYears$34': '2021',
    'chkYears$35': '2022',
    'btnSubmit': 'Submit'
}


def update_state(soup):
    """
    Update state (aspx related) to maintain authorization.
    Args:
        soup (bs4.BeautifulSoup): A BeautifulSoup object that represents the 
        HTML content of the page.
    Returns:
        None.
    """
    if soup is None:
        return None
    DATA['__VIEWSTATE'] = soup.find(
        'input', attrs={'id': '__VIEWSTATE'})['value']
    DATA['__VIEWSTATEGENERATOR'] = soup.find(
        'input', attrs={'id': '__VIEWSTATEGENERATOR'})['value']
    DATA['__EVENTVALIDATION'] = soup.find(
        'input', attrs={'id': '__EVENTVALIDATION'})['value']


def get_master_data(response):
    """
    Retrieves the master data from a given HTTP response and updates the AIRPORTS and AIRLINES 
    lists with the relevant information.
    Arguments:
        response (requests.models.Response): The HTTP response containing the master data.
    Returns:
        None.
    Raises:
        None.
    """

    if response is None:
        return None

    logging.debug('### Inside Master Call')
    AIRLINES.clear()
    AIRPORTS.clear()

    soup = BeautifulSoup(response.content, 'html.parser')
    update_state(soup)

    airport_list = soup.findAll('select', attrs={'id': 'cboAirport', 'name': 'cboAirport'})[0].\
        findAll('option')
    for air in airport_list:
        AIRPORTS.append(air['value'])

    airlines_list = soup.findAll('select', attrs={'id': 'cboAirline', 'name': 'cboAirline'})[0].\
        findAll('option')
    for air in airlines_list:
        AIRLINES.append(air['value'])

    logging.debug('### Outside Master Call')


def initial_page(session):
    """
    Sends a GET request to the BTS.gov URL and performs some initialization tasks such as 
    retrieving and parsing data from the response using the 'get_master_data' function.
    Arguments:
        session (session): Session object to query BTS.gov
    Returns:
        None.
    """
    if session is None or HEADERS is None:
        return None
    else:
        logging.debug('### Inside Initial Call')
        response = session.get(URL, headers=HEADERS, verify=False)
        get_master_data(response)
        logging.debug('### Outside Initial Call')


def get_airport_csv(session):
    """
    Modifies data to get a downloadable CSV from BTS.gov for a specific airport. 
    Resets the data back for the next airline/airport.
    Arguments:        
        session (session): Session object to query BTS.gov
    Returns:
        requests.Response: Response object from the post request to download the CSV.
    """
    if DATA is None or DATA['__VIEWSTATE'] == '':
        return None
    DATA['__EVENTTARGET'] = 'DL_CSV'
    DATA['__EVENTARGUMENT'] = ''
    del DATA['btnSubmit']
    response = session.post(URL, headers=HEADERS, data=DATA, verify=False)
    DATA['__EVENTTARGET'] = ''
    DATA['__EVENTARGUMENT'] = ''
    DATA['btnSubmit'] = 'Submit'
    return response


def query_aspx(airport, path, session):
    """
    Queries all airlines for a given airport and saves a single CSV file for an airport.
    Arguments:
        airport (str): The airport code for which data needs to be extracted.
        path (str):  The path where we need to store the CSV.
        session (session): Session object to query BTS.gov
    Returns:
        None.
    """
    if DATA is None:
        return None
    DATA['cboAirport'] = airport
    for airline in AIRLINES:
        DATA['cboAirline'] = airline
        response = session.post(URL, headers=HEADERS, data=DATA, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        update_state(soup)
        airport_csv = get_airport_csv(session)
        if airport_csv.status_code == 200:
            logging.debug('--------> Found data for %s', airline)
            airport_csv = airport_csv.content
            with open(path+'/'+airport+'.csv', 'ba') as file:
                start = airport_csv.find(b'\n\n')
                airport_csv = airport_csv[start+1:]
                end = airport_csv.find(b'\n\n')
                airport_csv = airport_csv[:end]
                file.write(airport_csv)
        else:
            logging.debug('Ran into a problem for : %s & %s : Code : %s',
                          airport, airline, str(airport_csv.status_code))


def extract_main(path):
    """
    Extracts data for all airports and saves it in a CSV file.
    Arguments:
        path (str): The path where the CSV files will be saved.
        nums (int): Added for testing. Since this method loads all the data from the website.
        nums will determine the number of airports to cover
    Returns:
        None.
    """
    session = requests.Session()
    session.headers.update(HEADERS)
    initial_page(session)
    for i in PROCESSED:
        try:
            AIRPORTS.remove(i)
        except ValueError:
            pass
    print(AIRPORTS)
    for airport in AIRPORTS:
        logging.debug('### Processing for %s', airport)
        query_aspx(airport, path,session)
        PROCESSED.append(airport)


if __name__ == "__main__":
    PROCESSED = []
    PATH = '../../data/pipeline_data'
    extract_main(PATH)

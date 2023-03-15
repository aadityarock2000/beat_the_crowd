# """

# This module extracts flight data from the transtats.bts.gov website and saves it to a file.

# The module provides the following functions:

#     - update_main: sends HTTP requests to retrieve flight data and saves it to a file.

#     Required packages:

#     - datetime
#     - sys
#     - logging
#     - requests
#     - extract (custom module)

# Usage:

#     - Import the module:

#         import update

#     - Call the update_main function to retrieve and save flight data:

#         path = 'path/to/data/folder'
#         update.update_main(path)

# """
# import datetime
# import sys
# import logging
# import requests

# #pylint: disable=wrong-import-position
# sys.path.append("pipeline/Extract")
# import extract
# #pylint: disable=wrong-import-position

# URL = 'https://www.transtats.bts.gov/ontime/departures.aspx'
# HEADERS = {'User-Agent':
#            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#            +'Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50'}
# AIRPORTS = []
# AIRLINES = []
# DATA = {
#     '__EVENTTARGET': '',
#     '__EVENTARGUMENT': '',
#     '__VIEWSTATE': '',
#     '__VIEWSTATEGENERATOR': '',
#     '__EVENTVALIDATION': '',
#     'chkAllStatistics': 'on',
#     'chkStatistics$0': '0',
#     'chkStatistics$1': '1',
#     'chkStatistics$2': '2',
#     'chkStatistics$3': '3',
#     'chkStatistics$4': '4',
#     'chkStatistics$5': '5',
#     'chkStatistics$6': '6',
#     'chkStatistics$7': '7',
#     'cboAirport': 'ABR',
#     'cboAirline': 'TZ',
#     'chkAllMonths': 'on',
#     'chkMonths$0': '1',
#     'chkMonths$1': '2',
#     'chkMonths$2': '3',
#     'chkMonths$3': '4',
#     'chkMonths$4': '5',
#     'chkMonths$5': '6',
#     'chkMonths$6': '7',
#     'chkMonths$7': '8',
#     'chkMonths$8': '9',
#     'chkMonths$9': '10',
#     'chkMonths$10': '11',
#     'chkMonths$11': '12',
#     'chkAllDays': 'on',
#     'chkDays$0': '1',
#     'chkDays$1': '2',
#     'chkDays$2': '3',
#     'chkDays$3': '4',
#     'chkDays$4': '5',
#     'chkDays$5': '6',
#     'chkDays$6': '7',
#     'chkDays$7': '8',
#     'chkDays$8': '9',
#     'chkDays$9': '10',
#     'chkDays$10': '11',
#     'chkDays$11': '12',
#     'chkDays$12': '13',
#     'chkDays$13': '14',
#     'chkDays$14': '15',
#     'chkDays$15': '16',
#     'chkDays$16': '17',
#     'chkDays$17': '18',
#     'chkDays$18': '19',
#     'chkDays$19': '20',
#     'chkDays$20': '21',
#     'chkDays$21': '22',
#     'chkDays$22': '23',
#     'chkDays$23': '24',
#     'chkDays$24': '25',
#     'chkDays$25': '26',
#     'chkDays$26': '27',
#     'chkDays$27': '28',
#     'chkDays$28': '29',
#     'chkDays$29': '30',
#     'chkDays$30': '31',
#     'btnSubmit': 'Submit'
# }



# def update_main(path):
#     """
#     update_main: sends HTTP requests to retrieve flight data from the transtats.bts.gov
#     website and saves it to a file.

#     Arguments:
#         path (str): path to directory where the extracted data will be stored.

#     Returns:
#         None
#     """
#     counter = 35
#     year = datetime.date.today().year
#     print(year)
#     counter += year-2022
#     key = 'chkYears$'+str(counter)
#     DATA[key] = str(year)

#     print(DATA)

#     session = requests.Session()
#     session.headers.update(HEADERS)
#     extract.initial_page(session)
#     for i in PROCESSED:
#         try:
#             AIRPORTS.remove(i)
#         except ValueError:
#             pass
#     print(AIRPORTS)
#     for airport in AIRPORTS:
#         logging.debug('### Processing for %s', airport)
#         extract.query_aspx(airport, path,session)
#         PROCESSED.append(airport)

#     session.close()


# if __name__ == "__main__":
#     PROCESSED = []
#     PATH = 'data/pipeline_update_data'
#     update_main(PATH)

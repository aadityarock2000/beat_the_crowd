import requests
from bs4 import BeautifulSoup

# Global Data Template
def reset():
    global headers
    global url
    global data
    global airports
    global airlines
    url = 'https://www.transtats.bts.gov/ontime/departures.aspx'
    headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50' }
    airports = []
    airlines = []
    data = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT':'',
    '__VIEWSTATE':'',
    '__VIEWSTATEGENERATOR':'',
    '__EVENTVALIDATION':'',
    'chkAllStatistics':'on',
    'chkStatistics$0':'0',
    'chkStatistics$1':'1',
    'chkStatistics$2':'2',
    'chkStatistics$3':'3',
    'chkStatistics$4':'4',
    'chkStatistics$5':'5',
    'chkStatistics$6':'6',
    'chkStatistics$7':'7',
    'cboAirport':'ABR',
    'cboAirline':'TZ',
    'chkAllMonths':'on',
    'chkMonths$0':'1',
    'chkMonths$1':'2',
    'chkMonths$2':'3',
    'chkMonths$3':'4',
    'chkMonths$4':'5',
    'chkMonths$5':'6',
    'chkMonths$6':'7',
    'chkMonths$7':'8',
    'chkMonths$8':'9',
    'chkMonths$9':'10',
    'chkMonths$10':'11',
    'chkMonths$11':'12',
    'chkAllDays':'on',
    'chkDays$0':'1',
    'chkDays$1':'2',
    'chkDays$2':'3',
    'chkDays$3':'4',
    'chkDays$4':'5',
    'chkDays$5':'6',
    'chkDays$6':'7',
    'chkDays$7':'8',
    'chkDays$8':'9',
    'chkDays$9':'10',
    'chkDays$10':'11',
    'chkDays$11':'12',
    'chkDays$12':'13',
    'chkDays$13':'14',
    'chkDays$14':'15',
    'chkDays$15':'16',
    'chkDays$16':'17',
    'chkDays$17':'18',
    'chkDays$18':'19',
    'chkDays$19':'20',
    'chkDays$20':'21',
    'chkDays$21':'22',
    'chkDays$22':'23',
    'chkDays$23':'24',
    'chkDays$24':'25',
    'chkDays$25':'26',
    'chkDays$26':'27',
    'chkDays$27':'28',
    'chkDays$28':'29',
    'chkDays$29':'30',
    'chkDays$30':'31',
    'chkAllYears':'on',
    'chkYears$0':'1987',
    'chkYears$1':'1988',
    'chkYears$2':'1989',
    'chkYears$3':'1990',
    'chkYears$4':'1991',
    'chkYears$5':'1992',
    'chkYears$6':'1993',
    'chkYears$7':'1994',
    'chkYears$8':'1995',
    'chkYears$9':'1996',
    'chkYears$10':'1997',
    'chkYears$11':'1998',
    'chkYears$12':'1999',
    'chkYears$13':'2000',
    'chkYears$14':'2001',
    'chkYears$15':'2002',
    'chkYears$16':'2003',
    'chkYears$17':'2004',
    'chkYears$18':'2005',
    'chkYears$19':'2006',
    'chkYears$20':'2007',
    'chkYears$21':'2008',
    'chkYears$22':'2009',
    'chkYears$23':'2010',
    'chkYears$24':'2011',
    'chkYears$25':'2012',
    'chkYears$26':'2013',
    'chkYears$27':'2014',
    'chkYears$28':'2015',
    'chkYears$29':'2016',
    'chkYears$30':'2017',
    'chkYears$31':'2018',
    'chkYears$32':'2019',
    'chkYears$33':'2020',
    'chkYears$34':'2021',
    'chkYears$35':'2022',
    'btnSubmit': 'Submit'
    }

        
def updateState(soup):  
    data['__VIEWSTATE']          = soup.find('input', attrs={'id': '__VIEWSTATE'})['value']
    data['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'id': '__VIEWSTATEGENERATOR'})['value']
    data['__EVENTVALIDATION']    = soup.find('input', attrs={'id': '__EVENTVALIDATION'})['value']   

# Extract master data of all airports and airlines from the initial page
def getMasterData(r):
    
    global airports
    global airlines
    airlines.clear()
    airports.clear()
    
    soup = BeautifulSoup(r.content, 'html.parser')
    updateState(soup)
    
    airportsList = soup.findAll('select', attrs={'id':'cboAirport','name':'cboAirport'})[0].findAll('option')
    for air in airportsList:        
        airports.append(air['value'])
    
    airlinesList = soup.findAll('select', attrs={'id':'cboAirline','name':'cboAirline'})[0].findAll('option')
    for air in airlinesList:        
        airlines.append(air['value'])
        
    

# Get the initial page 
def initialPage():
    global s
    r=s.get(url,headers=headers, verify=False)
    getMasterData(r)


# Function to modify data to get a downloadable CSV from BTS.gov. Resets the data back for next airline/airport
def getAirportCSV():
    global s
    global headers
    global data
    global url
    data['__EVENTTARGET']    = 'DL_CSV'
    data['__EVENTARGUMENT']    = ''
    del data['btnSubmit']
    r = s.post(url,headers=headers, data=data,verify=False)
    data['__EVENTTARGET']    = ''
    data['__EVENTARGUMENT']    = ''
    data['btnSubmit'] = 'Submit'
    return r

def extract_main(path):
    global headers
    global s
    global airports
    reset()
    s = requests.Session()
    s.headers.update(headers)
    initialPage()
    
if __name__ == "__main__":
    PATH = '../../data/pipeline_data'
    extract_main(PATH)

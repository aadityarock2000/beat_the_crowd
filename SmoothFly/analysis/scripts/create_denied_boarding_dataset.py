""" 
Create Denied Boarding Dataset: Created dataset of cleaned and processed denied boarding data. 
"""

import pandas as pd
years = list(map(str, list(range(2018, 2022, 1)))) # years with data available on BTS
quarters = ("Q1", "Q2", "Q3", "Q4")
denied_board_dfs = list()

# read in data that uses new reporting method - excel sheet with sheet for each quarter
for year in years:
    for quarter in quarters:
        file_path = "C:\\Users\\franc\\beat_the_crowd\\beat_the_crowd\\Analysis\\raw_data\\denied_boarding\\Denied-Confirmed-Space-" + year + "-Operating-Carrier.xlsx" # pylint: disable=line-too-long
        sheet = quarter + year
        df = pd.read_excel(file_path, sheet_name=sheet, header = 2)
        # column definitions changed in 2021
        if (year != "2021"): # pylint: disable=superfluous-parens
            df[6] = df[7]
            df[7] = df['8(c)']
            df = df[['CARRIER',
                     '1(a)',    
                     '1(b)',    
                     '2(a)',    
                     '2(b)',    
                     '2(c)',
                     3,
                     4,
                     5,
                     6,
                     7]]
        df['year'] = year
        df['quarter'] = quarter + " " + year
        df = df[pd.isna(df[6]) is not True]
        denied_board_dfs.append(df)

denied_boarding = pd.concat(denied_board_dfs)

denied_boarding[1] = denied_boarding['1(a)']+denied_boarding['1(b)']
denied_boarding[2] = denied_boarding['2(a)']+denied_boarding['2(b)']+denied_boarding['2(c)']
denied_boarding['perc_denied_boarding'] = round(((denied_boarding[3] + denied_boarding[5])/
                                                 denied_boarding[6])*100, 4)
denied_boarding['perc_denied_boarding_involuntary'] = round((denied_boarding[3]/
                                                             denied_boarding[6])*100, 6)
denied_boarding['perc_denied_boarding_voluntary'] = round((denied_boarding[5]/
                                                           denied_boarding[6]*100), 6)
denied_boarding['total_denials'] = denied_boarding[3]+denied_boarding[5]
denied_boarding['cash_per_vol_denial'] = round((denied_boarding[7]/denied_boarding[5]),2)

denied_boarding['date'] = pd.to_datetime([
    '-'.join(x.split()[::-1]) for x in denied_boarding['quarter']])

# Standardize naming conventions of airlines
denied_boarding.loc[denied_boarding.CARRIER == 'Allegiant Air', 'CARRIER'] = 'Allegiant Airlines'
denied_boarding.loc[denied_boarding.CARRIER ==
                    'Alaska Airlines Codeshare', 'CARRIER'] = 'Alaska Airlines'
denied_boarding.loc[denied_boarding.CARRIER == 'Republic Airways', 'CARRIER']= 'Republic Airline'
denied_boarding.loc[denied_boarding.CARRIER == 'United Airlines', 'CARRIER'] = 'United Air Lines'

denied_boarding.to_csv("..\\Analysis\\clean_data\\denied_boarding.csv", index = False)

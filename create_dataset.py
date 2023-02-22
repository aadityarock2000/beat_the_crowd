import pandas as pd
fares = pd.read_csv('raw_data\\Consumer_Airfare_Report__Table_7_-_Fare_Premiums_for_Select_Cities_with_More_Than_20_Passengers_per_Day.csv')
delay_cause = pd.read_csv('raw_data\\Airline_Delay_Cause_2003_2022.csv')
denied_boarding = pd.read_csv('raw_data\\Denied-Confirmed-Space-2021-Marketing-Carrier-Q1.csv')
denied_boarding = denied_boarding.iloc[:][1:20] # remove column definitions
denied_boarding.columns = ['carrier', 
                           'num_passengers_denied_boarding_involuntarily_1a', 
                           'num_passengers_denied_boarding_involuntarily_1b', 
                           'num_passengers_denied_boarding_involuntarily_2a', 
                           'num_passengers_denied_boarding_involuntarily_2b',
                           'num_passengers_denied_boarding_involuntarily_2c',
                           'num_passengers_denied_boarding_involuntarily_total',
                           'num_passengers_denied_boarding_involuntarily_and_received_comp_total',
                           'num_passengers_voluntarily_gave_up_seat',
                           'total_boardings', 
                           'total_comp_paid_to_passengers_voluntarily_gave_up_seat']

""" 1.  Number of passengers who were denied boarding involuntarily from flights that were oversold, and:										
(a)  who qualified for denied boarding compensation within the meaning of § 250.5(a)(2) and 250.5(b)(2)										
(b) who qualified for denied boarding compensation within the meaning of § 250.5(a)(3) and 250.5(b)(3) 										
2.  Number of passengers denied boarding involuntarily from flights that were oversold, who did not qualify for denied boarding compensation due to:										
(a) The passenger does not comply fully with the carrier's contract of carriage or tariff provisions regarding ticketing, reconfirmation, check-in, and acceptability for transportation (see § 250.6(a)) 										
(b) substitution of aircraft of lesser capacity or due to weight/balance restrictions on an aircraft with a designed passenger capacity of 60 or fewer seats (see § 250.6(b))										
(c) The carrier arranges comparable air transportation or other transportation that is planned to arrive not later than 1 hour after the planned arrival time of the passenger's original flight or flights (see § 250.6(d))carriage										
3.  TOTAL NUMBER DENIED BOARDING INVOLUNTARILY										
4.  Number of passengers denied boarding involuntarily from an oversold flight who actually received compensation, regardless of the type of compensation (e.g., voucher, cash).										
5.  Number of passengers who voluntarily accepted a carrier’s offer to give up reserved space due to a potential oversale situation and did not travel on their original flight in exchange for a payment of the carrier’s choosing.										
6.  Total Boardings										
7.  Amount of compensation paid to passengers who voluntarily accepted a carrier’s offer to give up reserved space on an oversold flight that received cash or cash equivalent payment.										
"""
denied_boarding['year'] = 2021
denied_boarding['quarter'] = 1

delay_cause['quarter'] = (delay_cause['month']-1)//3 + 1

denied_and_delayed_flights_quarterly = delay_cause.merge(denied_boarding, on = ['year', 'quarter'], how = 'left')

fares_denied_and_delayed_flights_quarterly = denied_and_delayed_flights_quarterly.merge(fares, on = ['year', 'quarter'], how = 'left')

denied_and_delayed_flights_quarterly.to_csv('denied_and_delayed_flights_quarterly.csv')
flight_data_raw = pd.read_csv('raw_data\\Detailed_Statistics_Departures.csv')


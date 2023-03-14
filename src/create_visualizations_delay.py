# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 19:50:09 2023

@author: mdbla
"""

import pandas as pd
import plotly as p
import plotly.express as px 
import plotly.io as pio
import plotly.graph_objects as go
import numpy as np
pio.templates.default = "plotly_dark"

# We'll load in our Delay dataset

delays = pd.read_csv('..\\raw_data\\Airline_Delay_Cause_2003_2022.csv')

delays = delays[delays['airport'] == 'SEA']

# We'll add columns to our dataset that denote the percentages for each 
# cause of the delay

delays['carrier_cause'] = round((delays['carrier_ct']/delays['arr_del15'])*100, 4)
delays['weather_cause'] = round((delays['weather_ct']/delays['arr_del15'])*100, 4)
delays['nas_cause'] = round((delays['nas_ct']/delays['arr_del15'])*100, 4)
delays['security_cause'] = round((delays['security_ct']/delays['arr_del15'])*100, 4)
delays['late_aircraft_cause'] = round((delays['late_aircraft_ct']/delays['arr_del15'])*100, 4)
delays['perc_total_delays'] = round((delays['arr_del15']/delays['arr_flights']),4)



def create_delay_ranking():
    sea_delays = delays[delays['airport'] == 'SEA']
    test = sea_delays.sort_values(['carrier_name', 
                                   'perc_total_delays']).groupby('carrier_name').head()
    test = test.groupby(['carrier_name']).mean().reset_index()
    test['Delay Rank'] = test['perc_total_delays'].rank(ascending=False)
    test = test.loc[:, ['carrier_name', 'perc_total_delays', 
                        'Delay Rank']].sort_values('Delay Rank', ascending = True)
    test['perc_total_delays'] = round(test['perc_total_delays']*100,
                                 4)
    test = test.rename(columns = {'carrier_name' : 'Carrier', 
                              'perc_total_delays' : 'Percent of Total Delays (%)',
                             'Delay Rank' : 'Rank'})
    fig = go.Figure(data=[go.Table(
            header=dict(values=list(test.columns),
                        #fill_color='paleturquoise',
                        align='left'),
                        cells=dict(values=[test.Carrier,
                                           test['Percent of Total Delays (%)'], test.Rank],                                        
                        align='left')),
                        ])
    fig.update_layout(title='Ranking of Airline Carriers by Delay (2003 - 2022)')
    return(fig)

def create_delay_ct_breakdown():
    pie_delays = delays.drop(['arr_cancelled', 'arr_diverted',
                              'arr_delay', 'carrier_delay', 'weather_delay',
                              'nas_delay', 'security_delay', 'late_aircraft_delay',
                              'carrier_cause', 'weather_cause', 'nas_cause',
                              'security_cause', 'late_aircraft_cause', 'perc_total_delays'], axis=1)
    
    pie_delays = pie_delays.rename(columns = {'carrier_ct' : 'Air Carrier Delay',
                                              'weather_ct' : 'Weather Delay',
                                              'nas_ct' : 'National Aviation System Delay',
                                              'security_ct' : 'Security Delay',
                                              'late_aircraft_ct' : 'Aircraft Arriving Late'})
    
    delays_reshape = pd.melt(pie_delays,
                             id_vars = ['year'], 
                             value_vars=['Air Carrier Delay', 
                                         'Weather Delay', 'National Aviation System Delay',
                                         'Security Delay', 'Aircraft Arriving Late'])
    
    df = delays_reshape[['year',
                         'variable',
                         'value']].set_index(['year', 'variable'])['value']
    
    
    figs = {
            c: px.pie(df.loc[c].reset_index(), values="value", names="variable", 
                      labels = {'value':'Total Passengers', 
                                'variable':'Delay Cause'
                                },
                                title='Cause of Delay by Year',
                                color_discrete_sequence=px.colors.qualitative.Dark24).update_traces(
                                        name=c, visible=False, 
                                        )
            for c in df.index.get_level_values("year").unique()
            }
            
    # integrate figures per category into one figure
    defaultcat = df.index.get_level_values("year").unique()[0]
    fig = figs[defaultcat].update_traces(visible=True)
    for k in figs.keys():
        if k != defaultcat:
            fig.add_traces(figs[k].data)
            
    # finally build dropdown menu
    fig.update_layout(
            updatemenus=[
                    {
                            "buttons": [
                                    {
                                            "label": k,
                                            "method": "update",
                                            # list comprehension for which traces are visible
                                            "args": [{"visible": [kk == k for kk in figs.keys()]},
                                                                  {"title":go.layout.xaxis.Title(
                                                                          text=f"Cause of Delay by Year <br><sup>{k} </sup>"
                                                                          )}],
    }
    for k in figs.keys()
    ]}])
    
    return(fig)
    
    
def create_delay_min_breakdown():
    pie_delays = delays.drop(['arr_cancelled', 'arr_diverted',
                              'arr_del15', 'carrier_ct', 'weather_ct',
                              'nas_ct', 'security_ct', 'late_aircraft_ct',
                              'carrier_cause', 'weather_cause', 'nas_cause',
                              'security_cause', 'late_aircraft_cause', 'perc_total_delays'],
                                axis=1)
    
    pie_delays = pie_delays.rename(columns = {'carrier_delay' : 'Air Carrier Delay', 
                                              'weather_delay' : 'Weather Delay',
                                              'nas_delay' : 'National Aviation System Delay',
                                              'security_delay' : 'Security Delay',
                                              'late_aircraft_delay' : 'Aircraft Arriving Late'})
    
    delays_reshape = pd.melt(pie_delays,
                             id_vars = ['year'], 
                             value_vars=['Air Carrier Delay', 
                                         'Weather Delay', 'National Aviation System Delay',
                                         'Security Delay', 'Aircraft Arriving Late'])
    
    df = delays_reshape[['year',
                         'variable',
                         'value']].set_index(['year', 'variable'])['value']
    
    
    figs = {
            c: px.pie(df.loc[c].reset_index(), values="value", names="variable", 
                      labels = {'value':'Total Passengers', 
                                'variable':'Delay Cause'
                                },
                                title='Cause of Delay by Year (in minutes)',
                                color_discrete_sequence=px.colors.qualitative.Dark24).update_traces(
                                        name=c, visible=False, 
                                        )
            for c in df.index.get_level_values("year").unique()
            }
            
    # integrate figures per category into one figure
    defaultcat = df.index.get_level_values("year").unique()[0]
    fig = figs[defaultcat].update_traces(visible=True)
    for k in figs.keys():
        if k != defaultcat:
            fig.add_traces(figs[k].data)
            
    # finally build dropdown menu
    fig.update_layout(
            updatemenus=[
                    {
                            "buttons": [
                                    {
                                            "label": k,
                                            "method": "update",
                                            # list comprehension for which traces are visible
                                            "args": [{"visible": [kk == k for kk in figs.keys()]},
                                                                  {"title":go.layout.xaxis.Title(
                                                                          text=f"Cause of Delay by Year <br><sup>{k} </sup>"
                                                                          )}],
    }
    for k in figs.keys()
    ]}])
    
    return(fig)
    
    
def pct_delays_by_carrier():
    fig = px.bar(delays.sort_values('perc_total_delays', ascending=False),
                 x="carrier_name", y="perc_total_delays", 
                 labels={"carrier_name": "Airline Carrier",
                         "perc_total_delays":"Percent of Delays", 
                         },
                         title="Percentage of Delays by Carrier", 
                         color_discrete_sequence=px.colors.qualitative.Alphabet_r)
    
    fig.update_xaxes(tickangle = 45)
    
    return(fig)
    
    


    
    
    
    
    
    
                
                
                
                
                
                
                
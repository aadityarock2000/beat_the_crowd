# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 20:24:58 2023

@author: mdbla
"""

import pandas as pd
import plotly as p
import plotly.express as px 
import plotly.io as pio
import plotly.graph_objects as go
import numpy as np
pio.templates.default = "plotly_dark"

consumer_fares = pd.read_csv("..\\raw_data\\Consumer_Airfare_Report__Table_7_-_Fare_Premiums_for_Select_Cities_with_More_Than_20_Passengers_per_Day.csv")
consumer_fares = consumer_fares.drop(['tbl', 'tbl7pk'], axis = 1) # dropping unncessary columns from data source

# We'll subset the dataframe to look only at flights leaving Seattle
consumer_fares = consumer_fares[consumer_fares['cityname'] == 'Seattle, WA']

# We'll subset this dataframe further to only look at the year 2021
# consumer_fares = consumer_fares[consumer_fares['year'] == 2021]

# Renaming columns for more practical use and interpretation 
consumer_fares = consumer_fares.rename(columns={'SHAvgHubFare' : 'Short_haul_avg_fare',
                                                'LHAvgHubFare' : 'Long_haul_avg_fare',
                                                'TotalAvgHubFare' : 'Total_avg_hub_fare',
                                                'TotalPerPrem' : 'Total_percent_premium',
                                                'SHPerPrem' : 'Short_haul_percent_premium',
                                                'LHPerPrem' : 'Long_haul_percent_premium'})

consumer_fares['perc_sh_passengers'] = round((consumer_fares['SHPax']/consumer_fares['TotalFaredPax']), 4)
consumer_fares['perc_lh_passengers'] = round((consumer_fares['LHPax']/consumer_fares['TotalFaredPax']), 4)

def avg_lh_sh_fares():

    avg_fares = consumer_fares[consumer_fares['cityname'] == 'Seattle, WA']

    fig = px.bar(avg_fares.rename(columns = { "Short_haul_avg_fare":"Short Haul Average Fare",
                                                  'Long_haul_avg_fare':"Long Haul Average Fare"}),
    x="year", y=['Short Haul Average Fare', "Long Haul Average Fare"],
    labels={"year": "Year",
            "value":"Average Fare", 
            "variable":"Flight Fares"
            },
            title="Average Fare for Flights from Seattle by Year (1997 - 2022)", 
            color_discrete_sequence=px.colors.qualitative.Dark24)

    fig.update_xaxes(tickangle = 45)

    return(fig)
    
    
def prem_disc_by_year():

    prem_disc = consumer_fares[consumer_fares['cityname'] == 'Seattle, WA']

    fig = px.bar(prem_disc.rename(columns = { "Short_haul_percent_premium":"Short Haul Percent Discount",
                                             'Long_haul_percent_premium':"Long Haul Percent Discount"}), 
    x="year", y=['Short Haul Percent Discount',
                 "Long Haul Percent Discount"], 
                 labels={
                         "year": "Year",
                         "value":"Premium Discounts", 
                         "variable":"Type of Flight"
                         },
                         title="Premium Discounts for Flights from Seattle by Year (1997 - 2022)", 
                         color_discrete_sequence=px.colors.qualitative.Dark24)

    fig.update_xaxes(tickangle = 45)

    return(fig)
    
def avg_fare_by_city():

    figs = {c: px.area(consumer_fares[consumer_fares['cityname'] == c].rename(
            columns = {'Total_avg_hub_fare':"Average Fare Across All Flights"}),
    x="date", y="Average Fare Across All Flights",
    labels = {
            'value':'Percent of Passengers Flying',
            'variable':'Type of Flight'
            },
            title="Percent of Passengers Flying based on the Average Fare Price",
            color_discrete_sequence=px.colors.qualitative.Dark24).update_traces(
                    name=c, visible=False)
    for c in consumer_fares.cityname.unique()
    }
    
    defaultcat = consumer_fares.cityname.unique()[0]
    fig = figs[defaultcat].update_traces(visible=True)
    for k in figs.keys():
        if k != defaultcat:
            fig.add_traces(figs[k].data)
            
    # finally build dropdown menu
    fig.update_layout(
            updatemenus=[{"buttons": [{
                    "label": k,
                    "method": "update",
                    # list comprehension for which traces are visible
                    "args": [{"visible": [kk == k for kk in figs.keys()]},
                                          {"title":go.layout.xaxis.Title(
                                                  text=f"Percent of Passengers flying vs. Average Airfare Prices <br><sup>{k} </sup>"
                                                  )}],
    }for k in figs.keys()]}])
    
    return(fig)
    
def pct_by_avg_fare():
    # create a figure for each category
    figs = {
            c: px.area(consumer_fares[consumer_fares['year'] ==c].rename(
                    columns = {"perc_sh_passengers":"Short Haul","perc_lh_passengers":"Long Haul" }), 
    x="Total_avg_hub_fare", y=["Short Haul","Long Haul"], 
    labels={
            "Total_avg_hub_fare": "Fare",
            "value":"Percent of Passengers", 
            "variable":"Flight Type"
            },
            title="Percent of Passengers Denied Boarding from 1990 to 2021",
            color_discrete_sequence=px.colors.qualitative.Dark24)
    for c in consumer_fares.year.unique()
    }
    
    # integrate figures per category into one figure
    defaultcat = consumer_fares.year.unique()[0]
    fig = figs[defaultcat].update_traces(visible=True)
    for k in figs.keys():
        if k != defaultcat:
            fig.add_traces(figs[k].data)
            
    # finally build dropdown menu
    fig.update_layout(updatemenus=[dict(
            buttons = list([
                    {
                            "label": k,
                            "method": "update",
                            # list comprehension for which traces are visible
                            "args": [{"visible": [kk == k for kk in figs.keys()]},
                                                  {"title":go.layout.xaxis.Title(
                                                          text=f"Percent of Passengers Flying by Average Fare Price <br><sup>{k} </sup>"
                                                          )}],}
    for k in figs.keys()
    ]), x = 1)])
    
    return(fig)

    
    
    
    
    
    
    
    
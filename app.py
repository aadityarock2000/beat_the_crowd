import streamlit as st
import numpy as np
import pandas as pd
import datetime

st.set_page_config(
     page_title="Beat The Crowd",
     page_icon="📊",
     layout="centered")

st.title('SmoothFly: Analyzing Domestic US Airlines for a Stress-Free Travel Experience')

st.markdown("""
<img src="https://images.unsplash.com/photo-1610967510782-6a3764bbef99" width="100%">
""", unsafe_allow_html=True)

st.write(" ")

st.markdown("""

SmoothFly is a data-driven project that aims to help travelers avoid flight delays and cancellations, particularly during the Covid-19 pandemic. By analyzing data on airlines and routes, SmoothFly identifies the domestic US airlines with the highest likelihood of providing a smooth travel experience based on arrival/departure delay, denied boarding, and approximate travel fare.

In addition to providing analysis to individual travelers, SmoothFly builds a data pipeline that extracts raw data from the Bureau of Transportation Statistics and provides it to users in different file formats, enabling them to perform their own analysis.

With a focus on user experience, SmoothFly aims to alleviate the stress and uncertainty of air travel by providing actionable insights and data-driven recommendations.

""")

#dfferent tabs for different tasks
tab_titles=["ReadMe", "Get your Own Data - The Pipeline", "Analysis - Question 1",
            "Analysis - Question 2","Insights"]
tabs=st.tabs(tab_titles)

with tabs[0]:
    st.header('Introduction to the Tool')
    st.markdown("""
    This website consists of 2 parts.
    1. A broad analysis on the airport scenario and quick insights
    2. The pipeline - You can select your Arrival airport, Departure airport, date range among other options to get the list of all direct flights from the departure to the arrival airport with the selected parameters. You can use this to conduct your own further analysis.

    We give you the option to work on multiple fire formats like Excel, CSV and SQL Database.
    
    """)
with tabs[1]:
    st.title('Flight Search')
    st.write('Select your data of interest and the file format that you require')

    # Define the list of airports
    airports = ['New York (JFK)', 'Los Angeles (LAX)', 'Chicago (ORD)', 'Dallas (DFW)', 'Miami (MIA)', 'San Francisco (SFO)', 'Seattle (SEA)', 'Washington DC (IAD)']
    
    col1, col2= st.columns(2)

    with col1:
        # Create searchable dropdowns for the source airport and destination airport
        source_airport = st.selectbox('Source Airport', options=airports, index=0)
        from_date = st.date_input('From', datetime.date.today() + datetime.timedelta(days=365))

    with col2:
        # Create input fields for the date range
        destination_airport = st.selectbox('Destination Airport', options=airports, index=1)
        to_date = st.date_input('To', datetime.date.today())

    file_format=st.selectbox('File Format',options=['Excel', 'CSV', 'MS SQL DB'], index=0)


    dummy1, dummy2,dummy3=st.columns([4,5,1])
    with dummy2:
        if st.button('Search Flights'):
            # Process the user's inputs and display the results
            st.write('Processing your search...')

    
    





    # # Print the user's inputs
    # st.write('You entered:')
    # st.write(f'Source Airport: {source_airport}')
    # st.write(f'Destination Airport: {destination_airport}')

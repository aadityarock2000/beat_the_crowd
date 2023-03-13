'''
This is the application that can be used to interact with the analysis and the pipeline created.
'''
import datetime

import streamlit as st
import numpy as np
import pandas as pd
import sqlite3

from website_utils import departure_input_data, sql_parsing
import analysis.create_visualizations.denied_boarding as db_viz


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
tab_titles=["ReadMe", "Get your Own Data - The Pipeline", "Analysis"]
tabs=st.tabs(tab_titles)

#ANy information - ReadMe
with tabs[0]:
    st.header('Introduction to the Tool')
    st.markdown("""
    This website consists of 2 parts.
    1. A broad analysis on the airport scenario and quick insights
    2. The pipeline - You can select your Arrival airport, Departure airport, date range among other options to get the list of all direct flights from the departure to the arrival airport with the selected parameters. You can use this to conduct your own further analysis.

    We give you the option to work on multiple fire formats like Excel, CSV and SQL Database.
    
    """)

#Pipeline tabs
with tabs[1]:
    st.title('Flight Search')
    st.write('Select your data of interest and the file format that you require')

    # Define the list of airports
    airports=departure_input_data.airport_list()
    col1, col2= st.columns(2)

    with col1:
        # Create searchable dropdowns for the source airport and destination airport
        source_airport = st.multiselect('Source Airport', options=airports)
        from_date = st.date_input('From', datetime.date.today() + datetime.timedelta(days=365))
        carrier= st.multiselect('Airline Carrier',options=departure_input_data.carrier_list())
        

    with col2:
        # Create input fields for the date range
        destination_airport = st.multiselect('Destination Airport', options=airports)
        to_date = st.date_input('To', datetime.date.today())
        file_format=st.selectbox('File Format',options=departure_input_data.file_types(), index=0)


    dummy1, dummy2,dummy3=st.columns([4,5,1])
    with dummy2:
        if st.button('Search Flights'):
            st.write('Processing your search...')
            #send the data to a function to process
            inputs={'source_airport':source_airport,
                    'from_date':from_date,
                    'file_format':file_format,
                    'destination_airport':destination_airport,
                    'to_date':to_date,
                    'carrier':carrier
                    }
            parsed_inputs = sql_parsing.input_preparation(inputs=inputs)
            query,from_date,to_date,file_format=sql_parsing.create_query_string(parsed_inputs = parsed_inputs)
            print(query,from_date,to_date,file_format)
            cnxn=sql_parsing.connect_sql_server()
            print(cnxn)
            if file_format=='CSV':
                csv_string=sql_parsing.execute_code(cnxn,query,from_date,to_date,file_format)
                st.download_button(
                    label="Download CSV",
                    data=csv_string,
                    file_name="output.csv",
                    mime="text/csv"
                )
            elif file_format=='Excel':
                excel_file=sql_parsing.execute_code(cnxn,query,from_date,to_date,file_format)
                #create a download button for the user
                st.download_button(
                    label="Download Excel",
                    data=excel_file.getvalue(),
                    file_name="output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                df=sql_parsing.execute_code(cnxn,query,from_date,to_date,file_format)
                 # create an in-memory SQLite database
                sqlite_conn = sqlite3.connect(':memory:')

                # create a table in the database from the DataFrame
                df.to_sql(name='table_name', con=sqlite_conn, index=False)

                # allow user to download database file
                with sqlite_conn:
                    bytes = sqlite_conn.backup().read()
                    st.download_button(
                        label="Download SQL Database",
                        data=bytes,
                        file_name="output.db",
                        mime="application/octet-stream"
                    )


#Analysis tabs
with tabs[2]:
    st.title('Analysis')
    tab_titles=["Denied Boarding","Fares","Delays"]
    tabs=st.tabs(tab_titles)
    # with tabs[0]:
    #     fig1=db_viz.db_plot_perc_denied_over_time()
    #     fig2=db_viz.db_plot_perc_denied_by_carrier()
    #     fig3=db_viz.db_plot_total_denied_by_carrier()
    #     fig4=db_viz.db_plot_denial_type_by_carrier()
    #     fig5=db_viz.db_plot_denied_compensation_reason()
    #     fig6=db_viz.db_plot_comp_voluntary_by_carrier()

    #     st.plotly_chart(fig1,use_container_width=True)
    #     st.plotly_chart(fig2,use_container_width=True)
    #     st.plotly_chart(fig3,use_container_width=True)
    #     st.plotly_chart(fig4,use_container_width=True)
    #     st.plotly_chart(fig5,use_container_width=True)
    #     st.plotly_chart(fig6,use_container_width=True)




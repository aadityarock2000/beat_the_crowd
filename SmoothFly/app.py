'''
This is the application that can be used to interact with the analysis and the pipeline created.
'''
import datetime
import sqlite3

import streamlit as st
import pandas as pd


from website_utils import departure_input_data, sql_parsing
import analysis.create_visualizations.denied_boarding as db_viz
import analysis.create_visualizations.delays as delay_viz
import analysis.create_visualizations.fares as fares_viz


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
            query,from_date,to_date,file_format=sql_parsing.\
                                                create_query_string(parsed_inputs = parsed_inputs)
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
                    bytes1 = sqlite_conn.backup().read()
                    st.download_button(
                        label="Download SQL Database",
                        data=bytes1,
                        file_name="output.db",
                        mime="application/octet-stream"
                    )


#Analysis tabs
with tabs[2]:
    st.title('Analysis')
    tab_titles=["Denied Boarding","Fares","Delays"]
    tabs=st.tabs(tab_titles)
    with tabs[0]:
        fig1=db_viz.db_plot_perc_denied_over_time()
        fig2=db_viz.db_plot_perc_denied_by_carrier()
        fig3=db_viz.db_plot_total_denied_by_carrier()
        fig4=db_viz.db_plot_denial_type_by_carrier()
        fig5=db_viz.db_plot_denied_compensation_reason()
        fig6=db_viz.db_plot_comp_voluntary_by_carrier()

        st.write("""Being denied boarding can add stress and uncertainty to travel plans and the goal of this dashboard
 is to help you understand how you can be best prepared for these sorts of situations and hopefully, 
avoid them all together.""")

        st.write("""The Covid-19 pandemic caused a huge disruption to air travel as we knew it and led to a lot of 
uncertainty around bookings, fares, and more. To first understand how denied boarding was impacted 
by the pandemic, this visual shows the percent of denied boarding between 2018 and 2021. Denied 
boarding most often happens when a flight has been overbooked, which explains why we see the lowest 
point of this plot in the summer of 2020. Due to the increase in travel restrictions and the spread of 
covid-19, it is likely that very few flights were fully booked, which would mean denials would be 
unnecessary. We see this percentage start to climb following the summer of 2021, and the percentage 
continues to increase through the end of 2021. Another important piece of information that can be 
gleaned from this graph, is that denials have been largely volunatry, meaning passengers have offered
to give up their seat on a flight in exchange for some form of compensation.""")
        st.plotly_chart(fig1,use_container_width=True)

        st.write("""A possible factor in denied boarding is airline carrier. This plot shows the percentage of passengers
that were denied boarding from 2018-2021 by their carrier. From this we can see that Endeaver Air
had the highest percentage of denials; however, Envoy Air was the carrier that had the highest
percentage of involuntary denials.""")
        st.plotly_chart(fig2,use_container_width=True)

        st.write("""This next visualization shows the total passengers that flew with a given airline versus the total 
passengers that were denied boarding by that airline. From this we can see that both Delta and American
had a large number of passengers denied boarding between 2018-2021, while United and Southwest had 
a similar amount of total passengers, but significantly fewer denials.""")
        st.plotly_chart(fig3,use_container_width=True)

        st.write("""Knowing whether or not denied boardings were voluntary or involuntary can help to understand whether 
or not you may want to fly with a specific airline. Additionally, within involuntary denials, there are
instances of passengers receiving compensation and not receiving compensation, which might be an 
additional factor to consider when selecting a carrier. Take Allegiant Airlines for example, 
they may not have raised any red flags so far, but if you look at their denials, over 1/4 of 
passengers were involuntarily denied boarding and provided no compensation! Explore the figure below
to understand which airline carriers might provide a secure and stress free travel experience.""")
        st.plotly_chart(fig4,use_container_width=True)

        st.write("""When viewing the figure above, you can see which airlines are frequently involuntarily denying 
passengers and how often they are providing compensation when they do. It may also be helpful to 
understand why passengers were denied compensation in the case they were involuntarly denied boarding. 
This visualization shows the breakdown by carrier of the reason for denied compensation within these 
passengers. Explore the figure below to determine whether or not the reason for denied compensation
would be satisfactory for your travel needs.""")
        st.plotly_chart(fig5,use_container_width=True)

        st.write("""The final factor you might be interested in when considering the possibility of being denied boarding 
on your upcoming trip is the amount of compensation provided. The visualization below shows the 
total passengers who voluntarily gave up their seat on an airline versus the total compensation that 
they were provided. We can see that JetBlue airlines had the highest average compensation, with 
Virgin as a close second. Alternatively, Frontier, Hawaiian, and Horizon all had an average 
compensation of almost nothing.""")
        st.plotly_chart(fig6,use_container_width=True)

    with tabs[1]:
        fig1=fares_viz.avg_lh_sh_fares()
        fig2=fares_viz.prem_disc_by_year()
        fig3=fares_viz.avg_fare_by_city()
        fig4=fares_viz.pct_by_avg_fare()

        st.write("""Travelers often like to get a sense of how much fares cost when flying. 
                The goal of this dashboard is to help users understand the cost of flying.""")

        st.write("""Here is a bar plot showing the costs of long and short haul flights over time. As expected,
        long haul flights are on average more expensive than short haul flights, but this plot can help
        the user begin to conceptualize how much more expensive long haul flights are to short haul flights.""")
        st.plotly_chart(fig1,use_container_width=True)
        
        st.write("""Here is a bar plot showing the premium discounts of long and short haul flights over time. Usually they
        range from 0-5% every year, but in 2017 there was a significant discount offered for both long and short 
        haul flights. One factor that may have caused this were lower fuel costs that airlines experienced, which
        allowed for airlines to add flights that otherwise would have been unprofitable, which in turn lower costs.""")
        st.plotly_chart(fig2,use_container_width=True)
        
        st.write("""Here is an area plot showing the average fare for all flights departing from a city. The user can select
their city of choice using the dropdown menu and observe the trends in the average fare of flights from 
that city over time.""")
        st.plotly_chart(fig3,use_container_width=True)
        
        st.write("""Here is an area plot showing the percent of passengers flying long and short haul flight against the
average fare across all flights. The user can select for their year of interest with the dropdown menu
and observe the trends of people flying long and short haul flights.""")
        st.plotly_chart(fig4,use_container_width=True)

    with tabs[2]:
        fig1=delay_viz.create_delay_ranking()
        fig2=delay_viz.create_delay_ct_breakdown()
        fig3=delay_viz.create_delay_min_breakdown()
        fig4=delay_viz.pct_delays_by_carrier()


        st.write("""Having your flight delayed can certainly be an inconvenience for travelers. The goal
                of this dashboard is to observe the common causes of flights and the airlines that they affect.""")
        
        st.plotly_chart(fig1,use_container_width=True)
        st.write("""Here is a table of the airline carriers that experiences delays from 2003 - 2022.
                As you can see, each airline carrier is ranked by the proportion of delays they experience
                during this time period.""")
        
        st.plotly_chart(fig2,use_container_width=True)
        st.write("""Here is a pie chart breaking down the individual causes of delays for all flights during
                2003 - 2022. Users can use the dropdown menu to select for the years they would like to 
                view the pie chart.""")
        st.write("""Here is a pie chart breaking down the delay time for all delayed flights in minutes by
                each individual cause of delay. This pie chart serves to provide the user with a first look
                as to the severity each cause contributes to delayed flights per year.""")
        st.plotly_chart(fig3,use_container_width=True)
        
        st.write("""Here is a bar plot extending the ranked table shown previously. This shows the percent of total
                delays experienced by each carrier for the year the user wants to observe.""")
        st.plotly_chart(fig4,use_container_width=True)


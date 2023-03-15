[![Coverage Status](https://coveralls.io/repos/github/aadityarock2000/beat_the_crowd/badge.svg?branch=main)](https://coveralls.io/github/aadityarock2000/beat_the_crowd?branch=main)

# SmoothFly

## Project Type: 
Covid-19 led to an increase in delays, cancellations, and other disruptions to air travel which can add stress and uncertainty to traveling. The Bureau of Transportation Statistics (BTS) holds a wealth of information on flight history in the US, but the data is largely inaccessible and lacks interpretability. The aim of this project is to develop a user-friendly tool that will increase the accessibility of flight data to allow users to gain insights into future travel plans with their own analysis and to provide interpretable analysis of key factors that a user may consider when booking including fares, delays, and denied boarding. 

In addition to helping individual travelers, this project aims to contribute to the overall understanding of airline industry trends. By analyzing large sets of flight data, this tool will be able to identify patterns and correlations that can inform industry-wide decisions related to pricing, scheduling, and customer service. This information could be used to optimize airline operations, improve customer experiences, and enhance the overall efficiency of air travel.

To achieve these goals, this project will use a variety of data science techniques, including data cleaning, data visualization, and website scraping. The resulting tool will be designed to be user-friendly and accessible, with a simple interface that allows users to interact with the tool in two different ways. If they want to obtain a set of flight data to perform their own analysis then they will input their desired specifications and obtain a subset of data from BTS that has been collected and filtered to match their desired qualifications. Alternatively, if they want to understand how flight data can inform their future travel plans, they can select one of three possible variables of intrest: fares, denied boarding, or delays. From there they will be able to view a dashboard with visualizations focused on their selected factor. 

By providing valuable insights into airline industry trends and helping individuals make informed travel decisions, this project aims to contribute to a more efficient, effective, and enjoyable travel experience for all.

## Questions of Interest: 
* How can the accessability of data from BTS be improved so that users can easily access data from more than one airline or origin city? 
* What are the average flight prices for different routes, and how do they vary between short-haul and long-haul flights? 
* What is the likelihood of flight delays for different airlines and travel routes, and how does this vary by time of year?
* What type of delay is most likely for a given flight route or carrier? 
* What is the likelihood of being denied boarding by a given carrier? 
* In the case of a denied boarding, what is the likelihood the denial is voluntary and what sort of compensation can be expected? 

## Project Output Goal: 
The goal of this project will be to produce a tool that can be used to help a user optimize their travel plans to fit their needs. This tool will increase the accessibility of flight data from the BTS to allow users to gain insights into future travel plans with their own analysis by providing the ability to obtain collected data from more than one origin city and carrier. Additionally, it will provide interpretable analysis of key factors that a user may consider when booking air travel including fares, denied boardings, and delays to help users make informed decisions when booking air travel. 

## Data Sources: 
* https://www.transtats.bts.gov/ontime/departures.aspx: This dataset contains information on air traffic by day for a given origin airport. This data was used to create the data pipeline functionality so that filtered datsets can be queried when requested by a user. 
* https://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp: This dataset contains information on flight delays and their cause. It was used to create the visualizations on air traffic delays. 
* https://www.transportation.gov/policy/aviation-policy/domestic-airline-consumer-airfare-report: This dataset contains fair information for flight routes in the US and was used to create the visualizations on fares. 
* https://www.bts.gov/denied-confirmed-space: This dataset contains information on voluntary and involuntary denied boardings by carrier and was used to create the denied boarding visualizations.  


## Setting up the project:

**Prerequisites:**
The project needs the user to have Microsoft SQL server in their machine where they intend to host/run the website. 

**Steps:**
1. Clone the repository
2. In the root folder, run the following commands to set up the project. <br> 
Windows:<br> 
py -m pip install --upgrade build<br> 
py -m build<br> 
Unix/macOS:<br> 
python3 -m pip install --upgrade build<br> 
python3 -m build
3. In the root folder, run the command `conda env create -f environment.yaml` to install all the required dependencies
4. Execute `stremalit run app.py` in the SmoothFly folder to launch the website and look at the analysis
5. To create the SQL Database, look at the pipeline_example.ipynb file in the examples doc to create the database and connect to your machine.
6. In the sql_parsing.py file in `SmoothFly/website_utils` path, edit the `connect_sql_server()` method, by adding in your server name.
7. Rerun using `streamlit run app.py` to look at the updated website, with the functionality to access the pipeline.

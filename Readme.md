# Beat The Crowd!

## Project Type: 
The aim of this project is to develop a user-friendly tool that can help Seattle residents determine the optimal time to travel to a particular destination. The tool will utilize historical airline arrival and departure data to identify trends and patterns in flight schedules, pricing, and delays. By analyzing various factors such as time of year, day of week, and popular destinations, the tool will be able to provide personalized recommendations to users on the best time to travel to their desired location.

In addition to helping individual travelers, this project aims to contribute to the overall understanding of airline industry trends. By analyzing large sets of arrival and departure data, this tool will be able to identify patterns and correlations that can inform industry-wide decisions related to pricing, scheduling, and customer service. This information could be used to optimize airline operations, improve customer experiences, and enhance the overall efficiency of air travel.

To achieve these goals, this project will use a variety of data science techniques, including data cleaning, data visualization, machine learning, and predictive modeling. The resulting tool will be designed to be user-friendly and accessible, with a simple interface that allows users to input their desired destination and receive personalized travel recommendations. By providing valuable insights into airline industry trends and helping individuals make informed travel decisions, this project aims to contribute to a more efficient, effective, and enjoyable travel experience for all.

## Questions of Interest: 
* How busy will a specific travel destination be at some point in the future? 
* How busy will different travel destinations be during a given period of time? 
* What are the most popular travel destinations for Seattle residents, and how do they vary by time of year and day of the week?
* What are the average flight prices for different travel destinations, and how do they vary by time of year and day of the week?
* What is the likelihood of flight delays for different airlines and travel routes, and how does this vary by time of day, week, and year?
* What are the best times to book a flight to a particular destination, and how much can travelers save by booking at different times?
* How can travelers optimize their travel schedules to avoid peak travel times and reduce the risk of flight delays and cancellations?

## Project Output Goal: 
The goal of this project will be to produce a tool that can be used to help a user determine the best time to travel to a destination based on how busy it is predicted to be. This tool will be able to take in a destination from the user and produce a time series visualization of how busy the destination will be over time. Additionally, the tool will be able to take in a range of dates and produce a visualization of predicted busyness in different locations in a specific time frame. 

## Data Sources: 
* https://www.transtats.bts.gov/ontime/departures.aspx: This dataset contains information on air traffic by day for a given origin airport. For the purposes of this project, we will begin by restricting our data to have Sea-Tac as the origin airport. We will use this dataset to determine the volume of air traffic to different possible travel destinations throughout the year. 
* https://data.world/tylerudite/airports-airlines-and-routes/workspace/file?filename=airports.csv: This dataset contains information on airports that can be used to identify the closest airport to the location entered by the user. This will allow users to enter a city, country, etc. as a travel destination of interest. It can be joined with the flights dataset on the 3-letter airport code.  





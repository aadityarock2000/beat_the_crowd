# Beat The Crowd!

## Project Type: 
This project will produce a tool that can be used to help a Seattle resident determine the best time to travel to a specific destination. 

## Questions of Interest: 
* How busy will a specific travel destination be at some point in the future? 
* How busy will different travel destinations be during a given period of time? 

## Project Output Goal: 
The goal of this project will be to produce a tool that can be used to help a user determine the best time to travel to a destination based on how busy it is predicted to be. This tool will be able to take in a destination from the user and produce a time series visualization of how busy the destination will be over time. Additionally, the tool will be able to take in a range of dates and produce a visualization of predicted busyness in different locations in a specific time frame. 

## Data Sources: 
* https://www.transtats.bts.gov/ontime/departures.aspx: This dataset contains information on air traffic by day for a given origin airport. For the purposes of this project, we will begin by restricting our data to have Sea-Tac as the origin airport. We will use this dataset to determine the volume of air traffic to different possible travel destinations throughout the year. 
* https://data.world/tylerudite/airports-airlines-and-routes/workspace/file?filename=airports.csv: This dataset contains information on airports that can be used to identify the closest airport to the location entered by the user. This will allow users to enter a city, country, etc. as a travel destination of interest. It can be joined with the flights dataset on the 3-letter airport code.  





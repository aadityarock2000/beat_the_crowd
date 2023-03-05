import pandas as pd
import plotly.express as px 
import plotly.io as pio
import plotly.graph_objects as go
pio.templates.default = "plotly_dark"

denied_boarding = pd.read_csv("C:\\Users\\franc\\beat_the_crowd\\beat_the_crowd\\clean_data\\denied_boarding.csv")

# create a figure for each category
figs = {
    c: px.area(denied_boarding[denied_boarding['CARRIER'] ==c]
               .rename(columns = {'perc_denied_boarding_involuntary':"Involuntary", 
                                                 "perc_denied_boarding_voluntary":"Voluntary"}), 
              x="date", y=["Voluntary","Involuntary"], 
                labels={
                    "date": "Date",
                     "value":"Percent of Passengers Denied Boarding", 
                     "variable":"Denial Type"
                 },
                title="Percent of Passengers Denied Boarding from 1990 to 2021", color_discrete_sequence=px.colors.qualitative.Dark24)
    
    for c in denied_boarding.CARRIER.unique()
}

# integrate figures per category into one figure
defaultcat = denied_boarding.CARRIER.unique()[0]
fig = figs[defaultcat].update_traces(visible=True)
for k in figs.keys():
    if k != defaultcat:
        fig.add_traces(figs[k].data)
        
# finally build dropdown menu
fig.update_layout(
    updatemenus=[
        dict(
            buttons = list([
                {
                    "label": k,
                    "method": "update",
                    # list comprehension for which traces are visible
                    "args": [{"visible": [kk == k for kk in figs.keys()]},
                             {"title":go.layout.xaxis.Title(
            text=f"Percent of Passengers Denied Boarding from 2018 to 2021 by Airline <br><sup>{k} </sup>"
           )}],
                }
                for k in figs.keys()
            ]), 
        x = 1
        ),
    ]
)

fig.show()

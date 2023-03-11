import pandas as pd
import plotly.express as px 
import plotly.io as pio
import plotly.graph_objects as go
pio.templates.default = "plotly_dark"

def first_plot():
    denied_boarding = pd.read_csv("..\\clean_data\\denied_boarding.csv")

    denied_boarding_reshape = pd.melt(denied_boarding.rename(columns = {
    'num_passengers_denied_boarding_involuntarily_1':'Involuntary - Received Compensation', 
    'num_passengers_denied_boarding_involuntarily_2':'Involuntary - No Compensation', 
    'num_passengers_voluntarily_gave_up_seat':'Voluntary - Received Compensation'
    }), 
                                  id_vars = ['carrier', 'year', 'quarter'], 
                                  value_vars=['Involuntary - Received Compensation', 
                                              'Involuntary - No Compensation',
                                              'Voluntary - Received Compensation'
                                              ])

    df = denied_boarding_reshape[['carrier', 'variable','value']].set_index(['carrier', 'variable'])['value']
    
    # create a figure for each category
    figs = {
        c: px.pie(df.loc[c].reset_index(), values="value", names="variable", 
                  labels = {
                     'value':'Total Passengers', 
                     'variable':'Denial Type'
                 }, 
            color_discrete_sequence=px.colors.qualitative.Dark24).update_traces(
            name=c, visible=False, 
        )
        for c in df.index.get_level_values("carrier").unique()
    }
    
    # integrate figures per category into one figure
    defaultcat = df.index.get_level_values("carrier").unique()[0]
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
                text=f"Denied Boardings by Airline Carrier <br><sup>{k} </sup>"
                )}],
                    }
                    for k in figs.keys()
                ]
            }
        ]
    )

"""
Denied Boarding Visualizations: Creates denied boarding visualizations for website.
Functions
---------
db_plot_perc_denied_over_time: return plot of percent of passengers denied boarding over time.
db_plot_perc_denied_by_carrier: return plot of percent of passengers denied boarding by carrier.
db_plot_total_denied_by_carrier: return plot of total passengers and denials by carrier.
db_plot_denial_type_by_carrier: return pie chart of denial type by carrier. 
db_plot_denied_compensation_reason: return pie chart of reason for denied compensation by carrier.
db_plot_comp_voluntary_by_carrier: return plot of total compensation paid out by carrier.
"""
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
pio.templates.default = "plotly_dark"
denied_boarding = pd.read_csv("analysis\\clean_data\\denied_boarding.csv")

def db_plot_perc_denied_over_time():
    """
    Create plot of the percentage of passengers being denied boarding over time.
    Return Value
    ------------
    fig -- plot of percent of passengers denied boarding over time
    """
    fig = px.area(denied_boarding.groupby('date').mean(numeric_only = True).
                  reset_index().rename(columns = {'perc_denied_boarding_involuntary':"Involuntary",
                                                  "perc_denied_boarding_voluntary":"Voluntary"}),
              x="date", y=["Voluntary","Involuntary"],
                labels={
                    "date": "Year",
                     "value":"Percent of Passengers Denied Boarding", 
                     "variable":"Denial Type"
                 },
                title="Percent of Passengers Denied Boarding over Time",
                color_discrete_sequence=px.colors.qualitative.Dark24)
    fig.update_xaxes(tickangle = 45)
    return(fig) # pylint: disable=superfluous-parens

def db_plot_perc_denied_by_carrier():
    """
    Create plot of the percentage of passengers being denied boarding by carrier.
    Return Value
    ------------
    fig -- plot of percent of passengers denied boarding by carrier
    """
    fig = px.bar(denied_boarding.groupby('CARRIER').mean(numeric_only =True).
                 reset_index().sort_values("perc_denied_boarding", ascending=False).
             rename(columns = {
    "perc_denied_boarding_voluntary":"Voluntary",
    "perc_denied_boarding_involuntary":"Involuntary"
    }),
             x="CARRIER", y=["Voluntary",
                             "Involuntary"],
             labels = {
                 "CARRIER":"Airline Carrier", 
                 "variable":"Denial Type",
                 "value":"Percent of Passengers Denied Boarding"
             },
                title="Percentage of Passengers Denied Boarding by Airline Carrier",
                color_discrete_sequence=px.colors.qualitative.Dark24)
    fig.update_xaxes(tickangle = 45)
    return(fig) # pylint: disable=superfluous-parens

def db_plot_total_denied_by_carrier():
    """
    Create plot of the total passengers versus denials by carrier.
    Return Value
    ------------
    fig -- plot of total passengers and denials by carrier
    """
    fig = px.scatter(denied_boarding.groupby('CARRIER').sum(numeric_only=True).reset_index(),
                 x='6', y="total_denials",
	         size="perc_denied_boarding", color="CARRIER",
                 hover_name="CARRIER", log_x=True, size_max=60,
                 labels={
                     "6": "Total Boardings",
                     "total_denials": "Total Passengers Denied Boarding",
                     "CARRIER": "Airline",
                     "perc_denied_boarding":"Percent Denied Boarding"
                 },
                title="Denied Boarding by Airline Carrier",
                color_discrete_sequence=px.colors.qualitative.Dark24)
    return(fig) # pylint: disable=superfluous-parens

def db_plot_denial_type_by_carrier():
    """
    Create pie chart of the denial type, involuntary/voluntary and compensation, by carrier.
    Return Value
    ------------
    fig -- pie chart of denial type with drop down menu to select carrier
    """
    denied_boarding_reshape = pd.melt(denied_boarding.rename(columns = {
        '1':'Involuntary - Received Compensation', 
        '2':'Involuntary - No Compensation', 
        '5':'Voluntary - Received Compensation'
        }),
                                      id_vars = ['CARRIER', 'year', 'quarter'],
                                      value_vars=['Involuntary - Received Compensation',
                                                  'Involuntary - No Compensation',
                                                  'Voluntary - Received Compensation'
                                                  ])

    denied_boarding_reshape = denied_boarding_reshape[['CARRIER',
                                  'variable',
                                  'value']].set_index(['CARRIER', 'variable'])['value']

    figs = {
        c: px.pie(denied_boarding_reshape.loc[c].reset_index(), values="value", names="variable",
                  labels = {
                     'value':'Total Passengers', 
                     'variable':'Denial Type'
                 },
            color_discrete_sequence=px.colors.qualitative.Dark24).update_traces(
            name=c, visible=False,
        )
        for c in denied_boarding_reshape.index.get_level_values("CARRIER").unique()
    }

    defaultcat = denied_boarding_reshape.index.get_level_values("CARRIER").unique()[0]
    fig = figs[defaultcat].update_traces(visible=True)
    for k in figs.keys():
        if k != defaultcat:
            fig.add_traces(figs[k].data)

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

    return(fig) # pylint: disable=superfluous-parens

def db_plot_denied_compensation_reason():
    """
    Create pie chart of reason for denied compensation by carrier.
    Return Value
    ------------
    fig -- pie chart of reason for denied compensation with dropdown to select carrier
    """
    denied_boarding_reshape = pd.melt(denied_boarding[denied_boarding['2']>0],
                                  id_vars = ['CARRIER', 'year', 'quarter'],
                                  value_vars=['2(a)','2(b)','2(c)'])

    denied_boarding_reshape = denied_boarding_reshape[['CARRIER',
                                                       'variable',
                                                       'value']].set_index(['CARRIER', 
                                                                            'variable'])['value']

    figs = {
    c: px.pie(denied_boarding_reshape.loc[c].reset_index(), values="value", names="variable",
              labels = {
                 'value':'Total Passengers', 
                 'variable':'Denial Type'
             },  category_orders={"variable":['2(a)','2(b)','2(c)']},
        color_discrete_sequence=px.colors.qualitative.Dark24,
        title = "Involuntary Denials: Reason for Denied Compensation by Airline").update_traces(
        name=c, visible=False,
    )
    for c in denied_boarding_reshape.index.get_level_values("CARRIER").unique()
    }

    defaultcat = denied_boarding_reshape.index.get_level_values("CARRIER").unique()[0]
    fig = figs[defaultcat].update_traces(visible=True)
    for k in figs.keys():
        if k != defaultcat:
            fig.add_traces(figs[k].data)

            fig.add_annotation(text='2(a): Passenger did not comply fully with carrier contract',
                               y = 0, x = -.3,
                showarrow=False,
                font = {"size": 10},
                yshift=10)
            fig.add_annotation(
                text='2(b): Substitution of an aircraft of lesser capacity or due to weight/balance restrictions on an aircraft with a designed passenger capacity of 60 or fewer seats', # pylint: disable=line-too-long
                               y = -0.1, x = -.3,
                showarrow=False,
                font = {"size": 10},
                yshift=10)
            fig.add_annotation(
                text = "2(c): Carrier arranged comparable air tansfer arriving no later than 1 hour past passengers' original arrival time", # pylint: disable=line-too-long
                               y = -0.2, x = -.3,
                showarrow=False,
                font = {"size": 10},
                yshift=10)

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
            text=f"Reason for Denied Compensation by Airline <br><sup>{k} </sup>"
            )}],
                }
                for k in figs.keys()
            ]
        }
    ]
)
    return(fig) # pylint: disable=superfluous-parens

def db_plot_comp_voluntary_by_carrier():
    """
    Create plot of total compensation paid out versus denied passengers by carrier.
    Return Value
    ------------
    fig -- plot of total compensation paid out by carrier
    """
    fig = px.scatter(denied_boarding.groupby('CARRIER').mean(numeric_only=True).reset_index(),
                 x='5', y='7',size="cash_per_vol_denial", color="CARRIER",
                 hover_name="CARRIER", log_x=True, size_max=60,
                 labels={
                     "5": "Total Passengers",
                     "7": "Total Compensation",
                     "CARRIER": "Airline",
                     "cash_per_vol_denial":"Avg. Compensation"
                 },
                title="Compensation of Passengers who Voluntarily Gave up their Seat",
                color_discrete_sequence=px.colors.qualitative.Dark24)
    return(fig) # pylint: disable=superfluous-parens

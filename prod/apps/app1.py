import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from textwrap import dedent
import numpy as np
from app import app
from utils import world_dataset_aggregation
from utils import load_dataset


df = load_dataset.load_covid()
df = pd.concat((df, world_dataset_aggregation.generate(df)))
all_location = df.location.dropna().unique()

columns_names = {'total_cases': 'Cases' ,
                 'total_deaths': 'Deaths',
                 'stringency_index': 'Stringency'}

layout = html.Div([
    html.H1('Dash App Basics',
    ),

    dcc.Markdown("Message à afficher"
    ),

    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': i, 'value': i} for i in all_location],
        multi=True,
        value=['Global']
    ),
    dcc.Checklist(
        id="input-fields",
        options=[
            {'label': 'Total Cases', 'value': 'total_cases'},
            {'label': 'Total Deaths', 'value': 'total_deaths'},
            {'label': 'Stringency', 'value': 'stringency_index'}
            ],
        value=["total_cases"])  ,
    dcc.Graph(id='timeseries-graph')
])

@app.callback(
    dash.dependencies.Output('timeseries-graph', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value'),
     dash.dependencies.Input('input-fields', 'value')])
def update_graph(country_values, fields):
    print(country_values)
    dff = df.loc[df['location'].isin(country_values)]
    locations = dff.location.unique()
    toPlot = []
    for loc in locations:
        for col in fields:
            toPlot.append((loc,col))
    return {
        'data': [go.Scatter(
            x=dff[dff['location'] == location]['date'],
            y=dff[dff['location'] == location][column],
            text="location ",
            mode='lines',
            name=location+"-"+columns_names[column],
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for location, column in toPlot],
        'layout': go.Layout(
            title="{0} over time, in {1}".format(", ".join([columns_names[col]
                                                            for col in fields]),
                                                    ", ".join(locations)),
            xaxis={'title': 'date'},
            yaxis={'title': 'stringency_index'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }

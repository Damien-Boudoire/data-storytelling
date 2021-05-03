import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from textwrap import dedent
import numpy as np
from app import app
from dash.dependencies import Output, Input
from utils import world_dataset_aggregation
from utils import load_dataset

df = load_dataset.load_covid()
df = pd.concat((df, world_dataset_aggregation.generate(df)))
all_location = df.location.dropna().unique()

load_dataset.save_cases_and_deaths_on_pop(df)
label_cases='cases_pop'
label_deaths='deaths_pop'

last_date = df['date'].max()


countries = df['iso_code'].unique()

all_countries = []
for iso in countries:
    country_stat = df[df['iso_code']==iso]
    last_country_date = country_stat['date'].max()
    all_countries.append(country_stat[country_stat['date']==last_country_date][['iso_code', 'location', label_cases, label_deaths, 'stringency_index']])

mapData = pd.concat(all_countries)
mapData.set_index('iso_code', inplace=True, drop=True)
mapData.drop('WORLD', inplace=True)

columns_names = {label_cases: 'Cases' ,
                 label_deaths: 'Deaths',
                 'stringency_index': 'Stringency'}


layout = html.Div([
    dbc.Row( html.H2('Page Title')),

    dbc.Row(
        dbc.Col(
            dcc.Dropdown(
            id='select-country',
            options=[{'label': i, 'value': i} for i in all_location],
            multi=True,
            value=['Global']
        ),
        width=12    )),
    dbc.Row([
        dbc.Col(
            dcc.Checklist(
            id="input-fields",
            options=[
                {'label': columns_names[label_cases], 'value': label_cases},
                {'label': columns_names[label_deaths], 'value': label_deaths},
                {'label': 'Stringency', 'value': 'stringency_index'}
            ],
            value=[label_cases]),
            width = 1
            ),

            dbc.Col(
                dcc.Graph(id='pandemic-stats-graph'),
                width=11)
        ], id="row_graph1"),
    dbc.Row([
        dbc.Col(
            dcc.RadioItems(
                id='map-field',
                options=[
                    {'label': columns_names[label_cases], 'value': label_cases},
                    {'label': columns_names[label_deaths], 'value': label_deaths},
                    {'label': 'Stringency', 'value': 'stringency_index'}
                ],
                value=label_cases),
            width = 1
        ),
        dbc.Col(
            dcc.Graph(id='world-map'),
            width = 11
        )
    ], id="row_map1")

])

@app.callback(
        Output('select-country', 'value'),
        Output('world-map', 'clickData'),
        Input('world-map', 'clickData'),
        Input('select-country', 'value'))
def select_country(click, countries):
    if click is None:
        return countries, None
    #print(click)
    clicked = click['points'][0]['text']
    #print(clicked)
    countries.append(clicked)
    return countries, None

@app.callback(
    Output('pandemic-stats-graph', 'figure'),
    Output('world-map','figure'),
    [Input('select-country', 'value'),
     Input('input-fields', 'value'),
     Input('map-field', 'value')])
def update_graph(country_values, fields, map_field):
    dff = df.loc[df['location'].isin(country_values)]
    locations = dff.location.unique()
    plotAxis1 = []
    plotAxis2 = []
    for loc in locations:
        if label_cases in fields:
            for location in country_values:
                plotAxis1.append(go.Scatter(
                                    x=dff[dff['location'] == location]['date'],
                                    y=dff[dff['location'] == location][label_cases],
                                    text="location ",
                                    mode='lines',
                                    name=location+"-"+columns_names[label_cases],
                                    marker={
                                        'size': 15,
                                        'opacity': 0.5,
                                        'line': {'width': 0.5, 'color': 'white'}
                                        }
                                    )
                                )
        if label_deaths in fields:
            for location in country_values:
                plotAxis1.append(go.Scatter(
                                    x=dff[dff['location'] == location]['date'],
                                    y=dff[dff['location'] == location][label_deaths],
                                    text="location ",
                                    mode='lines',
                                    name=location+"-"+columns_names[label_deaths],
                                    marker={
                                        'size': 15,
                                        'opacity': 0.5,
                                        'line': {'width': 0.5, 'color': 'white'}
                                        }
                                    )
                                )
        if 'stringency_index' in fields:
            for location in country_values:
                plotAxis2.append(go.Scatter(
                                    x=dff[dff['location'] == location]['date'],
                                    y=dff[dff['location'] == location]['stringency_index'],
                                    yaxis='y2',
                                    text="location",
                                    mode='lines',
                                    name=location+"-"+columns_names['stringency_index'],
                                    marker={
                                        'size': 15,
                                        'opacity': 0.5,
                                        'line': {'width': 0.5, 'color': 'white'}
                                        }
                                    )
                                )

        graph = make_subplots(specs=[[{"secondary_y": True}]])
        for plot in plotAxis1:
            graph.add_trace(plot, secondary_y=False)
        for plot in plotAxis2:
            graph.add_trace(plot, secondary_y=True)

        graph.update_layout(
            title="{0} over time, in {1}".format(", ".join([columns_names[col]
                                                            for col in fields]),
                                                    ", ".join(locations)),
            xaxis={'title': 'date'},
            yaxis={'title': 'cases & deaths in % of the population'},
            yaxis2={'title': 'stringency index'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )


    worldMap = {
        'data': [go.Choropleth(
            locations=mapData.index,
            z=mapData[map_field],
            colorscale="Reds",
            text=mapData['location'])],
        'layout': go.Layout(
                title = "State of the World on {0}".format(last_date),
                margin=dict(l=60, r=60, t=50, b=50, autoexpand=True)
            )
            }

    return graph, worldMap

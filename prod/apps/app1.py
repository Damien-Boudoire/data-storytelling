import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from textwrap import dedent
import numpy as np
from app import app
from utils import world_dataset_aggregation
from utils import load_dataset


df = load_dataset.load_covid()
df = pd.concat((df, world_dataset_aggregation.generate(df)))
all_location = df.location.dropna().unique()


last_date = df['date'].max()

mapData = df[df['date']==last_date][['iso_code', 'location', 'total_cases', 'total_deaths']]
mapData.set_index('iso_code')
mapData.drop(mapData[mapData['iso_code']=='WORLD'].index)

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
    dcc.Graph(id='timeseries-graph'),
    dcc.Graph(id='world-map')

])

@app.callback(
    dash.dependencies.Output('timeseries-graph', 'figure'),
    dash.dependencies.Output('world-map','figure'),
    [dash.dependencies.Input('country-dropdown', 'value'),
     dash.dependencies.Input('input-fields', 'value')])
def update_graph(country_values, fields):
    dff = df.loc[df['location'].isin(country_values)]
    locations = dff.location.unique()
    plotAxis1 = []
    plotAxis2 = []
    for loc in locations:
        if 'total_cases' in fields:
            for location in country_values:
                plotAxis1.append(go.Scatter(
                                    x=dff[dff['location'] == location]['date'],
                                    y=dff[dff['location'] == location]['total_cases'],
                                    text="location ",
                                    mode='lines',
                                    name=location+"-"+columns_names['total_cases'],
                                    marker={
                                        'size': 15,
                                        'opacity': 0.5,
                                        'line': {'width': 0.5, 'color': 'white'}
                                        }
                                    )
                                )
        if 'total_deaths' in fields:
            for location in country_values:
                plotAxis1.append(go.Scatter(
                                    x=dff[dff['location'] == location]['date'],
                                    y=dff[dff['location'] == location]['total_deaths'],
                                    text="location ",
                                    mode='lines',
                                    name=location+"-"+columns_names['total_deaths'],
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

        print(plotAxis1)
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
            yaxis={'title': 'cases & deaths'},
            yaxis2={'title': 'stringency index'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )


    worldMap = {
        'data': [go.Choropleth(
            locations=['iso_code'],
            z=mapData['total_cases'],
            colorscale="Reds",
            text=mapData['location'])],
        'layout': go.Layout()
            }

    return graph, worldMap

import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from utils import load_dataset
from app import app


df = load_dataset.load_covid()
df = df.rename(index=str, columns={"location": "Country", "total_cases": "Total_cases",
                                   "date": "Date", "total_deaths": "Total_deaths",
                                   "stringency_index": "Stringency_index", "population": "Pop"})

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets =[dbc.themes.DARKLY])

all_location = df.Country.dropna().unique()

layout = html.Div([
        dbc.Row(dbc.Col(html.H1('Influence of restrictions on total deaths and cases of Covid-19', style={'text-align': 'center'}),
                        ),
                ),
        dbc.Row(dbc.Col(html.H5("Select at least two countries:"),
                        ),
                ),
        dbc.Row(dbc.Col(dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': i, 'value': i} for i in all_location],
            multi=True,
            value=['Afghanistan', "France"],
            clearable = False,
            style= { "hight": "100px",'color': '#212121', 'background-color': '#212121', "font-size":"24px"}
                                   ),
                        width={'size': 4, 'offset': 0},
                        ),
                ),
        dbc.Row(dbc.Col(dcc.Graph(id='timeseries-graph', figure={},
                   config={
                       'staticPlot': False,  # True, False
                       'scrollZoom': True,  # True, False
                       'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                       'showTips': True,  # True, False
                       'displayModeBar': True,  # True, False, 'hover'
                       'watermark': True,
                   }
                                ),
            width={'size': 6, 'offset': 3},
                        ),
                ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="pie-graph", figure={}),
                        width=8, lg={'size': 3,  "offset": 2, 'order': 'first'}
                        ),
                dbc.Col(dcc.Graph(id="pie-graph1", figure={}),
                        width=4, lg={'size': 3,  "offset": 2, 'order': 'last'}
                        ),
            ]
                )
])

@app.callback(
    Output('timeseries-graph', 'figure'),
    [Input('country-dropdown', 'value')])
def update_graph(country_values):
    dff = df.loc[df['Country'].isin(country_values)]
    fig = px.line(dff, x='Date', y='Stringency_index', color='Country',
                  custom_data=['Country', 'Total_cases', 'Total_deaths', "Pop"])
    fig.update_traces(mode='lines+markers')
    fig.update_layout(plot_bgcolor= 'rgb(17,17,17)', paper_bgcolor ='#3E4449', font_color="white", font_size= 16)
    return fig


@app.callback(
    Output("pie-graph", "figure"),
    [Input("timeseries-graph", "hoverData"),
     Input("country-dropdown", "value")])
def generate_chart(hov_data, country_values):
    if hov_data is None:
        dff1 = df[df.Country.isin(country_values)]
        dff1 = dff1[dff1.Date == "2020-10-11"]
        fig1 = px.pie(dff1, values="Total_cases", names="Country", color='Country')
        fig1.update_layout(plot_bgcolor='rgb(17,17,17)', paper_bgcolor ='#3E4449', font_color="white")
        return fig1
    else:
        print(f'hover data: {hov_data}')
        dff1 = df[df.Country.isin(country_values)]
        hov_date = hov_data['points'][0]['x']
        dff1 = dff1[dff1.Date == hov_date]
        fig2 = px.pie(dff1, values='Total_cases', names='Country', color='Country', title=f'Total cases: {hov_date}')
        fig2.update_layout(plot_bgcolor='rgb(17,17,17)', paper_bgcolor ='#3E4449', font_color="white")
        return fig2

@app.callback(
    Output("pie-graph1", "figure"),
    [Input("timeseries-graph", "hoverData"),
     Input("country-dropdown", "value")])
def generate_chart(hov_data, country_values):
    if hov_data is None:
        dff1 = df[df.Country.isin(country_values)]
        dff1 = dff1[dff1.Date == "2020-10-11"]
        fig1 = px.pie(dff1, values="Total_deaths", names="Country", color='Country')
        fig1.update_layout(plot_bgcolor='rgb(17,17,17)', paper_bgcolor ='#3E4449', font_color="white")
        return fig1
    else:
        print(f'hover data: {hov_data}')
        dff1 = df[df.Country.isin(country_values)]
        hov_date = hov_data['points'][0]['x']
        dff1 = dff1[dff1.Date == hov_date]
        fig2 = px.pie(dff1, values='Total_deaths', names='Country', color='Country', title=f'Total deaths: {hov_date}')
        fig2.update_layout(plot_bgcolor='rgb(17,17,17)', paper_bgcolor ='#3E4449', font_color="white")
        return fig2

import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc



df = pd.read_csv("data_transformed.csv")
df = df.rename(index=str, columns={"location": "Country", "total_cases": "Total_cases",
                                   "date": "Date", "total_deaths": "Total_deaths",
                                   "stringency_index": "Stringency_index", "population": "Pop"})

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

all_location = df.Country.dropna().unique()

app.layout = html.Div([
    html.H1('Influence of restrictions on total deaths and cases of Covid-19'),

    dcc.Markdown("Select two countries"),

    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': i, 'value': i} for i in all_location],
        multi=True,
        value=['Afghanistan', "France"],
        clearable = False
    ),

    html.Div([
        dcc.Graph(id='timeseries-graph', figure={},
                  config={
                      'staticPlot': False,  # True, False
                      'scrollZoom': True,  # True, False
                      'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                      'showTips': True,  # True, False
                      'displayModeBar': True,  # True, False, 'hover'
                      'watermark': True,
                  }, className = "row"),
        html.Div([
            dcc.Graph(id="pie-graph", figure={}, className = "six columns"),
            dcc.Graph(id="pie-graph1", figure={}, className = "six columns")
        ], className = "row"),
        ])
])

@app.callback(
    Output('timeseries-graph', 'figure'),
    [Input('country-dropdown', 'value')])
def update_graph(country_values):
    dff = df.loc[df['Country'].isin(country_values)]
    fig = px.line(dff, x='Date', y='Stringency_index', color='Country',
                  custom_data=['Country', 'Total_cases', 'Total_deaths', "Pop"])
    fig.update_traces(mode='lines+markers')
    return fig


@app.callback(
    Output("pie-graph", "figure"),
    [Input("timeseries-graph", "hoverData"),
     #Input("timeseries-graph", "clickData"),
     #Input("timeseries-graph", "selectedData"),
     Input("country-dropdown", "value")])
def generate_chart(hov_data, country_values):
    if hov_data is None:
        dff1 = df[df.Country.isin(country_values)]
        dff1 = dff1[dff1.Date == "2020-10-11"]
        fig1 = px.pie(dff1, values="Total_cases", names="Country", color='Country')
        return fig1
    else:
        print(f'hover data: {hov_data}')
        dff1 = df[df.Country.isin(country_values)]
        hov_date = hov_data['points'][0]['x']
        dff1 = dff1[dff1.Date == hov_date]
        fig2 = px.pie(dff1, values='Total_cases', names='Country', color='Country', title=f'Total cases: {hov_date}')
        return fig2

@app.callback(
    Output("pie-graph1", "figure"),
    [Input("timeseries-graph", "hoverData"),
     #Input("timeseries-graph", "clickData"),
     #Input("timeseries-graph", "selectedData"),
     Input("country-dropdown", "value")])
def generate_chart(hov_data, country_values):
    if hov_data is None:
        dff1 = df[df.Country.isin(country_values)]
        dff1 = dff1[dff1.Date == "2020-10-11"]
        fig1 = px.pie(dff1, values="Total_deaths", names="Country", color='Country')
        return fig1
    else:
        print(f'hover data: {hov_data}')
        dff1 = df[df.Country.isin(country_values)]
        hov_date = hov_data['points'][0]['x']
        dff1 = dff1[dff1.Date == hov_date]
        fig2 = px.pie(dff1, values='Total_deaths', names='Country', color='Country', title=f'Total deaths: {hov_date}')
        return fig2

if __name__ == '__main__':
    app.run_server(debug=True)


# return {
#         'data': [go.Scatter(
#             x=dff[dff['location'] == location]['date'],
#             y=dff[dff['location'] == location]['stringency_index'],
#             text="location ",
#             mode='lines',
#             name=location,
#             marker={
#                 'size': 15,
#                 'opacity': 0.5,
#                 'line': {'width': 0.5, 'color': 'white'},
#            customdata = ['location', 'total_cases', 'total_deaths', "population"]
#             }
#         ) for location in dff.location.unique()],
#         'layout': go.Layout(
#             title="STI over time, by country",
#             xaxis={'title': 'Date'},
#             yaxis={'title': 'Indice des restrictions'},
#             margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
#             hovermode='closest'
#         )
#     }
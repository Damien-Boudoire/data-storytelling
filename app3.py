import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from textwrap import dedent
import numpy as np

# Gapminder dataset GAPMINDER.ORG, CC-BY LICENSE
#url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
df = pd.read_csv("data/data_transformed.csv") #pd.read_csv(url)
# df = df.rename(index=str, columns={"pop": "population",
#                                    "lifeExp": "life_expectancy",
#                                    "gdpPercap": "GDP_per_capita"})


# Dash app
app = dash.Dash()
# app.css.append_css({
#     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
# })

all_location = df.location.dropna().unique()

app.layout = html.Div([
    html.H1('Dash App Basics',
    ),

    dcc.Markdown("Message à afficher"
    ),

    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': i, 'value': i} for i in all_location],
        multi=True,
        value=['Afghanistan']
    ),

    dcc.Graph(id='timeseries-graph')

])

@app.callback(
    dash.dependencies.Output('timeseries-graph', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_graph(country_values):
    dff = df.loc[df['location'].isin(country_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['location'] == location]['date'],
            y=dff[dff['location'] == location]['total_cases'],
            text="location",
            mode='lines',
            name=location,
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for location in dff.location.unique()],
        'layout': go.Layout(
            title="Total cases over time, by country",
            xaxis={'title': 'date'},
            yaxis={'title': 'Total Cases'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)

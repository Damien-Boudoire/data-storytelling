import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graphic_objs as go

from app import app

colors = json.load(open("data/crayola.json"))["data"]

covid_data = pd.read_csv("./data/covidImpact.csv")
#data_country = [country for country in covid_data.loc["COUNTRY"]]

print(covid_data.describe())
print(covid_data.columns)

c_d_by_tc = covid_data.loc[:,["COUNTRY", "DATE", "TC"]]
c_d_by_tc["TC"] = c_d_by_tc["TC"].str.replace(",", ".")
c_d_by_tc["TC"]  = pd.to_numeric(c_d_by_tc["TC"])
top_c_by_tc = c_d_by_tc.groupby(["COUNTRY"]).sum().sort_values("TC", ascending=False)[:10]

print(top_c_by_tc)

hist_cases = go.Bar( x = top_c_by_tc.index, y = top_c_by_tc.values)
fig = dict(title= 'Cas Covid pour les 10 pays les plus touchés',
              xaxis = dict(title = 'dates',ticklen = 5,zeroline= False))


layout = html.Div([
    html.H3('App 1'),
    dcc.Graph(
        id="c_d_by_tc",
        figure={
            'data' : [go.Bar( x = top_c_by_tc.index, y = top_c_by_tc.values)]
            'layout': go.layout()
        }
    )
])


@app.callback(
    Output('app-1-display-value', 'children'),
    Input('app-1-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)

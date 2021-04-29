# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 11:36:18 2021

@author: meksi
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import app1, app2

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link("Page d'accueil", href='/apps/app1'),
        dcc.Link("Page d'accueil", href='/apps/app2'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    else:
        return "Welcome! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)

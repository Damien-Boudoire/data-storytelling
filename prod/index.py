# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 11:36:18 2021

@author: meksi
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import app1, app2
import home

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dbc.Nav([
            dbc.NavLink("Home", href='/home'),
            dbc.NavLink("Page 1", href='/apps/app1'),
            dbc.NavLink("Page 2", href='/apps/app2'),
        ]),
        html.H1("Main Title")
    ]),

    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return home.layout
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    else:
        return dcc.Location(pathname="/home", id="redirect")
                #"Welcome! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True)

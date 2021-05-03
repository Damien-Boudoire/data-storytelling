# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 11:36:53 2021

@author: meksi
"""

import dash
import dash_bootstrap_components as dbc

# meta_tags are required for the app layout to be mobile responsive
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets =[dbc.themes.DARKLY])
app = dash.Dash(__name__, external_stylesheets =[dbc.themes.DARKLY], suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

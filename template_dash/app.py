# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 11:36:53 2021

@author: meksi
"""

import dash

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server
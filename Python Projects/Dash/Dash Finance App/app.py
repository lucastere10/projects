#---------------------------------------------
### LIBS ###
from contextlib import nullcontext
from turtle import ht, width
import dash  #pip install dash
from dash import html, dcc, Output, Input, State, dash_table, callback                    
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import dash_daq as daq                     # pip install dash_daq
from dash.exceptions import PreventUpdate
import pandas as pd 
import requests
from pages import contact, home, overview, not_found_404

app = dash.Dash(__name__, use_pages=True, 
                external_stylesheets= [dbc.themes.LUX, dbc.icons.FONT_AWESOME],
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return contact.layout
    else:
        return not_found_404.layout

if __name__ == '__main__':
    app.run_server(debug=True)
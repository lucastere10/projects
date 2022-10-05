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
from pages import contact
from pages.create_card import create_card

app = dash.Dash(__name__, use_pages=True, 
                external_stylesheets= [dbc.themes.LUX, dbc.icons.FONT_AWESOME],
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

app.layout = html.Div([
    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),
    dash.page_container 
])

if __name__ == '__main__':
    app.run_server(debug=True)
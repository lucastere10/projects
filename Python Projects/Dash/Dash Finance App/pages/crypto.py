import dash  #pip install dash
from dash import html, dcc, Output, Input, State                              
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components

dash.register_page(__name__, path = '/crypto')

layout = html.Div(children=[
    html.H1(children='This is our crypto page'),
    html.Div(children='''
        This is our crypto page content.
    '''),
])
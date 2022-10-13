import dash  #pip install dash
from dash import html, dcc, Output, Input, State                              
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components

dash.register_page(__name__, path = '/portfolio')

layout = html.Div(children=[
    html.H1(children='This is our portfolio page'),
    html.Div(children='''
        This is our portfolio page content.
    '''),
])
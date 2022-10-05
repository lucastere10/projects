import dash  #pip install dash
from dash import html, dcc, Output, Input, State                              
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import dash_daq as daq                     # pip install dash_daq

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1(children='This is our Contact page'),

    html.Div(children='''
        This is our Contact page content.
    '''),

])
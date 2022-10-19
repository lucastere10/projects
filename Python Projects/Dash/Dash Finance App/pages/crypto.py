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

#---------------------------------------------
### LIBS ###
import sys
from turtle import ht, width
import dash  #pip install dash
from dash import html, dcc, Output, Input, State, dash_table, callback        
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import dash_daq as daq                     # pip install dash_daq
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#import sys path
sys.path.insert(0,'Python Projects\Dash\Dash Finance App')
from modules import module_cards, module_sidebar
from styles import app_styles
nasdaq = module_sidebar.nasdaq
crypto = module_sidebar.crypto

dash.register_page(__name__, path = '/crypto')

# LAYOUT --------------
layout = html.Div([
    #chart grid
    dcc.Interval(
        id='crypto-interval-component-id',
        interval=1*300000, # in milliseconds
        n_intervals=0
    ),
    html.Br(),
    #dbc.Row(dbc.Col(dbc.Button('GET DATA',id = 'chart-button-id'), width = 2)),
    #html.Br(),
    dbc.Row([
        dbc.Col(id='crypto-chart1-id'),
        dbc.Col(id='crypto-chart2-id'),
        dbc.Col(id='crypto-chart3-id'),
    ]),
    html.Br(),
    dbc.Row([
        dcc.Loading(
            id="crypto-loading-id", type="default", color = '#1a1a1a',
            children=html.Div(id="crypto-loading-output-id"),
        ),
    ]),
], id = 'crypto-layout-id')

### CALLBACKS ### ------------------------------------------------------------------

#load crypto-charts
@callback(
    Output('crypto-loading-output-id','children'),
    Output('crypto-chart1-id','children'),    
    Output('crypto-chart2-id','children'),
    Output('crypto-chart3-id','children'),
    Input('crypto-interval-component-id', 'n_intervals')   
)
def get_cards(x):
    return [{},
            module_cards.create_crypto_card('BTC'), 
            module_cards.create_crypto_card('ETH'), 
            module_cards.create_crypto_card('DOGE'),
            ]
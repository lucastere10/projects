#---------------------------------------------
### LIBS ###
from turtle import ht, width
import dash  #pip install dash
from dash import html, dcc, Output, Input, State                              
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import dash_daq as daq                     # pip install dash_daq
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from create_card import create_card

# APP --------------
app = dash.Dash(__name__, external_stylesheets= [dbc.themes.FLATLY, dbc.icons.FONT_AWESOME],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

### STYLES ### ------------------------------------------------------------------
# Sidebar Style ------------
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#f8f9fa",
}
SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 0,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}
# Content Style ------------
CONTENT_STYLE = {
    "margin-left": "15rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# Sidebar ------------------------------
sidebar = html.Div([
        html.H6("GRID", className="display-4"),
        html.Hr(),#fa-solid fa-user
        dbc.Nav([
                dbc.NavLink([html.I(className = "fa-solid fa-house"), "  Home"], href="/", active="exact"),                
                html.Hr(),
                dbc.NavLink([html.I(className = "fa-solid fa-chart-bar"), "  Stocks"], href="/stocks", active="exact"),
                dbc.NavLink([html.I(className = "fa-solid fa-coins"), "  Crypto"], href="/crypto", active="exact"),
                dbc.NavLink([html.I(className = "fa-solid fa-eye"), "  Watchlist"], href="/watchlist", active="exact"),
                html.Hr(),
                dbc.NavLink([html.I(className = "fa-solid fa-circle-question"), "  Discover"], href="/discover", active="exact"),
                dbc.NavLink([html.I(className = "fa-solid fa-solid fa-money-bill-trend-up"), "  Trade Markets"], href="/markets", active="exact"),
                html.Hr(),
                dbc.NavLink([html.I(className = "fa-solid fa-user"), "  My Portfolio"], href="/portfolio", active="exact"),
                dbc.NavLink([html.I(className = "fa-solid fa-envelope"), "  Contact"], href="/contact", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),            
    ], style=SIDEBAR_STYLE,  id="sidebar",
)


app.layout = dbc.Container([
    #chart grid
    dbc.Row([ #first row, title.
        html.H6('TITLE')
    ]),
    dbc.Row([
        dbc.Col([html.Div(create_card('PBR', 'Petrobrás'))]),
        dbc.Col([html.Div(create_card('BRT', 'Veículos RJ'))]),
        dbc.Col([html.Div(create_card('TSL', 'Tesla Motors'))]),
    ]),
    html.Div(sidebar),
], style = CONTENT_STYLE)

if __name__=='__main__':
    app.run_server(debug=True, port=3000)
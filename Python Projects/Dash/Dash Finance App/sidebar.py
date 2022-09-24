from dash import dcc, html, State, Input, Output
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import dash_daq as daq                     # pip install dash_daq
import pandas as pd

nasdaq = pd.read_csv('Python Projects\\Dash\\Dash Finance App\\data\\nasdaq.csv')

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
    "padding": "0.5rem 1rem", #"padding": "4rem 1rem 2rem",
    "background-color": "#f8f9fa",
}
SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 0,
    "left": "-14rem",
    "bottom": 0,
    "width": "14rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}       

# Sidebar ------------------------------
sidebar = html.Div([
            dbc.Row([
                dbc.Col([
                    html.H6("LOGO", className="display-4", style={'fontSize': '2rem'})
                ], align = 'center'),
                dbc.Col([
                    dbc.Button(html.I(
                    className = "fa-solid fa-angles-right"),
                    outline=True, 
                    color="secondary", 
                    className="mr-1", 
                    id="btn_sidebar"
                    ),
                ], align = 'center'),
            ], justify = 'start'),
        html.Hr(),
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
                daq.ToggleSwitch(id='my-toggle-switch',value=False),
            ],
            vertical=True,
            pills=True,
        ),            
    ], style=SIDEBAR_STYLE,  id="sidebar",
)

# navbar -------------
search_bar = dbc.Row([
    dbc.Col([
            dbc.Button([html.I(className = "fa-solid fa-filter")],
            color="secondary", className="ms-2", n_clicks=0,  style={'font-size': '12px', 'display': 'inline-block'},
            ),
    ], width = 'auto'),
    dbc.Col([
        dcc.Dropdown(nasdaq["Name"].values.tolist(), 
        id = 'search_stock_dropdown'
        ),
    ]),
    dbc.Col([
        dbc.Button([html.I(className = "fa-solid fa-magnifying-glass")],
        color="primary", className="ms-2", n_clicks=0, id = 'search_stock_button'
        ) 
    ], width="auto"),
])

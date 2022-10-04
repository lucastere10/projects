from operator import xor
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
                ],align = 'end'),
                dbc.Col([
                    dbc.Button(html.I(
                    className = "fa-solid fa-angles-right"),
                    outline=True, 
                    color="secondary", 
                    className="mr-1", 
                    id="btn_sidebar",
                    size="sm"
                    ),
                ]),
            ], justify = 'start'),
        html.Hr(),
        dbc.Nav([
                dbc.NavLink([html.I(className = "fa-solid fa-house"), "  Home"], href="/", active="exact"),                
                html.Hr(),
                dbc.NavLink([html.I(className = "fa-solid fa-chart-bar"), "  Stocks"], href="/stocks", active="exact"),
                dbc.NavLink([html.I(className = "fa-solid fa-coins"), "  Crypto"], href="/crypto", active="exact"),
                html.Hr(),
                dbc.NavLink([html.I(className = "fa-solid fa-circle-question"), "  Overview"], href="/overview", active="exact"),
                dbc.NavLink([html.I(className = "fa-solid fa-solid fa-money-bill-trend-up"), "  Trade Markets"], href="/markets", active="exact"),
                html.Hr(),
                dbc.NavLink([html.I(className = "fa-solid fa-user"), "  My Portfolio"], href="/portfolio", active="exact"),
                dbc.NavLink([html.I(className = "fa-solid fa-envelope"), "  Contact"], href="/contact", active="exact"),
                html.Hr(),
                daq.ToggleSwitch(id='my-toggle-switch',value=False),
            ],
            vertical=True,
            pills=True,
        ),            
    ], style=SIDEBAR_STYLE,  id="sidebar",
)

# navbar -------------
filter = html.Div(
    [
        dbc.Button([html.I(className = "fa-solid fa-filter")],
            color="primary", className="ms-2", n_clicks=0,  
            style={'font-size': '12px', 'display': 'inline-block'},
            id = 'filter-button-id', size="sm"
            ),
        dbc.Offcanvas([
            html.P(
                "This is the content of the Offcanvas. "
                "Close it by clicking on the close button, or "
                "the backdrop. Country/Sector/Industry" 
            ), html.Hr(),
            dcc.Dropdown(nasdaq['Country'].unique(), multi=True, id='offcanvas-filder-country-id'), html.Br(),
            dcc.Dropdown(nasdaq['Sector'].unique(), multi=True, id='offcanvas-filder-sector-id'), html.Br(),
            dcc.Dropdown(nasdaq['Industry'].unique(), multi=True, id='offcanvas-filder-industry-id'), html.Br(),
            dbc.Button([html.I(className = "fa-solid fa-filter"),' ','Add Filters'],
                color="primary", className="ms-2", n_clicks=0,  
                style={'font-size': '13px', 'display': 'inline-block'},
                id = 'add-filters-button-id'
                ),
        ],
        id="filter_offcanvas-id",
        title="Filters",
        is_open=False,
        ),
    ]
)

search_bar = dbc.Row([
    dbc.Col([filter], width = 'auto'),
    dbc.Col([
        dcc.Dropdown(nasdaq['Name'].unique(), id = 'search-stock-dropdown-id'),
    ])
])
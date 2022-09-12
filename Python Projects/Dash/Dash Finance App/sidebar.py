from dash import dcc, html, State, Input, Output
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components

# card ---------------
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

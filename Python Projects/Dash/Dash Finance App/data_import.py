#---------------------------------------------
### LIBS ###
from tracemalloc import stop
from turtle import ht, width
import dash  #pip install dash
from dash import html, dcc, Output, Input, State                              
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import dash_daq as daq                     # pip install dash_daq
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from alpha_vantage.timeseries import TimeSeries # pip install alpha-vantage

# DATA -------------------------------------------------------------------------
### Set up initial key and financial category ###
key = '1D0MB8E05Q6QOL2L' #Alpha API Key
ts = TimeSeries(key, output_format='pandas') # 'pandas' or 'json' or 'csv'
stock_symbol = "PBR"
nasdaq = pd.read_csv('Python Projects\\Dash\\Dash Finance App\\data\\nasdaq.csv')
ttm_data, ttm_meta_data = ts.get_intraday(symbol = stock_symbol,interval='1min', outputsize='compact')
df = ttm_data.reset_index()
# ------------------------------------------------------------------------------

# APP ------------
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
    "width": "16rem",
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
    "transition": "margin-left .5s",
    "margin-left": "17rem",
    "margin-right": "2rem",
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
# -------------------------------------------------------------------------------

# Sidebar ------------
sidebar = html.Div([
        html.H6("LOGO", className="display-4"),
        dbc.Button(html.I(
            className = "fa-solid fa-angles-right"),
            outline=True, 
            color="secondary", 
            className="mr-1", 
            id="btn_sidebar"
        ),
        html.I(className = "fa-solid fa-angles-right"),
        html.I(className = "fa-solid fa-angles-left"),
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
# content ------------
content = html.Div(id="page-content", style=CONTENT_STYLE)
# card ---------------
card = dbc.Card([
        dbc.CardImg(src = 'assets/unnamed.png',
                    top = 'True',
                    style = {"width":'6rem'},
                    class_name = "rounded-circle",
        ),
        dbc.CardBody([
            dbc.Row([               # STOCK NAME AND TOKEN
                dbc.Col([
                    html.P('TATA Motors')
                ]),
                dbc.Col([
                    html.P('TTM')
                ]) 
            ]),
            dbc.Row([               #GRAPH
                dbc.Col([
                    dcc.Graph(id='daily-line', figure={},
                                config={'displayModeBar':False})
                ])
            ]),
            dbc.Row([               # CHANGE, SELL, BUY
                dbc.Col([
                    dbc.Button("CHANGE"),
                ]),
                dbc.Col([
                    dbc.Button("LOW"),
                ]),
                dbc.Col([
                    dbc.Button("HIGH"),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='indicator-graph',figure={},
                                config = {'displayModeBar': False})
                ], width = 4),
                dbc.Col([
                    dbc.Label(id='low-price', children="12.237")
                ], width = 4),
                dbc.Col([
                    dbc.Label(id='high-price', children="13.418")
                ], width = 4)
            ]),
        ])
    ], style={"width": "24rem"}, className="mt-3"
    )

### --- APP LAYOUT --- ###
app.layout = dbc.Container([
    # Stock Input
    dcc.Dropdown(nasdaq["Name"].values.tolist(), "PBR", id = 'search_stock_id'),
    html.Div(id='dd-output-container'),
     # Cards ------
    html.Div([
        dbc.Row([
            dbc.Col([html.Div(card)], width=6),
            dbc.Col([]),
            dbc.Col([]),
        ], justify='center'),
        dbc.Row([
            dbc.Col([]),
            dbc.Col([]),
            dbc.Col([]),
        ], justify='center'),
        dbc.Row([
            dbc.Col([]),
            dbc.Col([]),
            dbc.Col([]),
        ]), 
    ], style = CONTENT_STYLE
    ),
    # Invervals ------
    dcc.Interval(id='update', n_intervals=0, interval=1000*5),
    # Sidebar ------
    html.Div([dcc.Location(id="url"), sidebar]),
    dcc.Store(id='side_click')
], style = CONTENT_STYLE)

### --- CALLBACKS --- ###
# Update Stock
@app.callback(
        Output('dd-output-container','children'),
        Input("search_stock_id","value")
)
def update_output(value):
    stock = nasdaq['Symbol'][nasdaq['Name'] == value]
    return f'You have selected {stock}'

# update graph --------------------
@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

# run some shit --------------------------------------------
if __name__=='__main__':
    app.run_server(debug=True, port=3000)
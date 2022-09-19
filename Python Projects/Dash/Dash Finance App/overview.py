#---------------------------------------------
### LIBS ###
from turtle import ht, width
import dash  #pip install dash
from dash import html, dcc, Output, Input, State, dash_table                    
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import dash_daq as daq                     # pip install dash_daq
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from create_card import create_card
from sidebar import sidebar, search_bar
import requests
key = '1D0MB8E05Q6QOL2L' #Alpha API Key

# APP --------------
app = dash.Dash(__name__, external_stylesheets= [dbc.themes.FLATLY, dbc.icons.FONT_AWESOME],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# Get Data ---------
symbol = 'BRAG'
url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={key}'
r = requests.get(url)
co_data = r.json()
co_id = co_data['Symbol']
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=BR&topics=economy&apikey={key}'
r = requests.get(url)
feed_data = r.json()

### STYLES ### ------------------------------------------------------------------
# Content Style ------------
CONTENT_STYLE = {
    "margin-left": "15rem",
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

overview = html.Div([
        dbc.Button("Info", id="overview_open", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(co_data['Name'])),
                dbc.ModalBody(co_data['Description']),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="overview_close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="overview",
            is_open=False,
        ),
    ]
)

tabs = dbc.Tabs([
        dbc.Tab('Overview', label="Overview"),
        dbc.Tab('Feed', label="Feed"),
        dbc.Tab('Stats', label="Stats"),
        dbc.Tab('Charts', label="Charts"),
])

#create cards
def small_card(x):
    return dbc.Card(
    dbc.CardBody(
        [
            html.H4(x, className="card-title"),
            html.H6(co_data[x], className="card-subtitle"),

        ]
    ),
    style={"width": "14rem"},
    )


app.layout = dbc.Container([
    #chart grid
    dbc.Row(dbc.Col([search_bar], width = 8, align='center'), justify="center"),
    html.Hr(),
    dbc.Row([
        html.Div([
            html.H4(co_data['Name'], id = f"{co_id}-name"),
            html.H4(co_data['Symbol'], id = f'{co_id}-id'),
            overview
        ])
    ],justify="start", style={'font-size': '6px'}
    ),
    html.Br(),
    dbc.Row([
        dbc.Col([        
        ], width=5),
        dbc.Col([
            
        ], width=7),
    ]),
    html.Br(),
    dbc.Row([
        tabs
    ]),
    html.Br(),  
    #charts
    dbc.Row([
        dbc.Col([
            small_card('Exchange')
        ]),
        dbc.Col([
            small_card('Currency')
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            small_card('Country')
        ]),
        dbc.Col([
            small_card('Sector')
        ])
    ]),
    dbc.Row([
        small_card('Industry')
    ]),
    sidebar,
], style = CONTENT_STYLE)








# CALLBACKS -----------------------------------------
@app.callback(
    Output("overview", "is_open"),
    [Input("overview_open", "n_clicks"), Input("overview_close", "n_clicks")],
    [State("overview", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Run App --------------------------------------------
if __name__=='__main__':
    app.run_server(debug=True, port=3000)


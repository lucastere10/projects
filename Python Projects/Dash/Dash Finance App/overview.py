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
symbol = 'SID'
url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={key}'
r = requests.get(url)
co_data = r.json()
co_id = co_data['Symbol']
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=BR&topics=economy&apikey={key}'
r = requests.get(url)
feed_data = r.json()
df = pd.read_csv('data\\ttm.csv')
df['date'] = pd.to_datetime(df["date"])

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
SMALLCARD_STYLE = {
    "width": "12rem",
    "padding": "0.2em",
    "background-color": "#f8f9fa",
}


### FUNCTIONS ### ------------------------------------------------------------------
#create cards
def small_card(x):
    return dbc.Card(
    dbc.CardBody([
            html.H4(x, className="card-title",style={'fontSize': '1em'}),
            html.H6(co_data[x], className="card-subtitle",style={'fontSize': '1em'}),
    ]),
    style = SMALLCARD_STYLE,
    )


### OBJECTS ### ------------------------------------------------------------------
# Stock Description
info = html.Div([
        dbc.Button(html.I(className='fa-solid fa-info'), id="info_open", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(co_data['Name'])),
                dbc.ModalBody(co_data['Description']),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="info_close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="info",
            is_open=False,
        ),
    ]
)

fig = go.Figure(data=[go.Candlestick(x=df['date'],
                open  = df[df['indicator'] == 'open'],
                high  = df[df['indicator'] == 'high'],
                low   = df[df['indicator'] == 'low'],
                close = df[df['indicator'] == 'close'])])

# Tabs Content
tab1_content = html.Div([
    html.Br(),
    dbc.Row([
        dbc.Col([
            small_card('Exchange')
        ]),
        dbc.Col([
            small_card('Currency')
        ]),
    ], justify = 'start'),
    dbc.Row([
        dbc.Col([
            small_card('Country')
        ]),
        dbc.Col([
            small_card('Sector')
        ])
    ]),
    dbc.Row([
        dbc.Col([
            small_card('Industry')
        ]),
        dbc.Col([

        ])
    ]),
])
tab2_content = html.Div([dcc.Graph(figure=fig)])


# Create Tabs
tabs = dbc.Tabs([
        dbc.Tab(tab1_content, label = "Overview"),
        dbc.Tab('Feed',     label = "Feed"),
        dbc.Tab('Stats',    label = "Stats"),
        dbc.Tab(tab2_content,   label = "Charts"),
])

### APP LAYOUT ### ------------------------------------------------------------------
app.layout = dbc.Container([
    # Search Bar
    dbc.Row(dbc.Col([search_bar], width = 8, align='center'), justify="center"),
    html.Hr(),
    # Name And Symbol
    dbc.Row([
        dbc.Col([
            html.H4([f"{co_data['Name']} | {co_data['Symbol']}", info], id = f"{co_id}-name"),
        ], style={'font-size': '6px'}
        ),
    ], justify="start",
    ),
    html.Br(),
    dbc.Row([
        tabs
    ]),
    sidebar,
], style = CONTENT_STYLE,)

### CALLBACKS ### ------------------------------------------------------------------
@app.callback(
    Output("info", "is_open"),
    [Input("info_open", "n_clicks"), Input("info_close", "n_clicks")],
    [State("info", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Run App --------------------------------------------
if __name__=='__main__':
    app.run_server(debug=True, port=3000)


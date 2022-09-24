#---------------------------------------------
### LIBS ###
from turtle import ht, width
import dash  #pip install dash
from dash import html, dcc, Output, Input, State, dash_table                    
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import dash_daq as daq                     # pip install dash_daq
from dash.exceptions import PreventUpdate
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from create_card import create_card
from sidebar import sidebar, search_bar
import requests
key = '1D0MB8E05Q6QOL2L' #Alpha API Key

# APP --------------
app = dash.Dash(__name__, external_stylesheets= [dbc.themes.FLATLY, dbc.icons.FONT_AWESOME],
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# Get Data ---------
df = pd.read_csv('Python Projects\Dash\Dash Finance App\data\\ttm.csv')
df['date'] = pd.to_datetime(df["date"])
#Stocks Tickters
nasdaq = pd.read_csv('Python Projects\Dash\Dash Finance App\data\\nasdaq.csv')

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
            html.H4(className="card-title",style={'fontSize': '1em'},id = f"{x}-sc-title-id"),
            html.H6(className="card-subtitle",style={'fontSize': '1em'},id = f"{x}-sc-sub-id"),
    ]),
    style = SMALLCARD_STYLE,
    )

### OBJECTS ### ------------------------------------------------------------------
# Stock Description
info = html.Div([
        dbc.Button(html.I(className='fa-solid fa-info'), id="info_open", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(id = 'description-title-id'),
                dbc.ModalBody(id = 'description-body-id'),
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

chart = go.Figure(data=[go.Candlestick(x=df['date'],
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
tab2_content = html.Div([dcc.Graph(figure=chart)])
tab3_content = html.Div([dcc.Graph(figure=chart)])
tab4_content = html.Div([dcc.Graph(figure=chart)])


# Create Tabs
tabs = dbc.Tabs([
        dbc.Tab(tab1_content, label = "Overview"),
        dbc.Tab(tab2_content, label = "Feed"),
        dbc.Tab(tab3_content, label = "Stats"),
        dbc.Tab(tab2_content, label = "Charts"),
])

### APP LAYOUT ### ------------------------------------------------------------------
app.layout = dbc.Container([
    #Stored data
    dcc.Store(id = 'info-store-id'),
    dcc.Store(id = 'feed-store-id'),
    # Search Bar
    dbc.Row(dbc.Col([search_bar], width = 8, align='center'), justify="center"),
    dbc.Row(html.Div(id = 'stock_drop')),
    html.Hr(),
    # Name And Symbol
    dbc.Row([
        dbc.Col([
            html.H4(id = "title-id"),
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
    if not "info":
        raise PreventUpdate
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('stock_drop', 'children'),
    Output('info-store-id', 'data'),
    Input('search_stock_dropdown', 'value'))
def fun_stock_search(value):
    if not value:
        raise PreventUpdate
    symbol = nasdaq[nasdaq['Name'] == value]['Symbol'].to_string().split()[1]
    print(symbol)
    #Get Stock Information
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={key}'
    print(url)
    r = requests.get(url)
    test_data = r.json()
    print(test_data)
    return nasdaq[nasdaq['Name'] == value]['Symbol'], test_data

@app.callback(
    Output('title-id','children'),
    Input('info-store-id','data')
)
def get_data(x):
    if not x:
        raise PreventUpdate
    print(f"your data: {x}")
    return [f"{x['Name']} | {x['Symbol']}", info]

# Run App --------------------------------------------
if __name__=='__main__':
    app.run_server(debug=True, port=3000)


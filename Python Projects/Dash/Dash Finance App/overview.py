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
    "padding": "0.5em",
    "background-color": "#f8f9fa",
}

### FUNCTIONS ### ------------------------------------------------------------------
#create cards
def small_card(x,y):
    return dbc.Card(
    dbc.CardBody([
            html.H4(y,className="card-title",style={'fontSize': '1em'},id = f"{y}-sc-title-id"),
            html.H6(x[y],className="card-subtitle",style={'fontSize': '1em'},id = f"{y}-sc-sub-id"),
    ]),
    style = SMALLCARD_STYLE,
    )

### OBJECTS ### ------------------------------------------------------------------
# Stock Description -------------
info = html.Div([
        dbc.Button(html.I(className='fa-solid fa-info'), id="info_open", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(id = 'modal-info-title-id'),
                dbc.ModalBody(id = 'modal-info-body-id'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="info_close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal-info-id",
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
            html.Div(id = 'country-id'),
        ]),
        dbc.Col([
            html.Div(id = 'sector-id'),
        ]),
    ], justify = 'start'),
    dbc.Row([
        dbc.Col([
            html.Div(id = 'industry-id'),
        ]),
        dbc.Col([
            html.Div(),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(),
        ]),
        dbc.Col([
            html.Div(),
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
    Output("modal-info-id", "is_open"),
    [Input("info_open", "n_clicks"), Input("info_close", "n_clicks")],
    [State("modal-info-id", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if not "modal-info-id":
        raise PreventUpdate
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('info-store-id', 'data'),
    Input('search_stock_dropdown', 'value'))
def fun_stock_search(value):
    if not value:
        raise PreventUpdate
    symbol = nasdaq[nasdaq['Name'] == value]['Symbol'].to_string().split()[1]
    #Get Stock Information
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={key}'
    r = requests.get(url)
    test_data = r.json()
    return test_data

@app.callback(
    Output('title-id','children'),
    Input('info-store-id','data')
)
def get_data(x):
    if not x:
        raise PreventUpdate
    return [f"{x['Name']} | {x['Symbol']}", info]

@app.callback(
    Output('modal-info-title-id','children'),
    Output('modal-info-body-id','children'),
    Input('info-store-id','data')
)
def get_info(x):
    if not x:
        raise PreventUpdate
    return x["Name"], x["Description"]

@app.callback(
    Output('country-id','children'),
    Output('sector-id','children'),
    Output('industry-id','children'),
    Input('info-store-id','data')
)
def get_small_cards(x):
    return small_card(x,'Country'), small_card(x,'Sector'), small_card(x,'Industry')


# Run App --------------------------------------------
if __name__=='__main__':
    app.run_server(debug=True, port=3000)


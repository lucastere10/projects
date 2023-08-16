#---------------------------------------------
### LIBS ###
import sys
import dash  #pip install dash
from dash import html, dcc, Output, Input, State, callback                   
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
from dash.exceptions import PreventUpdate
import pandas as pd 
import plotly.graph_objects as go
import requests

sys.path.insert(0,'Python Projects\Dash\Dash Finance App')
from modules import module_sidebar, module_keys
from styles import app_styles
nasdaq = module_sidebar.nasdaq
#apikey
key = module_keys.key

dash.register_page(__name__, path = '/overview')

#Stocks Tickters
nasdaq = pd.read_csv("data/nasdaq.csv")

### FUNCTIONS ### ------------------------------------------------------------------
#create cards
def small_card(x,y):
    return dbc.Card(
    dbc.CardBody([
            html.H4(y,className="card-title",style={'fontSize': '.7em'},id = f"{y}-sc-title-id"),
            html.H6(x[y],className="card-subtitle",style={'fontSize': '1em', 'font-weight': 'bold'},id = f"{y}-sc-sub-id"),
    ]),
    style = app_styles.SMALLCARD_STYLE,
    )

#feeds
def create_feed(x,title,summary,url,s_label,score):
    return dbc.Container([
                dcc.Link([
                    html.P(x[title] ,id=f'{x[title]}-feed-title-id', className="lead")
                ],  href = x[url], target="_blank", style={'font-weight': 'bold'}
                ),
                dbc.Badge(x[s_label], color="primary", id=f'{x[title]}-feed-badge-id',className="me-1"),
                html.Hr(className="my-2"),
                html.P(x[summary] ,id = f'{title}-feed-sumary-id'),
                dbc.Tooltip(f"Score = {x[score]}", target = f'{x[title]}-feed-badge-id', placement = 'right'),
            ], fluid=True, className="py-3")
            

### OBJECTS ### ------------------------------------------------------------------
# Stock Description -------------
info = html.Div([
        dbc.Button(html.I(className='fa-solid fa-info'), id="info_open", n_clicks=0, className="btn btn-primary btn-sm"),
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
        )
    ])

# Tabs Content
tab1_content = html.Div([
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(id = 'industry-id'),
        ]),
        dbc.Col([
            html.Div(id = 'sector-id'),
        ]),
    ], justify = 'start'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(id = 'RevenuePerShareTTM-id'),
        ]),
        dbc.Col([
            html.Div(id = 'OperatingMarginTTM-id'),
        ]),
    ], justify = 'start'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(id = 'ReturnOnAssetsTTM-id'),
        ]),
        dbc.Col([
            html.Div(id = 'ReturnOnEquityTTM-id'),
        ]),
    ], justify = 'start'),
])
tab2_content = html.Div([
    html.Br(),
    dbc.Container(id = 'tab2-nfeed-id'),
    dbc.Container(id = 'tab2-content-id'),
])
tab3_content = html.Div([
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(id = 'PERatio-id'),
        ]),
        dbc.Col([
            html.Div(id = 'PEGRatio-id'),
        ]),
    ], justify = 'start'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(id = 'DividendPerShare-id'),
        ]),
        dbc.Col([
            html.Div(id = 'DividendYield-id'),
        ]),
    ], justify = 'start'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(id = '52WeekHigh-id'),
        ]),
        dbc.Col([
            html.Div(id = '52WeekLow-id'),
        ]),
    ], justify = 'start'), 
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(id = "50DayMovingAverage-id"),
        ]),
        dbc.Col([
            html.Div(id = "200DayMovingAverage-id"),
        ]),
    ], justify = 'start'),
    html.Br(),     
])
tab4_content = html.Div([dcc.Graph('chart-id')])

# Create Tabs
tabs = dbc.Tabs([
        dbc.Tab(tab1_content, label = "Overview"),
        dbc.Tab(tab2_content, label = "Feed"),
        dbc.Tab(tab3_content, label = "Stats"),
        dbc.Tab(tab4_content, label = "Charts"), 
])

### APP LAYOUT ### ------------------------------------------------------------------

layout = html.Div([
    #Stored data
    dcc.Store(id = 'info-store-id'),
    dcc.Store(id = 'feed-store-id'),
    dcc.Store(id = 'chart-store-id'),
    # Search Bar
    # Name And Symbol | Description
    dcc.Loading(
        id="loading-id", type="default", color = '#1a1a1a',
        children=html.Div(id="overview-loading-output-id"), fullscreen = True
    ),
    dbc.Row([
        dbc.Col([
            html.H4(id = "title-id"),
        ], align='center' ,style={'font-size': '6px'}
        ),
        dbc.Col([
            html.Div(id = 'description-id')
        ],  align='center')
    ], justify="start",
    ),
    dbc.Row([
        tabs
    ]),
])


### CALLBACKS ### ------------------------------------------------------------------
# Modal Button
@callback(
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

#get stock tickers and data
@callback(
    Output('info-store-id',  'data'),
    Output('feed-store-id',  'data'),
    Output('chart-store-id', 'data'),
    Output('overview-loading-output-id','children'),
    Input('search-stock-dropdown-id', 'value'))
def fun_stock_search(value):
    if not value:
        raise PreventUpdate
    symbol = nasdaq[nasdaq['Name'] == value]['Symbol'].to_string().split()[1]
    #Get Stock Information
    stock_url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={key}'
    r = requests.get(stock_url)
    stock_data = r.json()
    #Get Stock Feed
    feed_url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={key}'
    f = requests.get(feed_url)
    feed_data = f.json()
    #Get Stock Chart
    chart_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={key}'
    c = requests.get(chart_url)
    chart_data = c.json()
    return stock_data, feed_data, chart_data, {}

#Get Stock Title and Symbol
@callback(
    Output('title-id','children'),
    Output('description-id','children'),
    Input('info-store-id','data')
)
def get_data(x):
    if not x:
        raise PreventUpdate
    return [f"{x['Name']} | {x['Symbol']}"], info

#get Stock description
@callback(
    Output('modal-info-title-id','children'),
    Output('modal-info-body-id','children'),
    Input('info-store-id','data')
)
def get_info(x):
    if not x:
        raise PreventUpdate
    return x["Name"], x["Description"]

#Get Stock overwiew information
@callback(
    #tab1-content
    Output('sector-id','children'),
    Output('industry-id','children'),
    Output('RevenuePerShareTTM-id','children'),
    Output('OperatingMarginTTM-id','children'),
    Output('ReturnOnAssetsTTM-id','children'),
    Output('ReturnOnEquityTTM-id','children'),
    #tab2-content
    Output('PERatio-id','children'),
    Output('PEGRatio-id','children'),    
    Output('DividendPerShare-id','children'),
    Output('DividendYield-id','children'),
    Output('52WeekHigh-id','children'),
    Output('52WeekLow-id','children'),
    Output('50DayMovingAverage-id','children'),
    Output('200DayMovingAverage-id','children'),
    #inputs
    Input('info-store-id','data')
)
def get_small_cards(x):
    return [#tab1 content
            small_card(x,'Sector'), small_card(x,'Industry'),
            small_card(x,'RevenuePerShareTTM'), small_card(x,'OperatingMarginTTM'),
            small_card(x, 'ReturnOnAssetsTTM'), small_card(x, 'ReturnOnEquityTTM'),
            #tab2 content
            small_card(x,'PERatio'), small_card(x,'PEGRatio'),
            small_card(x,'DividendPerShare'), small_card(x,'DividendYield'),
            small_card(x,'52WeekHigh'), small_card(x,'52WeekLow'),
            small_card(x,'50DayMovingAverage'), small_card(x,'200DayMovingAverage'),]

#Get Stock feed information
@callback(
    Output('tab2-content-id','children'),
    Input('feed-store-id','data')
)
def get_feed(x):
    if not x or not x['feed']:
        PreventUpdate
    return dbc.Row(children = [create_feed(x['feed'][n],'title', 'summary','url',
                        'overall_sentiment_label','overall_sentiment_score') for n in range(0,int(x['items']))
                    ])

#Create Chart
@callback(
    Output('chart-id','figure'),
    Input('chart-store-id','data'),
)
def get_chart(x):
    chart_data = pd.DataFrame.from_dict(x['Time Series (5min)'], orient = 'index').reset_index()
    chart_data['index'] = pd.to_datetime(chart_data['index'])
    #create chart fig
    fig = go.Figure(data=[go.Candlestick(x=chart_data['index'],
                    open  = chart_data['1. open'],
                    high  = chart_data['2. high'],
                    low   = chart_data['3. low'],
                    close = chart_data['4. close'])
                    ])
    return fig
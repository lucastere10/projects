#---------------------------------------------
### LIBS ###
from contextlib import nullcontext
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
app = dash.Dash(__name__, external_stylesheets= [dbc.themes.LUX, dbc.icons.FONT_AWESOME],
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
    "width": "16rem",
    "padding": "0.8em",
    "background-color": "#f8f9fa",
}

### FUNCTIONS ### ------------------------------------------------------------------
#create cards
def small_card(x,y):
    return dbc.Card(
    dbc.CardBody([
            html.H4(y,className="card-title",style={'fontSize': '.8em'},id = f"{y}-sc-title-id"),
            html.H6(x[y],className="card-subtitle",style={'fontSize': '1em'},id = f"{y}-sc-sub-id"),
    ]),
    style = SMALLCARD_STYLE,
    )

#feeds
def create_feed(x,title,summary,url,s_label):
    return html.Div(
        dbc.Container([
            html.P(x[title] ,id=f'{title}-feed-title-id', className="lead"),
            dbc.Badge(x[s_label], color="primary", id=f'{title}-feed-badge-id',className="me-1"),
            html.Hr(className="my-2"),
            html.P(x[summary] ,id = f'{title}-feed-sumary-id'),
            html.P(x[url] ,id = f'{title}-feed-url-id'),
            ],
            fluid=True,
            className="py-3",
        ),
        className="p-3 bg-light rounded-3",
    )

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

#stock chart
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
            html.Div(id = 'industry-id'),
        ]),
        dbc.Col([
            html.Div(id = 'sector-id'),
        ]),
    ], justify = 'start'),
    dbc.Row([
        dbc.Col([
            html.Div(id = 'DividendPerShare-id'),
        ]),
        dbc.Col([
            html.Div(id = 'DividendYield-id'),
        ]),
    ], justify = 'start'),
    dbc.Row([
        dbc.Col([
            html.Div(id = 'PERatio-id'),
        ]),
        dbc.Col([
            html.Div(id = 'PEGRatio-id'),
        ]),
    ], justify = 'start'),
])
tab2_content = html.Div([
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(id = 'feed-1-id'),
        ]),
    ], justify = 'start'),
    dbc.Row([
        dbc.Col([
            html.Div(id = 'feed-2-id'),
        ]),
    ], justify = 'start'),
    dbc.Row([
        dbc.Col([
            html.Div(id = 'feed-3-id'),
        ]),
    ], justify = 'start'),
])
tab3_content = html.Div([])
tab4_content = html.Div([dcc.Graph(figure=chart)])

# Create Tabs
tabs = dbc.Tabs([
        dbc.Tab(tab1_content, label = "Overview"),
        dbc.Tab(tab2_content, label = "Feed"),
        dbc.Tab(tab3_content, label = "Stats"),
        dbc.Tab(tab4_content, label = "Charts"), 
])

### APP LAYOUT ### ------------------------------------------------------------------

app.layout = dbc.Container([
    #Stored data
    dcc.Store(id = 'info-store-id'),
    dcc.Store(id = 'feed-store-id'),
    # Search Bar
    dbc.Row(dbc.Col([search_bar], width = 10, align='center'), justify="center"),
    html.Hr(),
    # Name And Symbol | Description
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
    sidebar,
], style = CONTENT_STYLE,)


### CALLBACKS ### ------------------------------------------------------------------
# Modal Button
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

# Open Offcanvas Button 
@app.callback(
    Output("filter_offcanvas-id", "is_open"),
    [Input("filter-button-id", "n_clicks"),Input('add-filters-button-id','n_clicks')],
    [State("filter_offcanvas-id", "is_open")],
)
def toggle_offcanvas(n1, n2, is_open):
    if not "filter_offcanvas-id":
        raise PreventUpdate
    if n1:
        return not is_open
    return is_open

# Filter Dropdown Values
@app.callback(
    Output('search-stock-dropdown-id','options'),
    Input('add-filters-button-id','n_clicks'),
    State('offcanvas-filder-country-id', 'value'),
    State('offcanvas-filder-sector-id', 'value'),
    State('offcanvas-filder-industry-id', 'value'),
)
def filter_data(n_clicks, x, y, z):
    if not n_clicks:
        PreventUpdate
    filtered_df = nasdaq
    if x is not None:
        filtered_df = filtered_df[filtered_df['Country'].isin(x)]
    if y is not None:
        filtered_df = filtered_df[filtered_df['Sector'].isin(y)]
    if z is not None:
        filtered_df = filtered_df[filtered_df['Industry'].isin(z)]
    if len(filtered_df['Name']) == 0:
        dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Not Found")),
                dbc.ModalBody("No Stock found with those filters")
        ], is_open = True),
        filtered_df = nasdaq
    return filtered_df['Name'].unique()

#get stock tickers and data
@app.callback(
    Output('info-store-id', 'data'),
    Output('feed-store-id', 'data'),
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
    return stock_data, feed_data

#Get Stock Title and Symbol
@app.callback(
    Output('title-id','children'),
    Output('description-id','children'),
    Input('info-store-id','data')
)
def get_data(x):
    if not x:
        raise PreventUpdate
    return [f"{x['Name']} | {x['Symbol']}"], info

#get Stock description
@app.callback(
    Output('modal-info-title-id','children'),
    Output('modal-info-body-id','children'),
    Input('info-store-id','data')
)
def get_info(x):
    if not x:
        raise PreventUpdate
    return x["Name"], x["Description"]

#Get Stock overwiew information
@app.callback(
    Output('sector-id','children'),
    Output('industry-id','children'),
    Output('DividendPerShare-id','children'),
    Output('DividendYield-id','children'),
    Output('PERatio-id','children'),
    Output('PEGRatio-id','children'),    
    Input('info-store-id','data')
)
def get_small_cards(x):
    return [small_card(x,'Sector'), 
            small_card(x,'Industry'),
            small_card(x,'DividendPerShare'), 
            small_card(x,'DividendYield'), 
            small_card(x,'PERatio'), 
            small_card(x,'PEGRatio')]

#Get Stock feed information
@app.callback(
    Output('feed-1-id','children'),
    Input('feed-store-id','data')
)
def get_feed(x):
    if not x:
        PreventUpdate
    if not x['feed']:
        PreventUpdate
    return create_feed(x['feed'][0],'title','summary','url','overall_sentiment_label')

# Run App --------------------------------------------
if __name__=='__main__':
    app.run_server(debug=True, port=3000)


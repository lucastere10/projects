#---------------------------------------------
### LIBS ###
import sys
from dash import dcc, html, State, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import requests

#import sys path
sys.path.insert(0,'Python Projects\Dash\Dash Finance App')
from modules import module_sidebar, module_keys
nasdaq = module_sidebar.nasdaq
crypto = module_sidebar.crypto
#api key
key = module_keys.key
# card ---------------
def create_card(ticker):  
    df = yf.Ticker(ticker)
    info = df.info
    hist = df.history('1d','1m').reset_index()
    while bool(hist.empty) is True:
        print('deu ruim')
        df = yf.Ticker(nasdaq['Symbol'].sample().to_string().split()[1])
        hist = df.history('1d','1m').reset_index()
        if bool(hist.empty) is False:
            print('agora deu bom')
            break
    return dbc.Card([
            dbc.Row([
                dbc.Col([
                    dbc.CardImg(
                        src = info['logo_url'],
                        top = 'False',
                        style = {"width":'4rem', "padding": "0.5rem 0.5rem"},
                        #class_name = "rounded-circle",
                    ),
                ], width = 3),
                dbc.Col([
                    dbc.Row([html.P(info['shortName'], id = f"{ticker}-title")], style={'font-size': '16px'}),
                    dbc.Row([html.H4(info['symbol'], id = f'{ticker}-id')], style={'font-size': '1px', 'font-weight' : 'bold'}),
                ], width = 9),
            ]),
            dbc.CardBody([
                dbc.Row([ #GRAPH
                    dbc.Col([
                        dcc.Graph(id='daily-line', figure=get_graph(hist), config={'displayModeBar':False})
                    ], width=12)
                ]),
                dbc.Row([ #change price
                    dbc.Col([
                        dcc.Graph(id='indicator-graph', figure=get_indicator(hist),
                                    config={'displayModeBar':False},
                                    )
                    ], width={'size':3,'offset':2})
                ]),
                dbc.Row([
                    dbc.Col([])               
                ], align = 'center', justify="evenly"
                ),
            ])
        ], style={"width": "22rem"}
        )

# tiny card ---------------
def create_tinycard(ticker):
    df = yf.Ticker(ticker)
    info = df.info
    hist = df.history('1d','1m').reset_index()
    while bool(hist.empty) is True:
        print('deu ruim tiny')
        df = yf.Ticker(nasdaq['Symbol'].sample().to_string().split()[1])
        hist = df.history('1d','1m').reset_index()
        if bool(hist.empty) is False:
            print('agora deu bom tiny')
            break
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Row(html.H4([info['symbol']])),
                    dbc.Row([
                        dcc.Graph(figure=get_indicator(hist),
                            config={'displayModeBar':False},
                        )
                    ])
                ]),
                dbc.Col([
                    dcc.Graph(figure=get_graph(hist), config={'displayModeBar':False})
                    ], width=7
                )
            ]),
        ])
    ])

### CRYPTO ###
def create_crypto_card(ticker):
    #Get Crypto Chart
    crypto_url = f'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol={ticker}&market=USD&interval=5min&apikey={key}'
    c = requests.get(crypto_url)
    chart_data = c.json()
    symbol = chart_data['Meta Data']['2. Digital Currency Code']
    name = chart_data['Meta Data']['3. Digital Currency Name']
    chart_data = pd.DataFrame.from_dict(chart_data['Time Series Crypto (5min)'], orient='index').reset_index()
    chart_data['Datetime'] = pd.to_datetime(chart_data['index'])
    chart_data['Close'] = pd.to_numeric(chart_data['4. close'])
    return dbc.Card([
        dbc.CardBody([
            dbc.Col([
                dbc.Row([html.P(name, id = f"{name}-title")], style={'font-size': '16px'}),
                dbc.Row([html.H4(symbol, id = f'{symbol}-id')], style={'font-size': '1px', 'font-weight' : 'bold'}),
            ], width = 9),
            dbc.Row([ #GRAPH
                dbc.Col([
                    dcc.Graph(id='daily-line', figure=get_graph(chart_data), config={'displayModeBar':False})
                ], width=12)
            ]),
            dbc.Row([ #change price
                dbc.Col([
                    dcc.Graph(id='indicator-graph', figure=get_indicator(chart_data),
                                config={'displayModeBar':False},
                                )
                ], width={'size':5,'offset':4.5})
            ]),
        ])
    ], style={"width": "22rem"}
    )
    return fig

# get indicator ---------------
def get_indicator(x):
    day_start = x[x['Datetime'] == x['Datetime'].min()]['Close'].values[0]
    day_end = x[x['Datetime'] == x['Datetime'].max()]['Close'].values[0]
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=day_end,
        number = {'prefix': "$"},
        delta={'reference': day_start, 'relative': True, 'valueformat':'.2%', 'position': "top"}))
    fig.update_traces(delta_font={'size':13}, number_font={'size':20, 'color':'black'})
    fig.update_layout(height=40, width=75)
    if day_end >= day_start:
        fig.update_traces(delta_increasing_color='green')
    elif day_end < day_start:
        fig.update_traces(delta_decreasing_color='red')
    return fig

# get graph ---------------
def get_graph(x):
    x_graph = x.iloc[::-1]
    fig = px.line(x_graph, x='Datetime', y='Close',
                   range_y=[x_graph['Close'].min(), x_graph['Close'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                             paper_bgcolor='rgba(0,0,0,0)',
                                             plot_bgcolor='rgba(0,0,0,0)',
                                             yaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ),
                                             xaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ))

    day_start = x_graph[x_graph['Datetime'] == x_graph['Datetime'].min()]['Close'].values[0]
    day_end = x_graph[x_graph['Datetime'] == x_graph['Datetime'].max()]['Close'].values[0]

    if day_end >= day_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif day_end < day_start:
        return fig.update_traces(fill='tozeroy',
                             line={'color': 'red'})
    return fig    
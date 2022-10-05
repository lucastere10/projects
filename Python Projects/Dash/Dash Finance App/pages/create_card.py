from dash import dcc, html, State, Input, Output
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import yfinance as yf
import plotly.graph_objects as go
from sidebar import nasdaq

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
    fig = go.Figure(data=[go.Candlestick(x=hist['Datetime'],
                    open  = hist['Open'],
                    high  = hist['High'],
                    low   = hist['Low'],
                    close = hist['Close'])
                    ])
    fig.update_layout(xaxis_rangeslider_visible=False,
                      yaxis={'visible': False, 'showticklabels': False},
                      xaxis={'visible': False, 'showticklabels': False},)
    return dbc.Card([
            dbc.Row([
                dbc.Col([
                    dbc.CardImg(
                        src = info['logo_url'],
                        top = 'False',
                        style = {"width":'4rem', "padding": "0.5rem 0.5rem"},
                        class_name = "rounded-circle",
                    ),
                ], width = 3),
                dbc.Col([
                    dbc.Row([html.H4(info['shortName'], id = f"{ticker}-title")], style={'font-size': '6px'}),
                    dbc.Row([html.P(info['symbol'], id = f'{ticker}-id')], style={'font-size': '16px'}),
                ], width = 9),
            ]),
            dbc.CardBody([
                dbc.Row([               #GRAPH
                    dbc.Col([
                        dcc.Graph(figure=fig)
                    ])
                ]),
                dbc.Row([               # CHANGE, SELL, BUY
                    dbc.Col([
                        html.H5("OPEN"),
                    ], width = 3),
                    dbc.Col([
                        html.H5("HIGH"),
                    ], width = 3),
                    dbc.Col([
                        html.H5("LOW"),
                    ], width = 3),
                    dbc.Col([
                        html.H5("CLOSE"),
                    ], width = 3),
                ], align = 'center', justify="evenly"
                ),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("${:,.2f}".format(float(hist['Open'][-1:])))
                    ], width = 3),
                    dbc.Col([
                        dbc.Label("${:,.2f}".format(float(hist['High'][-1:])))
                    ], width = 3),
                    dbc.Col([
                        dbc.Label("${:,.2f}".format(float(hist['Low'][-1:])))
                    ], width = 3),
                    dbc.Col([
                        dbc.Label("${:,.2f}".format(float(hist['Close'][-1:])))
                    ], width = 3),
                ], align = 'center', justify="evenly"
                ),
            ])
        ], style={"width": "22rem"}
        )
from dash import dcc, html, State, Input, Output
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import yfinance as yf

# card ---------------
def create_card(ticker):  
    df = yf.Ticker(ticker)
    info = df.info
    return dbc.Card([
            dbc.Row([
                dbc.Col([
                    dbc.CardImg(
                        src = info['logo_url'],
                        top = 'False',
                        style = {"width":'4rem', "padding": "0.5rem 0.5rem"},
                        class_name = "rounded-circle",
                    ),
                ], width = 2),
                dbc.Col([
                    dbc.Row([html.H4(info['shortName'], id = f"{ticker}-title")], style={'font-size': '6px'}),
                    dbc.Row([html.P(info['symbol'], id = f'{ticker}-id')], style={'font-size': '16px'}),
                ], width = 10),
            ]),
            dbc.CardBody([
                dbc.Row([               #GRAPH
                    dbc.Col([
                        dcc.Graph(figure={},
                                    config={'displayModeBar':False})
                    ])
                ]),
                dbc.Row([               # CHANGE, SELL, BUY
                    dbc.Col([
                        dbc.Button("CHANGE"),
                    ], width = 4),
                    dbc.Col([
                        dbc.Button("LOW"),
                    ], width = 4),
                    dbc.Col([
                        dbc.Button("HIGH"),
                    ], width = 4)
                ], align = 'center', justify="evenly"
                ),
                dbc.Row([
                    dbc.Col([
                        dbc.Label(children="1,32%")
                    ], width = 4),
                    dbc.Col([
                        dbc.Label(children="12.237")
                    ], width = 4),
                    dbc.Col([
                        dbc.Label(children="13.418")
                    ], width = 4)
                ],align = 'center', justify="evenly"
                ),
            ])
        ], style={"width": "22rem"}
        )
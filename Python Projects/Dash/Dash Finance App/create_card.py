from dash import dcc, html, State, Input, Output
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components

# card ---------------
def create_card(card_id, title):  
    return dbc.Card([
            dbc.Row([
                dbc.Col([
                    dbc.CardImg(
                        src = 'assets/unnamed.png',
                        top = 'False',
                        style = {"width":'4rem'},
                        class_name = "rounded-circle",
                    ),
                ], width = 4),
                dbc.Col([
                    dbc.Row([html.P(title, id = f"{card_id}-title")], align = 'rigth'),
                    dbc.Row([html.P(card_id, id = f'{card_id}-id')], align = 'rigth'),
                ], width = 8)
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
import dash
from dash import dcc, html

tab_1_layout = html.Div([
            html.Div([
                html.Div([
                    html.H6('Medical Specialty'),
                    dcc.Graph(
                        id='med-graph-1',
                        figure={
                            'data': [

                            ],
                            'layout': {
                                'title': 'Graph-1'
                            }
                        }
                    )
                ], className="six columns"),

                html.Div([
                    html.H6('Readmission'),
                    dcc.Graph(
                        id='med-graph-2',
                        figure={
                            'data': [

                            ],
                            'layout': {
                                'title': 'Graph-2'
                            }
                        }
                    )
                ], className="six columns"),

            ], className="row", style={"margin": "1% 3%"})
    ])
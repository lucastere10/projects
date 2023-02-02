#---------------------------------------------
### LIBS ###
import sys
import dash  #pip install dash
from dash import html, dcc, Output, Input, callback, dash_table      
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components

#import sys path
sys.path.insert(0,'Python Projects\Dash\Dash Finance App')
from modules import module_cards, module_sidebar
nasdaq = module_sidebar.nasdaq

dash.register_page(__name__, path = '/')

# LAYOUT --------------
layout = html.Div([
    #chart grid
    dcc.Interval(
        id='interval-component-id',
        interval=1*300000, # in milliseconds
        n_intervals=0
    ),
    html.Br(),
    dbc.Row([
        dbc.Col(id='chart1-id'),
        dbc.Col(id='chart2-id'),
        dbc.Col(id='chart3-id'),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(id = 'tinychart1-id', width=3),
        dbc.Col(id = 'tinychart2-id', width=3),
        dbc.Col(id = 'tinychart3-id', width=3),
        dbc.Col(id = 'tinychart4-id', width=3),
    ]),
    dbc.Row([
        dcc.Loading(
            id="loading-id", type="default", color = '#1a1a1a',
            children=html.Div(id="home-loading-output-id"),
        ),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                data = nasdaq.to_dict('records'), 
                columns = [{"name": i, "id": i} for i in nasdaq.columns],
                page_size = 10,
                style_cell={
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 350
                },
                tooltip_data=[
                    {
                        column: {'value': str(value), 'type': 'markdown'}
                        for column, value in row.items()
                    } for row in nasdaq.to_dict('records')
                ],
                tooltip_duration=None
            )
        ],width='auto')
    ])
], id = 'home-layout-id')

### CALLBACKS ### ------------------------------------------------------------------

#load charts
@callback(
    Output('home-loading-output-id','children'),
    Output('chart1-id','children'),    
    Output('chart2-id','children'),
    Output('chart3-id','children'),
    Output('tinychart1-id','children'),    
    Output('tinychart2-id','children'),
    Output('tinychart3-id','children'),
    Output('tinychart4-id','children'),
    Input('interval-component-id', 'n_intervals')   
)
def get_cards(x):
    print(nasdaq.columns),
    return [{},
            module_cards.create_card(nasdaq['Symbol'].sample().to_string().split()[1]), 
            module_cards.create_card(nasdaq['Symbol'].sample().to_string().split()[1]), 
            module_cards.create_card(nasdaq['Symbol'].sample().to_string().split()[1]),
            module_cards.create_tinycard(nasdaq['Symbol'].sample().to_string().split()[1]),
            module_cards.create_tinycard(nasdaq['Symbol'].sample().to_string().split()[1]),
            module_cards.create_tinycard(nasdaq['Symbol'].sample().to_string().split()[1]),
            module_cards.create_tinycard(nasdaq['Symbol'].sample().to_string().split()[1]),
            ]
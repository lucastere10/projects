#---------------------------------------------
### LIBS ###
from turtle import ht, width
import dash  #pip install dash
from dash import html, dcc, Output, Input, State, dash_table                    
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import dash_daq as daq                     # pip install dash_daq
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from create_card import create_card, create_tinycard
from sidebar import sidebar, search_bar, nasdaq, callback_sidebar_collapse, callback_open_offcanvas, callback_filter_dropdown, callback_open_mobile_offcanvas
from styles.styles import SIDEBAR_STYLE, SIDEBAR_HIDEN, CONTENT_STYLE, CONTENT_STYLE1

# APP --------------
app = dash.Dash(__name__, external_stylesheets= [dbc.themes.LUX, dbc.icons.FONT_AWESOME],
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# LAYOUT --------------
app.layout = dbc.Container([
    #chart grid
    dcc.Interval(
        id='interval-component-id',
        interval=1*300000, # in milliseconds
        n_intervals=0
    ),
    dbc.Row(dbc.Col([search_bar], width = 10, align='center'), justify="center"),
    html.Br(),
    #dbc.Row(dbc.Col(dbc.Button('GET DATA',id = 'chart-button-id'), width = 2)),
    #html.Br(),
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
            children=html.Div(id="loading-output-id"),
        ),
    ]),
    sidebar,
], style = CONTENT_STYLE, id = 'layout-id')

### CALLBACKS ### ------------------------------------------------------------------

#load charts
@app.callback(
    Output('loading-output-id','children'),
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
    print(x)
    return [{},
            create_card(nasdaq['Symbol'].sample().to_string().split()[1]), 
            create_card(nasdaq['Symbol'].sample().to_string().split()[1]), 
            create_card(nasdaq['Symbol'].sample().to_string().split()[1]),
            create_tinycard(nasdaq['Symbol'].sample().to_string().split()[1]),
            create_tinycard(nasdaq['Symbol'].sample().to_string().split()[1]),
            create_tinycard(nasdaq['Symbol'].sample().to_string().split()[1]),
            create_tinycard(nasdaq['Symbol'].sample().to_string().split()[1]),
            ]
            #nasdaq['Symbol'].sample().to_string().split()[1]
        
#collapse sidebar
callback_sidebar_collapse(app)

# Open Offcanvas Button 
callback_open_offcanvas(app)

# Filter Dropdown Values
callback_filter_dropdown(app)

# Mobile Dropdown Menu
callback_open_mobile_offcanvas(app)

if __name__=='__main__':
    app.run_server(debug=True, port=3000)
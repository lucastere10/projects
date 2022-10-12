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
from pages.sidebar import sidebar, search_bar
from pages.styles import styles #SIDEBAR_STYLE, SIDEBAR_HIDEN, CONTENT_STYLE, CONTENT_STYLE1

app = dash.Dash(__name__, use_pages=True, 
                external_stylesheets= [dbc.themes.LUX, dbc.icons.FONT_AWESOME],
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

app.layout = dbc.Container([
    html.Div([dbc.Row(dbc.Col([search_bar], width = 10, align='center'), justify="center")]),
    html.Div(id='content-id'),
    html.Div([sidebar.sidebar]),
], style = styles.CONTENT_STYLE, id = 'layout-id')

if __name__ == '__main__':
    app.run_server(debug=True)
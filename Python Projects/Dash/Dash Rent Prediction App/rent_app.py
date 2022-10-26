#libs
import sys
from cProfile import run
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

### - APP - ####
app = dash.Dash(__name__, use_pages=True, 
                external_stylesheets= [dbc.themes.LUX, dbc.icons.FONT_AWESOME],
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

#import sys path
sys.path.insert(0,'Python Projects\Dash\Dash Rent Prediction App')
from modules import module_sidebar
from styles import app_styles

### - LAYOUT - ###

app.layout = dbc.Container([
    html.Div([module_sidebar.sidebar]),
    html.Br(),
    dash.page_container,
], style = app_styles.CONTENT_STYLE, id = 'layout-id')


if __name__ == '__main__':
    app.run_server(debug=True)
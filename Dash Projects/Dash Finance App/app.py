#---------------------------------------------
### LIBS ###
import sys
import dash  #pip install dash
from dash import html, dcc             
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components

#import sys path
sys.path.insert(0,'Python Projects\Dash\Dash Finance App')
from modules import module_sidebar
from styles import app_styles

app = dash.Dash(__name__, use_pages=True, 
                external_stylesheets= [dbc.themes.LUX, dbc.icons.FONT_AWESOME],
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

app.layout = dbc.Container([
    html.Div([module_sidebar.sidebar]),
    html.Div([dbc.Row(dbc.Col([module_sidebar.searchbar], width = 10, align='center'), justify="center")]),
    html.Br(),
    dcc.Location(id='test-location-id', refresh=True),
    dash.page_container,
], style = app_styles.CONTENT_STYLE, id = 'layout-id')

### CALLBACKS ### --------------------------------------------------

#collapse sidebar
module_sidebar.callback_sidebar_collapse(app)

# Open Offcanvas Button 
module_sidebar.callback_open_offcanvas(app)

# Filter Dropdown Values
module_sidebar.callback_filter_dropdown(app)

# Mobile Dropdown Menu
module_sidebar.callback_open_mobile_offcanvas(app)

# Dropdown Tooltip
module_sidebar.callback_dropdown_tooltip(app)

if __name__ == '__main__':
    app.run_server(debug=True)

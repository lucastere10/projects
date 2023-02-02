#---------------------------------------------
### LIBS ###
from turtle import ht, width
import dash  #pip install dash
from dash import html, dcc, Output, Input, State                              
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import dash_daq as daq                     # pip install dash_daq
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

# ICONS --------------------------------------- 
"fa-brands fa-linkedin"
"fa-brands fa-github"



# APP -----------------------------------------
app = dash.Dash(__name__, external_stylesheets= [dbc.themes.FLATLY, dbc.icons.FONT_AWESOME],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# Sidebar Style -------------------------------------
SIDEBAR_STYLE = {               # the style arguments for the sidebar. We use position:fixed and a fixed width
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
CONTENT_STYLE = {               # the styles for the main content position it to the right of the sidebar
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Sidebar ---------------------------------
sidebar = html.Div([
        html.H1("Lucas Caldas", className="display-4", style={'fontSize': 42}),
        html.Sub('Welcome to my personal portfolio'),
        dbc.Row([
            dbc.Col([
                dbc.Button(html.I(
                    className= "fa-brands fa-linkedin"),  
                    className="rounded-circle",
                    href="https://www.linkedin.com/in/lucas-caldas50/", active="exact"
                ),
            ]),
            dbc.Col([
                dbc.Button(html.I(
                    className= "fa-brands fa-github"),  
                    className="rounded-circle",
                    href="https://github.com/lucastere10", active="exact"
                )
            ]),
        ], justify="evenly"
        ),
        html.Hr(),
        dbc.Nav([
                dbc.NavLink([html.I(className = "fa-solid fa-house"), "  Home"], href="/", active="exact"),
                dbc.NavLink("About", href="/about", active="exact"),
                dbc.NavLink("Portfolio", href="/portfolio", active="exact"),
                dbc.NavLink("Resume", href="/resume", active="exact"),
                html.Hr(),
                dbc.Button([
                    html.I(className = "fa-solid fa-envelope"), "  Contact Me"], 
                    href="/contact", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        daq.BooleanSwitch(
            on=True,
            id='darktheme-daq-powerbutton',
            className='dark-theme-control'
        ),            
    ], style=SIDEBAR_STYLE,
)
content = html.Div(id="page-content", style=CONTENT_STYLE)



### - APP LAYOUT - ###
app.layout = dbc.Container([
    #SIDEBAR
    html.Div([dcc.Location(id="url"), sidebar, content])
])

# run some shit --------------------------------------------
if __name__=='__main__':
    app.run_server(debug=True, port=3000)
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

# APP --------------
app = dash.Dash(__name__, external_stylesheets= [dbc.themes.FLATLY, dbc.icons.FONT_AWESOME],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# card
card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Title", className="card-title"),
            html.H6("Card subtitle", className="card-subtitle"),
            html.P(
                "Some quick example text to build on the card title and make "
                "up the bulk of the card's content.",
                className="card-text",
            ),
            dbc.CardLink("Card link", href="#"),
            dbc.CardLink("External link", href="https://google.com"),
        ]
    ),
    style={"width": "18rem"},
)


# Sidebar ------------------------------
sidebar = html.Div([
        html.H1('GRID TEST', className = {'font-size : 20'})
])
CONTENT_STYLE = {               # the styles for the main content position it to the right of the sidebar
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
content = html.Div(id="page-content", style=CONTENT_STYLE)

    #html.Div(card)


app.layout = dbc.Container([
    #chart grid
    dbc.Row([ #first row, title.
        html.H6('TITLE')
    ]),
    dbc.Row([
        dbc.Col([html.Div(card)]),
        dbc.Col([html.Div(card)]),
        dbc.Col([html.Div(card)]),
    ]),
    dbc.Row([
        dbc.Col([html.Div(card)]),
        dbc.Col([html.Div(card)]),
        dbc.Col([html.Div(card)]),
    ]),
    dbc.Row([
        dbc.Col([html.Div(card)]),
        dbc.Col([html.Div(card)]),
        dbc.Col([html.Div(card)]),
    ]),

])

if __name__=='__main__':
    app.run_server(debug=True, port=3000)
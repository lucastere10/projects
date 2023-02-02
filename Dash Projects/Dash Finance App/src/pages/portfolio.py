import dash  #pip install dash
from dash import html                              

dash.register_page(__name__, path = '/portfolio')

layout = html.Div(children=[
    html.H1(children='This is our portfolio page'),
    html.Div(children='''
        This is our portfolio page content.
    '''),
])
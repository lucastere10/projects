#---------------------------------------------
### LIBS ###
import dash  #pip install dash
from dash import html, dcc                              

dash.register_page(__name__, path = '/stocks')

layout = html.Div(children=[
    html.H1(children='This is our Stocks page'),
	html.Div([
        "Select a city: ",
        dcc.RadioItems(['New York City', 'Montreal','San Francisco'],
        'Montreal',
        id='analytics-input')
    ]),
	html.Br(),
    html.Div(id='analytics-output'),
])

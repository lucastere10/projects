#---------------------------------------------
### LIBS ###
from turtle import ht, width
import dash  #pip install dash
from dash import html, dcc, Output, Input, State, dash_table                    
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import dash_daq as daq                     # pip install dash_daq
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from create_card import create_card
from sidebar import sidebar, search_bar

#read csv
df = pd.read_csv('Python Projects\\Dash\\Dash Finance App\\data\\ttm.csv')

# APP --------------
app = dash.Dash(__name__, external_stylesheets= [dbc.themes.FLATLY, dbc.icons.FONT_AWESOME],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

### STYLES ### ------------------------------------------------------------------
# Content Style ------------
CONTENT_STYLE = {
    "margin-left": "15rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

app.layout = dbc.Container([
    #chart grid
    dbc.Row(dbc.Col([search_bar], width = 8, align='center'), justify="center"),
    dbc.Row([
        dbc.Col([html.Div(create_card('PBR', 'Petrobrás'))]),
        dbc.Col([html.Div(create_card('BRT', 'Veículos RJ'))]),
        dbc.Col([html.Div(create_card('TSL', 'Tesla Motors'))]),
    ]),
    sidebar,
    dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
], style = CONTENT_STYLE)

if __name__=='__main__':
    app.run_server(debug=True, port=3000)
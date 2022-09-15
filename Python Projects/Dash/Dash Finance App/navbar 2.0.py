import dash  #pip install dash
from dash import dcc, html, State, Input, Output
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import dash_daq as daq                     # pip install dash_daq
import pandas as pd
import requests
from alpha_vantage.timeseries import TimeSeries # pip install alpha-vantage
# DATA -------------------------------------------------------------------------
### Set up initial key and financial category ###
key = '1D0MB8E05Q6QOL2L' #Alpha API Key
ts = TimeSeries(key, output_format='pandas') # 'pandas' or 'json' or 'csv'
#stock_symbol = "PBR"
nasdaq = pd.read_csv('Python Projects\\Dash\\Dash Finance App\\data\\nasdaq.csv')
#ttm_data, ttm_meta_data = ts.get_intraday(symbol = stock_symbol,interval='1min', outputsize='compact')
#df = ttm_data.reset_index()
# ------------------------------------------------------------------------------

# APP --------------
app = dash.Dash(__name__, external_stylesheets= [dbc.themes.FLATLY, dbc.icons.FONT_AWESOME],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )


# NavBar -------------------------------
search_callback = []
search_bar = dbc.Row([
    dbc.Col([
        dcc.Dropdown(
        options = search_callback, 
        id = 'search_stock_id',
        placeholder="Search Stocks"
        ),
    ]),
    dbc.Col([
        dbc.Button([html.I(className = "fa-solid fa-magnifying-glass"), " Search"],
        color="primary", className="ms-2", n_clicks=0
        ) 
    ], width="auto"),
])

### --- APP LAYOUT --- ###
app.layout = dbc.Container([search_bar]) 

# Callbacks -----------------------------------------
@app.callback(
    Output('search_stock_id','options'),
    Input('search_stock_id','value')
) 
def update_dropdown(value):
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={value}&apikey={key}'
    r = requests.get(url)
    data = r.json()
    print(data["bestMatches"]["1. symbol"]) 

# Run App --------------------------------------------
if __name__=='__main__':
    app.run_server(debug=True, port=3000)
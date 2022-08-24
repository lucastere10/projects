#libs
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

#start
external_stylesheets = [] #add hare the dash bootstrap style you want
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions'] = True


if __name__ == "__main__":
    app.run_server()
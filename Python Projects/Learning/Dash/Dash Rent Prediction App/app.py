#libs
from cProfile import run
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from assets import eda_dashboard, ml_analysis, dataframe

### - Styles - ####
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=dbc.themes.Flatly)
server = app.server
colors = {"background": "#F3F6FA", "background_div": "white", 'text': '#009999'}
app.config['suppress_callback_exceptions']= True

#load dataframe
#return  dataframe.df

### - LAYOUT - ###
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1('House Rent Prediction Dashboard', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

      dcc.Tabs(id="tabs", className="row", style={"margin": "2% 3%","height":"20","verticalAlign":"middle"}, value='dem_tab', children=[
        dcc.Tab(label='EDA Dashboard', value='eda_tab'),
        dcc.Tab(label='ML Analysis', value='ml_tab')
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])

def render_content(tab):
    if tab == 'eda_tab':
        return eda_dashboard.tab_1_layout
    elif tab == 'ml_tab':
        return ml_analysis.tab_1_layout

if __name__ == '__main__':
    app.run_server(debug=True)
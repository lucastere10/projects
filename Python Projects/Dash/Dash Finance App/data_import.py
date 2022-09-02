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
from alpha_vantage.timeseries import TimeSeries # pip install alpha-vantage

# -------------------------------------------------------------------------------
### Set up initial key and financial category ###
""" key = '1D0MB8E05Q6QOL2L' #Alpha API Key
ts = TimeSeries(key, output_format='pandas') # 'pandas' or 'json' or 'csv'
ttm_data, ttm_meta_data = ts.get_intraday(symbol='TTM',interval='1min', outputsize='compact')
df = ttm_data.iloc[:50].copy()
df=df.transpose()
df.rename(index={"1. open":"open", "2. high":"high", "3. low":"low",
                 "4. close":"close","5. volume":"volume"},inplace=True)
df=df.reset_index().rename(columns={'index': 'indicator'})
df = pd.melt(df,id_vars=['indicator'],var_name='date',value_name='rate')
df = df[df['indicator']!='volume']
print(df.head())
df.to_csv("Python Projects\Learning\Dash\Dash Finance App\data", index=False)
exit() """

#-----------------------------------------------------------------------------------

#read data
dff = pd.read_csv("Python Projects\\Dash\\Dash Finance App\\data\\ttm.csv")
dff = dff[dff.indicator.isin(['high'])]

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
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
CONTENT_STYLE = {               # the styles for the main content position it to the right of the sidebar
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Dark Theme ----------------------------------------------------
theme = {
    'dark': True,   
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

# Sidebar ---------------------------------
sidebar = html.Div([
        html.H6("LOGO", className="display-4"),
        html.I(className = "fa-solid fa-angles-right"),
        html.I(className = "fa-solid fa-angles-left"),
        daq.BooleanSwitch(
            on=True,
            color=theme['primary'],
            id='darktheme-daq-powerbutton',
            className='dark-theme-control'
        ),
        html.Hr(),#fa-solid fa-user
        dbc.Nav([
                dbc.NavLink([html.I(className = "fa-solid fa-house"), "  Home"], href="/", active="exact"),                
                html.Hr(),
                dbc.NavLink([html.I(className = "fa-solid fa-chart-bar"), "  Stocks"], href="/stocks", active="exact"),
                dbc.NavLink([html.I(className = "fa-solid fa-coins"), "  Crypto"], href="/crypto", active="exact"),
                dbc.NavLink([html.I(className = "fa-solid fa-eye"), "  Watchlist"], href="/watchlist", active="exact"),
                html.Hr(),
                dbc.NavLink([html.I(className = "fa-solid fa-circle-question"), "  Discover"], href="/discover", active="exact"),
                dbc.NavLink([html.I(className = "fa-solid fa-solid fa-money-bill-trend-up"), "  Trade Markets"], href="/markets", active="exact"),
                html.Hr(),
                dbc.NavLink([html.I(className = "fa-solid fa-user"), "  My Portfolio"], href="/portfolio", active="exact"),
                dbc.NavLink([html.I(className = "fa-solid fa-envelope"), "  Contact"], href="/contact", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),            
    ], style=SIDEBAR_STYLE,
)
content = html.Div(id="page-content", style=CONTENT_STYLE)

#card
card = dbc.Card([
        dbc.CardImg(src = 'assets/unnamed.png',
                    top = 'True',
                    style = {"width":'6rem'},
                    class_name = "rounded-circle",
        ),
        dbc.CardBody([
            dbc.Row([               # STOCK NAME AND TOKEN
                dbc.Col([
                    html.P('TATA Motors')
                ]),
                dbc.Col([
                    html.P('TTM')
                ]) 
            ]),
            dbc.Row([               #GRAPH
                dbc.Col([
                    dcc.Graph(id='daily-line', figure={},
                                config={'displayModeBar':False})
                ])
            ]),
            dbc.Row([               # CHANGE, SELL, BUY
                dbc.Col([
                    dbc.Button("CHANGE"),
                ]),
                dbc.Col([
                    dbc.Button("LOW"),
                ]),
                dbc.Col([
                    dbc.Button("HIGH"),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='indicator-graph',figure={},
                                config = {'displayModeBar': False})
                ], width = 4),
                dbc.Col([
                    dbc.Label(id='low-price', children="12.237")
                ], width = 4),
                dbc.Col([
                    dbc.Label(id='high-price', children="13.418")
                ], width = 4)
            ]),
        ])
    ], style={"width": "24rem"}, className="mt-3"
    )

### --- APP LAYOUT --- ###
app.layout = dbc.Container([
     # Cards ------
    dbc.Row([
        dbc.Col([html.Div(card)], width=6),
        dbc.Col([]),
        dbc.Col([]),
    ], justify='center'),
    dbc.Row([
        dbc.Col([]),
        dbc.Col([]),
        dbc.Col([]),
    ], justify='center'),
    dbc.Row([
        dbc.Col([]),
        dbc.Col([]),
        dbc.Col([]),
    ], justify='center'),

    # Invervals ------
    dcc.Interval(id='update', n_intervals=0, interval=1000*5),
    # Sidebar ------
    html.Div([dcc.Location(id="url"), sidebar, content]),
    # Search Bar ------

])

#### CALLBACKS ####

# update graph --------------------
@app.callback(
    Output('indicator-graph','figure'),
    Input('update', 'n_intervals')
)
def update_graph(timer):
    dff_rv = dff.iloc[::-1]
    day_start = dff_rv[dff_rv['date'] == dff_rv['date'].min()]['rate'].values[0]
    day_end = dff_rv[dff_rv['date'] == dff_rv['date'].max()]['rate'].values[0]
    fig = go.Figure(go.Indicator(
        mode="delta",
        value=day_end,
        delta={'reference': day_start, 'relative': True, 'valueformat':'.2%'}))
    fig.update_traces(delta_font={'size':12})
    fig.update_layout(height=30, width=70)

    if day_end >= day_start:
        fig.update_traces(delta_increasing_color='green')
    elif day_end < day_start:
        fig.update_traces(delta_decreasing_color='red')
    return fig

# line graph ------------------------
@app.callback(
    Output('daily-line', 'figure'),
    Input('update', 'n_intervals')
)
def update_graph(timer):
    dff_rv = dff.iloc[::-1]
    fig = px.line(dff_rv, x='date', y='rate',
                   range_y=[dff_rv['rate'].min(), dff_rv['rate'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                             paper_bgcolor='rgba(0,0,0,0)',
                                             plot_bgcolor='rgba(0,0,0,0)',
                                             yaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ),
                                             xaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ))

    day_start = dff_rv[dff_rv['date'] == dff_rv['date'].min()]['rate'].values[0]
    day_end = dff_rv[dff_rv['date'] == dff_rv['date'].max()]['rate'].values[0]

    if day_end >= day_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif day_end < day_start:
        return fig.update_traces(fill='tozeroy',
                             line={'color': 'red'})

# run some shit --------------------------------------------
if __name__=='__main__':
    app.run_server(debug=True, port=3000)
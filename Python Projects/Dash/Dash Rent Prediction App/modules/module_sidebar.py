from dash import dcc, html, State, Input, Output, no_update
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import dash_daq as daq                     # pip install dash_daq
import pandas as pd
from dash.exceptions import PreventUpdate

# Sidebar ------------------------------
sidebar = html.Div([
            dcc.Store(id='side-click'),
            dbc.Row([
                dbc.Col([
                    html.H6("LOGO", className="display-4", style={'fontSize': '2rem'}, id = 'logo-id')
                ],align = 'end'),
                dbc.Col([
                    dbc.Button(
                    html.I(className = "fa-solid fa-angles-right", id = "btn-sidebar-icon-id"),
                    outline=True, 
                    color="secondary", 
                    className="mr-1", 
                    id="btn-sidebar-id",
                    size="sm"
                    ),
                ]),
            ], justify = 'start'),
        html.Hr(),
        dbc.Nav([
                dbc.NavLink([html.I(className = "fa-solid fa-house"), "  Home"], 
                            href="/", active="exact", id = 'home-id'),                
                html.Hr(),
                dbc.NavLink([html.I(className = "fa-solid fa-chart-bar"), "  Stocks"], 
                            href="/stocks", active="exact", id = 'stocks-id'),
                dbc.NavLink([html.I(className = "fa-solid fa-coins"), "  Crypto"], 
                            href="/crypto", active="exact", id = 'crypto-id'),
                dbc.NavLink([html.I(className = "fa-solid fa-eye"), "  Overview"], 
                            href="/overview", active="exact", id = 'overview-id'),
                #dbc.NavLink([html.I(className = "fa-solid fa-solid fa-money-bill-trend-up"), "  Trade Markets"], href="/markets", active="exact"),
                html.Hr(),
                dbc.NavLink([html.I(className = "fa-solid fa-user"), "  My Portfolio"], 
                            href="/portfolio", active="exact", id = 'portfolio-id'),
                dbc.NavLink([html.I(className = "fa-solid fa-envelope"), "  Contact"], 
                            href="/contact", active="exact", id = 'contact-id'),
                html.Hr(),
                html.Br(),
                daq.ToggleSwitch(id='toggle-switch-id',value=False),
            ],
            vertical=True,
            pills=True,
        ),            
    ], style=SIDEBAR_STYLE,  id="sidebar-id",
)
### MOBILE ###
# Mobile Sidebar -------------
mobile_sidebar = html.Div([
    dbc.Row([
        dbc.Nav([
                dbc.NavLink([html.I(className = "fa-solid fa-house"), "  Home"], 
                            href="/", active="exact", id = 'mhome-id'),                
                dbc.NavLink([html.I(className = "fa-solid fa-chart-bar"), "  Stocks"], 
                            href="/stocks", active="exact", id = 'mstocks-id'),
                dbc.NavLink([html.I(className = "fa-solid fa-coins"), "  Crypto"], 
                            href="/crypto", active="exact", id = 'mcrypto-id'),
                dbc.NavLink([html.I(className = "fa-solid fa-eye"), "  Overview"], 
                            href="/overview", active="exact", id = 'moverview-id'),
            ],
            pills=True,
        ),
    ])            
],  id="msidebar-id",
)

# Mobile offcanvas menu ------------------------------
mobile_offcanvas = html.Div(
    [   dbc.Button([html.I(className = "fa-solid fa-bars")],
            color="primary", className="ms-2", n_clicks=0,  
            style={'font-size': '12px', 'display': 'inline-block'},
            id = 'mobile-offcanvas-button-id', size="sm"
            ),
        dbc.Offcanvas([
                html.Hr(),
                dbc.NavLink([html.I(className = "fa-solid fa-user"), "  My Portfolio"], 
                            href="/portfolio", active="exact", id = 'mportfolio-id'),
                dbc.NavLink([html.I(className = "fa-solid fa-envelope"), "  Contact"], 
                            href="/contact", active="exact", id = 'mcontact-id'),
                html.Hr(),
                dbc.Button([html.I(className = "fa-solid fa-address-book"), "  Hire Me"])
        ],
        id="mobile_offcanvas-id",
        title="LOGO",
        is_open=False,
        ),
    ]
)

### CALLBACKS ###
#sidebar colapse
def callback_sidebar_collapse(app):
    @app.callback(
        [   #layout
            Output("sidebar-id", "style"),
            Output("layout-id", "style"),
            Output("side-click", "data"),
            #orientation
            Output("btn-sidebar-icon-id",'className'),
            #logo
            Output('logo-id','hidden'),
            #icons
            Output('home-id','children'),
            Output('stocks-id','children'),
            Output('crypto-id','children'),
            Output('overview-id','children'),
            Output('portfolio-id','children'),
            Output('contact-id','children'),
            #Toggle Switch        
            Output('toggle-switch-id','vertical')
        ],
        [   Input("btn-sidebar-id", "n_clicks")],
        [   State("side-click", "data"),
        ]
    )
    def toggle_sidebar(n, nclick):
        if n:
            if nclick == "SHOW":
                #layout
                sidebar_style = SIDEBAR_HIDEN
                content_style = CONTENT_STYLE1
                cur_nclick = "HIDDEN"   
                #orientation  
                icon_orientation = "fa-solid fa-angles-left"
                #logo
                logo_hidden = True    
                #icons
                icon_home = [html.I(className = "fa-solid fa-house")]
                icon_stocks = [html.I(className = "fa-solid fa-chart-bar")]
                icon_crypto = [html.I(className = "fa-solid fa-coins")]
                icon_overview = [html.I(className = "fa-solid fa-eye")]
                icon_portfolio = [html.I(className = "fa-solid fa-user")]
                icon_contact =  [html.I(className = "fa-solid fa-envelope")]          
                #toggle
                toggle_vertical = True
            else:
                #layout    
                sidebar_style = SIDEBAR_STYLE
                content_style = CONTENT_STYLE
                cur_nclick = "SHOW"
                #orientation 
                icon_orientation = "fa-solid fa-angles-right"
                #logo
                logo_hidden = False
                #icons
                icon_home = [html.I(className = "fa-solid fa-house"), "  Home"]
                icon_stocks = [html.I(className = "fa-solid fa-chart-bar"), "  Stocks"]
                icon_crypto = [html.I(className = "fa-solid fa-coins"), "  Crypto"]
                icon_overview = [html.I(className = "fa-solid fa-eye"), "  Overview"]
                icon_portfolio = [html.I(className = "fa-solid fa-user"), "  My Portfolio"]
                icon_contact =  [html.I(className = "fa-solid fa-envelope"), "  Contact"]
                #toggle
                toggle_vertical = False
        else:
            #layout
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
            #orientation 
            icon_orientation = "fa-solid fa-angles-right"
            #logo
            logo_hidden = False
            #icons        
            icon_home = [html.I(className = "fa-solid fa-house"), "  Home"]
            icon_stocks = [html.I(className = "fa-solid fa-chart-bar"), "  Stocks"]
            icon_crypto = [html.I(className = "fa-solid fa-coins"), "  Crypto"]
            icon_overview = [html.I(className = "fa-solid fa-eye"), "  Overview"]
            icon_portfolio = [html.I(className = "fa-solid fa-user"), "  My Portfolio"]
            icon_contact =  [html.I(className = "fa-solid fa-envelope"), "  Contact"]
            #toggle
            toggle_vertical = False
        return [sidebar_style, content_style, cur_nclick,
                icon_orientation, logo_hidden,
                icon_home, icon_stocks, icon_crypto, icon_overview, icon_portfolio, icon_contact,
                toggle_vertical,]

# Open Mobile Offcanvas Menu 
def callback_open_mobile_offcanvas(app):
    @app.callback(
        Output("mobile_offcanvas-id", "is_open"),
        [Input("mobile-offcanvas-button-id", "n_clicks")],
        [State("mobile_offcanvas-id", "is_open")],
    )
    def toggle_offcanvas(n1, is_open):
        if not "mobile_offcanvas-id":
            raise PreventUpdate
        if n1:
            return not is_open
        return is_open
#---------------------------------------------
### LIBS ###
import sys
import dash  #pip install dash
from dash import html, dcc, Output, Input, callback        
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components

#import sys path
dash.register_page(__name__, path = '/contact')

name_input = dbc.FormFloating(
    [
        dbc.Input(type="text", placeholder="Shaka Zulu"),
        dbc.Label("Name"),
    ]
)

email_input = dbc.FormFloating(
    [
        dbc.Input(type="email", placeholder="example@internet.com"),
        dbc.Label("Email Address"),
    ]
)

message_input = dbc.FormFloating(
    [
        dbc.Input(type="text", placeholder="What is your need?", size="lg"),
        dbc.Label("Message"),
    ]
)

form = dbc.Form([
    dbc.Row([
        dbc.Col(name_input, width=6)
    ], justify= 'center'),
    html.Br(),
    dbc.Row([
        dbc.Col(email_input, width=6)
    ], justify= 'center'),
    html.Br(),
    dbc.Row([
        dbc.Col(message_input, width=6)
    ], justify= 'center'),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Button("Submit", color="primary"), width="auto"),
    ], justify="center"),
])

icons =  dbc.Row([
            dbc.Col([
                dbc.Button(html.I(
                    className= "fa-brands fa-linkedin"),  
                    className="rounded-circle",
                    href="https://www.linkedin.com/in/lucas-caldas50/", active="exact"
                ),
            ], width = 1),
            dbc.Col([
                dbc.Button(html.I(
                    className= "fa-solid fa-envelope"),  
                    className="rounded-circle",
                    href="lucasmedeiroscaldas@yahoo.com.br", active="exact"
                ),
            ], width = 1),
            dbc.Col([
                dbc.Button(html.I(
                    className= "fa-brands fa-github"),  
                    className="rounded-circle",
                    href="https://github.com/lucastere10", active="exact"
                ),
            ], width = 1),
            dbc.Col([
                dbc.Button(html.I(
                    className= "fa-brands fa-instagram"),  
                    className="rounded-circle",
                    href="	https://www.instagram.com/lucas.mcaldas/", active="exact"
                )
            ], width = 1),
            dbc.Col([
                dbc.Button(html.I(
                    className= "fa-brands fa-file"),  
                    className="rounded-circle",
                    href="https://drive.google.com/file/d/1lFKemF02INTZ-tgHS3f1Qm5b0wr52bLF/view?usp=sharing", active="exact"
                )
            ], width = 1),
        ], justify="center")

layout = html.Div([
            dbc.Row([
                dbc.Col(html.H4("Contact"), width="auto"),
            ], justify="center"),
            dbc.Row([
                dbc.Col(html.P(
                    'Want do send a feedback? You can fill in the contact form below'
                        ), width="auto"),
            ], justify="center"),
            dbc.Row([
                dbc.Col(html.P(
                    'Follow me on the social channels below.'
                        ), width="auto"),
            ], justify="center"),
            html.Br(),
            icons,
            html.Hr(),
            form
])
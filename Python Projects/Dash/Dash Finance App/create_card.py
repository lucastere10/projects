from dash import dcc, html, State, Input, Output
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components

def create_card(card_id, title, description):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, id=f"{card_id}-title"),
                html.H2("100", id=f"{card_id}-value"),
                html.P(description, id=f"{card_id}-description")
            ]
        )
    )
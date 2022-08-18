# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc

# Define the navbar structure
def navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(
                    dbc.NavLink(
                        "Preprocessing", href="/preprocessing"
                    )
                ),
                
                dbc.NavItem(
                    dbc.NavLink(
                        "Dashboard", href="/dashboard"
                    )
                )
            ] ,
            brand="Home",
            brand_href="/home",
            brand_style={
                'fontSize': '15px', 
                'fontWeight': '700'
            },
            color='#92D050',
            dark=True,
            style={
                'color': 'white',
                'fontSize': '15px', 
                'fontWeight': '700',
                'height': "4vh"
            }
        ), 
    ])

    return layout
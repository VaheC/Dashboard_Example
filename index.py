# Import necessary libraries 
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# import flask
# from random import randint


# Connect to main app.py file
# from app import app

# Connect to your app pages
import preprocessing, home#, dashboard

# Connect the navbar to the index
from components import navbar

# Define the navbar
nav = navbar()

# server = flask.Flask(__name__)
# server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))

app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True) # server=server
server = app.server

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav, 
    html.Div(id='page-content', children=[]), 
])

# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dashboard':
        # return dashboard.layout
        return preprocessing.layout
    elif pathname == '/preprocessing':
        return preprocessing.layout
    elif pathname == '/home':
        return home.layout
    else: # if redirected to unknown link
        return home.layout #"404 Page Error! Please choose a link"

# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True)
# Import necessary libraries 
from dash import html
import dash_bootstrap_components as dbc
import os
import base64

# finding logo path
cwd_path = os.getcwd()
logo_file_name = 'enerwise_logo_varviline.png'
logo_path = os.path.join(cwd_path, logo_file_name)
encoded_image = base64.b64encode(open(logo_path, 'rb').read())

# Define the page layout
layout = dbc.Container([
    dbc.Row(
        [
         
            dbc.Col([
                # html.Br(),
                # html.Br(),
                # html.Br(),
                # html.Br(),
                html.Div(
                    children=[
                        html.Div(
                            html.Img(
                                src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                style={'height':'30%', 'width':'50%'}
                            )
                        ),
                        html.Div(
                            children='PUMP MONITORING', 
                            style={
                                'color': 'white', 
                                'fontSize': '30px', 
                                'fontWeight': '700', 
                                #"margin-left": "5px"
                            }
                        )
                    ], 
                    style={
                        #'display': 'inline-block', 
                        #'width': '50%', 
                        #'position': 'fixed', 
                        #'height': '50%',
                        'backgroundColor': '#92D050'
                    },
                    id='body'
                )
            ])
        ],
        align="center",
        justify="center",
        style={"height": "100vh"}
    )
])
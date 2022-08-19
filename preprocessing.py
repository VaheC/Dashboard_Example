# Import necessary libraries 
import dash
from dash import html, dcc, Input, Output, State, ctx, callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from mongo_funcs import *
import base64
import io

layout = dbc.Container(
    [
         dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Upload(html.Button('Upload File'), id='upload'),
                        html.Br(),
                        html.Span("", id='upload_text')
                    ],
                    width=2
                ),

                dbc.Col(
                    [
                        #dbc.Label("MongoDB User"),
                        dbc.Input(placeholder="MongoDB User", type="text", id='user'),
                        html.Br(),
                        dbc.Input(placeholder="MongoDB Password", type="text", id='password'),
                        html.Br(),
                        dbc.Input(placeholder="MongoDB Database", type="text", id='database'),
                        html.Br(),
                        dbc.Input(placeholder="MongoDB Table", type="text", id='table'),
                        # html.Br(),
                        # dbc.Input(placeholder="Start Time", type="text", id='stime'),
                        # html.Br(),
                        # dbc.Input(placeholder="End Time", type="text", id='etime'),
                    ],
                    width=3
                ),

                dbc.Col(
                    [
                        dbc.Button('Insert Data', id='insert', style={'width': '49%'}), #, size="lg"
                        html.Br(),
                        html.Br(),
                        dbc.Button('Delete Database', id='delete_db', style={'width': '49%'}),
                        html.Br(),
                        html.Br(),
                        dbc.Button('Delete Table', id='delete_table', style={'width': '49%'}),
                        # html.Br(),
                        # html.Br(),
                        # dbc.Button('Delete Data', id='delete_data', style={'width': '49%'}),
                        html.Br(),
                        html.Br(),
                        html.Span("", id='output_text')
                    ],
                    width={'offset': 1, 'size': 4}
                    # dcc.RadioItems(
                    #     options=['Mean', 'Median', 'FFill'],
                    #     value='Mean',
                    #     id='radio',
                    #     # style={
                    #     #     #'font-size': '12px',
                    #     #     'color': 'white',
                    #     #     #"margin-right": "5px"
                    #     # },
                    #     inline=True,
                    #     inputStyle={"margin-right": "5px", "margin-left": "5px"}
                    # )
                ),

                dbc.Col(
                    [
                        html.Span('Fillna method'),
                        html.Br(),
                        dcc.Dropdown(
                            options=['Mean', 'Median', 'FFill'],
                            value='Mean',
                            id='na_option', 
                            #optionHeight=20,
                            style={
                                # 'height':height,
                                # 'margin-top':   '0px',
                                # 'margin-left':  '10px',
                                'width': '80%',
                                'font-size': '12px'
                            }
                        ),
                        html.Br(),
                        html.Br(),
                        dbc.Button('Save', id='save', style={'width': '49%'}),
                        html.Br(),
                        html.Br(),
                        html.Span("", id='save_text')
                    ],
                    width=2
                )
            ],
            align="center",
            justify="center",
            style={"height": "100vh"}
        )
    ]   
)

def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    return df

def save_cred(user, password):
    cred_list = [user, password]
    with open('cred_file.txt', 'w') as file:
        file.write(' '.join(cred_list))

@callback(
    Output('upload_text', 'children'),
    Output('output_text', 'children'),
    Output('save_text', 'children'),
    inputs=[
        Input('insert', 'n_clicks'),
        Input('delete_db', 'n_clicks'),
        Input('delete_table', 'n_clicks'),
        Input('save', 'n_clicks'),
        # Input('delete_data', 'n_clicks'),
        # Input('upload', 'contents')
    ],
    state=[
        State('user', 'value'),
        State('password', 'value'),
        State('database', 'value'),
        State('table', 'value'),
        # State('stime', 'value'),
        # State('etime', 'value'),
        State('upload', 'contents'),
        State('na_option', 'value')
    ]
)
def click_button(n_ins, n_ddb, n_dt, n_s, user, password, database, table, upload_content, nafill_option): # n_dd, stime, etime, 
    # if ctx.triggered[0]["prop_id"] == "upload.contents":
    #     return 'Upload completed!!!', ''

    if ctx.triggered[0]["prop_id"] == "insert.n_clicks":

        save_cred(user=user, password=password)

        data = parse_contents(contents=upload_content)

        if len(database) > 0:
            insert_data(user=user, password=password, data=data, table_name=table, db_name=database)
        else:
            insert_data(user=user, password=password, data=data, table_name=table, db_name='enerwise')
        return '', 'Data inserted!!!', ''

    elif ctx.triggered[0]["prop_id"] == "delete_db.n_clicks":

        save_cred(user=user, password=password)

        if len(database) > 0:
            delete_db(user=user, password=password, db_name=database)
        else:
            delete_db(user=user, password=password, db_name='enerwise')
        return '', 'Database deleted!!!', ''

    elif ctx.triggered[0]["prop_id"] == "delete_table.n_clicks":

        save_cred(user=user, password=password)

        if len(database) > 0:
            delete_table(user=user, password=password, table_name=table, db_name=database)
        else:
            delete_table(user=user, password=password, table_name=table, db_name='enerwise')
        return '', 'Table deleted!!!', ''

    elif ctx.triggered[0]["prop_id"] == "save.n_clicks":

        with open('fillna_method.txt', 'w') as file:
            file.write(nafill_option)

        return '', '', 'Method saved!!!'

    else:
        raise PreventUpdate
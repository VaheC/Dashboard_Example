# Run this app with `python dash_app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# loading some packages
from dash import Dash, html, dcc, dash_table, Input, Output, State, ctx, callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from datetime import datetime as dt
import pandas as pd
from load_data import *
from mongo_funcs import get_data
from make_plotly_charts import *
import json
import os
import base64

# app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN], #BOOTSTRAP, COSMO, LUMEN
#     meta_tags=[{'name': 'viewport',
#                'content': 'width=device-width, initial-scale=1.0'}]
# )

# loading data for charts 1, 3, 4, and 5
# data_pump1 = load_main(filename='main_data_PUMP1.csv')

# data_pump2 = load_main(filename='main_data_PUMP2.csv')

with open('cred_file.txt', 'r') as file:
    line = file.readline()
user = line.split(' ')[0]
password = line.split(' ')[1]

with open('fillna_method.txt', 'r') as file:
    fillna_option = file.readline()

def fill_missing(df, fillna_option):

    temp_df = df.copy()

    temp_df['Time'] = pd.to_datetime(temp_df['Time'])
    temp_df.sort_values('Time', ascending=True, inplace=True)

    if fillna_option == 'FFill':
        temp_df.fillna(method='ffill', inplace=True)
    elif fillna_option == 'Mean':
        temp_df.fillna(temp_df.mean(), inplace=True)
    else:
        temp_df.fillna(temp_df.median(), inplace=True)

    return temp_df

#try:
data_pump1 = get_data(user=user, password=password, table_name='pump1', db_name='enerwise')
data_pump1 = fill_missing(df=data_pump1, fillna_option=fillna_option)

data_pump2 = get_data(user=user, password=password, table_name='pump2', db_name='enerwise')
data_pump2 = fill_missing(df=data_pump2, fillna_option=fillna_option)

data_chart2 = get_data(user=user, password=password, table_name='chart2', db_name='enerwise')

# except:
#     data_pump1 = load_main(filename='main_data_PUMP1.csv')

#     data_pump2 = load_main(filename='main_data_PUMP2.csv')

#     data_chart2 = pd.read_csv('data_chart2.csv')

data = data_pump1.copy()

# loading data for chart 2
data_chart2 = pd.read_csv('data_chart2.csv')

# calculating the KPIs
kpi_dict = calculate_kpi(df=data)

# constructing the table
table_df = create_summary_table(df_main=data, df_period=data)
fig_table = create_table(df=table_df)

# creating charts
fig_chart2 = create_chart2(df=data_chart2)
# fig_chart3 = create_chart3(df=data)
# fig_chart4 = create_chart4(df=data)
fig_chart3_4 = create_chart3_4(df=data)
fig_chart5 = create_chart5(df=data)
fig_chart1 = create_chart1(df=data)

# finding logo path
cwd_path = os.getcwd()
logo_file_name = 'enerwise_logo_varviline.png'
logo_path = os.path.join(cwd_path, logo_file_name)
encoded_image = base64.b64encode(open(logo_path, 'rb').read())

layout = dbc.Container(
    [  
        dbc.Row(
            dbc.Col(
                [
                    html.Div(
                        children = [
                            html.Div(
                                children=[
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
                                            ),

                                            html.Div(
                                                dcc.Dropdown(
                                                    options=['Pump1', 'Pump2'],
                                                    value='Pump 1',
                                                    id='dpump', 
                                                    #optionHeight=20,
                                                    style={
                                                        # 'height':height,
                                                        # 'margin-top':   '0px',
                                                        # 'margin-left':  '10px',
                                                        'width': '60%',
                                                        'font-size': '12px'
                                                    }
                                                ),
                                            )
                                        ], 
                                        style={
                                            'display': 'inline-block', 
                                            'width': '50%', 
                                            #'position': 'fixed', 
                                            'height': '165px',
                                            #'backgroundColor': '#92D050'
                                        }
                                    ),
                                    html.Div(
                                        children=[
                                            html.Div(
                                                children=[
                                                    #html.Br(),
                                                    html.Span(
                                                        'Power usage average; kW', 
                                                        style={
                                                            'color': 'white',
                                                            'textAlign': 'center',
                                                            'fontSize': '10px'
                                                        }
                                                    ),
                                                    html.Br(),
                                                    html.Br(),
                                                    html.Hr(style={'color':'white'}),
                                                    html.Span(
                                                        id='puakw', 
                                                        children=f"{kpi_dict['POWER USAGE AVERAGE; kW']:.0f}",
                                                        style={
                                                            'fontWeight': '700', 
                                                            'fontSize': '36px', 
                                                            'color': 'white', 
                                                            #'marginLeft': '20px'
                                                        }
                                                    ),
                                                    html.Br(),
                                                    html.Span(
                                                        id='pudkw', 
                                                        children=f"{kpi_dict['POWER USAGE DIFFERENCE; kW']:.0f}%",
                                                        style={
                                                            'fontWeight': '700', 
                                                            'fontSize': '18px', 
                                                            'color': 'red', 
                                                            'marginLeft': '50px'
                                                        }
                                                    )
                                                ], 
                                                style={
                                                    #'backgroundColor': '#92D050',
                                                    'width': '100px',
                                                    'height': '90px',
                                                    'textAlign': 'center',
                                                    'float': 'left',
                                                    'fontSize': '10px',
                                                    'fontWeight': '700',
                                                }
                                            ),
                                            html.Div(
                                                children=[
                                                    #html.Br(),
                                                    html.Span(
                                                        'Average efficiency; %',
                                                        style={
                                                            'color': 'white',
                                                            'textAlign': 'center'
                                                        }
                                                    ),
                                                    html.Br(),
                                                    html.Br(),
                                                    html.Br(),
                                                    html.Hr(style={'color':'white'}),
                                                    html.Span(
                                                        id='ae', 
                                                        children=f"{kpi_dict['AVERAGE EFFICIENCY']:.0f}",
                                                        style={
                                                            'fontWeight': '700', 
                                                            'fontSize': '36px', 
                                                            'color': 'white', 
                                                            #'marginLeft': '20px'
                                                        }
                                                    ),
                                                    html.Br(),
                                                    html.Span(
                                                        id='pcpbo', 
                                                        children=f"{kpi_dict['PER CENT POINTS BELOW OPTIMUM']:.0f}pp",
                                                        style={
                                                            'fontWeight': '700', 
                                                            'fontSize': '18px', 
                                                            'color': 'red', 
                                                            'marginLeft': '50px'
                                                        }
                                                    )
                                                ], 
                                                style={
                                                    #'backgroundColor': '#92D050',
                                                    'width': '100px',
                                                    'height': '90px',
                                                    'textAlign': 'center',
                                                    'float': 'left',
                                                    'marginLeft': '10px',
                                                    'fontSize': '10px',
                                                    'fontWeight': '700'
                                                }
                                            ),
                                            html.Div(
                                                children=[
                                                    #html.Br(),
                                                    html.Span(
                                                        'Average specific energy consumption; kW/m3/h',
                                                        style={
                                                            'color': 'white',
                                                            'textAlign': 'center'
                                                        }
                                                    ),
                                                    html.Hr(style={'color':'white'}),
                                                    html.Span(
                                                        id='asec', 
                                                        children=f"{kpi_dict['AVERAGE SPECIFIC ENERGY CONSUMPTION']:.1f}",
                                                        style={
                                                            'fontWeight': '700', 
                                                            'fontSize': '36px', 
                                                            'color': 'white', 
                                                            #'marginLeft': '20px'
                                                        }
                                                    ),
                                                    html.Br(),
                                                    html.Span(
                                                        id='pcbo', 
                                                        children=f"{kpi_dict['PER CENT BELOW OPTIMUM']:.0f}%",
                                                        style={
                                                            'fontWeight': '700', 
                                                            'fontSize': '18px', 
                                                            'color': 'red', 
                                                            'marginLeft': '50px'
                                                        }
                                                    )
                                                ], 
                                                style={
                                                    #'backgroundColor': '#92D050',
                                                    'width': '100px',
                                                    'height': '90px',
                                                    'textAlign': 'center',
                                                    'float': 'left',
                                                    'marginLeft': '10px',
                                                    'fontSize': '10px',
                                                    'fontWeight': '700'
                                                }
                                            )
                                        ], 
                                        style={
                                            'display': 'inline-block', 
                                            'width': '50%',
                                            'height': '165px', 
                                            'float': 'right',
                                            #'position': 'fixed',
                                            #'left': '340px',
                                            #'backgroundColor': '#92D050'
                                        }
                                    )
                                ], 
                                style = {
                                    #'backgroundColor': '#92D050', 
                                    'height': '165px', 
                                    'width': '50%', 
                                    'display': 'inline-block'
                                }
                            ), 
                            html.Div(
                                children=[
                                    # dcc.RadioItems(
                                    #     options=['Pump1', 'Pump2'],
                                    #     value='Pump1',
                                    #     id='radio',
                                    #     style={
                                    #         #'font-size': '12px',
                                    #         'color': 'white',
                                    #         #"margin-right": "5px"
                                    #     },
                                    #     inline=True,
                                    #     inputStyle={"margin-right": "5px", "margin-left": "5px"}
                                    # ),
                                    html.Br(),
                                    dcc.Dropdown(
                                        options=[col for col in data.columns 
                                                 if col not in ['Time', 'PEN5 A', 
                                                                'PEN5 P2 bar', 'PEN4 P2 bar']],
                                        value = ['Pump flow according to H; m3/h'],
                                        id='yaxis', 
                                        multi=True,
                                        optionHeight=20,
                                        style={
                                            # 'height':height,
                                            # 'margin-top':   '0px',
                                            # 'margin-left':  '10px',
                                            'font-size': '10px'}
                                    ),
                                ], 
                                style={
                                    'width': '35%', 
                                    'height': '165px', 
                                    'display': 'inline-block', 
                                    'float': 'right',
                                    'paddingLeft': '5px'
                                    #'position': 'fixed',
                                    #'left': '65%',#'950px',
                                    #'backgroundColor': '#92D050'
                                }
                            ),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=[
                                            html.Label('Start time', style={'color': 'white'}),
                                            html.Br(),
                                            dcc.Input(value=data['Time'].iloc[0].strftime("%Y-%m-%d %H:%M:%S"), type='text', id='start_time'),
                                            #html.Button('Filter', id='button1'),
                                            html.Br(),
                                            html.Label('End time', style={'color': 'white'}),
                                            html.Br(),
                                            dcc.Input(value=data['Time'].iloc[-1].strftime("%Y-%m-%d %H:%M:%S"), type='text', id='end_time'),
                                            html.Br(),
                                            html.Br(), 
                                            html.Button('Filter', id='button')
                                        ], 
                                    ),
                                ],
                                style={
                                    'width': '15%', 
                                    'height': '165px', 
                                    'display': 'inline-block', 
                                    'float': 'right',
                                    #'position': 'fixed',
                                    #'backgroundColor': '#92D050'
                                }
                            )
                        ], 
                        style = {
                            'backgroundColor': '#92D050',
                            'fontFamily': 'Source Sans Pro',
                            'zIndex': 2147483647,
                            'position': 'fixed',
                            # 'height': '165px'
                        }
                    ),
                ],
                xs=12, sm=12, md=12, lg=12, xl=12
                #color="#92D050",
                #fluid=True,
                #fixed='top',
                # style={
                #     'display': 'flex',

                # }
            ),
            # style = {
            #     'zIndex': 2147483647,
            #     'backgroudColor': "#92D050"
            # }
        ),
        
        #chart 1
        dbc.Row(
            dbc.Col(
                [
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dcc.Graph(
                        id='chart1', 
                        figure=fig_chart1, 
                        config = {
                            'displaylogo': False,
                            'modeBarButtonsToRemove': [
                                "zoomIn2d" , "zoomOut2d", "resetScale2d",
                                "pan2d", "lasso2d", "select2d"
                            ],
                           'modeBarButtonsToAdd': ["toggleSpikelines"] 
                        },
                        responsive=True,
                        style={'width': '97.77vw', 'height': '70vh'}
                    )
                ],
                #width=12
                xs=12, sm=12, md=12, lg=12, xl=12
            )
        ),
        # chart 3, 4, 2
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        dcc.Graph(
                            id="chart3_4", 
                            figure=fig_chart3_4, 
                            config = {
                                'displaylogo': False,
                                'modeBarButtonsToRemove': [
                                    "zoomIn2d" , "zoomOut2d", "resetScale2d",
                                    "pan2d", "lasso2d", "select2d"
                                ],
                                'modeBarButtonsToAdd': ["toggleSpikelines"]
                            },
                            responsive=True,
                            style={'width': '48.525vw', 'height': '70vh'}
                        )
                    ],
                    xs=12, sm=12, md=12, lg=6, xl=6
                ),
                dbc.Col(
                    [
                        html.Br(),
                        dcc.Graph(
                            id="chart2", 
                            figure=fig_chart2, 
                            config = {
                                'displaylogo': False,
                                'modeBarButtonsToRemove': [
                                    "zoomIn2d" , "zoomOut2d", "resetScale2d",
                                    "pan2d", "lasso2d", "select2d"
                                ],
                                'modeBarButtonsToAdd': ["toggleSpikelines"]
                            },
                            responsive=True,
                            style={'width': '48.525vw', 'height': '70vh'}
                        )
                    ],
                    #width={'size': 4}
                    xs=12, sm=12, md=12, lg=6, xl=6
                ),
            ]
        ),
        # table and chart 5
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        dcc.Graph(
                            id="table", 
                            figure=fig_table,
                            config = {
                                'displaylogo': False
                            },
                            responsive=True,
                            style={'width': '48.525vw', 'height': '70vh'}
                        )
                    ],
                    xs=12, sm=12, md=12, lg=6, xl=6
                ),
                dbc.Col(
                    [
                        html.Br(),
                        dcc.Graph(
                            id="chart5", 
                            figure=fig_chart5,
                            config = {
                                'displaylogo': False,
                                'modeBarButtonsToRemove': [
                                    "zoomIn2d" , "zoomOut2d", "resetScale2d",
                                    "pan2d", "lasso2d", "select2d"
                                ],
                                'modeBarButtonsToAdd': ["toggleSpikelines"]
                            },
                            responsive=True,
                            style={'width': '48.525vw', 'height': '70vh'}
                        )
                    ],
                    xs=12, sm=12, md=12, lg=6, xl=6
                )
            ]
        ),
        dbc.Row(
            [
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
            ]
        ),
        dcc.Store(id='selected_point'),
        dcc.Store(id='selected_range'),
        dcc.Store(id='pump')
    ],
fluid=True
)

@callback(
    Output('selected_point', 'data'),
    Output('chart1', 'clickData'),
    Output('chart3_4', 'clickData'),
    #Output('chart4', 'clickData'),
    Output('chart5', 'clickData'),
    inputs=[
        Input('chart1', 'clickData'),
        Input('chart3_4', 'clickData'),
        #Input('chart4', 'clickData'),
        Input('chart5', 'clickData'),
        Input('chart1', 'relayoutData'),
        Input('chart3_4', 'relayoutData'),
        #Input('chart4', 'relayoutData'),
        Input('chart5', 'relayoutData'),
        #Input('radio', 'value')
    ],
    state=[
        State('selected_point', 'data'),
        State('start_time', 'value'),
        State('end_time', 'value'),
        State('selected_range', 'data'),
        State('dpump', 'value'),
        State('pump', 'data'),
        #State('pump_data', 'data')
    ]
)
def save_click_point(clickData1, clickData2, clickData3, # clickData4,
                     relayoutData1, relayoutData2, relayoutData3, # relayoutData4,
                     temp_dic, start_time, end_time, range_xy, dpump_value,
                     pump_changed):#, pump_data, pump_changed

    if pump_changed is None:
        pump_changed = {}
        if temp_dic is None:
            pump_changed['point_dict'] = {}
        else:
            pump_changed['point_dict'] = json.loads(temp_dic)

        if range_xy is None:
            pump_changed['range_dict'] = {}
        else:
            pump_changed['range_dict'] = json.loads(range_xy)
        # pump_changed['changed'] = False
        # pump_changed['pump'] = dpump_value
    else:
        pump_changed = json.loads(pump_changed)

    if dpump_value == 'Pump1' or dpump_value is None:
        # data = pd.DataFrame(pump_data['Pump1'])
        data = data_pump1.copy()
    else:#elif dpump_value == 'Pump2':
        # data = pd.DataFrame(pump_data['Pump2'])
        data = data_pump2.copy()
    # data['Time'] = pd.to_datetime(data['Time'])

    if temp_dic is None:
        temp_dic = {}
    else:
        if len(pump_changed['point_dict']) == 0 and len(pump_changed['range_dict']) == 0:
            temp_dic = {}
        else:
            temp_dic = json.loads(temp_dic)

    range_xy = json.loads(range_xy)
    if len(pump_changed['point_dict']) == 0 and len(pump_changed['range_dict']) == 0:
        range_xy = {}

    temp_list = [relayoutData1, relayoutData2, relayoutData3]#, relayoutData4]
    list_index = [i for i in range(len(temp_list)) if temp_list[i] is not None]

    if len(list_index) == 0 and len(range_xy) == 0:
        temp_dic = {}
    elif ('autorange' in range_xy or 'dragmode' in range_xy or 'showspikes' in range_xy ) and 'range_index' not in range_xy:
        temp_dic = {}


    if range_xy is not None: # or len(range_xy) != 0:
        if 'range_index' not in range_xy:
            start_date = pd.to_datetime(start_time)
            end_date = pd.to_datetime(end_time)
            selected_data = data[(data['Time']>=start_date) & (data['Time']<=end_date)]
        else:
            if 'temp_data' not in range_xy:
                selected_data = data[data.index.isin(range_xy['range_index'])]
            else:
                selected_data = pd.DataFrame(range_xy['temp_data'])
                selected_data['Time'] = pd.to_datetime(selected_data['Time'])
                selected_data.set_index('init_pos', inplace=True)
    else:
        start_date = pd.to_datetime(start_time)
        end_date = pd.to_datetime(end_time)
        selected_data = data[(data['Time']>=start_date) & (data['Time']<=end_date)]

    index_list_last = list(selected_data.index)
    selected_data.reset_index(drop=True, inplace=True)

    chart5_data1 = selected_data['Mechanical power - measured; kW'].to_frame()
    chart5_data1 = chart5_data1.sort_values('Mechanical power - measured; kW', 
                                            ascending=False)
    chart5_data1['Tunnid'] = 1
    chart5_data1['Tunnid'] = chart5_data1['Tunnid'].cumsum()
    chart5_data1['Tunnid'] = 100 * chart5_data1['Tunnid'] / chart5_data1['Tunnid'].shape[0]
    chart5_data1.reset_index(inplace=True)
    chart5_data1.rename(columns={'index': 'init_pos'}, inplace=True)

    chart5_data2 = selected_data['Pump flow according to H; m3/h'].to_frame()
    chart5_data2 = chart5_data2.sort_values('Pump flow according to H; m3/h', 
                                            ascending=False)
    chart5_data2['Tunnid'] = 1
    chart5_data2['Tunnid'] = chart5_data2['Tunnid'].cumsum()
    chart5_data2['Tunnid'] = 100 * chart5_data2['Tunnid'] / chart5_data2['Tunnid'].shape[0]
    chart5_data2.reset_index(inplace=True)
    chart5_data2.rename(columns={'index': 'init_pos'}, inplace=True)

    click_list = [clickData1, clickData2, clickData3]#, clickData4]
    click_list_index = [i for i in range(len(click_list)) if click_list[i] is not None]

    if len(click_list_index) != 0:
        click_index = click_list_index[0]
        if clickData3 is None:
            temp_index = click_list[click_index]["points"][0]["pointIndex"]
            if len(list_index) != 0:
                temp_index = index_list_last.index(temp_index)
            #temp_index = index_list_last.index(temp_index)
            temp_index_mpmkw = list(chart5_data1[chart5_data1["init_pos"]==temp_index].index)[0]
            temp_index_pfah = list(chart5_data2[chart5_data2['init_pos']==temp_index].index)[0]
        else:
            temp_index = clickData3["points"][0]["pointIndex"]
            temp_index_mpmkw = temp_index
            temp_index_pfah = temp_index
            if clickData3['points'][0]['y'] == chart5_data1["Mechanical power - measured; kW"].iloc[temp_index]:
                temp_index = int(chart5_data1['init_pos'].iloc[temp_index])
            else:
                temp_index = int(chart5_data2['init_pos'].iloc[temp_index])

        temp_dic['point_index'] = temp_index
        temp_dic['chart5_point_index'] = [temp_index_mpmkw, temp_index_pfah]
    else:
        if len(temp_dic) != 0:
            temp_dic['point_index'] = index_list_last.index(temp_dic['point_index'])
            temp_index_mpmkw = list(chart5_data1[chart5_data1["init_pos"]==temp_dic['point_index']].index)[0]
            temp_index_pfah = list(chart5_data2[chart5_data2['init_pos']==temp_dic['point_index']].index)[0]
            temp_dic['chart5_point_index'] = [temp_index_mpmkw, temp_index_pfah]

    return json.dumps(temp_dic), None, None, None

@callback(
    Output('selected_range', 'data'),
    Output('chart1', 'relayoutData'),
    Output('chart3_4', 'relayoutData'),
    #Output('chart4', 'relayoutData'),
    Output('chart5', 'relayoutData'),
    inputs=[
        Input('chart1', 'relayoutData'),
        Input('chart3_4', 'relayoutData'),
        #Input('chart4', 'relayoutData'),
        Input('chart5', 'relayoutData'),
        #Input('radio', 'value')
    ],
    state=[
        State('selected_range', 'data'),
        State('start_time', 'value'),
        State('end_time', 'value'),
        State('yaxis', 'value'),
        State('dpump', 'value'),
        State('pump', 'data'),
        # State('pump_data', 'data')
    ]
)
def save_selected_range(relayoutData1, relayoutData2, relayoutData3, #relayoutData4, 
                        temp_dic, start_time, end_time, yaxis_values, 
                        dpump_value, pump_changed): # , pump_data

    if pump_changed is None:
        pump_changed = {}
        # pump_changed['changed'] = False
        # pump_changed['pump'] = dpump_value
        pump_changed['point_dict'] = {}
        if temp_dic is None:
            pump_changed['range_dict'] = {}
        else:
            pump_changed['range_dict'] = json.loads(temp_dic)
    else:
        pump_changed = json.loads(pump_changed) 

    if dpump_value == 'Pump1' or dpump_value is None:
        # data = pd.DataFrame(pump_data['Pump1'])
        data = data_pump1.copy()
    else:
        # data = pd.DataFrame(pump_data['Pump2'])
        data = data_pump2.copy()
    # data['Time'] = pd.to_datetime(data['Time'])

    if temp_dic is None:
        temp_dic = {}
    else:
        if len(pump_changed['point_dict']) == 0 and len(pump_changed['range_dict']) == 0:
            temp_dic = {}
        else:
            temp_dic = json.loads(temp_dic)

    temp_list = [relayoutData1, relayoutData2, relayoutData3]#, relayoutData4]
    list_index = [i for i in range(len(temp_list)) if temp_list[i] is not None]

    if len(list_index) == 0:
        temp_dic = {}
        #return json.dumps(temp_dic), None, None, None, None
    else:
        relay_index = list_index[0]

        if 'xaxis.autorange' in temp_list[relay_index]:
            #if relayoutData1['xaxis.autorange']:
            temp_dic = {}
            temp_dic['autorange'] = True
            #return json.dumps(temp_dic), None, None, None, None

        elif 'dragmode' in temp_list[relay_index]:
            temp_dic = {}
            temp_dic['dragmode'] = True
            #return json.dumps(temp_dic), None, None, None, None

        elif 'xaxis.showspikes' in temp_list[relay_index]:
            temp_dic = {}
            temp_dic['showspikes'] = True

        elif 'autosize' in temp_list[relay_index]:
            temp_dic = {}
            temp_dic['autosize'] = True

        else:
            if 'temp_data' not in temp_dic:

                start_date = pd.to_datetime(start_time)
                end_date = pd.to_datetime(end_time)
                selected_data = data[(data['Time']>=start_date) & (data['Time']<=end_date)]
                selected_data.reset_index(drop=True, inplace=True)

            else:
                selected_data = pd.DataFrame(temp_dic['temp_data'])
                selected_data['Time'] = pd.to_datetime(selected_data['Time'])
                selected_data.set_index('init_pos', inplace=True)
                selected_data.reset_index(drop=True, inplace=True)

            if 'xaxis.range[0]' in temp_list[relay_index].keys():
                xmin = temp_list[relay_index]['xaxis.range[0]']
                xmax = temp_list[relay_index]['xaxis.range[1]']

                ymin = temp_list[relay_index]['yaxis.range[0]']
                ymax = temp_list[relay_index]['yaxis.range[1]']
            else:
                xmin = temp_list[relay_index]['xaxis2.range[0]']
                xmax = temp_list[relay_index]['xaxis2.range[1]']

                ymin = temp_list[relay_index]['yaxis2.range[0]']
                ymax = temp_list[relay_index]['yaxis2.range[1]']

            if relay_index == 0:
                xmin = pd.to_datetime(xmin)
                xmax = pd.to_datetime(xmax)

                temp_index_list = list(
                    selected_data[
                        (selected_data['Time'].between(xmin, xmax)) &
                        (selected_data[yaxis_values[0]].between(ymin, ymax))
                    ].index
                )
            elif relay_index == 1:
                if 'xaxis.range[0]' in temp_list[relay_index].keys():
                    temp_index_list = list(
                        selected_data[
                            (selected_data['Pump flow according to H; m3/h'].between(xmin, xmax)) & 
                            (selected_data["Head; mH2O"].between(ymin, ymax))
                        ].index
                    )
                else:
                    temp_index_list = list(
                        selected_data[
                            (selected_data['Pump flow according to H; m3/h'].between(xmin, xmax)) & 
                            (selected_data["Mechanical power - measured; kW"].between(ymin, ymax))
                        ].index
                    )

            # elif relay_index == 2:
            #     temp_index_list = list(
            #         selected_data[
            #             (selected_data['Pump flow according to H; m3/h'].between(xmin, xmax)) & 
            #             (selected_data["Mechanical power - measured; kW"].between(ymin, ymax))
            #         ].index
            #     )
            else:
                if ymin >= chart5_data2[
                    chart5_data2['Tunnid'].between(xmin, xmax)
                ]['Pump flow according to H; m3/h'].max():
                    temp_index_list1 = list(
                        chart5_data1[
                            (chart5_data1['Tunnid'].between(xmin, xmax)) & 
                            (chart5_data1['Mechanical power - measured; kW'].between(ymin, ymax))
                        ]['init_pos'].values
                    )
                    temp_index_list2 = []
                elif ymax <= chart5_data1[
                    chart5_data1['Tunnid'].between(xmin, xmax)
                ]['Mechanical power - measured; kW'].min():
                    temp_index_list2 = list(
                        chart5_data2[
                            (chart5_data2['Tunnid'].between(xmin, xmax)) & 
                            (chart5_data2['Pump flow according to H; m3/h'].between(ymin, ymax))
                        ]['init_pos'].values
                    )
                    temp_index_list1 = []

                else:
                    temp_index_list1 = list(
                        chart5_data1[
                            (chart5_data1['Tunnid'].between(xmin, xmax)) & 
                            (chart5_data1['Mechanical power - measured; kW'].between(ymin, ymax))
                        ]['init_pos'].values
                    )

                    temp_index_list2 = list(
                        chart5_data2[
                            (chart5_data2['Tunnid'].between(xmin, xmax)) & 
                            (chart5_data2['Pump flow according to H; m3/h'].between(ymin, ymax))
                        ]['init_pos'].values
                    )

                temp_index_list1 = [int(k) for k in temp_index_list1]
                temp_index_list2 = [int(k) for k in temp_index_list2]
                temp_index_list = temp_index_list1
                temp_index_list.extend(temp_index_list2)
                temp_index_list = sorted(set(temp_index_list))

            temp_dic['range_index'] = temp_index_list
            if relayoutData3 is not None:
                temp_dic['chart5_range_index'] = [temp_index_list1, temp_index_list2]
            else:
                temp_dic['chart5_range_index'] = temp_index_list

            temp_data = selected_data[selected_data.index.isin(temp_index_list)]
            temp_data.reset_index(inplace=True)
            temp_data.rename(columns={'index': 'init_pos'}, inplace=True)
            temp_data['Time'] = temp_data['Time'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
            temp_dic['temp_data'] = temp_data.to_dict()

    return json.dumps(temp_dic), None, None, None

@callback(
     Output('chart3_4', 'figure'),
     #Output('chart4', 'figure'),
     Output('chart5', 'figure'),
     Output('chart1', 'figure'),
     Output('chart2', 'figure'),
     # Output('chart1', 'selectedData'),
     # Output('chart3', 'selectedData'),
     # Output('chart4', 'selectedData'),
     # Output('chart5', 'selectedData'),
     Output('button', 'n_clicks'),
     Output('puakw', 'children'),
     Output('pudkw', 'children'),
     Output('ae', 'children'),
     Output('pcpbo', 'children'),
     Output('asec', 'children'),
     Output('pcbo', 'children'),
     Output('table', 'figure'),
     Output('start_time', 'value'),
     Output('end_time', 'value'),
     Output('dpump', 'value'),
     Output('pump', 'data'),
     # Output('pump_data', 'data'),
     # Output('span8', 'children'),
     # Output('span9', 'children'),
     # Output('span10', 'children'),
     # Output('span11', 'children'),
     # Output('chart1', 'relayoutData'),
     # Output('chart3', 'relayoutData'),
     # Output('chart4', 'relayoutData'),
     # Output('chart5', 'relayoutData'),
     inputs=[
         Input('button', 'n_clicks'),
         Input('chart1', 'clickData'),
         Input('chart3_4', 'clickData'),
         #Input('chart4', 'clickData'),
         Input('chart5', 'clickData'),
         Input('chart1', 'relayoutData'),
         Input('chart3_4', 'relayoutData'),
         #Input('chart4', 'relayoutData'),
         Input('chart5', 'relayoutData'),
         Input('yaxis', 'value'),
         Input('dpump', 'value')
     ],
     state=[
         State('start_time', 'value'),
         State('end_time', 'value'),
         State('selected_point', 'data'),
         State('selected_range', 'data'),
         State('pump', 'data'),
         # State('pump_data', 'data')
        # State('intermediate-value', 'data')
     ]
)
def figure_callback(n_clicks, clickData1, clickData2, clickData3,#, clickData4, 
                    #selectedData1, selectedData2, selectedData3, selectedData4,
                    relayoutData1, relayoutData2, relayoutData3,#, relayoutData4,
                    yaxis_values, dpump_value, start_time, end_time, point_dict, 
                    range_dict, pump_changed):#, pump_data, , pump_changed

    point_dict = json.loads(point_dict)
    range_dict = json.loads(range_dict)
    if 'autosize' in range_dict:
        range_dict.pop('autosize')

    if ctx.triggered[0]["prop_id"] == "dpump.value":
        # if pump_changed is None:
        #     pump_changed = {}
        #     pump_changed['changed'] = False
        #     pump_changed['pump'] = dpump_value
        # else:
        #     pump_changed = json.loads(pump_changed)
        #     if pump_changed['pump'] != dpump_value:
        #         pump_changed['changed'] = True
        #         pump_changed['pump'] = dpump_value
        #     else:
        #         pump_changed['changed'] = False
        # pump_changed['times'] = 0
        pump_changed = {}
        pump_changed['point_dict'] = {}
        pump_changed['range_dict'] = {}

    else:
        # if pump_changed is None:
        pump_changed = {}
        pump_changed['point_dict'] = point_dict
        pump_changed['range_dict'] = range_dict
        # else:
        #     pump_changed = json.loads(pump_changed)
            # if pump_changed['changed']:
            #     pump_changed['times'] = pump_changed['times'] + 1


    if dpump_value == 'Pump1' or dpump_value is None:
        data = data_pump1.copy()
    else:
        data = data_pump2.copy()
    # data['Time'] = pd.to_datetime(data['Time'])

    # if dpump_value == 'Pump1':
    #     data = load_main(filename='main_data_PUMP1.csv')
    # else:#elif dpump_value == 'Pump2':
    #     data = load_main(filename='main_data_PUMP2.csv')

    # html_table = create_table(df=table_df)

    # return fig_chart3_4, fig_chart5, fig_chart1, fig_chart2, \
    #         None, \
    #         f"{kpi_dict['POWER USAGE AVERAGE; kW']:.0f}", \
    #         f"{kpi_dict['POWER USAGE DIFFERENCE; kW']:.0f}%", \
    #         f"{kpi_dict['AVERAGE EFFICIENCY']:.0f}", \
    #         f"{kpi_dict['PER CENT POINTS BELOW OPTIMUM']:.0f}pp",\
    #         f"{kpi_dict['AVERAGE SPECIFIC ENERGY CONSUMPTION']:.1f}",\
    #         f"{kpi_dict['PER CENT BELOW OPTIMUM']:.0f}%",\
    #         html_table, start_time, end_time, dpump_value,\
    #         json.dumps(pump_changed), \
    #         f"n_clicks: {n_clicks}", f"len(point_dict): {len(point_dict)}", \
    #         f"len(range_dict): {range_dict}", f"pump: {pump_changed['changed']}"
    #         #str(data.shape), dpump_value, str(pump_changed), f"from {start_time} to {end_time}"

    if ctx.triggered[0]["prop_id"] == "yaxis.value":
        start_date = pd.to_datetime(start_time)
        end_date = pd.to_datetime(end_time)
        selected_data = data[(data['Time']>=start_date) & (data['Time']<=end_date)]

        kpi_dict = calculate_kpi(df=selected_data)

        table_df = create_summary_table(df_main=data, df_period=selected_data)
        html_table = create_table(df=table_df)

        fig_chart2 = create_chart2(df=data_chart2)
        # fig_chart3 = create_chart3(df=selected_data)
        # fig_chart4 = create_chart4(df=selected_data)
        fig_chart3_4 = create_chart3_4(df=selected_data)
        fig_chart5 = create_chart5(df=selected_data)

        fig_chart1 = create_chart1(df=selected_data, yaxis_values=yaxis_values)
        
        return fig_chart3_4, fig_chart5, fig_chart1, fig_chart2, \
               None, \
               f"{kpi_dict['POWER USAGE AVERAGE; kW']:.0f}", \
               f"{kpi_dict['POWER USAGE DIFFERENCE; kW']:.0f}%", \
               f"{kpi_dict['AVERAGE EFFICIENCY']:.0f}", \
               f"{kpi_dict['PER CENT POINTS BELOW OPTIMUM']:.0f}pp",\
               f"{kpi_dict['AVERAGE SPECIFIC ENERGY CONSUMPTION']:.1f}",\
               f"{kpi_dict['PER CENT BELOW OPTIMUM']:.0f}%",\
               html_table, start_time, end_time, dpump_value, \
               json.dumps(pump_changed)\
               # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
               # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
               # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
               # {'xaxis.autorange': False, 'yaxis.autorange': False}

    # if n_clicks is not None:
    #     if n_clicks>0:
    elif ctx.triggered[0]["prop_id"] == "button.n_clicks":
        start_date = pd.to_datetime(start_time)
        end_date = pd.to_datetime(end_time)
        selected_data = data[(data['Time']>=start_date) & (data['Time']<=end_date)]

        kpi_dict = calculate_kpi(df=selected_data)

        table_df = create_summary_table(df_main=data, df_period=selected_data)
        html_table = create_table(df=table_df)

        fig_chart2 = create_chart2(df=data_chart2)
        # fig_chart3 = create_chart3(df=selected_data)
        # fig_chart4 = create_chart4(df=selected_data)
        fig_chart3_4 = create_chart3_4(df=selected_data)
        fig_chart5 = create_chart5(df=selected_data)

        if yaxis_values is None:
            fig_chart1 = create_chart1(df=selected_data)
        else:
            fig_chart1 = create_chart1(df=selected_data, yaxis_values=yaxis_values)

        return fig_chart3_4, fig_chart5, fig_chart1, fig_chart2, \
               None, \
               f"{kpi_dict['POWER USAGE AVERAGE; kW']:.0f}", \
               f"{kpi_dict['POWER USAGE DIFFERENCE; kW']:.0f}%", \
               f"{kpi_dict['AVERAGE EFFICIENCY']:.0f}", \
               f"{kpi_dict['PER CENT POINTS BELOW OPTIMUM']:.0f}pp",\
               f"{kpi_dict['AVERAGE SPECIFIC ENERGY CONSUMPTION']:.1f}",\
               f"{kpi_dict['PER CENT BELOW OPTIMUM']:.0f}%",\
               html_table, start_time, end_time, dpump_value,\
               json.dumps(pump_changed)
               # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
               # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
               # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
               # {'xaxis.autorange': False, 'yaxis.autorange': False}
        # else:
        #     pass

    elif ctx.triggered[0]["prop_id"] == "dpump.value": #pump_changed['changed'] and pump_changed['times'] == 0:
            # start_date = pd.to_datetime(start_time)
            # end_date = pd.to_datetime(end_time)
            # selected_data = data[(data['Time']>=start_date) & (data['Time']<=end_date)]
            
            # data.sort_values('Time', ascending=True, inplace=True)
            start_time = data['Time'].iloc[0].strftime("%Y-%m-%d %H:%M:%S")
            end_time = data['Time'].iloc[-1].strftime("%Y-%m-%d %H:%M:%S")
            selected_data = data.copy()

            kpi_dict = calculate_kpi(df=selected_data)

            table_df = create_summary_table(df_main=data, df_period=selected_data)
            html_table = create_table(df=table_df)

            fig_chart2 = create_chart2(df=data_chart2)
            # fig_chart3 = create_chart3(df=selected_data)
            # fig_chart4 = create_chart4(df=selected_data)
            fig_chart3_4 = create_chart3_4(df=selected_data)
            fig_chart5 = create_chart5(df=selected_data)

            fig_chart1 = create_chart1(df=selected_data, yaxis_values=yaxis_values)
            
            return fig_chart3_4, fig_chart5, fig_chart1, fig_chart2, \
                   None, \
                   f"{kpi_dict['POWER USAGE AVERAGE; kW']:.0f}", \
                   f"{kpi_dict['POWER USAGE DIFFERENCE; kW']:.0f}%", \
                   f"{kpi_dict['AVERAGE EFFICIENCY']:.0f}", \
                   f"{kpi_dict['PER CENT POINTS BELOW OPTIMUM']:.0f}pp",\
                   f"{kpi_dict['AVERAGE SPECIFIC ENERGY CONSUMPTION']:.1f}",\
                   f"{kpi_dict['PER CENT BELOW OPTIMUM']:.0f}%",\
                   html_table, start_time, end_time, dpump_value, \
                   json.dumps(pump_changed)
                   # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
                   # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
                   # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
                   # {'xaxis.autorange': False, 'yaxis.autorange': False}

    #else:

    #elif ctx.triggered[0]["prop_id"] in ['chart1.clickData', 'chart3_4.clickData', 'chart5.clickData']:
    elif len(point_dict) != 0:
        temp_index = point_dict['point_index']
        temp_index_mpmkw = point_dict['chart5_point_index'][0]
        temp_index_pfah = point_dict['chart5_point_index'][1]

        if 'range_index' not in list(range_dict.keys()):
            start_date = pd.to_datetime(start_time)
            end_date = pd.to_datetime(end_time)
            selected_data = data[(data['Time']>=start_date) & (data['Time']<=end_date)]
        else:
            if 'temp_data' not in range_dict:
                selected_data = data[data.index.isin(range_dict['range_index'])]
            else:
                selected_data = pd.DataFrame(range_dict['temp_data'])
                selected_data['Time'] = pd.to_datetime(selected_data['Time'])
                selected_data.set_index('init_pos', inplace=True)

        selected_data.reset_index(drop=True, inplace=True)

        kpi_dict = calculate_kpi(df=selected_data)

        table_df = create_summary_table(df_main=data, df_period=selected_data)
        html_table = create_table(df=table_df)


        if 'range_index' not in list(range_dict.keys()):
            fig_chart2 = create_chart2(df=data_chart2, point_highlight=True, point_index=temp_index, 
                                       main_df=selected_data)
            # fig_chart3 = create_chart3(df=selected_data, point_highlight=True, point_index=temp_index)
            # fig_chart4 = create_chart4(df=selected_data, point_highlight=True, point_index=temp_index)
            fig_chart3_4 = create_chart3_4(df=selected_data, point_highlight=True, point_index=temp_index)
            #fig_chart5 = create_chart5(df=selected_data)
            fig_chart5 = create_chart5(df=selected_data, point_highlight=True, 
                                       point_index=[temp_index_mpmkw, temp_index_pfah])

            if yaxis_values is None:
                fig_chart1 = create_chart1(df=selected_data, point_highlight=True, point_index=temp_index) 
            else:
                fig_chart1 = create_chart1(df=selected_data, point_highlight=True, point_index=temp_index, 
                                           yaxis_values=yaxis_values)
        else:
            # selected_data = data[data.index.isin(rdata_list[0]['range_index'])]
            # temp_index = list(selected_data.index)[temp_index]
            start_time = selected_data['Time'].min().strftime('%Y-%m-%d %H:%M:%S')
            end_time = selected_data['Time'].max().strftime('%Y-%m-%d %H:%M:%S')

            chart5_temp_index = range_dict['chart5_range_index']
            temp_index_list = range_dict['range_index']

            fig_chart2 = create_chart2(df=data_chart2, point_highlight=True, 
                                       point_index=temp_index, main_df=selected_data)
            # fig_chart3 = create_chart3(df=selected_data, point_highlight=True, point_index=temp_index)#, 
            #                            #filter_points=True, points_range=temp_index_list)
            # fig_chart4 = create_chart4(df=selected_data, point_highlight=True, point_index=temp_index)#, 
            #                            #filter_points=True, points_range=temp_index_list)
            fig_chart3_4 = create_chart3_4(df=selected_data, point_highlight=True, point_index=temp_index)#, 
                                           #filter_points=True, points_range=temp_index_list)

            fig_chart5 = create_chart5(df=selected_data, point_highlight=True, 
                                       point_index=[temp_index_mpmkw, temp_index_pfah])
            # if i != 3:
            #     fig_chart5 = create_chart5(df=selected_data, filter_points=True, points_range=temp_index_list)
            #     chart5_index_list = temp_index_list
            # else:
            #     fig_chart5 = create_chart5(df=selected_data, filter_points=True, 
            #                                points_range=rdata_list[0]['chart5_range_index'])
            #     chart5_index_list = rdata_list[0]['chart5_range_index']
            # if i != 3:
            #     fig_chart5 = create_chart5(df=selected_data, point_highlight=True, point_index=chart5_temp_index,
            #                                filter_points=True, points_range=temp_index_list)
            #     chart5_index_list = temp_index_list
            # else:
            #     fig_chart5 = create_chart5(df=selected_data, point_highlight=True, point_index=chart5_temp_index, 
            #                                filter_points=True, 
            #                                points_range=rdata_list[0]['chart5_range_index'])
            #     chart5_index_list = rdata_list[0]['chart5_range_index']
            # fig_chart1 = create_chart1(df=selected_data, filter_points=True, points_range=temp_index_list, 
            #                            left_yaxis=left_yaxis, right_yaxis=right_yaxis)

            if yaxis_values is None:
                fig_chart1 = create_chart1(df=selected_data, point_highlight=True, point_index=temp_index)#, 
                                           #filter_points=True, points_range=temp_index_list)
            else:
                fig_chart1 = create_chart1(df=selected_data, yaxis_values=yaxis_values,
                                           point_highlight=True, point_index=temp_index)#, 
                                           #filter_points=True, points_range=temp_index_list)

        return fig_chart3_4, fig_chart5, fig_chart1, fig_chart2, \
               None, \
               f"{kpi_dict['POWER USAGE AVERAGE; kW']:.0f}", \
               f"{kpi_dict['POWER USAGE DIFFERENCE; kW']:.0f}%", \
               f"{kpi_dict['AVERAGE EFFICIENCY']:.0f}", \
               f"{kpi_dict['PER CENT POINTS BELOW OPTIMUM']:.0f}pp",\
               f"{kpi_dict['AVERAGE SPECIFIC ENERGY CONSUMPTION']:.1f}",\
               f"{kpi_dict['PER CENT BELOW OPTIMUM']:.0f}%",\
               html_table, start_time, end_time, dpump_value, \
               json.dumps(pump_changed)
               # {'point_index': temp_index, 'chart5_point_index': [temp_index_mpmkw, temp_index_pfah]}, \
               # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
               # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
               # {'xaxis.autorange': False, 'yaxis.autorange': False}
            
        # else:
        #     pass #return_list.append(None)       

    #elif ctx.triggered[0]["prop_id"] in ['chart1.relayoutData', 'chart3_4.relayoutData', 'chart5.relayoutData']:
    elif len(range_dict) != 0:
        if 'range_index' in range_dict:
            temp_index_list = range_dict['range_index']
            chart5_index_list = range_dict['chart5_range_index']

            if 'temp_data' not in range_dict:
                selected_data = data[data.index.isin(temp_index_list)]
            else:
                selected_data = pd.DataFrame(range_dict['temp_data'])
                selected_data['Time'] = pd.to_datetime(selected_data['Time'])
                selected_data.set_index('init_pos', inplace=True)

            start_time = selected_data['Time'].min().strftime('%Y-%m-%d %H:%M:%S')
            end_time = selected_data['Time'].max().strftime('%Y-%m-%d %H:%M:%S')

            kpi_dict = calculate_kpi(df=selected_data)

            table_df = create_summary_table(df_main=data, df_period=selected_data)
            html_table = create_table(df=table_df)

            if 'point_index' in list(point_dict.keys()):
                temp_index = point_dict['point_index']
                chart5_temp_index = point_dict['chart5_point_index']

                fig_chart2 = create_chart2(df=data_chart2, point_highlight=True, 
                                           point_index=temp_index, main_df=selected_data)
                # fig_chart3 = create_chart3(df=selected_data, point_highlight=True, point_index=temp_index)
                # fig_chart4 = create_chart4(df=selected_data, point_highlight=True, point_index=temp_index)
                fig_chart3_4 = create_chart3_4(df=selected_data, point_highlight=True, point_index=temp_index)
                fig_chart5 = create_chart5(df=selected_data, point_highlight=True, point_index=chart5_temp_index)
                # if i != 3:
                #     chart5_index_list = temp_index_list
                # else:
                #     chart5_index_list = [temp_index_list1, temp_index_list2]
                # if i != 3:
                #     fig_chart5 = create_chart5(df=selected_data, point_highlight=True, point_index=chart5_temp_index,
                #                                filter_points=True, points_range=temp_index_list)
                #     chart5_index_list = temp_index_list
                # else:
                #     fig_chart5 = create_chart5(df=selected_data, point_highlight=True, point_index=chart5_temp_index, 
                #                                filter_points=True, 
                #                                points_range=[temp_index_list1, temp_index_list2])
                #     chart5_index_list = [temp_index_list1, temp_index_list2]
                # fig_chart1 = create_chart1(df=selected_data, filter_points=True, points_range=temp_index_list, 
                #                            left_yaxis=left_yaxis, right_yaxis=right_yaxis)

                if yaxis_values is None:
                    fig_chart1 = create_chart1(df=selected_data, point_highlight=True, point_index=temp_index)
                else:
                    fig_chart1 = create_chart1(df=selected_data, yaxis_values=yaxis_values,
                                               point_highlight=True, point_index=temp_index)
                
            else:
                fig_chart2 = create_chart2(df=data_chart2)
                # fig_chart3 = create_chart3(df=selected_data)
                # fig_chart4 = create_chart4(df=selected_data)
                fig_chart3_4 = create_chart3_4(df=selected_data)
                fig_chart5 = create_chart5(df=selected_data)
                # if i != 3:
                #     chart5_index_list = temp_index_list
                # else:
                #     # fig_chart5 = create_chart5(df=selected_data, filter_points=True, 
                #     #                            points_range=[temp_index_list1, temp_index_list2])
                #     chart5_index_list = [temp_index_list1, temp_index_list2]

                if yaxis_values is None:
                    fig_chart1 = create_chart1(df=selected_data)#, filter_points=True, points_range=temp_index_list)
                else:
                    fig_chart1 = create_chart1(df=selected_data, yaxis_values=yaxis_values)#, 
                                               #filter_points=True, points_range=temp_index_list)

            return fig_chart3_4, fig_chart5, fig_chart1, fig_chart2, \
                   None, \
                   f"{kpi_dict['POWER USAGE AVERAGE; kW']:.0f}", \
                   f"{kpi_dict['POWER USAGE DIFFERENCE; kW']:.0f}%", \
                   f"{kpi_dict['AVERAGE EFFICIENCY']:.0f}", \
                   f"{kpi_dict['PER CENT POINTS BELOW OPTIMUM']:.0f}pp",\
                   f"{kpi_dict['AVERAGE SPECIFIC ENERGY CONSUMPTION']:.1f}",\
                   f"{kpi_dict['PER CENT BELOW OPTIMUM']:.0f}%",\
                   html_table, start_time, end_time, dpump_value, \
                   json.dumps(pump_changed)
                   # {'range_index': temp_index_list, 'chart5_range_index': chart5_index_list}, \
                   # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
                   # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
                   # {'xaxis.autorange': False, 'yaxis.autorange': False}

        elif 'dragmode' in range_dict:
            raise PreventUpdate
            
        elif 'showspikes' in range_dict:
            raise PreventUpdate

        elif 'autosize' in range_dict:
            raise PreventUpdate

        elif 'autorange' in range_dict:
            start_time = data['Time'].min().strftime('%Y-%m-%d %H:%M:%S')
            end_time = data['Time'].max().strftime('%Y-%m-%d %H:%M:%S')
            # selected_data = data[(data['Time']>=start_date) & (data['Time']<=end_date)]

            kpi_dict = calculate_kpi(df=data)

            table_df = create_summary_table(df_main=data, df_period=data)
            html_table = create_table(df=table_df)

            fig_chart2 = create_chart2(df=data_chart2)
            # fig_chart3 = create_chart3(df=data)
            # fig_chart4 = create_chart4(df=data)
            fig_chart3_4 = create_chart3_4(df=data)
            fig_chart5 = create_chart5(df=data)

            if yaxis_values is None:
                fig_chart1 = create_chart1(df=data)
            else:
                fig_chart1 = create_chart1(df=data, yaxis_values=yaxis_values)

            return fig_chart3_4, fig_chart5, fig_chart1, fig_chart2, \
                   None, \
                   f"{kpi_dict['POWER USAGE AVERAGE; kW']:.0f}", \
                   f"{kpi_dict['POWER USAGE DIFFERENCE; kW']:.0f}%", \
                   f"{kpi_dict['AVERAGE EFFICIENCY']:.0f}", \
                   f"{kpi_dict['PER CENT POINTS BELOW OPTIMUM']:.0f}pp",\
                   f"{kpi_dict['AVERAGE SPECIFIC ENERGY CONSUMPTION']:.1f}",\
                   f"{kpi_dict['PER CENT BELOW OPTIMUM']:.0f}%",\
                   html_table, start_time, end_time, dpump_value, \
                   json.dumps(pump_changed)
                   # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
                   # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
                   # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
                   # {'xaxis.autorange': False, 'yaxis.autorange': False}

    # elif yaxis_values is not None:
    #     start_date = pd.to_datetime(start_time)
    #     end_date = pd.to_datetime(end_time)
    #     selected_data = data[(data['Time']>=start_date) & (data['Time']<=end_date)]

    #     kpi_dict = calculate_kpi(df=selected_data)

    #     table_df = create_summary_table(df_main=data, df_period=selected_data)
    #     html_table = create_table(df=table_df)

    #     fig_chart2 = create_chart2(df=data_chart2)
    #     # fig_chart3 = create_chart3(df=selected_data)
    #     # fig_chart4 = create_chart4(df=selected_data)
    #     fig_chart3_4 = create_chart3_4(df=selected_data)
    #     fig_chart5 = create_chart5(df=selected_data)

    #     fig_chart1 = create_chart1(df=selected_data, yaxis_values=yaxis_values)
        
    #     return fig_chart3_4, fig_chart5, fig_chart1, fig_chart2, \
    #            None, \
    #            f"{kpi_dict['POWER USAGE AVERAGE; kW']:.0f}", \
    #            f"{kpi_dict['POWER USAGE DIFFERENCE; kW']:.0f}%", \
    #            f"{kpi_dict['AVERAGE EFFICIENCY']:.0f}", \
    #            f"{kpi_dict['PER CENT POINTS BELOW OPTIMUM']:.0f}pp",\
    #            f"{kpi_dict['AVERAGE SPECIFIC ENERGY CONSUMPTION']:.1f}",\
    #            f"{kpi_dict['PER CENT BELOW OPTIMUM']:.0f}%",\
    #            html_table, start_time, end_time, dpump_value, \
    #            json.dumps(pump_changed), \
    #            str(data.shape), dpump_value, str(pump_changed), f"from {start_time} to {end_time}"
    #            # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
    #            # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
    #            # {'xaxis.autorange': False, 'yaxis.autorange': False}, \
    #            # {'xaxis.autorange': False, 'yaxis.autorange': False}

    else:
        raise PreventUpdate


# if __name__ == '__main__':
#     app.run_server(debug=True)
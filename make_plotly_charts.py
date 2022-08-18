# loading some packages
import plotly.graph_objects as go
# from  plotly.offline import plot
# import chart_studio.plotly as py
from plotly.subplots import make_subplots
import os
import base64
from get_screen_size import get_ss
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

screen_size = get_ss()

def get_poly_coef(X, y, p=4):
    '''Returns polynomial coefficients

       Params:
       X: series, independent variable to compute polynomials for
       y: series, target variable
       p: int, polynomial degree

       Returns:
       pol_curve: list, polynomial estimated coefficients
    '''

    temp_x = X.values
    temp_y = y.values
    pol_coef = np.polyfit(temp_x, temp_y, p)

    # lr = LinearRegression()

    # temp_df = pd.DataFrame()
    # for i in range(1, p+1):
    #     temp_df[f'p{i}'] = X ** i

    # lr.fit(temp_df, y)
    # pol_coef = list(lr.coef_)
    return pol_coef

def get_point(pol_coef, ref_point):
    '''Returns work or opti point based on regression 
       coefficients and reference point

       Params:
       pol_coef: list, polynomial estimated coefficients
       ref_point: int or float, a point for which to calculate polynomial value

       Returns:
       output_point: int, work or opti point
    '''
    pol_curve = np.poly1d(pol_coef)
    output_point = pol_curve(ref_point)
    # output_point = 0
    # for i in range(len(pol_coef)):
    #     if i == 0:
    #         output_point += pol_coef[i]
    #     else:
    #         output_point += pol_coef[i] * ref_point ** i
    # output_point = round(output_point, 0)
    return output_point

def create_chart1(df, point_highlight=False, filter_points=False, point_index=None, points_range=None,
    yaxis_values=['Pump flow according to H; m3/h'], screen_size=screen_size):
    '''Creates chart 1

       Params:
       df: dataframe, contains the data for the chart
       point_highlight: boolean, True if a point should be highlighted
       filter_points: boolean, True if a range of points is selected
       point_index: int, index of a point to highlight in the data
       points_range: list, contains indexes of coordinates to include in the chart
       yaxis_values: list, names of columns to show on y axis

       Returns
       fig: plotly figure object
    '''

    # setting colors' list for y axis variables (chart1)
    color_list = ['blue', 'orange', 'green', 'purple', 'red',
                  'olivedrab', 'pink', 'blueviolet', 'brown', 'burlywood', 
                  'cadetblue', 'aliceblue',  'aqua', 'aquamarine', 'darkturquoise']

    left_yaxis = [yaxis_values[i] for i in range(len(yaxis_values)) if i % 2 == 0]
    right_yaxis = [yaxis_values[i] for i in range(len(yaxis_values)) if i % 2 != 0]
    # overall_yaxis = left_yaxis.copy()
    # overall_yaxis.extend(right_yaxis)

    if filter_points:
        df = df[df.index.isin(points_range)]
    else:
        pass

    left_yaxis_trace = []

    # creating plots for left y axis
    for col in left_yaxis:
        # if col == 'Frequency; Hz':
        #     temp_hover_list1 = ['Time: %{x}', col + ': %{y}']
        # else:
        #     temp_hover_list1 = ['Time: %{x}', col + ': %{y:.2f}']
        # if len(overall_yaxis) > 1: #left_yaxis.index(col) == 0 and 
        #     temp_rest_col_list = [i_col for i_col in overall_yaxis if i_col!=col]
        #     temp_hover_list2 = [i_col +  ': %{' + f"customdata[{temp_rest_col_list.index(i_col)}]:.2f" + '}'
        #                         if i_col!='Frequency; Hz' 
        #                         else
        #                         i_col +  ': %{' + f"customdata[{temp_rest_col_list.index(i_col)}]" + '}'
        #                         for i_col in temp_rest_col_list]
        #     temp_hover_list1.extend(temp_hover_list2)

        #     temp_trace = go.Scattergl(
        #         x=df["Time"], 
        #         y=df[col], 
        #         mode='lines',
        #         line_color=color_list[left_yaxis.index(col)],
        #         name=col, 
        #         yaxis=f'y{left_yaxis.index(col)+1}',
        #         customdata=df[[i_col for i_col in overall_yaxis if i_col!=col]],
        #         hovertemplate='<br>'.join(temp_hover_list1)
        #     )
        # else:

        if col == 'Frequency; Hz':
            temp_hover_list1 = '%{y}'
        else:
            temp_hover_list1 = '%{y:.2f}'

        temp_trace = go.Scattergl(
            x=df["Time"], 
            y=df[col], 
            mode='lines',
            line_color=color_list[left_yaxis.index(col)],
            name=col, 
            yaxis=f'y{left_yaxis.index(col)+1}',
            #hovertemplate='<br>'.join(temp_hover_list1)
            hovertemplate=temp_hover_list1
        )
        left_yaxis_trace.append(temp_trace)

    right_yaxis_trace = []

    # creating plots for right y axis
    for col in right_yaxis:
        # if col == 'Frequency; Hz':
        #     temp_hover_list1 = ['Time: %{x}', col + ': %{y}']
        # else:
        #     temp_hover_list1 = ['Time: %{x}', col + ': %{y:.2f}']
        # temp_rest_col_list = [i_col for i_col in overall_yaxis if i_col!=col]
        # temp_hover_list2 = [i_col +  ': %{' + f"customdata[{temp_rest_col_list.index(i_col)}]:.2f" + '}'
        #                     if i_col!='Frequency; Hz' 
        #                     else
        #                     i_col +  ': %{' + f"customdata[{temp_rest_col_list.index(i_col)}]" + '}'
        #                     for i_col in temp_rest_col_list]
        # temp_hover_list1.extend(temp_hover_list2)

        if col == 'Frequency; Hz':
            temp_hover_list1 = '%{y}'
        else:
            temp_hover_list1 = '%{y:.2f}'

        temp_trace = go.Scattergl(
            x=df["Time"], 
            y=df[col], 
            mode='lines',  
            line_color=color_list[right_yaxis.index(col)+len(left_yaxis)],
            name=col,
            yaxis=f'y{right_yaxis.index(col)+1+len(left_yaxis)}',
            #customdata=df[[i_col for i_col in overall_yaxis if i_col!=col]],
            #hovertemplate='<br>'.join(temp_hover_list1)
            hovertemplate=temp_hover_list1
        )
        right_yaxis_trace.append(temp_trace)
   
    overall_trace = left_yaxis_trace.copy()
    overall_trace.extend(right_yaxis_trace)

    fig = go.Figure(data=overall_trace)
    fig['layout']['clickmode']='event+select'

    x_left = len(left_yaxis) * 0.025
    y_left = 1 - len(right_yaxis) * 0.025

    # setting left y axis' tick color and position for each additional variable
    for col in left_yaxis:
        if left_yaxis.index(col) == 0:
            fig['layout']['yaxis'] = dict(
                                        color=color_list[left_yaxis.index(col)],
                                        # showspikes=True,
                                        # spikemode='across+toaxis',
                                        # spikesnap='cursor',
                                        # showline=True,
                                        # showgrid=True
                                    )
        else:
            fig['layout'][f'yaxis{left_yaxis.index(col)+1}'] = dict(
                                                                    overlaying='y',
                                                                    side='left',
                                                                    color=color_list[left_yaxis.index(col)],
                                                                    anchor="free",
                                                                    position=x_left - left_yaxis.index(col)*0.025,
                                                                    # showspikes=True,
                                                                    # spikemode='across+toaxis',
                                                                    # spikesnap='cursor',
                                                                    # showline=True,
                                                                    # showgrid=True
                                                                )

    # setting right y axis' tick color and position for each additional variable
    for col in right_yaxis:
        if right_yaxis.index(col) == 0:
            fig['layout'][f'yaxis{right_yaxis.index(col)+1+len(left_yaxis)}'] = dict(
                                                                                    overlaying='y',
                                                                                    side='right',
                                                                                    color=color_list[right_yaxis.index(col)+len(left_yaxis)],
                                                                                    anchor="x",
                                                                                    # showspikes=True,
                                                                                    # spikemode='across+toaxis',
                                                                                    # spikesnap='cursor',
                                                                                    # showline=True,
                                                                                    # showgrid=True
                                                                                )
        else:
            fig['layout'][f'yaxis{right_yaxis.index(col)+1+len(left_yaxis)}'] = dict(
                                                                                    overlaying='y',
                                                                                    side='right',
                                                                                    color=color_list[right_yaxis.index(col)+len(left_yaxis)],
                                                                                    anchor="free",
                                                                                    position=y_left + right_yaxis.index(col)*0.025,
                                                                                    # showspikes=True,
                                                                                    # spikemode='across+toaxis',
                                                                                    # spikesnap='cursor',
                                                                                    # showline=True,
                                                                                    # showgrid=True
                                                                                )

    # setting logo path
    cwd_path = os.getcwd()
    logo_file_name = 'enerwise_logo_varviline.png'
    logo_path = os.path.join(cwd_path, logo_file_name)
    encoded_image = base64.b64encode(open(logo_path, 'rb').read())

    # if screen_size[1] > 1366:
    #     w_percent = 0.75 * 2*0.4868228404099561
    # else:
    #     w_percent = 2*0.4868228404099561

    # add logo to the chart 1
    fig.add_layout_image(
        dict(
            source='data:image/png;base64,{}'.format(encoded_image.decode()),
            xref="paper", yref="paper",
            x=0.025*len(left_yaxis), y=1.10,#0.001393229*screen_size[0],#1.07,
            sizex=0.8,#0.0000732064*screen_size[1],#0.1,#0.00016105417*screen_size[1],#0.22,# + (len(left_yaxis)-1)*0.005, 
            sizey=0.1,#0.0000911458*screen_size[0],#0.00013020833*screen_size[0],#0.1, #+ (len(left_yaxis)-1)*0.005,
            xanchor="left", yanchor="top",
        )
    )

    # setting layout of chart 1 
    fig.update_layout(
        #modebar_orientation='v',    # position of toolbox (select box, autoscale, ...)
        xaxis=dict(                 
            domain=[x_left, y_left],
            # showspikes=True,
            # spikemode='across+toaxis+marker',
            # spikesnap='cursor',
            # showline=True,
            # showgrid=True,
            #spikedash = 'solid'
        ),
        # yaxis=dict(
        #     showspikes=True,
        #     spikemode='across+toaxis',
        #     spikesnap='cursor',
        #     showline=True,
        #     showgrid=True,
        #     #spikedash = 'solid'
        # ),
        # yaxis2=dict(
        #     showspikes=True,
        #     spikemode='across+toaxis',
        #     spikesnap='cursor',
        #     showline=True,
        #     showgrid=True,
        #     #spikedash = 'solid'
        # ),
        legend=dict(                # setting legend parameters (chart1)
            orientation="v",
            x=1,
            y=0.99,
            traceorder="normal",
            font=dict(
                family="ISOCPEUR",
                size=8,
                color="black"
            ),
        ),
        margin=go.layout.Margin(    # setting margin
            l=0, #left margin
            r=0, #right margin
            b=0, #bottom margin
            t=40, #top margin
        ),
        width=500,#w_percent*screen_size[1],#2*0.4868228404099561*screen_size[1],#0.98*screen_size[1], # setting width of the chart 1 584187408
        height=450, #0.65104166666*screen_size[0],  # setting height of the chart 1
        autosize=False,
        font=dict(
            family="ISOCPEUR",
            size=12
        ),
        plot_bgcolor='#F9F9F9',
        title='''<b>OPERATIONAL DATA</b>''',
        titlefont=dict(
            family="ISOCPEUR",
            size=24
        ),
        title_x=0.5,
        # showlegend=False,
        hovermode="x"
    )

    fig.update_xaxes(gridcolor='#D9D9D9')
    fig.update_yaxes(gridcolor='#D9D9D9')

    # if filter_points:
    #     df = df[df.index.isin(points_range)]

    #     left_yaxis_trace = []

    #     for col in left_yaxis:
    #         temp_trace = go.Scattergl(
    #             x=df["Time"], 
    #             y=df[col], 
    #             mode='lines+markers', 
    #             line_color=color_list[left_yaxis.index(col)],
    #             name=col, 
    #             yaxis=f'y{left_yaxis.index(col)+1}'
    #         )
    #         left_yaxis_trace.append(temp_trace)

    #     right_yaxis_trace = []

    #     for col in right_yaxis:
    #         temp_trace = go.Scattergl(x=df["Time"], 
    #                                   y=df[col], 
    #                                   mode='lines+markers', 
    #                                   #marker_symbol='diamond', 
    #                                   line_color=color_list[right_yaxis.index(col)+len(left_yaxis)],
    #                                   name=col,
    #                                   yaxis=f'y{right_yaxis.index(col)+1+len(left_yaxis)}')
    #         right_yaxis_trace.append(temp_trace)

    #     overall_trace = left_yaxis_trace.copy()
    #     overall_trace.extend(right_yaxis_trace)

    #     fig = go.Figure(data=overall_trace)
    #     fig['layout']['clickmode']='event+select'

    #     x_left = len(left_yaxis) * 0.025
    #     y_left = 1 - len(right_yaxis) * 0.025

    #     for col in left_yaxis:
    #         if left_yaxis.index(col) == 0:
    #             fig['layout']['yaxis'] = dict(color=color_list[left_yaxis.index(col)])
    #         else:
    #             fig['layout'][f'yaxis{left_yaxis.index(col)+1}'] = dict(
    #                                                                    overlaying='y',
    #                                                                    side='left',
    #                                                                    color=color_list[left_yaxis.index(col)],
    #                                                                    anchor="free",
    #                                                                    position=x_left - left_yaxis.index(col)*0.025
    #                                                                )

    #     for col in right_yaxis:
    #         if right_yaxis.index(col) == 0:
    #             fig['layout'][f'yaxis{right_yaxis.index(col)+1+len(left_yaxis)}'] = dict(
    #                                                                                 overlaying='y',
    #                                                                                 side='right',
    #                                                                                 color=color_list[right_yaxis.index(col)+len(left_yaxis)],
    #                                                                                 anchor="x"
    #                                                                               )
    #         else:
    #             fig['layout'][f'yaxis{right_yaxis.index(col)+1+len(left_yaxis)}'] = dict(
    #                                                                                 overlaying='y',
    #                                                                                 side='right',
    #                                                                                 color=color_list[right_yaxis.index(col)+len(left_yaxis)],
    #                                                                                 anchor="free",
    #                                                                                 position=y_left + right_yaxis.index(col)*0.025
    #                                                                               )

    #     fig.update_layout(
    #         modebar_orientation='v',
    #         xaxis=dict(
    #             domain=[x_left, y_left]
    #         ),
    #         legend=dict(
    #             orientation="h",
    #             x=0,
    #             y=1.15,
    #             traceorder="normal",
    #             font=dict(
    #                 family="sans-serif",
    #                 size=10,
    #                 color="black"
    #             ),
    #         ),
    #         margin=go.layout.Margin(
    #         l=0, #left margin
    #         r=25, #right margin
    #         b=0, #bottom margin
    #         t=22, #top margin
    #     ),
    #         width=1340, height=270)


    #     if point_highlight:
    #         for col in left_yaxis:
    #             chart1_x1 = [df.loc[point_index, "Time"]] 
    #             chart1_y1 = [df.loc[point_index, col]]

    #             fig.add_scatter(x=chart1_x1, 
    #                                    y=chart1_y1, 
    #                                    mode='markers', 
    #                                    # marker_color="green",
    #                                    # marker_symbol='circle-open',
    #                                    # marker_size=10
    #                                    marker=dict(
    #                                                 color='green',
    #                                                 size=15,
    #                                                 symbol='circle-open',
    #                                                 line=dict(
    #                                                     color='green',
    #                                                     width=3
    #                                                 )
    #                                     ),
    #                                    showlegend=False,
    #                                    yaxis=f'y{left_yaxis.index(col)+1}')

    #             if left_yaxis.index(col) == 0:
    #                 fig.add_annotation(
    #                     x=chart1_x1[0], 
    #                     y=chart1_y1[0],
    #                     text=f'({chart1_x1[0].strftime("%Y-%m-%d %H:%M")}, <br> {chart1_y1[0]:.2f})',
    #                     yanchor='bottom',
    #                     showarrow=True,
    #                     arrowhead=1,
    #                     arrowsize=1,
    #                     arrowwidth=2,
    #                     arrowcolor="black",
    #                     ax=-50,
    #                     ay=-30,
    #                     font=dict(size=15, color='black', family="Courier New, monospace"),
    #                     align="left"
    #                 )
    #             else:
    #                 fig.add_annotation(
    #                 x=chart1_x1[0], 
    #                 y=chart1_y1[0],
    #                 text=f'({chart1_y1[0]:.2f})',
    #                 yanchor='bottom',
    #                 showarrow=True,
    #                 arrowhead=1,
    #                 arrowsize=1,
    #                 arrowwidth=2,
    #                 arrowcolor="black",
    #                 ax=-50,
    #                 ay=-30,
    #                 font=dict(size=15, color='black', family="Courier New, monospace"),
    #                 align="left",
    #                 yref=f'y{left_yaxis.index(col)+1}'
    #                 )

    #         for col in right_yaxis:
    #             chart1_x2 = [df.loc[point_index, "Time"]]  
    #             chart1_y2 = [df.loc[point_index, col]]

    #             fig.add_scatter(x=chart1_x2, 
    #                                    y=chart1_y2, 
    #                                    mode='markers', 
    #                                    # marker_color="green",
    #                                    # marker_symbol='circle-open',
    #                                    # marker_size=10
    #                                    marker=dict(
    #                                                 color='green',
    #                                                 size=15,
    #                                                 symbol='circle-open',
    #                                                 line=dict(
    #                                                     color='green',
    #                                                     width=3
    #                                                 )
    #                                     ),
    #                                    showlegend=False,
    #                                    yaxis=f'y{right_yaxis.index(col)+1+len(left_yaxis)}')
    #             fig.add_annotation(
    #                 x=chart1_x2[0], 
    #                 y=chart1_y2[0],
    #                 text=f'({chart1_y2[0]:.2f})', # {chart1_x2[0].strftime("%Y-%m-%d %H:%M")}, <br> 
    #                 yanchor='bottom',
    #                 showarrow=True,
    #                 arrowhead=1,
    #                 arrowsize=1,
    #                 arrowwidth=2,
    #                 arrowcolor="black",
    #                 ax=60,
    #                 ay=-30,
    #                 font=dict(size=15, color="black", family="Courier New, monospace"),
    #                 align="left",
    #                 yref=f'y{right_yaxis.index(col)+1+len(left_yaxis)}'
    #             )
    #     else:
    #         pass
            
    #     return fig
    # else:
    if point_highlight:
        for col in left_yaxis:
            temp_metric_left = col.split(';')[-1]
            chart1_x1 = [df.loc[point_index, "Time"]] 
            chart1_y1 = [df.loc[point_index, col]]

            chart1_y1_max = df[col].max()
            chart1_y1_ay = chart1_y1[0] - df[col].max() - 50

            fig.add_scatter(
                x=chart1_x1, 
                y=chart1_y1, 
                mode='markers', 
                marker=dict(   # setting highlighted point related parameters: marker representation, left y axis
                    color='black',
                    size=15,
                    symbol='circle-open',
                    line=dict(
                        color='black',
                        width=3
                    )
                 ),
                showlegend=False,
                yaxis=f'y{left_yaxis.index(col)+1}'
            )

            # setting annotation for left y axis (chart 1)
            if left_yaxis.index(col) == 0:
                fig.add_annotation(
                    x=chart1_x1[0], 
                    y=chart1_y1[0],
                    text=f'<b>{chart1_x1[0].strftime("%Y-%m-%d %H:%M")}, <br>{chart1_y1[0]:.0f} {temp_metric_left}</b>',
                    yanchor='bottom',
                    # showarrow=True,
                    # arrowhead=1,
                    # arrowsize=1,
                    # arrowwidth=2,
                    # arrowcolor="black",
                    ax=-50,
                    ay=chart1_y1_ay,#-100,
                    font=dict(size=12, color='black', family="ISOCPEUR"),
                    align="left",
                    bgcolor="white"
                )
            else:
                fig.add_annotation(
                    x=chart1_x1[0], 
                    y=chart1_y1[0],
                    text=f'<b>{chart1_y1[0]:.2f}  {temp_metric_left}</b>',
                    yanchor='bottom',
                    # showarrow=True,
                    # arrowhead=1,
                    # arrowsize=1,
                    # arrowwidth=2,
                    # arrowcolor="black",
                    ax=-50-left_yaxis.index(col)*80,
                    ay=chart1_y1_ay, #-30-left_yaxis.index(col)*10,
                    font=dict(size=12, color='black', family="ISOCPEUR"),
                    align="left",
                    yref=f'y{left_yaxis.index(col)+1}',
                    bgcolor="white"
                )

        for col in right_yaxis:
            temp_metric_right = col.split(';')[-1]
            chart1_x2=[df["Time"].iloc[point_index]] 
            chart1_y2=[df[col].iloc[point_index]]

            chart1_y2_max = df[col].max()
            chart1_y2_ay = chart1_y2[0] - df[col].max() - 50

            fig.add_scatter(
                x=chart1_x2, 
                y=chart1_y2, 
                mode='markers', 
                marker=dict(      # setting highlighted point related parameters: marker representation, right y axis
                    color='black',
                    size=15,
                    symbol='circle-open',
                    line=dict(
                        color='black',
                        width=3
                    )
                 ),
                showlegend=False,
                yaxis=f'y{right_yaxis.index(col)+1+len(left_yaxis)}'
            )

            # setting annotation for right y axis (chart 1)
            fig.add_annotation(
                x=chart1_x2[0], 
                y=chart1_y2[0],
                text=f'<b>{chart1_y2[0]:.2f} {temp_metric_right}</b>', 
                yanchor='bottom',
                # showarrow=True,
                # arrowhead=1,
                # arrowsize=1,
                # arrowwidth=2,
                # arrowcolor="black",
                ax=50+right_yaxis.index(col)*80,
                ay=chart1_y2_ay,#-30-right_yaxis.index(col)*10,
                font=dict(size=12, color="black", family="ISOCPEUR"),
                align="left",
                yref=f'y{right_yaxis.index(col)+1+len(left_yaxis)}',
                bgcolor="white"
            )

        # fig.update_traces(
        #     # overwrite=True,
        #     # marker={"opacity": 0.1},
        #     opacity=0.07
        # )
    else:
        pass
       
    return fig

def create_chart2(df, point_highlight=False, main_df=None, point_index=None, points_range=None, screen_size=screen_size):
    '''Creates chart 2

       Params:
       df: dataframe, contains the data for the chart2
       point_highlight: boolean, True if a point should be highlighted
       main_df: dataframe, contains the data for the rest of the charts
       point_index: int, index of a point to highlight in the data
       points_range: list, contains indexes of coordinates to include in the chart

       Returns
       fig: plotly figure object
    '''
    # creating plot the first plot (chart 2)
    fig1 = go.Figure(
        data=go.Scattergl(
            x=df["Q [m3/h]_50hz"], 
            y=df['H [m]_50hz'], 
            mode='lines', 
            line_color='blue', 
            name='50 HZ curve',
        )
    )

    fig1.add_scatter(
        x=[df["Q [m3/h]_50hz"].iloc[-1]+10], 
        y=[df['H [m]_50hz'].iloc[-1]], 
        mode='text', 
        #text_color='blue',
        #marker_color="blue",
        #marker_symbol='diamond', 
        #name='Working Point-Head'
        text='50 HZ',
        textfont=dict(
            color='blue'
        )
    )

    # # plotting specific points for the first plot (chart 2)
    # fig1.add_scatter(
    #     x=[150], 
    #     y=[500], 
    #     mode='markers', 
    #     marker_color="red",
    #     marker_symbol='diamond', 
    #     name='Design WP'
    # )
    # fig1.add_scatter(
    #     x=df["Q [m3/h]_48h"], 
    #     y=df['H [m]_48h'], 
    #     mode='lines', 
    #     line_color='orange', 
    #     name='Work1 curve'
    # )
    # fig1.add_scatter(
    #     x=[150], 
    #     y=[455], 
    #     mode='markers', 
    #     marker_color="yellow",
    #     marker_symbol='diamond', 
    #     name='Work1 WP - H'
    # )
    # fig1.add_scatter(
    #     x=df["Q [m3/h]_46h"], 
    #     y=df['H [m]_46h'], 
    #     mode='lines', 
    #     line_color='green', 
    #     name='Opti curve'
    # )
    # fig1.add_scatter(
    #     x=[138], 
    #     y=[420], 
    #     mode='markers', 
    #     marker_color="green",
    #     marker_symbol='diamond', 
    #     name='Work1 WP - P'
    # )
    # fig1.add_scatter(
    #     x=[142], 
    #     y=[455], 
    #     mode='markers', 
    #     marker_color="blue",
    #     marker_symbol='diamond', 
    #     name='Opti WP'
    # )
    
    # creating plot the second plot (chart 2)
    fig2 = go.Figure(
        data=go.Scattergl(
            x=df["Q [m3/h]_50hz"], 
            y=df['Pmech[kW]_50hz'], 
            mode='lines', 
            line_color='red', 
            name='50Hz graafik'
        )
    )

    fig2.add_scatter(
        x=[df["Q [m3/h]_50hz"].iloc[-1]+10], 
        y=[df['Pmech[kW]_50hz'].iloc[-1]], 
        mode='text', 
        #marker_color="red",
        #text_color='red',
        #marker_symbol='diamond', 
        #name='Working Point-Head'
        text='50 HZ',
        textfont=dict(
            color='red'
        )
    )

    # # plotting specific points for the second plot (chart 2)
    # fig2.add_scatter(
    #     x=[145], 
    #     y=[250], 
    #     mode='markers', 
    #     marker_color="red",
    #     marker_symbol='diamond',
    #     name='50Hz graafik'
    # )
    # fig2.add_scatter(
    #     x=df["Q [m3/h]_48h"], 
    #     y=df['Pmech[kW]_48h'], 
    #     mode='lines', 
    #     line_color='lightgreen', 
    #     name='Work1 sagedus'
    # )
    # fig2.add_scatter(
    #     x=[138], 
    #     y=[220], 
    #     mode='markers', 
    #     marker_color="darkblue",
    #     marker_symbol='diamond', 
    #     name='Working Point - Power'
    # )
    # fig2.add_scatter(
    #     x=df["Q [m3/h]_46h"], 
    #     y=df['Pmech[kW]_46h'], 
    #     mode='lines', 
    #     line_color='purple', 
    #     name='Opti sagedus'
    # )
    # fig2.add_scatter(
    #     x=[150], 
    #     y=[228], 
    #     mode='markers', 
    #     marker_color="orange",
    #     marker_symbol='diamond', 
    #     name='Working Point-Head'
    # )
    # fig2.add_scatter(
    #     x=[160], 
    #     y=[211], 
    #     mode='markers', 
    #     marker_color="purple",
    #     marker_symbol='diamond',
    #     name='Opti sagedus'
    # )

    figures = [fig1, fig2]

    fig = make_subplots(rows=len(figures), cols=1, vertical_spacing=0.03)

    for i, figure in enumerate(figures):
        for trace in range(len(figure["data"])):
            fig.append_trace(figure["data"][trace], row=i+1, col=1)

    # title and its font size for y and x axis of each plot
    fig['layout']['yaxis']['title'] = "Head, mH2O"
    fig['layout']['yaxis']['title']['font']['size'] = 12
    fig['layout']['xaxis']['showticklabels'] = False
    fig['layout']['xaxis2']['title'] = "Flow, m3/h"
    fig['layout']['xaxis2']['title']['font']['size'] = 12
    fig['layout']['yaxis2']['title'] = "Mech. power, kW"
    fig['layout']['yaxis2']['title']['font']['size'] = 12

    fig['layout']['clickmode']='event+select'

    # setting logo path
    cwd_path = os.getcwd()
    logo_file_name = 'enerwise_logo_varviline.png'
    logo_path = os.path.join(cwd_path, logo_file_name)
    encoded_image = base64.b64encode(open(logo_path, 'rb').read())

    # if screen_size[1] > 1366:
    #     w_percent = 0.75 * 0.48
    # else:
    #     w_percent = 0.48

    # add logo to the chart 1
    fig.add_layout_image(
        dict(
            source='data:image/png;base64,{}'.format(encoded_image.decode()),
            xref="paper", yref="paper",
            x=0, y=1.09,#0.001380208*screen_size[0],#1.06,
            sizex=0.22,#0.0001098097*screen_size[1],#0.15, #0.00016105417*screen_size[1],#0.22 
            sizey=0.1,#0.0000911458*screen_size[0],#0.07 #0.00013020833*screen_size[0],#0.1
            xanchor="left", yanchor="top"
        )
    )


    fig.update_layout(
        # modebar_orientation='v', # position of toolbox (select box, autoscale, ...)
        margin=go.layout.Margin( # setting margin
            l=0, #left margin
            r=0, #right margin
            b=0, #bottom margin
            t=40, #top margin
        ),
        legend=dict(            # setting legend parameters (chart2)
            orientation="h",
            x=0,
            y=-0.25,
            traceorder="normal",
            font=dict(
                family="ISOCPEUR",
                size=7,
                color="black"
            ),
        ),
        font=dict(
            family="ISOCPEUR",
            size=12
        ),
        plot_bgcolor='#F9F9F9',
        title='''<b>PUMP DESIGN CURVES</b>''',
        titlefont=dict(
            family="ISOCPEUR",
            size=24
        ),
        width=500,#w_percent*screen_size[1],#0.4868228404099561*screen_size[1],#0.492*screen_size[1], # setting width of the chart 2 68228404099561
        height=450, #0.78125*screen_size[0], # setting height of the chart 2
        autosize=False,
        title_x=0.5,
        # xaxis=dict(                 
        #     showspikes=True,
        #     spikemode='across+toaxis',
        #     spikesnap='cursor',
        #     showline=True,
        #     showgrid=True,
        #     #spikedash = 'solid'
        # ),
        # yaxis=dict(
        #     showspikes=True,
        #     spikemode='across+toaxis',
        #     spikesnap='cursor',
        #     showline=True,
        #     showgrid=True,
        #     #spikedash = 'solid'
        # ),
        # xaxis2=dict(                 
        #     showspikes=True,
        #     spikemode='across+toaxis',
        #     spikesnap='cursor',
        #     showline=True,
        #     showgrid=True,
        #     #spikedash = 'solid'
        # ),
        # yaxis2=dict(
        #     showspikes=True,
        #     spikemode='across+toaxis',
        #     spikesnap='cursor',
        #     showline=True,
        #     showgrid=True,
        #     #spikedash = 'solid'
        # )
    )

    fig.update_xaxes(gridcolor='#D9D9D9')
    fig.update_yaxes(gridcolor='#D9D9D9')

    if point_highlight:

        work_freq = main_df.loc[point_index, "Frequency; Hz"]
        df[f"Q [m3/h]_{work_freq}h"] = df["Q [m3/h]_50hz"] * (work_freq / 50)
        df[f'H [m]_{work_freq}h'] = df['H [m]_50hz'] * (work_freq / 50) ** 2
        df[f'Pmech[kW]_{work_freq}h'] = df['Pmech[kW]_50hz'] * (work_freq / 50) ** 3

        df_dp_ay1 = 500 - df['H [m]_50hz'].max()

        # opti_freq = 46
        # df[f"Q [m3/h]_{opti_freq}h"] = df["Q [m3/h]_50hz"] * (opti_freq / 50)
        # df[f'H [m]_{opti_freq}h'] = df['H [m]_50hz'] * (opti_freq / 50) ** 2
        # df[f'Pmech[kW]_{opti_freq}h'] = df['Pmech[kW]_50hz'] * (opti_freq / 50) ** 3

        # plotting specific points for the first plot (chart 2)
        fig.add_scatter(
            x=[150], 
            y=[500], 
            mode='markers', 
            marker=dict(   # setting highlighted point related parameters: marker representation, left y axis
                color='black',
                size=15,
                symbol='circle-open',
                line=dict(
                    color='black',
                    width=3
                )
             ), 
            name='Design WP',
            row=1, 
            col=1
        )

        fig.add_annotation(
            x=150, 
            y=500,
            #text=f'<b>{chart1_x1[0].strftime("%Y-%m-%d %H:%M")}, <br> {chart1_y1[0]:.0f} {temp_metric_left}</b>',
            text='<b>Design <br>150 m3/h <br>500 mH2O</b>',
            yanchor='bottom',
            # showarrow=True,
            # arrowhead=1,
            # arrowsize=1,
            # arrowwidth=2,
            # arrowcolor="black",
            ax=60,
            ay=df_dp_ay1,#chart3_y[0]-main_df["Head; mH2O"].max()-20,
            font=dict(size=12, color='black', family="ISOCPEUR"),
            align="left",
            #bgcolor="white"
            row=1, 
            col=1
        )

        fig.add_scatter(
            x=df[f"Q [m3/h]_{work_freq}h"], 
            y=df[f'H [m]_{work_freq}h'], 
            mode='lines', 
            line_color='orange', 
            name='Work1 curve',
            row=1, 
            col=1
        )

        fig.add_scatter(
            x=[df[f"Q [m3/h]_{work_freq}h"].iloc[-1]+10], 
            y=[df[f'H [m]_{work_freq}h'].iloc[-1]], 
            mode='text', 
            #text_color='blue',
            #marker_color="blue",
            #marker_symbol='diamond', 
            #name='Working Point-Head'
            text=f'{work_freq} HZ',
            textfont=dict(
                color='orange'
            ),
            row=1, 
            col=1
        )

        # pol_coef21 = get_poly_coef(
        #     X=df[f'H [m]_{work_freq}h'], 
        #     y=df[f"Q [m3/h]_{work_freq}h"]
        # )

        # G55 = get_point(
        #     pol_coef=pol_coef21, 
        #     ref_point=455
        # )

        # fig.add_scatter(
        #     x=[G55], 
        #     y=[455], 
        #     mode='markers', 
        #     marker_color="yellow",
        #     marker_symbol='diamond', 
        #     name='Work1 WP - H',
        #     row=1, 
        #     col=1
        # )
        
        # fig.add_scatter(
        #     x=df[f"Q [m3/h]_{opti_freq}h"], 
        #     y=df[f'H [m]_{opti_freq}h'], 
        #     mode='lines', 
        #     line_color='green', 
        #     name='Opti curve',
        #     row=1, 
        #     col=1
        # )

        # pol_coef22 = get_poly_coef(
        #     X=df[f'Pmech[kW]_{work_freq}h'], 
        #     y=df[f"Q [m3/h]_{work_freq}h"]
        # )

        # G48 = 225 * (690 / 1000) * 0.9 * 1.73 * 0.94 * 0.97

        # G56 = get_point(
        #     pol_coef=pol_coef22, 
        #     ref_point=G48
        # )

        # fig.add_scatter(
        #     x=[G56], 
        #     y=[455], 
        #     mode='markers', 
        #     marker_color="green",
        #     marker_symbol='diamond', 
        #     name='Work1 WP - P',
        #     row=1, 
        #     col=1
        # )

        # pol_coef30 = get_poly_coef(
        #     X=df[f'H [m]_{opti_freq}h'], 
        #     y=df[f"Q [m3/h]_{opti_freq}h"]
        # )

        # H55 = get_point(
        #     pol_coef=pol_coef30, 
        #     ref_point=420
        # )

        # fig.add_scatter(
        #     x=[H55], 
        #     y=[420], 
        #     mode='markers', 
        #     marker_color="blue",
        #     marker_symbol='diamond', 
        #     name='Opti WP',
        #     row=1, 
        #     col=1
        # )

        # plotting specific points for the second plot (chart 2)
        pol_coef10 = get_poly_coef(
            X=df["Q [m3/h]_50hz"], 
            y=df['Pmech[kW]_50hz']
        )

        F46 = get_point(
            pol_coef=pol_coef10, 
            ref_point=150
        )

        fig.add_scatter(
            x=[150], 
            y=[F46], 
            mode='markers',
            marker=dict(   # setting highlighted point related parameters: marker representation, left y axis
                color='black',
                size=15,
                symbol='circle-open',
                line=dict(
                    color='black',
                    width=3
                )
             ), 
            # marker_color="red",
            # marker_symbol='diamond',
            name='50Hz graafik',
            row=2, 
            col=1
        )

        df_dp_ay2 = F46 - df['Pmech[kW]_50hz'].max()

        fig.add_annotation(
            x=150, 
            y=F46,
            #text=f'<b>{chart1_x1[0].strftime("%Y-%m-%d %H:%M")}, <br> {chart1_y1[0]:.0f} {temp_metric_left}</b>',
            text=f'<b>Design <br>150 m3/h <br>{F46:.0f} mH2O</b>',
            yanchor='bottom',
            # showarrow=True,
            # arrowhead=1,
            # arrowsize=1,
            # arrowwidth=2,
            # arrowcolor="black",
            ax=60,
            ay=df_dp_ay2,#chart4_y[0]-main_df["Mechanical power - measured; kW"].max()-20,
            font=dict(size=12, color='black', family="ISOCPEUR"),
            align="left",
            #bgcolor="white"
            row=2, 
            col=1
        )

        fig.add_scatter(
            x=df[f"Q [m3/h]_{work_freq}h"], 
            y=df[f'Pmech[kW]_{work_freq}h'], 
            mode='lines', 
            line_color='lightgreen', 
            name='Work1 sagedus',
            row=2, 
            col=1
        )

        fig.add_scatter(
            x=[df[f"Q [m3/h]_{work_freq}h"].iloc[-1]+10], 
            y=[df[f'Pmech[kW]_{work_freq}h'].iloc[-1]], 
            mode='text', 
            #text_color='blue',
            #marker_color="blue",
            #marker_symbol='diamond', 
            #name='Working Point-Head'
            text=f'{work_freq} HZ',
            textfont=dict(
                color='lightgreen'
            ),
            row=2, 
            col=1
        )

        # fig.add_scatter(
        #     x=[G56], 
        #     y=[round(G48, 0)], 
        #     mode='markers', 
        #     marker_color="darkblue",
        #     marker_symbol='diamond', 
        #     name='Working Point - Power',
        #     row=2, 
        #     col=1
        # )

        # fig.add_scatter(
        #     x=df[f"Q [m3/h]_{opti_freq}h"], 
        #     y=df[f'Pmech[kW]_{opti_freq}h'], 
        #     mode='lines', 
        #     line_color='purple', 
        #     name='Opti sagedus',
        #     row=2, 
        #     col=1
        # )

        # pol_coef19 = get_poly_coef(
        #     X=df[f'Q [m3/h]_{work_freq}h'], 
        #     y=df[f"Pmech[kW]_{work_freq}h"]
        # )

        # G47 = get_point(
        #     pol_coef=pol_coef19, 
        #     ref_point=G55
        # )

        # fig.add_scatter(
        #     x=[G55], 
        #     y=[G47], 
        #     mode='markers', 
        #     marker_color="orange",
        #     marker_symbol='diamond', 
        #     name='Working Point-Head',
        #     row=2, 
        #     col=1
        # )

        # pol_coef28 = get_poly_coef(
        #     X=df[f'Q [m3/h]_{opti_freq}h'], 
        #     y=df[f"Pmech[kW]_{opti_freq}h"]
        # )

        # H47 = get_point(
        #     pol_coef=pol_coef28, 
        #     ref_point=H55
        # )

        # fig.add_scatter(
        #     x=[H55], 
        #     y=[H47], 
        #     mode='markers', 
        #     marker_color="purple",
        #     marker_symbol='diamond',
        #     name='Opti sagedus',
        #     row=2, 
        #     col=1
        # )


        chart3_time = [main_df.loc[point_index, "Time"]]
        chart3_x = [main_df.loc[point_index, "Pump flow according to H; m3/h"]]
        chart3_y = [main_df.loc[point_index, "Head; mH2O"]]

        fig.add_scatter(
            x=chart3_x, 
            y=chart3_y, 
            mode='markers', 
            marker=dict(   # setting highlighted point related parameters: marker representation, left y axis
                color='black',
                size=15,
                symbol='circle-open',
                line=dict(
                    color='black',
                    width=3
                )
             ), 
            showlegend=False, 
            hovertemplate='',
            row=1, 
            col=1
        )

        wf_wp_ay1 = chart3_y[0] - df[f'H [m]_{work_freq}h'].max()

        # setting annotation for the first plot (chart 2)
        fig.add_annotation(
            x=chart3_x[0], 
            y=chart3_y[0],
            #text=f'<b>{chart3_time[0].strftime("%Y-%m-%d %H:%M")}, <br> {chart3_x[0]:.0f} m3/h <br> {chart3_y[0]:.0f} mH2O</b>',
            text=f'<b>Working <br>{chart3_x[0]:.0f} m3/h <br>{chart3_y[0]:.0f} mH2O</b>',
            # showarrow=True,
            # arrowhead=1,
            # arrowsize=1,
            # arrowwidth=2,
            # arrowcolor="#636363",
            ax=-120,
            ay=df_dp_ay1-30,#chart3_y[0]-main_df["Head; mH2O"].min()-20,
            font=dict(size=12, color="black", family="ISOCPEUR"),
            align="left", row=1, col=1
        )

        chart4_time = [main_df.loc[point_index, "Time"]]
        chart4_x = [main_df.loc[point_index, "Pump flow according to H; m3/h"]]
        chart4_y = [main_df.loc[point_index, "Mechanical power - measured; kW"]]

        fig.add_scatter(
            x=chart4_x, 
            y=chart4_y, 
            mode='markers',
            marker=dict(   # setting highlighted point related parameters: marker representation, left y axis
                color='black',
                size=15,
                symbol='circle-open',
                line=dict(
                    color='black',
                    width=3
                )
             ), 
            showlegend=False, 
            hovertemplate='',
            row=2, 
            col=1
        )

        wf_wp_ay2 = chart4_y[0] - df[f'Pmech[kW]_{work_freq}h'].max()

        # setting annotation for the second plot (chart 1)
        fig.add_annotation(
            x=chart4_x[0], 
            y=chart4_y[0],
            #text=f'<b>{chart4_time[0].strftime("%Y-%m-%d %H:%M")}, <br> {chart4_x[0]:.0f} m3/h <br> {chart4_y[0]:.0f} kW</b>',
            text=f'<b>Working <br>{chart4_x[0]:.0f} m3/h <br>{chart4_y[0]:.0f} kW</b>',
            #yanchor='bottom',
            # showarrow=True,
            # arrowhead=1,
            # arrowsize=1,
            # arrowwidth=2,
            # arrowcolor="#636363",
            ax=-120,
            ay=df_dp_ay2-30,#chart4_y[0]-main_df["Mechanical power - measured; kW"].min()-20,
            font=dict(size=12, color="black", family="ISOCPEUR"),
            align="left", row=2, col=1
        )
    else:
        pass

    fig.update_layout(showlegend=False)

    return fig

def create_chart3(df, point_highlight=False, filter_points=False, point_index=None, points_range=None, screen_size=screen_size):
    '''Creates chart 3

       Params:
       df: dataframe, contains the data for the chart
       point_highlight: boolean, True if a point should be highlighted
       filter_points: boolean, True if a range of points is selected
       point_index: int, index of a point to highlight in the data
       points_range: list, contains indexes of coordinates to include in the chart

       Returns
       fig: plotly figure object
    '''

    if filter_points:
        df = df[df.index.isin(points_range)]
    else:
        pass

    # creating the plot
    fig = go.Figure(
        data=go.Scattergl(
            x=df["Pump flow according to H; m3/h"], 
            y=df["Head; mH2O"], 
            mode='markers', 
            marker_color='blue'
        )
    )
    
    # setting title and its font size for y axis
    fig['layout']['yaxis']['title']="Head, mH2O"
    fig['layout']['yaxis']['title']['font']['size'] = 12

    # fig['layout']['xaxis']['title']="Flow, m3/h"
    # fig['layout']['xaxis']['title']['font']['size'] = 12

    fig['layout']['xaxis']['showticklabels']=False

    fig['layout']['clickmode']='event+select'

    # setting logo path
    cwd_path = os.getcwd()
    logo_file_name = 'enerwise_logo_varviline.png'
    logo_path = os.path.join(cwd_path, logo_file_name)
    encoded_image = base64.b64encode(open(logo_path, 'rb').read())

    # add logo to the chart 1
    fig.add_layout_image(
        dict(
            source='data:image/png;base64,{}'.format(encoded_image.decode()),
            xref="paper", yref="paper",
            x=0, y=1.15,
            sizex=0.23, #0.000168375*screen_size[1],#0.23, 
            sizey=0.2, #0.000260417*screen_size[0],#0.2,
            xanchor="left", yanchor="top"
        )
    )

    fig.update_layout(
        # modebar_orientation='v',  # position of toolbox (select box, autoscale, ...)
        margin=go.layout.Margin(  # setting margin
            l=0, #left margin
            r=0, #right margin
            b=0, #bottom margin
            t=40, #top margin
        ),
        font=dict(
            family="ISOCPEUR",
            size=12
        ),
        plot_bgcolor='#F9F9F9',
        title='''<b>H-Q CURVES</b>''',
        titlefont=dict(
            family="ISOCPEUR",
            size=24
        ),
        width=0.4612005856515373*screen_size[1],  # setting width of the chart 3
        height=0.390625*screen_size[0],  # setting height of the chart 3
        autosize=False,
        title_x=0.5,
        # xaxis=dict(                 
        #     showspikes=True,
        #     spikemode='across+toaxis',
        #     spikesnap='cursor',
        #     showline=True,
        #     showgrid=True,
        #     #spikedash = 'solid'
        # ),
        # yaxis=dict(
        #     showspikes=True,
        #     spikemode='across+toaxis',
        #     spikesnap='cursor',
        #     showline=True,
        #     showgrid=True,
        #     #spikedash = 'solid'
        # )
    )

    fig.update_xaxes(gridcolor='#D9D9D9')
    fig.update_yaxes(gridcolor='#D9D9D9')

    # if filter_points:
    #     df = df[df.index.isin(points_range)]

    #     fig = go.Figure(data=go.Scattergl(x=df["Pump flow according to H; m3/h"], 
    #                                     y=df["Head; mH2O"], 
    #                                     mode='markers', 
    #                                     marker_color='blue'
    #                                     )
    #     )
    #     #fig['layout']['xaxis']['title']="Flow, m3/h"
    #     fig['layout']['yaxis']['title']="Head, mH2O"
    #     fig['layout']['yaxis']['title']['font']['size'] = 10
    #     fig['layout']['xaxis']['showticklabels']=False
    #     fig['layout']['clickmode']='event+select'

    #     fig.update_layout(
    #         modebar_orientation='v',
    #         margin=go.layout.Margin(
    #         l=0, #left margin
    #         r=25, #right margin
    #         b=0, #bottom margin
    #         t=7, #top margin
    #     ),
    #         width=300, height=115)

    #     if point_highlight:
    #         chart3_x = [df.loc[point_index, "Pump flow according to H; m3/h"]]
    #         chart3_y = [df.loc[point_index, "Head; mH2O"]]

    #         fig.add_scatter(
    #             x=chart3_x, 
    #             y=chart3_y, 
    #             mode='markers', 
    #             # marker_color="green",
    #             # marker_symbol='circle-open',
    #             # marker_size=10,
    #             marker=dict(
    #                 color='green',
    #                 size=15,
    #                 symbol='circle-open',
    #                 line=dict(
    #                     color='green',
    #                     width=3
    #                 )
    #             ),
    #             showlegend=False
    #         )

    #         fig.add_annotation(
    #             x=chart3_x[0], 
    #             y=chart3_y[0],
    #             text=f'({chart3_x[0]:.2f}, {chart3_y[0]:.2f})',
    #             #yanchor='bottom',
    #             showarrow=True,
    #             arrowhead=1,
    #             arrowsize=1,
    #             arrowwidth=2,
    #             arrowcolor="#636363",
    #             # ax=-20,
    #             # ay=-30,
    #             font=dict(size=15, color="black", family="Courier New, monospace"),
    #             align="left"
    #         )
    #         fig.update_layout(showlegend=False)
    #     else:
    #         pass
    #     return fig
    # else:
    if point_highlight:
        chart3_x = [df.loc[point_index, "Pump flow according to H; m3/h"]]
        chart3_y = [df.loc[point_index, "Head; mH2O"]]
        chart3_time = [df.loc[point_index, "Time"]]
        # chart3_x=[df["Pump flow according to H; m3/h"].iloc[point_index]]
        # chart3_y=[df["Head; mH2O"].iloc[point_index]]

        # plotting specific point for the first plot (chart 3)
        fig.add_scatter(
            x=chart3_x, 
            y=chart3_y, 
            mode='markers', 
            marker=dict(            # setting highlighted point related parameters: marker representation
                color='black',
                size=15,
                symbol='circle-open',
                line=dict(
                    color='black',
                    width=3
                )
            ),
            showlegend=False
        )

        # setting annotation (chart 3)
        fig.add_annotation(
            x=chart3_x[0], 
            y=chart3_y[0],
            text=f'<b>{chart3_time[0].strftime("%Y-%m-%d %H:%M")}, <br> {chart3_x[0]:.0f} m3/h, <br> {chart3_y[0]:.0f} mH2O</b>',
            # showarrow=True,
            # arrowhead=1,
            # arrowsize=1,
            # arrowwidth=2,
            # arrowcolor="#636363",
            font=dict(
                size=12, 
                color="black", 
                family="ISOCPEUR"
            ),
            align="left",
            bgcolor="white"
        )

        fig.update_layout(showlegend=False)

        # fig.update_traces(
        #     # overwrite=True,
        #     # marker={"opacity": 0.1},
        #     opacity=0.07
        # )
    else:
        pass

    return fig

def create_chart4(df, point_highlight=False, filter_points=False, point_index=None, points_range=None, screen_size=screen_size):
    '''Creates chart 4

       Params:
       df: dataframe, contains the data for the chart
       point_highlight: boolean, True if a point should be highlighted
       filter_points: boolean, True if a range of points is selected
       point_index: int, index of a point to highlight in the data
       points_range: list, contains indexes of coordinates to include in the chart

       Returns
       fig: plotly figure object
    '''
    if filter_points:
        df = df[df.index.isin(points_range)]
    else:
        pass

    # creating the plot (chart 4)
    fig = go.Figure(
        data=go.Scattergl(
            x=df["Pump flow according to H; m3/h"], 
            y=df["Mechanical power - measured; kW"], 
            mode='markers', 
            marker_color='blue'
        )
    )

    # setting title and font size for x and y axis
    fig['layout']['xaxis']['title']="Flow, m3/h"
    fig['layout']['yaxis']['title']="Power mechanical, kW"
    fig['layout']['yaxis']['title']['font']['size'] = 12
    fig['layout']['xaxis']['title']['font']['size'] = 12

    fig['layout']['clickmode']='event+select'

    # setting logo path
    cwd_path = os.getcwd()
    logo_file_name = 'enerwise_logo_varviline.png'
    logo_path = os.path.join(cwd_path, logo_file_name)
    encoded_image = base64.b64encode(open(logo_path, 'rb').read())

    # add logo to the chart 1
    fig.add_layout_image(
        dict(
            source='data:image/png;base64,{}'.format(encoded_image.decode()),
            xref="paper", yref="paper",
            x=0, y=1.18,
            sizex=0.23,#0.000168375*screen_size[1],#0.23, 
            sizey=0.22,#0.000286458*screen_size[0],#0.22,
            xanchor="left", yanchor="top"
        )
    )

    # setting layout of chart 4
    fig.update_layout(
        # modebar_orientation='v',   # position of toolbox (select box, autoscale, ...)
        margin=go.layout.Margin(   # setting margin
            l=0, #left margin
            r=0, #right margin
            b=0, #bottom margin
            t=40, #top margin
        ),
        font=dict(
            family="ISOCPEUR",
            size=12
        ),
        plot_bgcolor='#F9F9F9',
        title='''<b>P-Q CURVES</b>''',
        titlefont=dict(
            family="ISOCPEUR",
            size=24
        ),
        width=0.4612005856515373*screen_size[1], # setting width of the chart 4
        height=0.390625*screen_size[0], # setting height of the chart 4
        autosize=False,
        title_x=0.5,
        # xaxis=dict(                 
        #     showspikes=True,
        #     spikemode='across+toaxis',
        #     spikesnap='cursor',
        #     showline=True,
        #     showgrid=True,
        #     #spikedash = 'solid'
        # ),
        # yaxis=dict(
        #     showspikes=True,
        #     spikemode='across+toaxis',
        #     spikesnap='cursor',
        #     showline=True,
        #     showgrid=True,
        #     #spikedash = 'solid'
        # )
    )

    fig.update_xaxes(gridcolor='#D9D9D9')
    fig.update_yaxes(gridcolor='#D9D9D9')
    # if filter_points:
    #     df = df[df.index.isin(points_range)]
    #     fig = go.Figure(data=go.Scattergl(x=df["Pump flow according to H; m3/h"], 
    #                                     y=df["Mechanical power - measured; kW"], 
    #                                     mode='markers', 
    #                                     marker_color='blue'
    #                                     )
    #     )
    #     fig['layout']['xaxis']['title']="Flow, m3/h"
    #     fig['layout']['yaxis']['title']="Power mechanical, kW"
    #     fig['layout']['yaxis']['title']['font']['size'] = 10
    #     fig['layout']['xaxis']['title']['font']['size'] = 10
    #     fig['layout']['clickmode']='event+select'
    #     # fig = go.FigureWidget(fig)

    #     fig.update_layout(
    #         modebar_orientation='v',
    #         margin=go.layout.Margin(
    #         l=0, #left margin
    #         r=25, #right margin
    #         b=0, #bottom margin
    #         t=7, #top margin
    #     ),
    #         # legend=dict(
    #         #     orientation="h",
    #         #     x=0,
    #         #     y=1.15,
    #         #     traceorder="normal",
    #         #     font=dict(
    #         #         family="sans-serif",
    #         #         size=12,
    #         #         color="black"
    #         #     ),
    #         # ),
    #         width=300, height=155)

    #     if point_highlight:

    #         chart4_x = [df.loc[point_index, "Pump flow according to H; m3/h"]]
    #         chart4_y = [df.loc[point_index, "Mechanical power - measured; kW"]]

    #         fig.add_scatter(x=chart4_x, 
    #                                y=chart4_y, 
    #                                mode='markers', 
    #                                # marker_color="green",
    #                                # marker_symbol='circle-open',
    #                                # marker_size=10
    #                                marker=dict(
    #                                             color='green',
    #                                             size=15,
    #                                             symbol='circle-open',
    #                                             line=dict(
    #                                                 color='green',
    #                                                 width=3
    #                                             )
    #                                 ),
    #                                showlegend=False)
    #         fig.add_annotation(
    #             x=chart4_x[0], 
    #             y=chart4_y[0],
    #             text=f'({chart4_x[0]:.2f}, {chart4_y[0]:.2f})',
    #             #yanchor='bottom',
    #             showarrow=True,
    #             arrowhead=1,
    #             arrowsize=1,
    #             arrowwidth=2,
    #             arrowcolor="#636363",
    #             # ax=-20,
    #             # ay=-30,
    #             font=dict(size=15, color="black", family="Courier New, monospace"),
    #             align="left"
    #         )
    #         fig.update_layout(showlegend=False)
    #     else:
    #         pass
    #     return fig
    # else:
    if point_highlight:
        chart4_x = [df.loc[point_index, "Pump flow according to H; m3/h"]]
        chart4_y = [df.loc[point_index, "Mechanical power - measured; kW"]]
        chart4_time = [df.loc[point_index, "Time"]]
        # chart4_x=[df["Pump flow according to H; m3/h"].iloc[point_index]]
        # chart4_y=[df["Mechanical power - measured; kW"].iloc[point_index]]

        # plotting a specific point for the first plot (chart 4)
        fig.add_scatter(
            x=chart4_x, 
            y=chart4_y, 
            mode='markers', 
            marker=dict(             # setting highlighted point related parameters: marker representation
                color='black',
                size=15,
                symbol='circle-open',
                line=dict(
                    color='black',
                    width=3
                )
            ),
            showlegend=False
        )

        # setting annotation (chart 4)
        fig.add_annotation(
            x=chart4_x[0], 
            y=chart4_y[0],
            text=f'<b>{chart4_time[0].strftime("%Y-%m-%d %H:%M")}, <br> {chart4_x[0]:.0f} m3/h, <br> {chart4_y[0]:.0f} kW</b>',
            # showarrow=True,
            # arrowhead=1,
            # arrowsize=1,
            # arrowwidth=2,
            # arrowcolor="#636363",
            font=dict(
                size=12, 
                color="black", 
                family="ISOCPEUR"
            ),
            align="left",
            bgcolor="white"
        )

        fig.update_layout(showlegend=False)

        # fig.update_traces(
        #     # overwrite=True,
        #     # marker={"opacity": 0.1},
        #     opacity=0.07
        # )
    else:
        pass

    return fig

def create_chart5(df, point_highlight=False, filter_points=False, point_index=None, points_range=None, screen_size=screen_size):
    '''Creates chart 5

       Params:
       df: dataframe, contains the data for the chart
       point_highlight: boolean, True if a point should be highlighted
       filter_points: boolean, True if a range of points is selected
       point_index: list, list of point indexes to highlight in each variable/parameter
       points_range: list, contains indexes of coordinates or 
                           2 lists containing indexes of coordinates for the seperate parameters
                           to include in the chart

       Returns
       fig: plotly figure object
    '''
    # if 'chart5_1' in list(df.columns):
    #     chart5_data1 = df[['chart5_1', 'Mechanical power - measured; kW']]
    #     chart5_data1 = chart5_data1.sort_values('Mechanical power - measured; kW', 
    #                                             ascending=False)
    #     chart5_data1.reset_index(drop=False, inplace=True)
    #     chart5_data1.rename(columns={'index': 'init_pos', 'chart5_1': 'Tunnid'}, inplace=True)

    #     chart5_data2 = df[['chart5_2', 'Pump flow according to H; m3/h']]
    #     chart5_data2 = chart5_data2.sort_values('Pump flow according to H; m3/h', 
    #                                             ascending=False)
    #     chart5_data2.reset_index(drop=False, inplace=True)
    #     chart5_data2.rename(columns={'index': 'init_pos', 'chart5_2': 'Tunnid'}, inplace=True)
    # else:
    time_diff = df['Time'].max() - df['Time'].min()
    hours_in_df = time_diff.total_seconds() / 3600

    chart5_data1 = df[['Mechanical power - measured; kW', 'Time']].reset_index()
    chart5_data1 = chart5_data1.sort_values('Mechanical power - measured; kW', 
                                            ascending=False)
    chart5_data1['Tunnid'] = 1
    chart5_data1['Tunnid'] = chart5_data1['Tunnid'].cumsum()
    chart5_data1['Tunnid'] = 100 * chart5_data1['Tunnid'] / chart5_data1['Tunnid'].shape[0]
    chart5_data1.reset_index(drop=False, inplace=True)
    chart5_data1.rename(columns={'index': 'init_pos'}, inplace=True)

    chart5_data2 = df[['Pump flow according to H; m3/h', 'Time']].reset_index()
    chart5_data2 = chart5_data2.sort_values('Pump flow according to H; m3/h', 
                                            ascending=False)
    chart5_data2['Tunnid'] = 1
    chart5_data2['Tunnid'] = chart5_data2['Tunnid'].cumsum()
    chart5_data2['Tunnid'] = 100 * chart5_data2['Tunnid'] / chart5_data2['Tunnid'].shape[0]
    chart5_data2.reset_index(drop=False, inplace=True)
    chart5_data2.rename(columns={'index': 'init_pos'}, inplace=True)
    
    # creating the first plot (chart 5)
    fig = go.Figure(
        data=go.Scattergl(
            x=chart5_data1["Tunnid"], 
            y=chart5_data1['Mechanical power - measured; kW'], 
            mode='markers', 
            marker_color='blue', 
            name='Load profile - Mechanical power',
            yaxis='y1'
        )
    )

    # creating the second plot (chart 5)
    fig.add_scatter(
        x=chart5_data2["Tunnid"], 
        y=chart5_data2['Pump flow according to H; m3/h'], 
        mode='markers', 
        marker_color='red',
        name='Load profile - Flow',
        yaxis='y2'
    )

    # fig['layout']['yaxis1']['title'] = "Mechanical Power; kW"
    # fig['layout']['yaxis1']['title']['font']['size'] = 12

    # fig['layout']['yaxis2']['title'] = "Flow; m3/h"
    # fig['layout']['yaxis2']['title']['font']['size'] = 12

    fig['layout']['clickmode']='event+select'

    # setting logo path
    cwd_path = os.getcwd()
    logo_file_name = 'enerwise_logo_varviline.png'
    logo_path = os.path.join(cwd_path, logo_file_name)
    encoded_image = base64.b64encode(open(logo_path, 'rb').read())

    # if screen_size[1] > 1366:
    #     w_percent = 0.75 * 0.48
    # else:
    #     w_percent = 0.48

    # add logo to the chart 1
    fig.add_layout_image(
        dict(
            source='data:image/png;base64,{}'.format(encoded_image.decode()),
            xref="paper", yref="paper",
            x=0, y=1.09,#0.00140625*screen_size[0],#1.08,
            sizex=0.22,#0.00011713*screen_size[1],#0.16, #0.000175695*screen_size[1],#0.24, 
            sizey=0.1,#0.000117188*screen_size[0],#0.09, #0.000286458*screen_size[0],#0.22,
            xanchor="left", yanchor="top"
        )
    )

    # setting layout of chart 5
    fig.update_layout(
        legend=dict(                # setting legend parameters (chart5)
            orientation="h",
            x=0,
            y=-0.4,
            traceorder="normal",
            font=dict(
                family="ISOCPEUR",
                size=8,
                color="black"
            ),
        ),
        # modebar_orientation='v',    # position of toolbox (select box, autoscale, ...)
        margin=go.layout.Margin(    # setting margin
            l=0, #left margin
            r=0, #right margin
            b=0, #bottom margin
            t=40, #top margin
        ),
        font=dict(
            family="ISOCPEUR",
            size=12
        ),
        plot_bgcolor='#F9F9F9',
        title='''<b>LOAD PROFILE</b>''',
        titlefont=dict(
            family="ISOCPEUR",
            size=24
        ),
        width=500,#w_percent*screen_size[1],#0.48316251830161056*screen_size[1],  # setting width of the chart 5
        height=450, #0.625*screen_size[0], # setting height of the chart 5
        autosize=False,
        showlegend=False,
        title_x=0.5,
        # xaxis=dict(                 
        #     showspikes=True,
        #     spikemode='across+toaxis',
        #     spikesnap='cursor',
        #     showline=True,
        #     showgrid=True,
        #     #spikedash = 'solid'
        # ),
        # yaxis=dict(
        #     showspikes=True,
        #     spikemode='across+toaxis',
        #     spikesnap='cursor',
        #     showline=True,
        #     showgrid=True,
        #     #spikedash = 'solid'
        # ),
        # yaxis2=dict(
        #     showspikes=True,
        #     spikemode='across+toaxis',
        #     spikesnap='cursor',
        #     showline=True,
        #     showgrid=True,
        #     #spikedash = 'solid'
        # )
    )

    fig.update_xaxes(gridcolor='#D9D9D9')
    fig.update_xaxes(rangemode="tozero")
    # fig.update_yaxes(gridcolor='#D9D9D9')

    #setting title and font size for x axis
    fig['layout']['xaxis']['title'] = f"% of the time from {hours_in_df:.2f} h"
    fig['layout']['xaxis']['title']['font']['size'] = 12

    fig['layout']['yaxis'] = dict(
        title="Mechanical Power; kW",
        titlefont = dict(
            size=12
        ),
        color='blue',
        showgrid=True,
        gridcolor='#D9D9D9',
        # showspikes=True,
        # spikemode='across+toaxis',
        # spikesnap='cursor',
        # showline=True,
    )

    fig['layout']['yaxis2'] = dict(
        title="Flow; m3/h",
        titlefont = dict(
            size=12
        ),
        overlaying='y',
        side='right',
        color='red',
        showgrid=False,
        # showspikes=True,
        # spikemode='across+toaxis',
        # spikesnap='cursor',
        # showline=True
    )

    if filter_points:
        if isinstance(points_range[0], list) or isinstance(points_range[1], list):
            if len(points_range[0]) != 0:
                chart5_data1 = chart5_data1[chart5_data1['init_pos'].isin(points_range[0])]
            else:
                chart5_data2 = chart5_data2[chart5_data2['init_pos'].isin(points_range[1])]

                # creating the plot (chart 5)
                fig = go.Figure(
                    data=go.Scattergl(
                        x=chart5_data2["Tunnid"], 
                        y=chart5_data2['Pump flow according to H; m3/h'], 
                        mode='markers', 
                        marker_color='red',
                        name='Load profile - Flow',
                        yaxis='y2'
                    )
                )

                # setting title and font size for x axis
                # fig['layout']['xaxis']['title']="% of the time from 30'001 h"
                # fig['layout']['xaxis']['title']['font']['size'] = 12

                # fig['layout']['yaxis']['title']="Mechanical Power; kW"
                # fig['layout']['yaxis']['title']['font']['size'] = 12

                fig['layout']['clickmode']='event+select'

                # setting logo path
                cwd_path = os.getcwd()
                logo_file_name = 'enerwise_logo_varviline.png'
                logo_path = os.path.join(cwd_path, logo_file_name)
                encoded_image = base64.b64encode(open(logo_path, 'rb').read())

                # add logo to the chart 1
                fig.add_layout_image(
                    dict(
                        source='data:image/png;base64,{}'.format(encoded_image.decode()),
                        xref="paper", yref="paper",
                        x=0, y=1.09,#0.00140625*screen_size[0],#1.08,
                        sizex=0.22,#0.00011713*screen_size[1],#0.16, #0.000175695*screen_size[1],#0.24, 
                        sizey=0.1,#0.000117188*screen_size[0],#0.09, #0.000286458*screen_size[0],#0.22,
                        xanchor="left", yanchor="top"
                    )
                )

                # setting layout of chart 5
                fig.update_layout(
                    legend=dict(           # setting legend parameters (chart5)
                        orientation="h",
                        x=0,
                        y=-0.4,
                        traceorder="normal",
                        font=dict(
                            family="sans-serif",
                            size=8,
                            color="black"
                        ),
                    ),
                    # modebar_orientation='v',  # position of toolbox (select box, autoscale, ...)
                    margin=go.layout.Margin(  # setting margin
                        l=0, #left margin
                        r=0, #right margin
                        b=0, #bottom margin
                        t=40, #top margin
                    ),
                    font=dict(
                        family="ISOCPEUR",
                        size=12
                    ),
                    plot_bgcolor='#F9F9F9',
                    title='''<b>LOAD PROFILE</b>''',
                    titlefont=dict(
                        family="ISOCPEUR",
                        size=24
                    ),
                    width=500,#w_percent*screen_size[1],#0.48316251830161056*screen_size[1],  # setting width of the chart 5
                    height=450, #0.625*screen_size[0], # setting height of the chart 5
                    autosize=False,
                    showlegend=False,
                    title_x=0.5,
                    # xaxis=dict(                 
                    #     showspikes=True,
                    #     spikemode='across+toaxis',
                    #     spikesnap='cursor',
                    #     showline=True,
                    #     showgrid=True,
                    #     #spikedash = 'solid'
                    # ),
                    # yaxis=dict(
                    #     showspikes=True,
                    #     spikemode='across+toaxis',
                    #     spikesnap='cursor',
                    #     showline=True,
                    #     showgrid=True,
                    #     #spikedash = 'solid'
                    # ),
                    # yaxis2=dict(
                    #     showspikes=True,
                    #     spikemode='across+toaxis',
                    #     spikesnap='cursor',
                    #     showline=True,
                    #     showgrid=True,
                    #     #spikedash = 'solid'
                    # )
                )

                fig.update_xaxes(gridcolor='#D9D9D9')
                fig.update_xaxes(rangemode="tozero")
                # fig.update_yaxes(gridcolor='#D9D9D9')

                #setting title and font size for x axis
                fig['layout']['xaxis']['title'] = f"% of the time from {hours_in_df:.2f} h"
                fig['layout']['xaxis']['title']['font']['size'] = 12

                fig['layout']['yaxis'] = dict(
                    title="Mechanical Power; kW",
                    titlefont = dict(
                        size=12
                    ),
                    color='blue',
                    showgrid=True,
                    gridcolor='#D9D9D9',
                    # showspikes=True,
                    # spikemode='across+toaxis',
                    # spikesnap='cursor',
                    # showline=True
                )

                fig['layout']['yaxis2'] = dict(
                    title="Flow; m3/h",
                    titlefont = dict(
                        size=12
                    ),
                    overlaying='y',
                    side='right',
                    color='red',
                    showgrid=False,
                    # showspikes=True,
                    # spikemode='across+toaxis',
                    # spikesnap='cursor',
                    # showline=True
                )

                if point_highlight:
                    # chart5_x1 = [chart5_data1.loc[point_index[0], "Tunnid"]]
                    # chart5_y1 = [chart5_data1.loc[point_index[0], "Mechanical power - measured; kW"]]

                    # fig.add_scatter(x=chart5_x1, 
                    #                        y=chart5_y1, 
                    #                        mode='markers', 
                    #                        # marker_color="green",
                    #                        # marker_symbol='circle-open',
                    #                        # marker_size=10
                    #                        marker=dict(
                    #                                     color='green',
                    #                                     size=15,
                    #                                     symbol='circle-open',
                    #                                     line=dict(
                    #                                         color='green',
                    #                                         width=3
                    #                                     )
                    #                         ),
                    #                        showlegend=False)
                    # fig.add_annotation(
                    #     x=chart5_x1[0], 
                    #     y=chart5_y1[0],
                    #     text=f'({chart5_x1[0]:.0f}, {chart5_y1[0]:.2f})',
                    #     #yanchor='bottom',
                    #     showarrow=True,
                    #     arrowhead=1,
                    #     arrowsize=1,
                    #     arrowwidth=2,
                    #     arrowcolor="#636363",
                    #     # ax=-20,
                    #     # ay=-30,
                    #     font=dict(size=15, color="black", family="Courier New, monospace"),
                    #     align="left"
                    # )

                    chart5_x2 = [chart5_data2.loc[point_index[1], "Tunnid"]]
                    chart5_y2 = [chart5_data2.loc[point_index[1], 'Pump flow according to H; m3/h']]
                    chart52_time = [chart5_data2.loc[point_index[1], 'Time']]

                    chart5_y2_ay = chart5_y2[0] - chart5_data2['Pump flow according to H; m3/h'].max() - 30

                    # plotting a specific point for the second plot (chart 5)
                    fig.add_scatter(
                        x=chart5_x2, 
                        y=chart5_y2, 
                        mode='markers', 
                        marker=dict(      # setting highlighted point related parameters: marker representation
                            color='black',
                            size=15,
                            symbol='circle-open',
                            line=dict(
                                color='black',
                                width=3
                            )
                        ),
                        showlegend=False,
                        yaxis='y2'
                    )

                    # setting annotation for the second plot(chart 5)
                    fig.add_annotation(
                        x=chart5_x2[0], 
                        y=chart5_y2[0],
                        text=f'<b>{chart52_time[0].strftime("%Y-%m-%d %H:%M")}, <br>{chart5_x2[0]:.0f} %, <br>{chart5_y2[0]:.0f} m3/h</b>',
                        # showarrow=True,
                        # arrowhead=1,
                        # arrowsize=1,
                        # arrowwidth=2,
                        # arrowcolor="#636363",
                        font=dict(
                            size=12, 
                            color="black", 
                            family="ISOCPEUR"
                        ),
                        align="left",
                        yref='y2',
                        bgcolor="white",
                        ax=60,
                        ay=chart5_y2_ay
                    )

                    # fig.update_traces(
                    #     # overwrite=True,
                    #     # marker={"opacity": 0.1},
                    #     opacity=0.07
                    # )      
                else:
                    pass

                return fig

            if len(points_range[1]) != 0:
                chart5_data2 = chart5_data2[chart5_data2['init_pos'].isin(points_range[1])]
            else:
                chart5_data1 = chart5_data1[chart5_data1['init_pos'].isin(points_range[0])]

                # creating the first plot (chart 5)
                fig = go.Figure(
                    data=go.Scattergl(
                        x=chart5_data1["Tunnid"], 
                        y=chart5_data1['Mechanical power - measured; kW'], 
                        mode='markers', 
                        marker_color='blue', 
                        name='Load profile - Mechanical power',
                        yaxis='y1'
                    )
                )

                # setting title and font size for x axis
                # fig['layout']['xaxis']['title']="% of the time from 30'001 h"
                # fig['layout']['xaxis']['title']['font']['size'] = 12

                # fig['layout']['yaxis']['title']="Mechanical Power; kW"
                # fig['layout']['yaxis']['title']['font']['size'] = 12

                fig['layout']['clickmode']='event+select'

                # setting logo path
                cwd_path = os.getcwd()
                logo_file_name = 'enerwise_logo_varviline.png'
                logo_path = os.path.join(cwd_path, logo_file_name)
                encoded_image = base64.b64encode(open(logo_path, 'rb').read())

                # add logo to the chart 1
                fig.add_layout_image(
                    dict(
                        source='data:image/png;base64,{}'.format(encoded_image.decode()),
                        xref="paper", yref="paper",
                        x=0, y=1.09,#0.00140625*screen_size[0],#1.08,
                        sizex=0.22,#0.00011713*screen_size[1],#0.16, #0.000175695*screen_size[1],#0.24, 
                        sizey=0.1,#0.000117188*screen_size[0],#0.09, #0.000286458*screen_size[0],#0.22,
                        xanchor="left", yanchor="top"
                    )
                )

                # setting layout of chart 5 
                fig.update_layout(
                    legend=dict(               # setting legend parameters (chart5)
                        orientation="h",
                        x=0,
                        y=-0.4,
                        traceorder="normal",
                        font=dict(
                            family="ISOCPEUR",
                            size=8,
                            color="black"
                        ),
                    ),
                    # modebar_orientation='v',     # position of toolbox (select box, autoscale, ...)
                    margin=go.layout.Margin(     # setting margin
                        l=0, #left margin
                        r=0, #right margin
                        b=0, #bottom margin
                        t=40, #top margin
                    ),
                    font=dict(
                        family="ISOCPEUR",
                        size=12
                    ),
                    plot_bgcolor='#F9F9F9',
                    title='''<b>LOAD PROFILE</b>''',
                    titlefont=dict(
                        family="ISOCPEUR",
                        size=12
                    ),
                    width=500,#w_percent*screen_size[1],#0.48316251830161056*screen_size[1],  # setting width of the chart 5
                    height=450, #0.625*screen_size[0], # setting height of the chart 5
                    autosize=False,
                    showlegend=False,
                    title_x=0.5,
                    # xaxis=dict(                 
                    #     showspikes=True,
                    #     spikemode='across+toaxis',
                    #     spikesnap='cursor',
                    #     showline=True,
                    #     showgrid=True,
                    #     #spikedash = 'solid'
                    # ),
                    # yaxis=dict(
                    #     showspikes=True,
                    #     spikemode='across+toaxis',
                    #     spikesnap='cursor',
                    #     showline=True,
                    #     showgrid=True,
                    #     #spikedash = 'solid'
                    # ),
                    # yaxis2=dict(
                    #     showspikes=True,
                    #     spikemode='across+toaxis',
                    #     spikesnap='cursor',
                    #     showline=True,
                    #     showgrid=True,
                    #     #spikedash = 'solid'
                    # )
                )


                fig.update_xaxes(gridcolor='#D9D9D9')
                fig.update_xaxes(rangemode="tozero")
                # fig.update_yaxes(gridcolor='#D9D9D9')

                #setting title and font size for x axis
                fig['layout']['xaxis']['title'] = f"% of the time from {hours_in_df:.2f} h"
                fig['layout']['xaxis']['title']['font']['size'] = 12

                fig['layout']['yaxis'] = dict(
                    title="Mechanical Power; kW",
                    titlefont = dict(
                        size=12
                    ),
                    color='blue',
                    showgrid=True,
                    gridcolor='#D9D9D9',
                    # showspikes=True,
                    # spikemode='across+toaxis',
                    # spikesnap='cursor',
                    # showline=True
                )

                fig['layout']['yaxis2'] = dict(
                    title="Flow; m3/h",
                    titlefont = dict(
                        size=12
                    ),
                    overlaying='y',
                    side='right',
                    color='red',
                    showgrid=False,
                    # showspikes=True,
                    # spikemode='across+toaxis',
                    # spikesnap='cursor',
                    # showline=True
                )

                if point_highlight:
                    chart5_x1 = [chart5_data1.loc[point_index[0], "Tunnid"]]
                    chart5_y1 = [chart5_data1.loc[point_index[0], "Mechanical power - measured; kW"]]
                    chart51_time = [chart5_data1.loc[point_index[0], "Time"]]

                    chart5_y1_ay = chart5_y1[0] - chart5_data1["Mechanical power - measured; kW"].max() - 30

                    # plotting a specific point for the first plot (chart 5)
                    fig.add_scatter(
                        x=chart5_x1, 
                        y=chart5_y1, 
                        mode='markers', 
                        marker=dict(              # setting highlighted point related parameters: marker representation
                            color='black',
                            size=15,
                            symbol='circle-open',
                            line=dict(
                                color='black',
                                width=3
                            )
                        ),
                        showlegend=False,
                        yaxis='y1'
                    )

                    # setting annotation for the first plot (chart 5)
                    fig.add_annotation(
                        x=chart5_x1[0], 
                        y=chart5_y1[0],
                        text=f'<b>{chart51_time[0].strftime("%Y-%m-%d %H:%M")}, <br>{chart5_x1[0]:.0f} %, <br>{chart5_y1[0]:.0f} kW</b>',
                        # showarrow=True,
                        # arrowhead=1,
                        # arrowsize=1,
                        # arrowwidth=2,
                        # arrowcolor="#636363",
                        font=dict(
                            size=12, 
                            color="black", 
                            family="ISOCPEUR"
                        ),
                        align="left",
                        yref='y1',
                        bgcolor="white",
                        ax=240,
                        ay=chart5_y1_ay
                    )

                    # fig.update_traces(
                    #     # overwrite=True,
                    #     # marker={"opacity": 0.1},
                    #     opacity=0.07
                    # )

                    # chart5_x2 = [chart5_data2.loc[point_index[1], "Tunnid"]]
                    # chart5_y2 = [chart5_data2.loc[point_index[1], 'Pump flow according to H; m3/h']]

                    # fig.add_scatter(x=chart5_x2, 
                    #                        y=chart5_y2, 
                    #                        mode='markers', 
                    #                        # marker_color="green",
                    #                        # marker_symbol='circle-open',
                    #                        # marker_size=10
                    #                        marker=dict(
                    #                                     color='green',
                    #                                     size=15,
                    #                                     symbol='circle-open',
                    #                                     line=dict(
                    #                                         color='green',
                    #                                         width=3
                    #                                     )
                    #                         ),
                    #                        showlegend=False)
                    # fig.add_annotation(
                    #     x=chart5_x2[0], 
                    #     y=chart5_y2[0],
                    #     text=f'({chart5_x2[0]:.0f}, {chart5_y2[0]:.2f})',
                    #     #yanchor='bottom',
                    #     showarrow=True,
                    #     arrowhead=1,
                    #     arrowsize=1,
                    #     arrowwidth=2,
                    #     arrowcolor="#636363",
                    #     # ax=-20,
                    #     # ay=-30,
                    #     font=dict(size=15, color="black", family="Courier New, monospace"),
                    #     align="left"
                    # )       
                else:
                    pass

                return fig

        else:
            chart5_data1 = chart5_data1[chart5_data1['init_pos'].isin(points_range)]
            chart5_data2 = chart5_data2[chart5_data2['init_pos'].isin(points_range)]

        # creating plot the first plot (chart 5)
        fig = go.Figure(
            data=go.Scattergl(
                x=chart5_data1["Tunnid"], 
                y=chart5_data1['Mechanical power - measured; kW'], 
                mode='markers', 
                marker_color='blue', 
                name='Load profile - Mechanical power',
                yaxis='y1'
            )
        )

        # creating plot the second plot (chart 5)
        fig.add_scatter(
            x=chart5_data2["Tunnid"], 
            y=chart5_data2['Pump flow according to H; m3/h'], 
            mode='markers', 
            marker_color='red',
            name='Load profile - Flow',
            yaxis='y2'
        )

        # setting title and font size for x axis
        # fig['layout']['xaxis']['title']="% of the time from 30'001 h"
        # fig['layout']['xaxis']['title']['font']['size'] = 12

        # fig['layout']['yaxis']['title']="Mechanical Power; kW"
        # fig['layout']['yaxis']['title']['font']['size'] = 12

        fig['layout']['clickmode']='event+select'

        # setting logo path
        cwd_path = os.getcwd()
        logo_file_name = 'enerwise_logo_varviline.png'
        logo_path = os.path.join(cwd_path, logo_file_name)
        encoded_image = base64.b64encode(open(logo_path, 'rb').read())

        # add logo to the chart 1
        fig.add_layout_image(
            dict(
                source='data:image/png;base64,{}'.format(encoded_image.decode()),
                xref="paper", yref="paper",
                x=0, y=1.09,#0.00140625*screen_size[0],#1.08,
                sizex=0.22,#0.00011713*screen_size[1],#0.16, #0.000175695*screen_size[1],#0.24, 
                sizey=0.1,#0.000117188*screen_size[0],#0.09, #0.000286458*screen_size[0],#0.22,
                xanchor="left", yanchor="top"
            )
        )

        # setting layout of chart 5
        fig.update_layout(
            legend=dict(                    # setting legend parameters (chart5)
                orientation="h",
                x=0,
                y=-0.4,
                traceorder="normal",
                font=dict(
                    family="ISOCPEUR",
                    size=8,
                    color="black"
                ),
            ),
            # modebar_orientation='v',        # position of toolbox (select box, autoscale, ...)
            margin=go.layout.Margin(        # setting margin
                l=0, #left margin
                r=0, #right margin
                b=0, #bottom margin
                t=40, #top margin
            ),
            font=dict(
                family="ISOCPEUR",
                size=12
            ),
            plot_bgcolor='#F9F9F9',
            title='''<b>LOAD PROFILE</b>''',
            titlefont=dict(
                family="ISOCPEUR",
                size=24
            ),
            width=500,#w_percent*screen_size[1],#0.48316251830161056*screen_size[1],  # setting width of the chart 5
            height=450, #0.625*screen_size[0], # setting height of the chart 5
            autosize=False,
            showlegend=False,
            title_x=0.5,
            # xaxis=dict(                 
            #     showspikes=True,
            #     spikemode='across+toaxis',
            #     spikesnap='cursor',
            #     showline=True,
            #     showgrid=True,
            #     #spikedash = 'solid'
            # ),
            # yaxis=dict(
            #     showspikes=True,
            #     spikemode='across+toaxis',
            #     spikesnap='cursor',
            #     showline=True,
            #     showgrid=True,
            #     #spikedash = 'solid'
            # ),
            # yaxis2=dict(
            #     showspikes=True,
            #     spikemode='across+toaxis',
            #     spikesnap='cursor',
            #     showline=True,
            #     showgrid=True,
            #     #spikedash = 'solid'
            # )
        )

        fig.update_xaxes(gridcolor='#D9D9D9')
        fig.update_xaxes(rangemode="tozero")
        # fig.update_yaxes(gridcolor='#D9D9D9')

        #setting title and font size for x axis
        fig['layout']['xaxis']['title'] = f"% of the time from {hours_in_df:.2f} h"
        fig['layout']['xaxis']['title']['font']['size'] = 12

        fig['layout']['yaxis'] = dict(
            title="Mechanical Power; kW",
            titlefont = dict(
                size=12
            ),
            color='blue',
            showgrid=True,
            gridcolor='#D9D9D9',
            # showspikes=True,
            # spikemode='across+toaxis',
            # spikesnap='cursor',
            # showline=True
        )

        fig['layout']['yaxis2'] = dict(
            title="Flow; m3/h",
            titlefont = dict(
                size=12
            ),
            overlaying='y',
            side='right',
            color='red',
            showgrid=False,
            # showspikes=True,
            # spikemode='across+toaxis',
            # spikesnap='cursor',
            # showline=True
        )

        if point_highlight:
            # chart5_data1.rename(columns={'index': 'point_index'}, inplace=True)
            # chart5_data2.rename(columns={'index': 'point_index'}, inplace=True)
            # chart5_x1=[chart5_data1["Tunnid"].iloc[point_index[0]]]
            # chart5_y1=[chart5_data1["Mechanical power - measured; kW"].iloc[point_index[0]]]
            chart5_x1 = [chart5_data1.loc[point_index[0], "Tunnid"]]
            chart5_y1 = [chart5_data1.loc[point_index[0], "Mechanical power - measured; kW"]]
            chart51_time = [chart5_data1.loc[point_index[0], "Time"]]

            chart5_y1_ay = chart5_y1[0] - chart5_data1["Mechanical power - measured; kW"].max() - 30

            # plotting a specific point for the first plot (chart 5)
            fig.add_scatter(
                x=chart5_x1, 
                y=chart5_y1, 
                mode='markers', 
                marker=dict(           # setting highlighted point related parameters: marker representation
                    color='black',
                    size=15,
                    symbol='circle-open',
                    line=dict(
                        color='black',
                        width=3
                    )
                ),
                showlegend=False,
                yaxis='y1'
            )

            # setting annotation for the first plot (chart 5)
            fig.add_annotation(
                x=chart5_x1[0], 
                y=chart5_y1[0],
                text=f'<b>{chart51_time[0].strftime("%Y-%m-%d %H:%M")}, <br>{chart5_x1[0]:.0f} %, <br>{chart5_y1[0]:.0f} kW</b>',
                # showarrow=True,
                # arrowhead=1,
                # arrowsize=1,
                # arrowwidth=2,
                # arrowcolor="#636363",
                font=dict(
                    size=12, 
                    color="black", 
                    family="ISOCPEUR"
                ),
                align="left",
                yref='y1',
                bgcolor="white",
                ax=240,
                ay=chart5_y1_ay
            )

            # chart5_x2=[chart5_data2["Tunnid"].iloc[point_index[1]]]
            # chart5_y2=[chart5_data2['Pump flow according to H; m3/h'].iloc[point_index[1]]]
            chart5_x2 = [chart5_data2.loc[point_index[1], "Tunnid"]]
            chart5_y2 = [chart5_data2.loc[point_index[1], 'Pump flow according to H; m3/h']]
            chart52_time = [chart5_data2.loc[point_index[1], 'Time']]

            chart5_y2_ay = chart5_y2[0] - chart5_data2['Pump flow according to H; m3/h'].max() - 30

            # plotting a specific point for the second plot (chart 5)
            fig.add_scatter(
                x=chart5_x2, 
                y=chart5_y2, 
                mode='markers', 
                marker=dict(              # setting highlighted point related parameters: marker representation
                    color='black',
                    size=15,
                    symbol='circle-open',
                    line=dict(
                        color='black',
                        width=3
                    )
                ),
                showlegend=False,
                yaxis='y2'
            )

            # setting annotation for the second plot (chart 5)
            fig.add_annotation(
                x=chart5_x2[0], 
                y=chart5_y2[0],
                text=f'<b>{chart52_time[0].strftime("%Y-%m-%d %H:%M")}, <br>{chart5_x2[0]:.0f} %, <br>{chart5_y2[0]:.0f} m3/h</b>',
                # showarrow=True,
                # arrowhead=1,
                # arrowsize=1,
                # arrowwidth=2,
                # arrowcolor="#636363",
                font=dict(
                    size=12, 
                    color="black", 
                    family="ISOCPEUR"
                ),
                align="left",
                yref='y2',
                bgcolor="white",
                ax=60,
                ay=chart5_y2_ay
            )

            # fig.update_traces(
            #     # overwrite=True,
            #     # marker={"opacity": 0.1},
            #     opacity=0.07
            # )     
        else:
            pass
        return fig
    else:
        if point_highlight:
            # chart5_data1.rename(columns={'index': 'point_index'}, inplace=True)
            # chart5_data2.rename(columns={'index': 'point_index'}, inplace=True)
            # chart5_x1=[chart5_data1["Tunnid"].iloc[point_index[0]]]
            # chart5_y1=[chart5_data1["Mechanical power - measured; kW"].iloc[point_index[0]]]
            chart5_x1 = [chart5_data1.loc[point_index[0], "Tunnid"]]
            chart5_y1 = [chart5_data1.loc[point_index[0], "Mechanical power - measured; kW"]]
            chart51_time = [chart5_data1.loc[point_index[0], "Time"]]

            chart5_y1_ay = chart5_y1[0] - chart5_data1["Mechanical power - measured; kW"].max() - 30

            # plotting a specific point for the first plot (chart 5)
            fig.add_scatter(
                x=chart5_x1, 
                y=chart5_y1, 
                mode='markers', 
                marker=dict(           # setting highlighted point related parameters: marker representation
                    color='black',
                    size=15,
                    symbol='circle-open',
                    line=dict(
                        color='black',
                        width=3
                    )
                ),
                showlegend=False,
                yaxis='y1'
            )

            # setting annotation for the first plot (chart 5)
            fig.add_annotation(
                x=chart5_x1[0], 
                y=chart5_y1[0],
                text=f'<b>{chart51_time[0].strftime("%Y-%m-%d %H:%M")}, <br>{chart5_x1[0]:.0f} %, <br>{chart5_y1[0]:.0f} kW</b>',
                # showarrow=True,
                # arrowhead=1,
                # arrowsize=1,
                # arrowwidth=2,
                # arrowcolor="#636363",
                font=dict(
                    size=12, 
                    color="black", 
                    family="ISOCPEUR"
                ),
                align="left",
                yref='y1',
                bgcolor="white",
                ax=240,
                ay=chart5_y1_ay
            )

            # chart5_x2=[chart5_data2["Tunnid"].iloc[point_index[1]]]
            # chart5_y2=[chart5_data2['Pump flow according to H; m3/h'].iloc[point_index[1]]]
            chart5_x2 = [chart5_data2.loc[point_index[1], "Tunnid"]]
            chart5_y2 = [chart5_data2.loc[point_index[1], 'Pump flow according to H; m3/h']]
            chart52_time = [chart5_data2.loc[point_index[1], 'Time']]

            chart5_y2_ay = chart5_y2[0] - chart5_data2['Pump flow according to H; m3/h'].max() - 30

            # plotting a specific point for the second plot (chart 5)
            fig.add_scatter(
                x=chart5_x2, 
                y=chart5_y2, 
                mode='markers', 
                marker=dict(              # setting highlighted point related parameters: marker representation
                    color='black',
                    size=15,
                    symbol='circle-open',
                    line=dict(
                        color='black',
                        width=3
                    )
                ),
                showlegend=False,
                yaxis='y2'
            )

            # setting annotation for the second plot (chart 5)
            fig.add_annotation(
                x=chart5_x2[0], 
                y=chart5_y2[0],
                text=f'<b>{chart52_time[0].strftime("%Y-%m-%d %H:%M")}, <br>{chart5_x2[0]:.0f} %, <br>{chart5_y2[0]:.0f} m3/h</b>',
                # showarrow=True,
                # arrowhead=1,
                # arrowsize=1,
                # arrowwidth=2,
                # arrowcolor="#636363",
                font=dict(
                    size=12, 
                    color="black", 
                    family="ISOCPEUR"
                ),
                align="left",
                yref='y2',
                bgcolor="white",
                ax=60,
                ay=chart5_y2_ay
            )

            # fig.update_traces(
            #     # overwrite=True,
            #     # marker={"opacity": 0.1},
            #     opacity=0.07
            # )     
        else:
            pass

    return fig

def create_table(df, screen_size=screen_size):
    '''Creates plotly table
       
       Params:
       df: dataframe, contains the table data 

       Returns:
       fig: plotly table
    '''

    # creating the table
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(df.columns),
                    fill_color='#92D050',
                    align='left',
                    font=dict(
                        size=12,
                        family='Source Sans Pro',
                        color='white'
                    ),
                    height=20,
                    line_color='#D9D9D9'
                ),
                cells=dict(
                    values=[df[col] for col in df.columns],
                    fill_color='#F9F9F9',
                    align='left',
                    font_size=12,
                    height=20,
                    font_family='Source Sans Pro',
                    line_color='#D9D9D9'
                ),
                columnwidth = [8, 3, 5.5, 5.5, 6]
            )
        ]
    )

    # if screen_size[1] > 1366:
    #     w_percent = 0.75 * 0.48
    # else:
    #     w_percent = 0.48

    # setting the layout for the table
    fig.update_layout(
        # modebar_orientation='v',   # position of toolbox (select box, autoscale, ...)
        margin=go.layout.Margin(   # setting margin
            l=0, #left margin
            r=0, #right margin
            b=0, #bottom margin
            t=40, #top margin
        ),
        font=dict(
            family="ISOCPEUR",
            size=12
        ),
        plot_bgcolor='#F9F9F9',
        titlefont=dict(
            family="ISOCPEUR",
            size=12
        ),
        width=500,#w_percent*screen_size[1],#0.4612005856515373*screen_size[1],  # setting width of the table
        height=300, #0.5208333333333334*screen_size[0],  # setting height of the table
        autosize=False,
        # title = '''<b><span style="color:#0000be; font-size:30px">Enerwise</span></b>
        # <br> <span style="color:gray; font-size:12px">    Analytical Engineering</span>
        # ''',
        #title_x=0
    )

    return fig

def create_chart3_4(df, point_highlight=False, filter_points=False, point_index=None, points_range=None, screen_size=screen_size):
    '''Creates chart 3

       Params:
       df: dataframe, contains the data for the chart
       point_highlight: boolean, True if a point should be highlighted
       filter_points: boolean, True if a range of points is selected
       point_index: int, index of a point to highlight in the data
       points_range: list, contains indexes of coordinates to include in the chart

       Returns
       fig: plotly figure object
    '''

    if filter_points:
        df = df[df.index.isin(points_range)]
    else:
        pass

    # creating the plot (chart 3)
    fig1 = go.Figure(
        data=go.Scattergl(
            x=df["Pump flow according to H; m3/h"], 
            y=df["Head; mH2O"], 
            mode='markers', 
            marker_color='blue',
        )
    )

    # fig1.update_layout(
    #     # modebar_orientation='v',  # position of toolbox (select box, autoscale, ...)
    #     margin=go.layout.Margin(  # setting margin
    #         l=0, #left margin
    #         r=0, #right margin
    #         b=0, #bottom margin
    #         t=40, #top margin
    #     ),
    #     title='''<b>H-Q CURVES</b>''',
    #     titlefont=dict(
    #         family="ISOCPEUR",
    #         size=24
    #     ),
    #     title_x=0.5,
    # )

    # creating the plot (chart 4)
    fig2 = go.Figure(
        data=go.Scattergl(
            x=df["Pump flow according to H; m3/h"], 
            y=df["Mechanical power - measured; kW"], 
            mode='markers', 
            marker_color='blue'
        )
    )

    # fig2.update_layout(
    #     # modebar_orientation='v',  # position of toolbox (select box, autoscale, ...)
    #     margin=go.layout.Margin(  # setting margin
    #         l=0, #left margin
    #         r=0, #right margin
    #         b=0, #bottom margin
    #         t=40, #top margin
    #     ),
    #     title='''<b>P-Q CURVES</b>''',
    #     titlefont=dict(
    #         family="ISOCPEUR",
    #         size=24
    #     ),
    #     title_x=0.5,
    # )

    figures = [fig1, fig2]

    fig = make_subplots(
        rows=len(figures), 
        cols=1, 
        vertical_spacing=0.03, 
        # subplot_titles=(
        #     '<b>H-Q CURVES</b>', 
        #     '<b>P-Q CURVES</b>'
        # )
    )

    for i, figure in enumerate(figures):
        for trace in range(len(figure["data"])):
            fig.append_trace(figure["data"][trace], row=i+1, col=1)
    
    # setting title and its font size for y axis in chart 3
    fig['layout']['yaxis']['title']="Head, mH2O"
    fig['layout']['yaxis']['title']['font']['size'] = 12
    # fig['layout']['xaxis']['title']="Flow, m3/h"
    # fig['layout']['xaxis']['title']['font']['size'] = 12
    fig['layout']['xaxis']['showticklabels']=False
    fig['layout']['title'] = dict(
        text='''<b>PUMP WORKING CURVES</b>''',
        font=dict(
            family="ISOCPEUR",
            size=24
        )
    )

    # setting title and font size for x and y axis in chart 4
    fig['layout']['xaxis2']['title']="Flow, m3/h"
    fig['layout']['yaxis2']['title']="Power mechanical, kW"
    fig['layout']['yaxis2']['title']['font']['size'] = 12
    fig['layout']['xaxis2']['title']['font']['size'] = 12
    # fig['layout']['title2'] = dict(
    #     text='''<b>P-Q CURVES</b>''',
    #     font=dict(
    #         family="ISOCPEUR",
    #         size=24
    #     )
    # )

    fig['layout']['clickmode']='event+select'

    # setting logo path
    cwd_path = os.getcwd()
    logo_file_name = 'enerwise_logo_varviline.png'
    logo_path = os.path.join(cwd_path, logo_file_name)
    encoded_image = base64.b64encode(open(logo_path, 'rb').read())

    # if screen_size[1] > 1366:
    #     w_percent = 0.75 * 0.48
    # else:
    #     w_percent = 0.48

    # add logo to the chart 1
    fig.add_layout_image(
        dict(
            source='data:image/png;base64,{}'.format(encoded_image.decode()),
            xref="paper", yref="paper",
            x=0, y=1.09,#0.001380208*screen_size[0],#1.06,
            sizex=0.22,#0.0001098097*screen_size[1],#0.15, #0.00016105417*screen_size[1],#0.22 
            sizey=0.1,#0.0000911458*screen_size[0],#0.07, #0.00013020833*screen_size[0],#0.1
            xanchor="left", yanchor="top"
        )
    )

    fig.update_layout(
        # modebar_orientation='v',  # position of toolbox (select box, autoscale, ...)
        margin=go.layout.Margin(  # setting margin
            l=0, #left margin
            r=0, #right margin
            b=0, #bottom margin
            t=40, #top margin
        ),
        font=dict(
            family="ISOCPEUR",
            size=12
        ),
        plot_bgcolor='#F9F9F9',
        # title='''<b>H-Q CURVES</b>''',
        # titlefont=dict(
        #     family="ISOCPEUR",
        #     size=24
        # )
        width=500,#w_percent*screen_size[1],#0.4868228404099561*screen_size[1], # setting width of the chart 3_4
        # height=0.78125*screen_size[0], # setting height of the chart 3_4
        # width=0.492*screen_size[1],
        height=450, #0.78125*screen_size[0], 
        autosize=False,
        title_x=0.5,
        showlegend=False
        # xaxis=dict(                 
        #     showspikes=True,
        #     spikemode='across+toaxis',
        #     spikesnap='cursor',
        #     showline=True,
        #     showgrid=True,
        #     #spikedash = 'solid'
        # ),
        # yaxis=dict(
        #     showspikes=True,
        #     spikemode='across+toaxis',
        #     spikesnap='cursor',
        #     showline=True,
        #     showgrid=True,
        #     #spikedash = 'solid'
        # )
    )

    # fig.update_layout(
    #     title='''<b>H-Q CURVES</b>''',
    #     titlefont=dict(
    #         family="ISOCPEUR",
    #         size=24
    #     ),
    #     title_x=0.5,
    #     row=1,
    #     col=1
    # )

    fig.update_xaxes(gridcolor='#D9D9D9')
    fig.update_yaxes(gridcolor='#D9D9D9')

    fig.update_annotations(font=dict(family="ISOCPEUR", size=24))
    # if filter_points:
    #     df = df[df.index.isin(points_range)]

    #     fig = go.Figure(data=go.Scattergl(x=df["Pump flow according to H; m3/h"], 
    #                                     y=df["Head; mH2O"], 
    #                                     mode='markers', 
    #                                     marker_color='blue'
    #                                     )
    #     )
    #     #fig['layout']['xaxis']['title']="Flow, m3/h"
    #     fig['layout']['yaxis']['title']="Head, mH2O"
    #     fig['layout']['yaxis']['title']['font']['size'] = 10
    #     fig['layout']['xaxis']['showticklabels']=False
    #     fig['layout']['clickmode']='event+select'

    #     fig.update_layout(
    #         modebar_orientation='v',
    #         margin=go.layout.Margin(
    #         l=0, #left margin
    #         r=25, #right margin
    #         b=0, #bottom margin
    #         t=7, #top margin
    #     ),
    #         width=300, height=115)

    #     if point_highlight:
    #         chart3_x = [df.loc[point_index, "Pump flow according to H; m3/h"]]
    #         chart3_y = [df.loc[point_index, "Head; mH2O"]]

    #         fig.add_scatter(
    #             x=chart3_x, 
    #             y=chart3_y, 
    #             mode='markers', 
    #             # marker_color="green",
    #             # marker_symbol='circle-open',
    #             # marker_size=10,
    #             marker=dict(
    #                 color='green',
    #                 size=15,
    #                 symbol='circle-open',
    #                 line=dict(
    #                     color='green',
    #                     width=3
    #                 )
    #             ),
    #             showlegend=False
    #         )

    #         fig.add_annotation(
    #             x=chart3_x[0], 
    #             y=chart3_y[0],
    #             text=f'({chart3_x[0]:.2f}, {chart3_y[0]:.2f})',
    #             #yanchor='bottom',
    #             showarrow=True,
    #             arrowhead=1,
    #             arrowsize=1,
    #             arrowwidth=2,
    #             arrowcolor="#636363",
    #             # ax=-20,
    #             # ay=-30,
    #             font=dict(size=15, color="black", family="Courier New, monospace"),
    #             align="left"
    #         )
    #         fig.update_layout(showlegend=False)
    #     else:
    #         pass
    #     return fig
    # else:
    if point_highlight:
        chart3_x = [df.loc[point_index, "Pump flow according to H; m3/h"]]
        chart3_y = [df.loc[point_index, "Head; mH2O"]]
        chart3_time = [df.loc[point_index, "Time"]]
        # chart3_x=[df["Pump flow according to H; m3/h"].iloc[point_index]]
        # chart3_y=[df["Head; mH2O"].iloc[point_index]]

        # plotting specific point for the first plot (chart 3)
        fig.add_scatter(
            x=chart3_x, 
            y=chart3_y, 
            mode='markers', 
            marker=dict(            # setting highlighted point related parameters: marker representation
                color='black',
                size=15,
                symbol='circle-open',
                line=dict(
                    color='black',
                    width=3
                )
            ),
            showlegend=False,
            row=1, 
            col=1
        )

        # chart3_x_median = df["Pump flow according to H; m3/h"].median()
        # chart3_y_median = df["Head; mH2O"].median()
        # chart3_ap_x = chart3_x[0] - chart3_x_median
        # chart3_ap_y = chart3_y[0] - chart3_y_median

        # setting annotation (chart 3)
        fig.add_annotation(
            x=chart3_x[0], 
            y=chart3_y[0],
            text=f'<b>{chart3_time[0].strftime("%Y-%m-%d %H:%M")}, <br>{chart3_x[0]:.0f} m3/h, <br>{chart3_y[0]:.0f} mH2O</b>',
            # showarrow=True,
            # arrowhead=1,
            # arrowsize=1,
            # arrowwidth=2,
            # arrowcolor="#636363",
            ax=-40,
            ay=-60,
            font=dict(
                size=12, 
                color="black", 
                family="ISOCPEUR"
            ),
            align="left",
            bgcolor="white",
            row=1, 
            col=1
        )

        chart4_x = [df.loc[point_index, "Pump flow according to H; m3/h"]]
        chart4_y = [df.loc[point_index, "Mechanical power - measured; kW"]]
        chart4_time = [df.loc[point_index, "Time"]]
        # chart4_x=[df["Pump flow according to H; m3/h"].iloc[point_index]]
        # chart4_y=[df["Mechanical power - measured; kW"].iloc[point_index]]

        # plotting a specific point for the first plot (chart 4)
        fig.add_scatter(
            x=chart4_x, 
            y=chart4_y, 
            mode='markers', 
            marker=dict(             # setting highlighted point related parameters: marker representation
                color='black',
                size=15,
                symbol='circle-open',
                line=dict(
                    color='black',
                    width=3
                )
            ),
            showlegend=False,
            row=2, 
            col=1
        )

        # chart4_x_median = df["Pump flow according to H; m3/h"].median()
        # chart4_y_median = df["Mechanical power - measured; kW"].median()
        # chart4_x_ap = chart4_x[0] - chart4_x_median
        # chart4_y_ap = chart4_y[0] - chart4_y_median

        # setting annotation (chart 4)
        fig.add_annotation(
            x=chart4_x[0], 
            y=chart4_y[0],
            text=f'<b>{chart4_time[0].strftime("%Y-%m-%d %H:%M")}, <br>{chart4_x[0]:.0f} m3/h, <br>{chart4_y[0]:.0f} kW</b>',
            # showarrow=True,
            # arrowhead=1,
            # arrowsize=1,
            # arrowwidth=2,
            # arrowcolor="#636363",
            ax=-40,
            ay=-60,
            font=dict(
                size=12, 
                color="black", 
                family="ISOCPEUR"
            ),
            align="left",
            bgcolor="white",
            row=2, 
            col=1
        )

        fig.update_layout(showlegend=False)

        # fig.update_traces(
        #     # overwrite=True,
        #     # marker={"opacity": 0.1},
        #     opacity=0.07
        # )
    else:
        pass

    return fig
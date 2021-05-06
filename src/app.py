# authors: Yuanzhe Marco Ma, Sicheng Sun, Guanshu Tao, Yuan Xiong
# date: 2021-01-23
import dash
from dash import no_update
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output
from data_manager import DataManager
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go

# retrieve data
data = DataManager().get_data()

# land-on page graphics
table = DataManager().make_table(data)
chart_natn, chart_club, scatter = DataManager().plot_altair(data)
ranking_histo = DataManager().plot_histo(data)

# app layout
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, title='FIFA19 DASHBOARD', external_stylesheets=external_stylesheets)
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = 'FIFA19 Star Board'
app.layout = dbc.Container([
    html.H1('FIFA19 STAR BOARD', style={'backgroundColor': '#697d8d',
                                        'padding': 25,
                                        'margin-top': 20,
                                        'margin-bottom': 10,
                                        'font-size': '44px',
                                        'color': 'white',
                                        'textAlign': 'center'}),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H4(['Select Attributes:']),
            dcc.Dropdown(
                id='attribute-widget',
                value=['Name', 'Nationality', 'Age', 'Value(€)', 'Overall'],
                options=[{'label': col, 'value': col} for col in data.columns],
                multi=True,
                style={'font-size': '16px'}
            ),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Div(['Rank By:'], style={'font-size': '14px'}),
                    dcc.Dropdown(
                        id='rankby-widget',
                        value='Overall',
                        options=[{'label': col, 'value': col} for col in data.columns],
                        style={
                           'background-color': '#e6e6e6',
                           'font-size': '14px'
                        }
                    ),
                ]),
                dbc.Col([
                    html.Div(['Order:'], style={'font-size': '14px'}),
                    dcc.Dropdown(
                        id='order-widget',
                        value='True',
                        options=[{'label': 'Descending', 'value': 'True'},
                                 {'label': 'Ascending', 'value': 'False'}],
                        style={
                            'background-color': '#e6e6e6',
                            'font-size': '14px'
                        }
                    ),
                ]),
                dbc.Col([
                    html.Div(['Continent:'], style={'font-size': '14px'}),
                    dcc.Dropdown(
                        id='filter-cont-widget',
                        value='',
                        options=[{'label': val, 'value': val} for val in data['Continent'].unique()],
                        style={
                            'background-color': '#e6e6e6',
                            'font-size': '14px'
                        }
                    ),
                ]),
                dbc.Col([
                    html.Div(['Club:'], style={'font-size': '14px'}),
                    dcc.Dropdown(
                        id='filter-club-widget',
                        value='',
                        options=[{'label': val, 'value': val} for val in data['Club'].dropna().unique()],
                        style={
                            'background-color': '#e6e6e6',
                            'font-size': '14px'
                        }
                    ),
                ])
            ]),
            html.Br(),
            dbc.Tabs([
                dbc.Tab([
                    html.Br(),
                    dbc.Row([
                        dcc.Slider(id='slider_update', vertical=True, verticalHeight=400, 
                                   tooltip=dict(always_visible=True, placement='left'), min=1, max=table.shape[0],
                                   step=1, value=1),
                        html.Br(),
                        html.Div([dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in table.columns],
                            data=table.to_dict('records'),
                            style_cell={'width': 120,
                                        'minWidth': '25%',
                                        'whiteSpace': 'normal',
                                        'overflow': 'hidden',
                                        'font-size': '12px',
                                        'textAlign': 'right'},
                            style_header={'backgroundColor': 'lightslategrey',
                                          'color' : 'white',
                                          'fontWeight': 'bold',
                                          'textAlign': 'right',
                                          'font-size': '13px'
                                         },
                            style_data_conditional=[{
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'navajowhite'}]
                        )])
                    ]),
                    html.Div([
                        '**Overall and potential rating are calculated by FIFA19 development team.',
                        html.Br(),
                        'For more information on how they care calculated, please visit ',
                        html.A('https://www.fifauteam.com/player-ratings-guide-fifa-19/',
                                href='https://www.fifauteam.com/player-ratings-guide-fifa-19/',
                                target="_blank")
                    ], style={'margin-left': '50px'}
                    )
                ], label='Table', style={'width': '100vh', 'height': '65vh'}),
                dbc.Tab(
                    dcc.Graph(id="map-graph"),
                    label='Map',
                    style={'width': '100vh', 'height': '65vh'}
                )
            ], style={'fontSize': 15}),
            html.Iframe(
                id='rank-histogram',
                style={'border-width': '0', 'width': '200%', 'height': '200px',
                       'margin-left': '80px', 'margin-top': '10px'},
                srcDoc=ranking_histo.to_html()
            )
        ], md=9),
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(
                    html.Iframe(
                        id='natn-chart',
                        srcDoc=chart_natn.to_html(),
                        style={'border-width': '0', 'width': '150%', 'height': '320px'}
                    ),
                    label='By Nationality'
                ),
                dbc.Tab(
                    html.Iframe(
                        id='club-chart',
                        srcDoc=chart_club.to_html(),
                        style={'border-width': '0', 'width': '150%', 'height': '320px'}
                    ),
                    label='By Club'
                )
            ], style={'fontSize': 15, 'margin-top': '145px'}),
            html.Iframe(
                id='scatter',
                srcDoc=scatter.to_html(),
                style={'border-width': '0', 'width': '160%', 'height': '300px'}
            ),
            html.Div(
                ['About Us:',
                    html.Br(),
                    'Yuanzhe Marco Ma, Sicheng Sun, Guanshu Tao, Yuan Xiong. We are students of the UBC MDS Program.', 
                    html.Br(),
                    html.Br(),
                    'Data source: ',
                    html.A('Kaggle', href='https://www.kaggle.com/karangadiya/fifa19', target="_blank"),
                    html.Br(),
                    'Source code: ',
                    html.A('visit our GitHub', href='https://github.com/UBC-MDS/DSCI532_Group17', target="_blank")
                ]
            )
        ])
    ])
])


# updates table from all 5 dropdowns
# Inputs:
#     by : string, the column to rank by
#     order : string, descending or ascending
#     cols : list of string, the columns selected to present
#     filter_cont : string, the continent to filter on
#     filter_club : string, the club to filter on
#     slider_update : number, the location of the slider
# Returns:
#     data : dict
#     columns : list of string
#     slider_max : number
@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Output('slider_update', 'max'),
    Input('rankby-widget', 'value'),
    Input('order-widget', 'value'),
    Input('attribute-widget', 'value'),
    Input('filter-cont-widget', 'value'),
    Input('filter-club-widget', 'value'), 
    Input('slider_update', 'value'))
def update_table(by, order, cols, filter_cont, filter_club, slider_update):
    table, table_len = DataManager().update_table(data, by, order == 'True',
                                                  cols, filter_cont, filter_club, slider_update)
    columns = [{"name": i, "id": i} for i in table.columns]

    return table.to_dict('records'), columns, table_len


# Updates charts with Rank-by selection
# Updates only when selected col is numeric
# Inputs:
#     by : string, the rank-by column selected
# Returns:
#     srcDoc : bar-plot by nationality
#     srcDoc : bar-plot by clubs
#     srcDoc : scatter-plot
#     slider_max : number
@app.callback(
    Output('natn-chart', 'srcDoc'),
    Output('club-chart', 'srcDoc'),
    Output('scatter', 'srcDoc'),
    Output('rank-histogram', 'srcDoc'),
    Input('rankby-widget', 'value'))
def update_charts(by):
    global chart_natn, chart_club, scatter
    global ranking_histo
    if not (np.issubdtype(data[by], int) or
            np.issubdtype(data[by], float)):
        return no_update
    else:
        chart_natn, chart_club, scatter = DataManager().plot_altair(data, by=by)
        ranking_histo = DataManager().plot_histo(data, by=by)
        
        return (chart_natn.to_html(), chart_club.to_html(), scatter.to_html(),
                ranking_histo.to_html())


# Updates map according to rank-by column
# Inputs: 
#     by : string, the rank-by column selected
# Returns:
#     figure : the output map
@app.callback(
    Output("map-graph", "figure"),
    Input("rankby-widget", "value")
)
def update_figure(selected):
    # make sure it's numerical column, otherwise no change
    if type(data[selected][0]) == str:
        return no_update

    dff = DataManager.prepare_map(data)
    dff['hover_text'] = dff["Nationality"] + ": " + dff[selected].apply(str)
    trace = go.Choropleth(locations=dff['CODE'], z=dff[selected],
                          text=dff['hover_text'],
                          hoverinfo="text",
                          marker_line_color='white',
                          autocolorscale=False,
                          showscale=True,
                          showlegend=True,
                          reversescale=True,
                          colorscale="RdBu", marker={'line': {'color': 'rgb(180,180,180)', 'width': 0.5}},
                          colorbar={"thickness": 10, "len": 0.3, "x": 0.9, "y": 0.7,
                                    'title': {"text": 'mean of attribute', "side": "top"}})

    return {"data": [trace],
            "layout": go.Layout(height=500, width=800, margin=dict(l=0, r=0, t=0, b=0),
                                geo={'showframe': False, 'showcoastlines': False,
                                     'projection': {'type': "natural earth"}})}


# Additional callback to manually control table overflow
# When there are too many columns, column size are shrunk to fit in display area
# Inputs: 
#     selected_cols : list of string, the attributes selected
#     rankby_col : string, the rank-by column selected
# Returns:
#     style_cell : style configuration of the dash table
@app.callback(
    Output('table', 'style_cell'),
    Input('attribute-widget', 'value'),
    Input('rankby-widget', 'value')
)
def table_maintenance(selected_cols, rankby_col):
    total_cols = len(selected_cols) if rankby_col in selected_cols else len(selected_cols) + 1
    if (total_cols > 5):
        return {'width': 650 // total_cols, 'minWidth': '25%',
                'whiteSpace': 'normal', 'overflow': 'hidden'}
    else:
        return no_update


if __name__ == '__main__':
    app.run_server()

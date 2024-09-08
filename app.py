# Importing necessary dependencies, like libraries under dash etc.
import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from dash.dash_table.Format import Format, Scheme
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the MAPBOX_TOKEN from environment variables
token = os.getenv("MAPBOX_TOKEN")
px.set_mapbox_access_token(token)


# a blank figure function to take place when the callbacks are still loading
def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None,
                      plot_bgcolor="rgba( 0, 0, 0, 0)",
                      paper_bgcolor="rgba( 0, 0, 0, 0)", )
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig


# configuration for plotly graphs
config = { 'displaylogo':False,
           'modeBarButtonsToAdd':['drawrect',
                                  'eraseshape'
                                  ]
           }

# Reading the processed data sets through pandas
main_data = pd.read_csv('data_main.csv')
data_mcs = pd.read_csv('mini_container.csv')
summary = pd.read_csv('summary.csv')
summary = summary.rename(columns={ 'Unnamed: 0':'' })
avg_speed = pd.read_csv('avg_speed.csv')
time_speed = pd.read_csv('time_speed.csv')

# Initialising the app instance
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# The app layout
# Contains Dash Html components & core components dcc
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('sit.png'), id='sit-logo-img')
        ], id='sit-logo'),
        html.Div([
            html.P('Data Analysis using Plotly Dash', id='title-p1'),
            html.P('June Route Bus Data', id='title-p2')
        ], id='title')
    ], id='header'),
    html.Div([
        html.Div([
            html.Div([
                html.P('Range of Days (Month of June)', className='card-txt'),
                dcc.Slider(min=1, max=30, step=1, value=1, id='slider')
            ], id='slider-container', className='container'),
            html.Div([
                html.Div([
                    html.P([], id='day', className='card-big-txt'),
                    html.P('Day', className='card-small-txt')
                ], className='card'),
                html.Div([
                    html.P([], id='n-events', className='card-big-txt'),
                    html.P('No. of Events', className='card-small-txt')
                ], className='card'),
                html.Div([
                    html.P([], id='h-speed', className='card-big-txt'),
                    html.P('Highest speed of the day', className='card-small-txt')
                ], className='card'),
                html.Div([
                    html.P([], id='l-speed', className='card-big-txt'),
                    html.P('Lowest speed of the day', className='card-small-txt')
                ], className='card'),
            ], id='cards')
        ], id='slider-and-cards'),
        html.Div([
            html.Div([
                html.P('Data Summary', id='summary-text')
            ], id='summary-text-container'),
            html.Div([
                dash_table.DataTable(
                    data=summary.to_dict('records'),
                    columns=[{ "name":i, "id":i, 'type':'numeric', 'format':Format(precision=2, scheme=Scheme.fixed) }
                             for i in summary.columns],
                    style_data_conditional=[
                        {
                            'if':{
                                'column_id':'',
                            },
                            'backgroundColor':'white',
                            'color':'black',
                        }, ],
                    style_data={ 'font-size':'23px', 'color':'red' },
                    style_cell={ 'border':'0px solid white', 'padding':'10px', 'border-left':'2px solid black',
                                 'border-right':'2px solid black'
                                 },
                    style_table={ 'border-bottom':'2px solid black', 'border-top':'2px solid black' },
                    style_header={
                        'backgroundColor':'white', 'color':'black', 'fontWeight':'bold',
                        'border-bottom':'2px solid black', 'font-size':'20px'
                    }
                )
            ], id='summary-content')
        ], id='summary', className='container'),
        html.Div([dcc.Graph(id='bar-fig', figure=blank_fig(), config=config)], id='bar', className='container'),
        html.Div([dcc.Graph(id='map-fig', figure=blank_fig(), config=config)], id='map', className='container'),
        html.Div([dcc.Graph(id='line-fig', figure=blank_fig(), config=config)], id='line', className='container'),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='driver-dropdown',
                    options=[i for i in main_data['Driver'].unique()],
                    placeholder='Select a driver',
                    clearable=False,
                    value=str(main_data['Driver'][1]))
            ], id='dropdown-container'),
            html.Div([
                dcc.Graph(id='donut-fig', figure=blank_fig(), config=config),
            ], id='donut-container'),
        ], id='donuts', className='container'),
        html.Div([
            html.Div([
                dcc.Graph(id='dot-fig', figure=blank_fig(), config=config),
            ], id='dot-fig-container'),
            html.Div([
                dcc.Checklist(
                    [
                        {
                            "label":html.Div(
                                [
                                    html.Span(className='circle', id='peak-circle'),
                                    html.Div("Peak hour", style={ 'font-size':15, 'padding-left':10 }),
                                ], style={ 'display':'flex', 'margin-left':'10px' }
                            ),
                            "value":"peak-hour",
                        },
                        {
                            "label":html.Div(
                                [
                                    html.Span(className='circle', id='non-peak-circle'),
                                    html.Div("Non peak hour", style={ 'font-size':15, 'padding-left':10 }),
                                ], style={ 'display':'flex', 'margin-left':'10px' }
                            ),
                            "value":"non-peak-hour",
                        }],
                    value=['peak-hour', 'non-peak-hour'],
                    id='hour-checklist'
                )

            ], id='checklist-container')
        ], id='dot', className='container')
    ], id='main')
], id='layout')


# the callback for connecting the cards to the slider
@app.callback(
    [Output('day', 'children'),
     Output('n-events', 'children'),
     Output('h-speed', 'children'),
     Output('l-speed', 'children'), ],
    Input('slider', 'value')
)

def update_day(day):
    try:
        df = data_mcs
        df['day'] = df['day'].astype(int)
        n_events = df[df['day'] == day]['event count']
        h_speed = list(df[df['day'] == day]['highest speed'])[0]
        l_speed = list(df[df['day'] == day]['lowest speed'])[0]
    except:
        pass


    return [day, n_events, str(h_speed) + ' km/h', str(l_speed) + ' km/h']


# callback for connecting the slider to the bar graph
@app.callback(
    Output('bar-fig', 'figure'),
    Input('slider', 'value')
)
def update_bar(day):
    while True:
        df2 = data_mcs
        df2['day'] = df2['day'].astype(str)
        color_discrete_map = { }
        for i in range(30):
            color_discrete_map[str(i + 1)] = 'grey'
        color_discrete_map[str(day)] = 'blue'

        fig = px.bar(df2, x='day', y='event count', color='day',
                     color_discrete_map=color_discrete_map, title='No. of events per day.')

        if fig['data'][0]['x'][0] == '1':
            fig.update_layout(margin=dict(t=45, b=10, l=10, r=10), showlegend=False, title_x=0.5)
            return fig


# the callback for the mapbox
@app.callback(
    Output('map-fig', 'figure'),
    Input('slider', 'value')
)
def update_map(day):
    df = main_data
    df = df[df['day'] == day]  # To link slider to the mapbox
    fig = px.scatter_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        color="Vehicle",
        zoom=11,
        title='Mapbox of Locations Travelled Per Vehicle',
        custom_data=['Hour', 'Vehicle', 'Driver', 'Longitude', 'Latitude']
    )

    fig.update_layout(margin=dict(t=45, b=10, l=10, r=10), title_x=0.5)
    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{customdata[0]}</b>",
            "------------",
            "Vehicle:  <b>%{customdata[1]}</b>",
            "Driver:  <b>%{customdata[2]}</b>",
            "Latitude:  <b>%{customdata[3]}</b>",
            "Longitude:  <b>%{customdata[4]}</b>",
        ]),
    )
    return fig


# callback to connect the line graph to the mapbox
@app.callback(
    Output('line-fig', 'figure'),
    Input('map-fig', 'hoverData')
)
def update_line(driver_data):
    if driver_data:
        driver = driver_data['points'][0]['customdata'][2]
        vehicle = driver_data['points'][0]['customdata'][1]
    else:
        driver = 'Ridwan'
        vehicle = 'SBS6289D'

    df = avg_speed
    df_driver = main_data
    df_driver = df_driver[(df_driver['Driver'] == driver) & (df_driver['Vehicle'] == vehicle)]
    df_driver = df_driver.groupby('day', as_index=False).mean()[['day', 'Speed']]

    avg_all = dict(
        x=df['day'],
        y=df['Speed'],
        mode='lines',
        type='scatter',
        name='Avg. all',
        line=dict(shape='spline', color='rgb(255, 0, 0)', width=2),
        connectgaps=True
    )

    avg_driver = dict(
        x=df_driver['day'],
        y=df_driver['Speed'],
        mode='lines',
        type='scatter',
        name=driver,
        line=dict(shape='spline', color='rgb(0, 0, 0)', width=2),
        connectgaps=True
    )

    layout = dict(
        xaxis=dict(title='Day'),
        yaxis=dict(title='Avg speed', range=[0, 50]),
        margin=dict(
            l=10,
            r=10,
            b=10,
            t=40
        ),
        title=f'Driver: {driver}, Vehicle: {vehicle}',
        title_x=0.5,
        showlegend=False,
        hovermode="x"
    )

    data = [avg_all, avg_driver]
    fig = go.Figure(data=data, layout=layout)
    return fig


# the callback for the donut graphs
@app.callback(
    Output('donut-fig', 'figure'),
    Input('driver-dropdown', 'value'),
)
def update_donut1(driver):
    df = main_data

    df1 = df.groupby('Event', as_index=False).count()[['Event', 'Driver']].rename(columns={ 'Driver':'Event count' })

    df2 = df[df['Driver'] == driver]
    df2 = df2.groupby('Event', as_index=False).count()[['Event', 'Driver']].rename(columns={ 'Driver':'Event count' })

    fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5], specs=[[{ "type":"pie" }, { "type":"pie" }]])
    fig.add_trace(go.Pie(labels=df1['Event'], values=df1['Event count'], hole=0.5, name='All drivers'), row=1, col=1)
    fig.add_trace(go.Pie(labels=df2['Event'], values=df2['Event count'], hole=0.5, name=driver), row=1, col=2)
    fig.update_layout(
        legend=dict(orientation='h'),
        title='Total Count of Types of Events in month of June',
        title_x=0.5,
        margin=dict(b=0, t=40, l=10, r=10)
    )
    return fig


# the callback for the dot plot
@app.callback(
    Output('dot-fig', 'figure'),
    Input('hour-checklist', 'value')
)
def update_dot(hours):
    df = time_speed
    fig = px.scatter(df, x='Hour', y='Speed', color_discrete_sequence=['black'])
    fig.update_layout(
        title='Average Speed against Time',
        title_x=0.5,
        margin=dict(t=40, b=10, l=10, r=10),
        hovermode='x'
    )
    if 'peak-hour' in hours:
        fig.add_vrect(x0="6", x1="9", fillcolor="#f26d99", opacity=0.5, line_width=0)
        fig.add_vrect(x0="18", x1="20", fillcolor="#f26d99", opacity=0.5, line_width=0)
    if 'non-peak-hour' in hours:
        fig.add_vrect(x0="9", x1="18", fillcolor="#66e9ff", opacity=0.5, line_width=0)
        fig.add_vrect(x0="20", x1="24", fillcolor="#66e9ff", opacity=0.5, line_width=0)
        fig.add_vrect(x0="0", x1="6", fillcolor="#66e9ff", opacity=0.5, line_width=0)

    return fig


# if __name__ == '__main__':
#     app.run_server(debug=False)
if __name__ == '__main__':
    # For Development only, otherwise use gunicorn or uwsgi to launch, e.g.
    # gunicorn -b 0.0.0.0:8050 index:app.server
    app.run_server(
        port=8050,
        host='0.0.0.0'
    )
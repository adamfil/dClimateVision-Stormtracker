from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

theme = [dbc.themes.SLATE]

tab_style = {
    "background": "white",
    'color': 'black',
    'font-weight': 600,
    'align-items': 'center',
    'justify-content': 'center',
    'border-radius': '4px',
    'padding':'6px'
}

tab_selected_style = {
    "background": "white",
    'color': 'black',
    'font-weight': 600,
    'align-items': 'center',
    'justify-content': 'center',
    'border-radius': '4px',
    'padding':'6px'
}

app = Dash(__name__, external_stylesheets=theme, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div(

    style={
        #"background-image": "url('assets/greenbrier2.jpg')",
        "background-color": "#002451",
        "background-size": "100%",
        "color": "white",
        "min-height" : "100vh",
        "font-size": "16px",
        "padding": "12px"
    },
    
    children=[
    html.H1(children='Stormtracker', style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}),

    html.Div(children='''
        View historical and forecasted storm data
    ''', style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}
        ),
html.Div([
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
        dcc.Tab(label='Forecasted Data', value='tab-1-example-graph', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Historical Data', value='tab-2-example-graph', style=tab_style, selected_style=tab_selected_style),
    ]),
    html.Div(id='tabs-content-example-graph')
]),

html.Div([
    # plot figure
    html.A("github.com/adamfil/dclimatevision-stormtracker", href='https://github.com/adamfil/dclimatevision-stormtracker', target="_blank"),
    ], style={
        'display': 'flex', "justify-content": "center", "align-items": "center"
    }),

])

@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
                            
                    html.Div(children=
                        dcc.Dropdown(
                            id="id_of_dropdown",
                            options=[
                                {'label': 'North Atlantic', 'value': 'atcf-AL.csv'},
                                {'label': 'Central North Pacific', 'value': 'atcf-CP.csv'},
                                {'label': 'North-East Pacific', 'value': 'atcf-EP.csv'},
                                ],
                            value='atcf-CP.csv',
                            searchable=False,
                        ),
                        style={"display": "flex",
                        "justify-content": "center",
                        "align-items": "center",}
                        ),

                    dcc.Loading(
                        id='loading',
                        color="#c6ceff",
                        style={"padding": "200px"},
                        children=[
                        html.Div(children=
                            dcc.Graph(
                                id='example-graph',
                                figure={},
                            ),
                            style={"display": "flex",
                            "justify-content": "center",
                            "align-items": "center",}
                            ),
                        ])
                ])
    elif tab == 'tab-2-example-graph':
        return html.Div([
                            
                    html.Div(children=
                        dcc.Dropdown(
                            id="id_of_dropdown2",
                            options=[
                                {'label': 'North Indian Ocean', 'value': 'historical-NI.csv'},
                                {'label': 'South Indian Ocean', 'value': 'historical-SI.csv'},       
                                {'label': 'North Atlantic', 'value': 'historical-NA.csv'},                           
                                {'label': 'Eastern Pacific', 'value': 'historical-EP.csv'},
                                {'label': 'Western Pacific', 'value': 'historical-WP.csv'},
                                {'label': 'Southern Pacific', 'value': 'historical-SP.csv'},
                                ],
                            value='historical-NI.csv',
                            searchable=False,
                        ),
                        style={"display": "flex",
                        "justify-content": "center",
                        "align-items": "center",}
                        ),

                    dcc.Loading(
                        id='loading2',
                        color="#c6ceff",
                        style={"padding": "200px"},
                        children=[
                        html.Div(children=
                            dcc.Graph(
                                id='example-graph2',
                                figure={},
                            ),
                            style={"display": "flex",
                            "justify-content": "center",
                            "align-items": "center",}
                            ),
                        ])
                ])



@app.callback(
    [Output(component_id='example-graph', component_property='figure')],
    [Input(component_id='id_of_dropdown', component_property='value')]
)
def update_graph(dropdown):
    frame = pd.read_csv(dropdown)
    frame = frame.dropna(axis=0, subset=['STORMNAME'])
    frame = frame[frame['VMAX'].notna()]
    frame = frame.dropna(axis=1, how='any')
    frame = frame[frame.STORMNAME != 'NONAME']
    frame = frame[frame.STORMNAME != 'INVEST']
    frame = frame[frame.STORMNAME != 'TEST']
    frame = frame.sort_values('STORMNAME')
    frame['STORMNAME'] = frame['STORMNAME'] + ': ' + frame['HOUR'].astype(str).str[0:4]


    shown_data = list(frame)
    shown_data.remove('lat')
    shown_data.remove('lon')
    shown_data.remove('STORMNAME')

    fig = px.scatter_geo(frame, lat=frame.lat, lon=frame.lon, color=frame.STORMNAME, size=frame.VMAX, hover_data=(shown_data), width=1080, height=600).update_traces(visible="legendonly")
    fig.update_geos(
        resolution=110,
        showcoastlines=True, coastlinecolor="RebeccaPurple",
        showland=True, landcolor="LightGreen",
        showocean=True, oceancolor="LightBlue",
        showlakes=True, lakecolor="LightBlue",
        showrivers=True, rivercolor="LightBlue",
        fitbounds="locations",
        projection_type="equirectangular",
    )

    fig.update_layout(
        paper_bgcolor="#06356d",
        font_color="white",
        title_text="Forecasted Storms",
        title_x=0.5,
    )

    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))

    return [fig]

@app.callback(
    [Output(component_id='example-graph2', component_property='figure')],
    [Input(component_id='id_of_dropdown2', component_property='value')]
)
def update_graph(dropdown):
        # assume you have a "long-form" data frame
    # see https://plotly.com/python/px-arguments/ for more options
    frame = pd.read_csv(dropdown)
    frame = frame.dropna(axis=0, subset=['NAME'])
    #frame = frame.query("STORMNAME in " + str(storm_list))
    #print(frame)
    #drop all rows missing vmax 
    frame = frame[frame['STORM_SPEED'].notna()]
    frame = frame.dropna(axis=1, how='any')
    frame = frame[frame.NAME != 'NONAME']
    frame = frame[frame.NAME != 'NOT_NAMED']
    frame = frame[frame.NAME != 'INVEST']
    frame = frame[frame.NAME != 'TEST']
    frame = frame.sort_values('NAME')
    frame['NAME'] = frame['NAME'] + ': ' + frame['HOUR'].astype(str).str[0:4]


    shown_data = list(frame)
    shown_data.remove('lat')
    shown_data.remove('lon')
    shown_data.remove('NAME')

    fig = px.scatter_geo(frame, lat=frame.lat, lon=frame.lon, color=frame.NAME, size=frame.STORM_SPEED, hover_data=(shown_data), width=1080, height=600).update_traces(visible="legendonly")
    fig.update_geos(
        resolution=110,
        showcoastlines=True, coastlinecolor="RebeccaPurple",
        showland=True, landcolor="LightGreen",
        showocean=True, oceancolor="LightBlue",
        showlakes=True, lakecolor="LightBlue",
        showrivers=True, rivercolor="LightBlue",
        fitbounds="locations",
        projection_type="equirectangular",
    )

    fig.update_layout(
        paper_bgcolor="#06356d",
        font_color="white",
        title_text="Historical Storms",
        title_x=0.5,
    )

    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))

    return [fig]

if __name__ == '__main__':
    app.run_server(debug=False)
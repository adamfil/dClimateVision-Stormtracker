from logging import PlaceHolder
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
frame = pd.read_csv('atcf-CP.csv')
frame = frame.dropna(axis=0, subset=['STORMNAME'])
#frame = frame.query("STORMNAME in " + str(storm_list))
#print(frame)

frame = frame.dropna(axis=1, how='any')
shown_data = list(frame)
shown_data.remove('lat')
shown_data.remove('lon')
shown_data.remove('STORMNAME')

fig = px.scatter_geo(frame, lat=frame.lat, lon=frame.lon, color=frame.STORMNAME, hover_data=(shown_data), width=1080, height=600).update_traces(visible="legendonly")
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
)

fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))

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
    html.H1(children='dClimateVision - Stormpath', style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}),

    html.Div(children='''
        View storm data from the dClimate free API- made with Plotly, Dash, and Python.
    ''', style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}
        ),
    html.Div(children=
        dcc.Graph(
            id='example-graph',
            figure=fig,
        ),
        style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}
        ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
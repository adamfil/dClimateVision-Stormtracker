from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
frame = pd.read_csv('atcf-CP.csv')
frame = frame.dropna(axis=0, subset=['STORMNAME'])
frame = frame.query("STORMNAME in ['WALI', 'UPANA']")
#print(frame)

frame = frame.dropna(axis=1, how='any')
shown_data = list(frame)
shown_data.remove('lat')
shown_data.remove('lon')
shown_data.remove('STORMNAME')

fig = px.scatter_geo(frame, lat=frame.lat, lon=frame.lon, color=frame.STORMNAME, hover_data=(shown_data))
fig.update_geos(
    resolution=50,
    showcoastlines=True, coastlinecolor="RebeccaPurple",
    showland=True, landcolor="LightGreen",
    showocean=True, oceancolor="LightBlue",
    showlakes=True, lakecolor="LightBlue",
    showrivers=True, rivercolor="LightBlue",
    fitbounds="locations"
)


app.layout = html.Div(children=[
    html.H1(children='dClimateVision - Stormpath'),

    html.Div(children='''
        A web app for visualizing storm weather data from the dClimate free API- made with Plotly, Dash, and Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
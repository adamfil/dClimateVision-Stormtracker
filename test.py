import pandas as pd
import plotly.express as px
frame = pd.read_csv('atcf-CP.csv')
frame = frame.dropna(axis=0, subset=['STORMNAME'])
frame = frame.query("STORMNAME in ['WALI', 'UPANA']")
#print(frame)

frame = frame.dropna(axis=1, how='any')
print(frame)
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
fig.show()

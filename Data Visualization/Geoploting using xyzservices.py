import xyzservices.providers as xyz
from bokeh.models import WMTSTileSource
from bokeh.plotting import figure, show
from bokeh.tile_providers import get_provider
import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, OpenURL, TapTool

#tile provider
tile_provider = get_provider(xyz.CartoDB.Voyager)

p = figure(x_range=(-2000000, 6000000), y_range=(-1000000, 7000000),
           x_axis_type="mercator", y_axis_type="mercator"), #tools = "tap")
p.add_tile(tile_provider)

#convert dec lon/lat to Web Mercator format
def web_mercator(df, lon='lon', lat='lat'):
    k = 6378137
    df['x'] = df[lon] * (k * np.pi/180)
    df['y'] = np.log(np.tan((90 + df[lat]) * np.pi / 360)) * k
    return df

#latitude & longitude data from inat

data = dict(
    lat = [1],
    lon = [1],
    #name = [128351919]
)

df = pd.DataFrame(data)
map_df = web_mercator(df)
print(map_df.head())

url = 'https://www.inaturalist.org/observations/@name'
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)

p.circle(x = df['x'], y = df['y'], fill_color = "green", size = 5)

show(p)
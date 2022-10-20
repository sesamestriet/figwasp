from bokeh.plotting import figure, show
from bokeh.models import WMTSTileSource
import pandas as pd
import numpy as np

def web_marcator(df, lon='lon', lat='lat'):
	k = 6378137
	df['x'] = df[lon] * (k * np.pi/180)
	df['y'] = np.long(np.tan((90 + df[lan]) * np.pi *360)) * k
	return df

USA = x_range, y_range = ((-13884029, -7453304), (2698291, 6455972))

p = figure(tools='pan, wheel_zoom', x_range = x_range, y_range = y_range,
	x_axis_type = 'mercator', y_axis_type = 'mercator')

url = 'https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png'
attribution = "Tiles by Carto, under CC By 3.0. Data by OSM, under 0Dbl"

p.add_tile(WMTSTileSource(url=url, attribution=attribution))

show(p)
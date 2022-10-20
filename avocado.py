from ast import arg
from distutils.command.install_egg_info import to_filename
from turtle import title
from IPython.display import display
import xyzservices.providers as xyz
from bokeh.plotting import (
    figure, ColumnDataSource, show, output_file
    )
from bokeh.layouts import Row, Column, gridplot, layout
from bokeh.tile_providers import get_provider
from bokeh.models import(
    ColumnDataSource, OpenURL, TapTool,
    HoverTool, MultiChoice, Div, Row, BoxAnnotation, Toggle
    )
from bokeh.models.callbacks import CustomJS
from bokeh.models.selections import Selection
from bokeh.models.widgets import DataTable, TableColumn, Button
import pandas as pd
import numpy as np
import os

###Map Tile
#tile_provider = get_provider(xyz.CartoDB.Voyager)

plot_width = int(750)
plot_height = int(700)
x_range=(-2000000, 6000000)
y_range=(-1000000, 7000000)

###Globe
p = figure(x_range = x_range, y_range= y_range,
           x_axis_type="mercator", y_axis_type="mercator",
           title = "iNaturalist Observations overlayed with Google Maps Results of Temples",
           tools = ("tap", "pan", "wheel_zoom", "reset", "save", "lasso_select", "box_zoom"),
           plot_width = plot_width,
           plot_height = plot_height,
           toolbar_location = "below",
           toolbar_sticky = False
           )
p.add_tile(get_provider(xyz.CartoDB.Voyager))

###Globe 2
p2 = figure(x_range = p.x_range, y_range= p.y_range,
           x_axis_type="mercator", y_axis_type="mercator",
           title = "Heatmap",
           tools = ("pan", "wheel_zoom", "reset", "save", "lasso_select", "box_zoom"),
           plot_width = 750,
           plot_height = 700,
           toolbar_location = "below",
           toolbar_sticky = False
           )
p2.add_tile(get_provider(xyz.CartoDB.Voyager))

###Excel file dicts
df = pd.read_excel('withimages.xlsx')
df_ver = pd.read_excel('ver.xlsx')
df_budd = pd.read_excel('08-01-22_ONLY Buddhist Temples US.xlsx')
df_wasp = pd.read_excel('08-02-22_iNaturalist_Fig wasp_FL.xlsx')
df_hind = pd.read_excel('08-10-22_ONLY Hindu Temples US.xlsx')
df_FLusers = pd.read_excel('FLuserswhosentsamplesback.xlsx')
#to display on terminal use: display(df.head())

###Converting latitudinal & longitudinal data into mercator coordinates
def x_coord(x, y):
    
    lat = x
    lon = y
    
    r_major = 6378137.000
    x = r_major * np.radians(lon)
    scale = x/lon
    y = 180.0/np.pi * np.log(np.tan(np.pi/4.0 + 
        lat * (np.pi/180.0)/2.0)) * scale
    return (x, y)

###Define coordinates as tuple (lat, long)
df['coordinates'] = list(zip(df['latitude'], df['longitude']))
df_ver['coordinates_ver'] = list(zip(df_ver['latitude'], df_ver['longitude']))
df_budd['coordinates_budd'] = list(zip(df_budd['Latitude'], df_budd['Longitude']))
df_wasp['coordinates_wasp'] = list(zip(df_wasp['latitude'], df_wasp['longitude']))
df_hind['coordinates_hind'] = list(zip(df_hind['Latitude'], df_hind['Longitude']))
df_FLusers['coordinates_FLusers'] = list(zip(df_FLusers['latitude'], df_FLusers['longitude']))

###Converted coordinates into mercator coordinates
mercators = [x_coord(x, y) for x, y in df['coordinates']]
mercators_ver = [x_coord(x, y) for x, y in df_ver['coordinates_ver']]
mercators_budd = [x_coord(x, y) for x, y in df_budd['coordinates_budd']]
mercators_wasp = [x_coord(x, y) for x, y in df_wasp['coordinates_wasp']]
mercators_hind = [x_coord(x, y) for x, y in df_hind['coordinates_hind']]
mercators_FLusers = [x_coord(x, y) for x, y in df_FLusers['coordinates_FLusers']]
###Mercator column in dicts
df['mercator'] = mercators
df_ver['mercator_ver'] = mercators_ver
df_budd['mercator_budd'] = mercators_budd
df_wasp['mercator_wasp'] = mercators_wasp
df_hind['mercator_hind'] = mercators_hind
df_FLusers['mercator_FLusers'] = mercators_FLusers

###Splitting mercator column into two separate mercator_x and mercator_y columns
###Research grade F. religiosa observations
df[['mercator_x', 'mercator_y']] = df['mercator'].apply(pd.Series)
source = ColumnDataSource(data = df)
source2 = ColumnDataSource(data = dict(
    mercator_x = [],
    mercator_y = [],
    latitude = [],
    longitude = []
    ))

columns = [TableColumn(field = 'latitude', title = 'F. religiosa Latitudes'),
            TableColumn(field = 'longitude', title = 'F. religiosa Longitudes')]

table = DataTable(
    source = source2,
    columns = columns,
    width = 750,
    height = 182,
    sortable = True,
    selectable = True
    )

###F. religiosa observations grade (non Research Grade)
df_ver[['mercator_x_ver', 'mercator_y_ver']] = df_ver['mercator_ver'].apply(pd.Series)
source_ver = ColumnDataSource(data = df_ver)

###Buddhist temples
df_budd[['mercator_x_budd', 'mercator_y_budd']] = df_budd['mercator_budd'].apply(pd.Series)
source_budd = ColumnDataSource(data = df_budd)

source2_budd = ColumnDataSource(data = dict(
    mercator_x_budd = [],
    mercator_y_budd = [],
    Latitude = [],
    Longitude = []
    ))

columns_budd = [TableColumn(field = 'Latitude', title = 'Buddhist Temple Latitudes'),
                TableColumn(field = 'Longitude', title = 'Buddhist Temple Longitudes')]

table_budd = DataTable(
    source = source2_budd,
    columns = columns_budd,
    width = 750,
    height = 182,
    sortable = True,
    selectable = True
    )


###Fig wasp observations
df_wasp[['mercator_x_wasp', 'mercator_y_wasp']] = df_wasp['mercator_wasp'].apply(pd.Series)
source_wasp = ColumnDataSource(data = df_wasp)

###Hindu temples FL
df_hind[['mercator_x_hind', 'mercator_y_hind']] = df_hind['mercator_hind'].apply(pd.Series)
source_hind = ColumnDataSource(data = df_hind)

###iNaturalist users in Florida who sent samples back
df_FLusers[['mercator_x_FLusers', 'mercator_y_FLusers']] = df_FLusers['mercator_FLusers'].apply(pd.Series)
source_FLusers = ColumnDataSource(data = df_FLusers)

###iNaturalist observations display
inat_fig = p.inverted_triangle(
    x = 'mercator_x', 
    y = 'mercator_y',
    fill_color = "green",
    source = source,
    size = 10,
    fill_alpha = 1,
    legend_label = "Research Grade iNaturalist F. religiosa Observations",
    muted_color = "green",
    muted_alpha = 0.1
    )
    
#change 'source = source' to 'source = source2' for CustomJS
muting = p2.inverted_triangle(
    x = 'mercator_x',
    y = 'mercator_y',
    fill_color = "green",
    selection_color = "red",
	source = source,
    size = 10,
    fill_alpha = 1,
    muted_color = "green",
    legend_label = "Research Grade iNaturalist F. religiosa Observations",
    muted_alpha = 0.1
    )

###Verified grade
inat_fig_ver = p.inverted_triangle(
    x = 'mercator_x_ver', 
    y = 'mercator_y_ver',
    fill_color = "blue",
    source = source_ver,
    size = 10,
    fill_alpha = 1,
    legend_label = "iNaturalist F. religiosa Observations",
    muted_color = "blue",
    muted_alpha = 0.1
    )

muting_ver = p2.inverted_triangle(
    x = 'mercator_x_ver',
    y = 'mercator_y_ver',
    fill_color = "blue",
    selection_color = "red",
	source = source_ver,
    size = 10,
    fill_alpha = 1,
    muted_color = "blue",
    legend_label = "iNaturalist F. religiosa Observations",
    muted_alpha = 0.1
    )

inat_wasp = p.hex(
    x = 'mercator_x_wasp',
    y = 'mercator_y_wasp',
    fill_color = "yellow",
	source = source_wasp,
    size = 20,
    fill_alpha = 1,
    legend_label = "iNaturalist P. quadraticeps Observations",
    muted_color = "yellow",
    muted_alpha = 0.1
    )

muting_wasp = p2.hex(
    x = 'mercator_x_wasp',
    y = 'mercator_y_wasp',
    fill_color = "yellow",
	source = source_wasp,
    size = 20,
    fill_alpha = 1,
    muted_color = "yellow",
    legend_label = "iNaturalist P. quadraticeps Observations",
    muted_alpha = 0.1
    )

###Buddhist temples display
budd = p.circle(
    x = 'mercator_x_budd',
    y = 'mercator_y_budd',
    fill_color = "orange",
	source = source_budd,
    size = 8,
    fill_alpha = 0.5,
    legend_label = "Buddhist Temples",
    muted_color = "orange",
    muted_alpha = 0.1
    )

muting_budd = p2.circle(
    x = 'mercator_x_budd',
    y = 'mercator_y_budd',
    fill_color = "orange",
	source = source_budd,
    size = 8,
    fill_alpha = 0.5,
    muted_color = "orange",
    legend_label = "Buddhist Temples",
    muted_alpha = 0.1
    )

###Hindu temples display
hind = p.square_pin(
    x = 'mercator_x_hind',
    y = 'mercator_y_hind',
    fill_color = "red",
	source = source_hind,
    size = 8,
    fill_alpha = 0.5,
    legend_label = "Hindu Temples",
    muted_color = "red",
    muted_alpha = 0.1
    )

muting_hind = p2.square_pin(
    x = 'mercator_x_hind',
    y = 'mercator_y_hind',
    fill_color = "red",
	source = source_hind,
    size = 8,
    fill_alpha = 0.5,
    muted_color = "red",
    legend_label = "Hindu Temples",
    muted_alpha = 0.1
    )

###iNaturalist users in Florida who sent samples back display
FLusers = p.inverted_triangle(
    x = 'mercator_x_FLusers', 
    y = 'mercator_y_FLusers',
    fill_color = "pink",
    source = source_FLusers,
    size = 10,
    fill_alpha = 1,
    legend_label = "Acquired Samples (FL)",
    muted_color = "pink",
    muted_alpha = 0.1
    )
    
#change 'source = source' to 'source = source2' for CustomJS
muting_FLusers = p2.inverted_triangle(
    x = 'mercator_x_FLusers',
    y = 'mercator_y_FLusers',
    fill_color = "pink",
    selection_color = "red",
	source = source_FLusers,
    size = 10,
    fill_alpha = 1,
    muted_color = "pink",
    legend_label = "Acquired Samples (FL)",
    muted_alpha = 0.1
    )

###Glyph ON/OFF
p.legend.click_policy = "hide"
p2.legend.click_policy = "hide"

muting.muted = True
muting_budd.muted = True
muting_hind.muted = True
muting_wasp.muted = True
muting_ver.muted = True
muting_FLusers.muted = True
###after debugging and appraising the data type of each column in my excel file, I decided to try plugging in 'id' for the @
###after a few days of researching, this simple solution turned out to be the one that worked
###my reasoning after my success was that the 'data' is already contained in 'source', therefore, 'id' should derive from "df['id']"

###renderers add parameters to tools, these parameters are specified inside []'s

#url = 'https://www.inaturalist.org/observations/@id'
#taptool = p.select(type=TapTool)
#taptool.renderers = [inat_fig, inat_wasp]
#taptool.callback = OpenURL(url=url)

###I think that if I use '@gmaps_url', or any other direct column name, rather than the 'https://...' address, it directly pulls from the C:/ directory and causes errors
#url_budd = 'https:////www.google.com/maps/place/@gmaps_url'
#taptool_budd = p.select(type=TapTool)
#taptool_budd.renderers = [budd]
#taptool_budd.callback = OpenURL(url=url_budd)

###THIS is the nonworking code I had prior to URL opening on click, I think it didn't work because I had set 'source.data' (in the running code below) equal to 'source_budd.data' which
###confused the editor
#code = """
#if(source_budd.selected.indices != ""){
#    window.open(source_budd.data['gmaps_url'][source_budd.selected.indices])
#}
#"""

###When using '07-27-22_iNaturalist_USA.xlsx' change 'url' to 'id_url'
code = """
if(source1.selected.indices != ""){
    window.open(source1.data['url'][source1.selected.indices])
}
if(source2.selected.indices != ""){
    window.open(source2.data['gmaps_url'][source2.selected.indices])
}
if(source3.selected.indices != ""){
    window.open(source3.data['hfpxzc href'][source3.selected.indices])
}
if(source4.selected.indices != ""){
    window.open(source4.data['url'][source4.selected.indices])
}
if(source5.selected.indices != ""){
    window.open(source5.data['url'][source5.selected.indices])
}
"""


###The plot uses mercator_x, y coordinates, but the data I want requires lat/lng coordinates
code_select ="""
var inds = cb_obj.indices;
var d1 = source.data;
var d2 = source2.data;
d2['mercator_x'] = []
d2['mercator_y'] = []
d2['latitude'] = []
d2['longitude'] = []
for (var i = 0; i < inds.length; i++) {
    d2['mercator_x'].push(d1['mercator_x'][inds[i]])
    d2['mercator_y'].push(d1['mercator_y'][inds[i]])
    d2['latitude'].push(d1['latitude'][inds[i]])
    d2['longitude'].push(d1['longitude'][inds[i]])
}
source2.change.emit();
table.change.emit();
"""


code_select_budd ="""
var inds = cb_obj.indices;
var d1 = source.data;
var d2 = source2.data;
d2['mercator_x_budd'] = []
d2['mercator_y_budd'] = []
d2['Latitude'] = []
d2['Longitude'] = []
for (var i = 0; i < inds.length; i++) {
    d2['mercator_x_budd'].push(d1['mercator_x_budd'][inds[i]])
    d2['mercator_y_budd'].push(d1['mercator_y_budd'][inds[i]])
    d2['Latitude'].push(d1['Latitude'][inds[i]])
    d2['Longitude'].push(d1['Longitude'][inds[i]])
}
source2.change.emit();
table_budd.change.emit();
"""

taptool = p.select(type=TapTool)
taptool.callback = CustomJS(args = dict(source1 = source, source2 = source_budd, source3 = source_hind, source4 = source_ver, source5 = source_wasp), code = code)

###CustomJS for selection
source.selected.js_on_change('indices', CustomJS(args = dict(source = source, source2 = source2, table = table), code = code_select))
source_budd.selected.js_on_change('indices', CustomJS(args = dict(source = source_budd, source2 = source2_budd, table = table_budd), code = code_select_budd))

p.add_tools(HoverTool(
    renderers = [inat_fig, inat_fig_ver, inat_wasp],
#    tooltips = [("ID", "@id")]
    tooltips =
    """
        <div>
            <div>
                <img
                    src="@image_url" height="225" alt="@imgs" width="225"
                    style="float: center; margin: 0px 0px 0px 0px;"
                    border="0"
                ></img>
            </div>
        """
))

###Manual code that either opens iNaturalist or Google Maps
#taptool = p.select(type=TapTool)

button = Button(label="Download", button_type="success")
button.js_on_click(CustomJS(args=dict(source=source2),code=open(os.path.join(os.path.dirname(__file__),"download.js")).read()))

grid = gridplot([[p, p2], [table, table_budd], [button, None]])

show(grid)
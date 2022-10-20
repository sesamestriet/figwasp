from bokeh.io import show
from bokeh.models import ColumnDataSource, Circle, OpenURL, TapTool
from bokeh.plotting import figure
from bokeh.models.callbacks import CustomJS

source = ColumnDataSource(data=dict(
    x = [1, 2],
    y = [3, 4],
    url = ["http://google.com", "http://bing.com"],
))

p = figure(tools="tap")
p.circle('x', 'y', size=15, source=source)

#code = """
#selection = require("core/util/selection")
#indices = selection.get_indices(source)
#for (i = 0; i < indices.length; i++) {
#    ind = indices[i]
#    url = source.data['url'][indices]
#    window.open(url, "_blank")
#}
#"""

#THIS is the running code, I wonder if the other code has outdated syntax
code = """
if(source.selected.indices != ""){
    window.open(source.data['url'][source.selected.indices])
}
"""

taptool = p.select(type=TapTool)
taptool.callback = CustomJS(args=dict(source=source), code=code)

show(p)
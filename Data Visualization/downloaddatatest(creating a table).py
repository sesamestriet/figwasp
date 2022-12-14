from random import random

import bokeh.io
from bokeh.io import output_notebook, show

from bokeh.layouts import row
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.plotting import figure
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn

#from bokeh.resources import INLINE
#bokeh.io.output_notebook(INLINE)

x = [random() for x in range(500)]
y = [random() for y in range(500)]

s1 = ColumnDataSource(data=dict(x=x, y=y))
p1 = figure(plot_width=400, plot_height=400, tools="lasso_select", title="Select Here")
p1.circle('x', 'y', source=s1, alpha=0.6)

s2 = ColumnDataSource(data=dict(x=[], y=[]))
p2 = figure(plot_width=400, plot_height=400, x_range=(0, 1), y_range=(0, 1),
            tools="", title="Watch Here")
p2.circle('x', 'y', source=s2, alpha=0.6)

columns = [TableColumn(field ="x",  title = "X axis"),
            TableColumn(field ="y",  title = "Y axis")]

table = DataTable(source =s2, columns = columns, width =155, height = 380)


s1.selected.js_on_change('indices', CustomJS(args=dict(s1=s1, s2=s2, table=table), code="""
        var inds = cb_obj.indices;
        var d1 = s1.data;
        var d2 = s2.data;
        d2['x'] = []
        d2['y'] = []
        for (var i = 0; i < inds.length; i++) {
            d2['x'].push(d1['x'][inds[i]])
            d2['y'].push(d1['y'][inds[i]])
        }
        s2.change.emit();
        table.change.emit();
    """)
)

layout = row(p1, p2, table)

show(layout)
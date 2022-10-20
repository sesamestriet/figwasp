
import numpy as np
from random import choice
from string import ascii_lowercase

from bokeh.models.tools import *
from bokeh.plotting import *
from bokeh.models import CustomJS



output_notebook()


TOOLS="pan,wheel_zoom,reset,hover,poly_select,box_select"
p = figure(title = "My chart", tools=TOOLS)
p.xaxis.axis_label = 'X'
p.yaxis.axis_label = 'Y'

source = ColumnDataSource(
    data=dict(
        xvals=list(range(0, 10)),
        yvals=list(np.random.normal(0, 1, 10)),
        letters = [choice(ascii_lowercase) for _ in range(10)]
    )
)
p.scatter("xvals", "yvals",source=source,fill_alpha=0.2, size=5)

select_tool = p.select(dict(type=BoxSelectTool))[0]

source.js_property_callbacks('indices', CustomJS(args=dict(source = source), code="""
        var inds = cb_obj.get('selected')['1d'].indices;
        var d1 = cb_obj.get('data');
        console.log(d1)
        var kernel = IPython.notebook.kernel;
        IPython.notebook.kernel.execute("inds = " + inds);
        """
))

show(p)
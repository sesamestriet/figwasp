from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Button
from bokeh.io import show
import os

source = ColumnDataSource({'list1':[0,1,2,3],'list2':[4,5,6,7]})
button = Button(label="Download", button_type="success")
button.js_on_click(CustomJS(args=dict(source=source),code=open(os.path.join(os.path.dirname(__file__),"download.js")).read()))
show(button)
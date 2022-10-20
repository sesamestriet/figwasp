import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, CustomJS, Div, Row
from bokeh.events import *

source = ColumnDataSource({'x': [], 'y': []})

p = figure(plot_width = 900)
lines = [p.line(np.arange(10), np.random.random(10)) for i in range(3)]
lilne = p.line('x', 'y', line_color = 'red', line_dash = 'dashed', source = source)
div = Div(text='')

callback_tap = '''
if (true === Bokeh.drawing) {
    Bokeh.drawing = false
}
else {
    if (!Bokeh.drawing) {
        src.data = {'x':[], 'y':[]}        
        src.change.emit()
    }

    src.data['x'].push(cb_obj.x)
    src.data['y'].push(cb_obj.y)

    Bokeh.drawing = true
    Bokeh.sx_start = cb_obj.sx
    Bokeh.x_start = cb_obj.x
}'''

callback_mousemove = '''
if (Bokeh.drawing) {  
    if (src.data['x'].length > 1) {
        src.data['x'].pop()
        src.data['y'].pop()   
    }

    src.data['x'].push(cb_obj.x)
    src.data['y'].push(cb_obj.y)
    src.change.emit()

    div.text = 'Distance: ' + Math.round(cb_obj.sx - Bokeh.sx_start) + ' px' + ' (' + (Math.round((cb_obj.x - Bokeh.x_start) * 100) / 100) + ' units)'
}'''

p.js_on_event('tap', CustomJS(args = {'src': source}, code = callback_tap))
p.js_on_event('mousemove', CustomJS(args = {'src': source, 'div': div}, code = callback_mousemove))

show(Row(p, div))
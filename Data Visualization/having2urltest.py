from bokeh.io import show
from bokeh.models import ColumnDataSource, Circle, OpenURL, TapTool
from bokeh.plotting import figure
from bokeh.models.callbacks import CustomJS

x1 = [1,1,1]
y1 = [1,2,3]
x2 = [3,3,3]
y2 = [1,2,3]
url1 = ["http://www.colors.commutercreative.com/navy/", "http://www.colors.commutercreative.com/orange/",
        "http://www.colors.commutercreative.com/olive/"]
url2 = ["http://www.colors.commutercreative.com/firebrick/", "http://www.colors.commutercreative.com/gold/",
        "http://www.colors.commutercreative.com/green/"]

source1 = ColumnDataSource(data=dict(x=x1, y=y1, url = url1))
source2 = ColumnDataSource(data=dict(x=x2, y=y2, url = url2))

plot = figure(plot_width=400, plot_height=400, title='TapTool example')

plot1 = plot.circle('x', 'y', size=20, fill_color="lightcoral", source=source1)
plot2 = plot.circle('x', 'y', size=20, fill_color='lightblue', source=source2)


tapcb = CustomJS(args=dict(source1=plot1.data_source, source2=plot2.data_source),
    code="""
        if(source1.selected.indices != ""){
            window.open(source1.data["url"][source1.selected.indices])
        }
        if(source2.selected.indices != ""){
            window.open(source2.data["url"][source2.selected.indices])
        }
    """)
taptool = TapTool(callback=tapcb)
plot.tools.append(taptool)
show(plot)
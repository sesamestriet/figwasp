from bokeh.plotting import figure, output_file, show
import pandas

#Read in csv
df = pandas.read_csv('.csv')

car = df['Car']
hp = df['Horsepower']

x = [1, 2, 3]
y = [4, 5, 6]

output_file('index.html')

#Add plot
p = figure(
	y_range = car
	plot_width
	plot_height
	title='title',
	x_axis_label = 'X Axis',
	y_axis_label = 'Y Axis'
	tools = ""
)

#Render glyph
p.line(x, y, legend_label = 'Test', line_width=2)

#Show result
show(p)
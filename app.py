import dash
import dash_core_components as dcc
import dash_html_components as html
from Objects import ListingsTracker

app = dash.Dash()
server = app.server


listingsTracker = ListingsTracker()
data = listingsTracker.getPPN()

app.layout = html.Div(children=[

	html.H1(children='Hello Dash'),

	html.Div(children=''' Dash: A web application framework for Python. '''),

	dcc.Graph(
		id='example-graph',
		figure = {
			'data': [
                {'x': list(data.keys()), 'y': list(data.values()), 'type': 'bar', 'name': 'PPN'}
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
		}
	),
	html.Div(id='display-value')

])
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


if __name__ == '__main__':
	app.run_server(debug=True)

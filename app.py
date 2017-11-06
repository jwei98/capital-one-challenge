import dash
import dash_core_components as dcc
import dash_html_components as html
from Objects import ListingsTracker
import avg_income_calculator as calculator

app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

server = app.server


listingsTracker = ListingsTracker()
ppnData = listingsTracker.getPPN()

app.layout = html.Div(children=[

	html.H1(children='Optimizing Airbnb Listings'),

	html.Div(children=''' '''),

	dcc.Graph(
		id='ppn-graph',
		figure = {
			'data': [
                {'x': list(ppnData.keys()), 'y': list(ppnData.values()), 'type': 'bar', 'name': 'PPN'}
            ],
            'layout': {
                'title': 'Average Price per Night'
            }
		}
	),

	# inputs for latitude/longitude average income calculator
	html.H3(children='Given latitude and longitude, calculate average weekly income:'),
	dcc.Input(
    	id='latitude-input',
    	placeholder='Enter latitude...',
    	type='number',
    	value='37.74944922'
    ),
	dcc.Input(
    	id='longitude-input',
    	placeholder='Enter latitude...',
    	type='number',
    	value='-122.4095556'
    ),
    html.Button('Calculate', id='calculate-average-weekly-income'),
    html.Div(id='average-weekly-income-output',
             children="Enter latitude and longitude, and press calculate"
    ),
    

])


# given latitude/longitude, calculate average weekly income
@app.callback(
	dash.dependencies.Output(component_id='average-weekly-income-output', component_property='children'),
	[dash.dependencies.Input(component_id='calculate-average-weekly-income', component_property='n_clicks')],
	[dash.dependencies.State('latitude-input', 'value'),
	 dash.dependencies.State('longitude-input', 'value')]
)
def calculateAverageWeeklyIncome(n_clicks, latitude, longitude):
	return 'The listing at {}, {} is located in the {} neighborhood!'.format(latitude,longitude,calculator.getNeighbourhood(latitude, longitude))

if __name__ == '__main__':
	app.run_server(debug=True)

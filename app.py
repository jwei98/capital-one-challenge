import dash
import dash_core_components as dcc
import dash_html_components as html
from Objects import ListingsTracker
import avg_income_calculator as calculator
import plotly.graph_objs as go
import colorlover as cl

mapbox_access_token = 'pk.eyJ1IjoianVzdGlud2VpIiwiYSI6ImNqOWdqd2JlMzJwODMyeHBhZ3JzZTBqcm0ifQ.BR96rueM9hQkPc7GeozPiw'

app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

server = app.server


listingsTracker = ListingsTracker()
ppnData = listingsTracker.getPPN()

def generateColors(colorArray):
	scale = cl.scales['10']['div']
	for set in scale:
		for colors in scale[set]:
			colorArray.append(colors)

	

colors = []
generateColors(colors)


def generateMap():
	data = []
	counter = 0
	for n in listingsTracker.getNeighbourhoods():
		data.append(
			    go.Scattermapbox(
			        name=n,
			        lat=listingsTracker.getLatitudes(n),
			        lon=listingsTracker.getLongitudes(n),
			        mode='markers',
			        marker= go.Marker(
			            size=5,
			            color=colors[counter],
			        ),
			        text=listingsTracker.getIds(n),
			    )
		)
		counter = counter + 1
	return html.Div(
    	dcc.Graph(
	    	id='map-graph',
	    	figure= {
	    		'data' : go.Data(data),
				'layout' : go.Layout(
					title= 'Map of Listings',
				    autosize=True,
				    hovermode='closest',
				    mapbox=dict(
				        accesstoken=mapbox_access_token,
				        bearing=0,
				        center=dict(
				            lat=37.759338,
				            lon=-122.429020
				        ),
				        pitch=0,
				        zoom=10
				    ),
				    height=600
				)
	    	}
	    )
    )
def generatePPNChart():
	neighbourhoods = []
	avgPPN = []
	for n in listingsTracker.getNeighbourhoods():
		neighbourhoods.append(n)
		avgPPN.append(ppnData.get(n))
	return dcc.Graph(
				id='ppn-graph',
				figure = {
					'data': [
		                {'x': neighbourhoods,
		                'y': avgPPN,
		                'type': 'bar',
		                'name': 'PPN',
		                'marker': dict(color = colors[0:37])
		                }
		            ],
		            'layout': {
		                'title': 'Average Price per Night',
		            }
				}
			)
# page layout
app.layout = html.Div(children=[

	html.H1(children='Optimizing Airbnb Listings'),

	html.Div(children=''' '''),

	html.Div([
        html.Div([
            generateMap()
        ], className="seven columns"),

        html.Div([
            generatePPNChart()
        ], className="five columns"),
    ], className="row"),


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

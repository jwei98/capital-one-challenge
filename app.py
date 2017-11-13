import dash
import dash_core_components as dcc
import dash_html_components as html
from Objects import ListingsTracker
import geopy_calculator as calculator
import plotly.graph_objs as go
import colorlover as cl
import json
from collections import OrderedDict
import os
from flask import Flask, send_from_directory

server = Flask(__name__, static_folder='static')
mapbox_access_token = os.environ.get('MAPBOX_KEY')

app = dash.Dash(server=server)
app.title = 'myAirbnb'
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.config['suppress_callback_exceptions']=True

geopyToAirbnbDictionary = {'Bayview District': 'Bayview', 'Castro District': 'Castro/Upper Market', \
	'Crocker-Amazon': 'Crocker Amazon', 'Civic Center': 'Downtown/Civic Center',
	'Portola':'Excelsior', 'Richmond District': 'Inner Richmond', 'Anza Vista': 'Western Addition'}


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


def generateMap(latitude = None, longitude = None):
	userInput = not (latitude is None or longitude is None)
	zoom = 11
	data = []
	colorCounter = 0
	listingsCounter = 0
	for n in listingsTracker.getNeighbourhoods():
		data.append(
			    go.Scattermapbox(
			        name=n,
			        lat=listingsTracker.getLatitudes(n),
			        lon=listingsTracker.getLongitudes(n),
			        mode='markers',
			        marker= go.Marker(
			            size=5,
			            color=colors[colorCounter],
			        ),
			    )
		)
		
		colorCounter = colorCounter + 1
	if userInput:
		zoom = 11.5
		data.append(
			go.Scattermapbox(
			        name="Your Location",
			        lat=[str(latitude)],
			        lon=[str(longitude)],
			        mode='markers',
			        marker= go.Marker(
			            size=25,
			            color='gold',
			        ),
			)
		)
	return html.Div(
    	dcc.Graph(
	    	id='map-graph',
	    	figure= {
	    		'data' : go.Data(data),
				'layout' : go.Layout(
					title= 'Map of SF Airbnb Listings',
				    autosize=True,
				    hovermode='closest',
				    mapbox=dict(
				        accesstoken=mapbox_access_token,
				        bearing=0,
				        center=dict(
				            lat= 37.759338 if not userInput else latitude,
				            lon=-122.429020 if not userInput else longitude,
				        ),
				        pitch=0,
				        zoom=zoom,
				        
				    ),
				    height=600,
				)
	    	}
	    ),
	    id='map-graph-div'
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
		                'visible': True,
		            }
				}
			)

def generateHeader():
	return html.Div([
		html.H1("myAirbnb Calculator"),
		html.P("by Justin Wei"),], style={'textAlign':'center'})
def generateCalculator():
	return html.Div([
				# inputs for latitude/longitude average income calculator
				html.H2(children='Calculator'),
				dcc.Input(
			    	id='latitude-input',
			    	placeholder='Enter latitude...',
			    	type='number',
			    	value=''
			    ),
				dcc.Input(
			    	id='longitude-input',
			    	placeholder='Enter longitude...',
			    	type='number',
			    	value=''
			    ),
			    
			    html.Button('Calculate', id='calculate-average-weekly-income'),
			    generateDropdown(False),
			    html.H2(''),
			    html.Div(id='average-weekly-income-output',
			             children=["Enter latitude and longitude, and press calculate"]
			    )
		    ]
	)
def generateDropdown(isDisable):
	complete_data = []
	values = []
	for neighbourhood in listingsTracker.getNeighbourhoods():
		data = OrderedDict()
		data['label'] = neighbourhood
		data['value'] = neighbourhood
		values.append(neighbourhood)
		complete_data.append(data)
	return dcc.Dropdown(
		id='neighbourhood-selector',
	    options= complete_data,
	    multi=False,
	    value=values,
	    disabled=isDisable
	)
def generateNumberListingsPerNeighbourhoodChart():
	numberListings = listingsTracker.getNumberListingsPerNeighbourhood()
	neighbourhoods = []
	count = []
	for n in listingsTracker.getNeighbourhoods():
		neighbourhoods.append(n)
		count.append(numberListings.get(n))
	
	counter = 0
	return dcc.Graph(
			id='rs-graph',
			figure = {
				'data': [
	                {'x': neighbourhoods,
	                'y': count,
	                'type': 'bar',
	                'name': 'Number of Listings per Neighbourhood',
	                'marker': dict(color = colors[0:37])
	                }
	            ],
	            'layout': {
	                'title': 'Number Listings per Neighbourhood',
	                'visible': True,
	                'yaxis': dict(range=[min(count)-5,max(count)+5]),
	            }
			}
	)
def generateReviewScoresPerNeighbourhoodChart():
	reviewScores = listingsTracker.getReviewScoresPerNeighbourhood()
	neighbourhoods = []
	scores = []
	for n in listingsTracker.getNeighbourhoods():
		neighbourhoods.append(n)
		scores.append(reviewScores.get(n))
	
	counter = 0
	return dcc.Graph(
			id='rs-graph',
			figure = {
				'data': [
	                {'x': neighbourhoods,
	                'y': scores,
	                'type': 'bar',
	                'name': 'Review Score',
	                'marker': dict(color = colors[0:37])
	                }
	            ],
	            'layout': {
	                'title': 'Average Review Score per Neighbourhood',
	                'visible': True,
	                'yaxis': dict(range=[min(scores)-5,100]),
	            }
			}
	)

def generateValueChart():
	reviewScores = listingsTracker.getReviewScoresPerNeighbourhood()

	neighbourhoods = []
	values = []
	for n in listingsTracker.getNeighbourhoods():
		neighbourhoods.append(n)
		values.append(reviewScores.get(n)/ppnData.get(n))
	counter = 0
	return dcc.Graph(
			id='value-graph',
			figure = {
				'data': [
	                {'x': neighbourhoods,
	                'y': values,
	                'type': 'bar',
	                'name': 'Value',
	                'marker': dict(color = colors[0:37])
	                }
	            ],
	            'layout': {
	                'title': 'Average Value (Score/Price) per Neighbourhood',
	                'visible': True,
	            }
			}
	)

def generatePromptUserForNeighbourhood(latitude, longitude, neighbourhood):
	return html.Div(children = [
		html.P('We were able to track the coordinates ({}, {}) to a neighbourhood called {} neighborhood! Please help us by selecting the appropriate neighbourhood above!'.format(latitude,longitude, neighbourhood)),
	])

def generateFoundListingNeighbourhood(latitude, longitude, neighbourhood, userInput):
	if userInput:
		introLine = 'The listing at ({}, {}) is located in the {} neighborhood!'.format(latitude,longitude, neighbourhood)
	else:
		introLine = ''
	optimalPrice, optimalRevenue, optimalWeekly = listingsTracker.getOptimalPrice(neighbourhood)
	return html.Div(children = [
		html.P('{0} Given an average price per night of ${1:.2f} and {2:.2f} bookings per week, your estimated weekly average income being in the {3} neighbourhood is:'.format(introLine, listingsTracker.getPPN(neighbourhood), listingsTracker.getAverageBookingsPerWeek(neighbourhood), neighbourhood)),
		html.H4('${0:.2f}'.format(listingsTracker.getAverageWeeklyIncome(neighbourhood))),
		html.P('You should list your property at...'),
		html.H4('${0:.2f}'.format(optimalPrice)),
		html.P('Houses at this price tend to be rented out {0:.2f} times a week, for a total weekly revenue of: '.format(optimalWeekly)),
		html.H4('${0:.2f}!'.format(optimalRevenue))
	], style={
		'text-align': 'center',
		'border': '2px solid ' + colors[listingsTracker.getNeighbourhoods().index(neighbourhood)],
		'border-radius': '5px'
    })
	
def generateAllCharts():
	return html.Div([
	    dcc.Tabs(
	    	tabs=[
	    		{'label': 'Number of Listings', 'value': 0},
	    		{'label': 'Average Price Per Night', 'value': 1},
	    		{'label': 'Average Review Score', 'value': 2},
	    		{'label': 'Average Value', 'value': 3},
	    	],
	    	value=0,
	    	id='tabs'
	    ),
	    html.Div(id='tab-output')
    ])
	




# PAGE LAYOUT

app.layout = html.Div(children=[
	generateHeader(),
    html.Div([
    	html.Div([
    		generateMap()
        ], className="eight columns"),
        html.Div([
        	generateCalculator()
        ], className="four columns"),
    ], className="row"),

	generateAllCharts(),
	html.Br(),
	html.Br(),
	html.Div([
		html.A('View Project Github', href='https://github.com/jwei98/capital-one-challenge'),
	], style = {
		'text-align': 'center'
	})
	

])



# CALLBACKS



# given latitude/longitude, calculate average weekly income
@app.callback(dash.dependencies.Output('tab-output', 'children'), [dash.dependencies.Input('tabs', 'value')])
def display_content(value):
    if value == 0:
    	return generateNumberListingsPerNeighbourhoodChart()
    elif value == 1:
    	return generatePPNChart()
    elif value == 2:
    	return generateReviewScoresPerNeighbourhoodChart()
    else:
    	return generateValueChart()

@app.callback(dash.dependencies.Output(component_id='neighbourhood-selector', component_property='value'),
	[dash.dependencies.Input(component_id='calculate-average-weekly-income', component_property='n_clicks')])
def clearSelector(n_clicks):
	return listingsTracker.getNeighbourhoods()


@app.callback(dash.dependencies.Output(component_id='average-weekly-income-output', component_property='children'),
	[dash.dependencies.Input(component_id='calculate-average-weekly-income', component_property='n_clicks'),
	 dash.dependencies.Input(component_id='neighbourhood-selector', component_property='value')],
	[dash.dependencies.State('latitude-input', 'value'),
	 dash.dependencies.State('longitude-input', 'value')])
def calculateAverageWeeklyIncome(n_clicks, neighbourhoodSelector, latitude, longitude):
	isNeighbourhoodSelectorOn = not isinstance(neighbourhoodSelector, list)
	if (latitude == '' or longitude == ''):
		if not isNeighbourhoodSelectorOn:
			return 'Enter latitude and longitude of your listing, i.e. (37.76, -122.43), then press calculate to see your estimated weekly average income and suggested listing price!  Alternatively, you may select a neighbourhood to see average prices below!'
		elif isNeighbourhoodSelectorOn:
			if neighbourhoodSelector in listingsTracker.getNeighbourhoods():
				return generateFoundListingNeighbourhood(latitude, longitude, neighbourhoodSelector, False)
			else:
				return generatePromptUserForNeighbourhood(latitude, longitude, geopy_neighbourhood)
	elif (latitude != '' and longitude != ''):
		# try getting neighbourhood
		geopy_neighbourhood = calculator.getNeighbourhood(latitude, longitude)
		# 1) bad location
		if geopy_neighbourhood is None:
			return 'Sorry! It appears your listing at ({}, {}) does not exist any San Francisco neighbourhood... Please try again! '.format(latitude,longitude)
		# 2) found everything perfectly
		elif geopy_neighbourhood in listingsTracker.getNeighbourhoods():
			return generateFoundListingNeighbourhood(latitude, longitude, geopy_neighbourhood, True)
		# 3) valid location, but need user help
		else:
			if geopy_neighbourhood in geopyToAirbnbDictionary:
				return generateFoundListingNeighbourhood(latitude, longitude, geopyToAirbnbDictionary[geopy_neighbourhood], True)
			elif isNeighbourhoodSelectorOn:
				return generateFoundListingNeighbourhood(latitude, longitude, neighbourhoodSelector, False)
			else:
				return generatePromptUserForNeighbourhood(latitude, longitude, geopy_neighbourhood)
		
		

# have a "or select a neighborhood" instruction so that we can always display the select neighborhood field

# handles map callbacks
@app.callback(
	dash.dependencies.Output(component_id='map-graph-div', component_property='children'),
	[dash.dependencies.Input(component_id='calculate-average-weekly-income', component_property='n_clicks'),
	dash.dependencies.Input(component_id='neighbourhood-selector', component_property='value')],
	[dash.dependencies.State('latitude-input', 'value'),
	 dash.dependencies.State('longitude-input', 'value')]
)
def mapCallback(n_clicks, neighbourhoodSelector, latitude, longitude):
	isNeighbourhoodSelectorOn = not isinstance(neighbourhoodSelector, list)
	if not (latitude == '' or longitude == '' or n_clicks is None) and not isNeighbourhoodSelectorOn:
		geopy_neighbourhood = calculator.getNeighbourhood(latitude, longitude)
		if geopy_neighbourhood is None:
			return generateMap()
		else:
			return generateMap(latitude, longitude)
	elif latitude != '' and longitude != '':
		return generateMap(latitude, longitude)
	elif isNeighbourhoodSelectorOn:
		if neighbourhoodSelector == "Outer Sunset":
			location = calculator.getCoordsOfNeighbourhood("Sunset District")
		else:
			location = calculator.getCoordsOfNeighbourhood(neighbourhoodSelector)
		return generateMap(location[0], location[1])
	else:
		return generateMap()

@server.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(server.root_path, 'static'),
                               'favicon.ico', mimetype='image/airbnb.ico')

if __name__ == '__main__':
	app.run_server(debug=True)

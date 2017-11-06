from geopy.geocoders import Nominatim

geolocator = Nominatim()
geopyToAirbnbDictionary = {'Bayview District': 'Bayview', 'Castro District': 'Castro/Upper Market', \
	'Crocker-Amazon': 'Crocker Amazon', 'Civic Center': 'Downtown/Civic Center',
	'Portola':'Excelsior'}

def getNeighbourhood(latitude, longitude):
	coords = str(latitude) + "," + str(longitude)
	location = geolocator.reverse(coords)
	location_neighbourhood = location.raw.get("address").get("neighbourhood")
	return location_neighbourhood

def main():
	print(getNeighbourhood(37.804941, -122.468161))

if __name__ == "__main__":
	main()
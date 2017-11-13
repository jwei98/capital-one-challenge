from geopy.geocoders import Nominatim

geolocator = Nominatim()
geolocatorDict = {"Downtown/Civic Center": "Civic Center", "Castro/Upper Market": "Castro", "Treasure Island/YBI": "Treasure Island"}

def getNeighbourhood(latitude, longitude):
	coords = str(latitude) + "," + str(longitude)
	location = geolocator.reverse(coords)
	if location.raw.get("address") is None:
		return None
	else:
		location_neighbourhood = location.raw.get("address").get("neighbourhood")
		return location_neighbourhood

def getCoordsOfNeighbourhood(neighbourhood):
	if neighbourhood in geolocatorDict:
		neighbourhood = geolocatorDict.get(neighbourhood)

	location = geolocator.geocode(neighbourhood + ", San Francisco")
	return [location.raw['lat'], location.raw['lon']]

if __name__ == "__main__":
	main()
import csv

class Listing:
	def __init__(self, id, latitude, longitude, price, neighbourhood_cleansed):
		self.id = id
		self.coords = [latitude, longitude]
		self.price = float(price)
		self.neighbourhood = neighbourhood_cleansed
		self.nightsBookedPerWeek = 0

class ListingsTracker:
	def __init__(self):
		self.latitudes = []
		self.longitudes = []
		self.ids = []
		self.neighbourhoods = []
		self.ppn = {}
		self.listings = []
		self.freeNightsPerPrice = {}
		self.listingsPerPrice = {}

		# for neighbourhood specific things
		self.latitudesByNeighbourhood = {}
		self.longitudesByNeighbourhood = {}
		self.idsByNeighbourhood = {}


		self.readNeighbourhoods()
		self.readListings()
		self.readAvailabilities()


	# returns list of neighbourhoods
	def readNeighbourhoods(self):
		with open('./data/neighbourhoods.csv', newline='', errors='ignore') as neighbourhoodsFile:
			reader = csv.DictReader(neighbourhoodsFile, delimiter=',')
			# read through entries, adding to neighbourhood list and price per neighbourhood dictionary
			for row in reader:
				neighbourhood = row["neighbourhood"]
				self.neighbourhoods.append(neighbourhood)
				self.latitudesByNeighbourhood[neighbourhood] = []
				self.longitudesByNeighbourhood[neighbourhood] = []
				self.idsByNeighbourhood[neighbourhood] = []
				self.ppn[neighbourhood] = 0


	def readListings(self):
		neighbourhoodTotalPrices = {}
		neighbourhoodCount = {}
		with open('./data/listings.csv', newline='', errors='ignore') as listingsFile:
			# DictReader reads specific column
			reader = csv.DictReader(listingsFile, delimiter=',')
			for row in reader:
				# cut out listings where not all fields exist
				if row["id"] and row["latitude"] and row["longitude"] and row["price"] and row["neighbourhood_cleansed"]:
					newListing = Listing(row["id"], row["latitude"], row["longitude"], row["price"].replace(',','').replace('$',''), row["neighbourhood_cleansed"])
					self.listings.append(newListing)
					self.latitudes.append(row["latitude"])
					self.longitudes.append(row["longitude"])
					self.latitudesByNeighbourhood[row["neighbourhood_cleansed"]].append(row["latitude"])
					self.longitudesByNeighbourhood[row["neighbourhood_cleansed"]].append(row["longitude"])
					self.ids.append(row["id"])

					# edit price per neighbourhood dictionary
					newNeighbourhood = newListing.neighbourhood
					if newNeighbourhood in neighbourhoodTotalPrices:
						neighbourhoodTotalPrices[newNeighbourhood] = neighbourhoodTotalPrices[newNeighbourhood] + newListing.price
						neighbourhoodCount[newNeighbourhood] = neighbourhoodCount[newNeighbourhood] + 1
					else:
						neighbourhoodTotalPrices[newNeighbourhood] = newListing.price
						neighbourhoodCount[newNeighbourhood] = 0

		for neighbourhood in neighbourhoodTotalPrices:
			self.ppn[neighbourhood] = neighbourhoodTotalPrices[neighbourhood] / neighbourhoodCount[neighbourhood]

	def readAvailabilities(self):
		with open('./data/calendar_available_only.csv', newline='', errors='ignore') as availabilityFile:
			reader = csv.DictReader(availabilityFile, delimiter=',')
			# read through entries, adding to neighbourhood list and price per neighbourhood dictionary
			for row in reader:
				if row["price"] and row["listing_id"]:
					price = float(row["price"].replace(',','').replace('$',''))
					if price in self.freeNightsPerPrice:
						self.freeNightsPerPrice[price] = self.freeNightsPerPrice[price] + 1
						if not row["listing_id"] in self.listingsPerPrice[price]:
							self.listingsPerPrice[price].append(row["listing_id"])
					else:
						self.freeNightsPerPrice[price] = 1
						self.listingsPerPrice[price] = [row["listing_id"]]
					
					

	# getters
	def getListings(self):
		return self.listings
	def getNeighbourhoods(self):
		return self.neighbourhoods
	def getLongitudes(self, neighbourhood=None):
		if neighbourhood is None:
			return self.longitudes
		else:
			return self.longitudesByNeighbourhood[neighbourhood]
		
	def getLatitudes(self, neighbourhood=None):
		if neighbourhood is None:
			return self.latitudes
		else:
			return self.latitudesByNeighbourhood[neighbourhood]

	def getIds(self, neighbourhood=None):
		if neighbourhood is None:
			return self.ids
		else:
			return self.idsByNeighbourhood[neighbourhood]

	def getPPN(self):
		return self.ppn
	def getBookedNightsPerPrice(self):
		bookedNightsPerPrice = {}
		for price in self.freeNightsPerPrice:
			if price < 500 and price > 95:
				numberListingsPerPrice = len(self.listingsPerPrice[price])
				print(str(price) + ": " + str(self.freeNightsPerPrice[price]) + " : " + str(numberListingsPerPrice))
				bookedNightsPerPrice[price] = (356 - float(self.freeNightsPerPrice[price]/numberListingsPerPrice))/52
		return bookedNightsPerPrice

	def printPPN(self):
		for n in self.ppn:
			print ("{0}: ${1:.2f}".format(n,self.ppn[n]))






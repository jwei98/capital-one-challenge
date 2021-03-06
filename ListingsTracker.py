import csv

class Neighbourhood:
	def __init__(self, name):
		self.name = name
		self.ids = []
		self.latitudes = []
		self.longitudes = []
		self.totalReviewScore = 0
		self.totalCost = 0
		self.totalNightsBooked = 0
		self.numberListings = 0
		self.numberWeeklyBookingsPerPrice = {}
		self.numberListingsPerPrice = {}

	# update the neighbourhood class everytime we get a new listing
	def addListing(self, idNum, lat, lon, price, score, availableInYear):
		self.ids.append(idNum)
		self.numberListings = self.numberListings + 1
		self.latitudes.append(lat)
		self.longitudes.append(lon)
		self.totalCost = self.totalCost + price
		self.totalReviewScore = self.totalReviewScore + float(score)
		# assume that when airbnb is not available, it's been booked
		nightsBookedInYear = 365 - int(availableInYear)
		self.totalNightsBooked = self.totalNightsBooked + nightsBookedInYear
		# if the airbnb is available the whole year, skip the division (ends up being a float rounding error)
		# hard-code fix with Presidio because there are so few listings
		if int(availableInYear) == 0 and self.name != "Presidio":
			timesBookedInWeek = 7
		else:
			timesBookedInWeek = nightsBookedInYear / 52

		if price in self.numberWeeklyBookingsPerPrice:
			self.numberWeeklyBookingsPerPrice[price] = self.numberWeeklyBookingsPerPrice[price] + timesBookedInWeek
			self.numberListingsPerPrice[price] = self.numberListingsPerPrice[price] + 1
		else:
			self.numberWeeklyBookingsPerPrice[price] = timesBookedInWeek
			self.numberListingsPerPrice[price] = 1

	def getIDs(self):
		return self.ids
	def getLatitudes(self):
		return self.latitudes
	def getLongitudes(self):
		return self.longitudes
	def getNumberListings(self):
		return self.numberListings
	# returns average price per night of neighbourhood
	def getAveragePPN(self):
		return self.totalCost / self.numberListings
	# returns average review score of neighbourhood
	def getAverageReviewScore(self):
		return self.totalReviewScore / self.numberListings
	def getAverageNumberNightsBookedPerWeek(self):
		return (float(self.totalNightsBooked) / float(self.numberListings)) / 52
	# returns expected income of home in this neighbourhood
	def getAverageWeeklyIncome(self):
		return self.getAveragePPN() * self.getAverageNumberNightsBookedPerWeek()
	# returns ideal PPN to list booking at to maximize revenue
	def getIdealPPN(self):
		returnArray = [0,0,0] # returnArray[0] = best price, returnArray[1] = best revenue
		for price in self.numberWeeklyBookingsPerPrice.keys():
			# threshold so that if there is only one listing for that price point, we don't consider the information as valuable
			if self.numberListingsPerPrice[price] > 1 or self.name == "Presidio":
				weeklyBookings = float(self.numberWeeklyBookingsPerPrice[price]) / float(self.numberListingsPerPrice[price])
				expectedRevenue = price * (weeklyBookings)

				if float(expectedRevenue) > float(returnArray[1]):
					returnArray[0] = price
					returnArray[1] = expectedRevenue
					returnArray[2] = weeklyBookings
				
		return returnArray


class ListingsTracker:
	def __init__(self):
		self.neighbourhoods = {}

		self.readNeighbourhoods()
		self.readListings()

	# creates new neighbourhood classes
	def readNeighbourhoods(self):
		with open('./data/neighbourhoods.csv', newline='', errors='ignore') as neighbourhoodsFile:
			reader = csv.DictReader(neighbourhoodsFile, delimiter=',')
			# read through entries, adding to neighbourhood list and price per neighbourhood dictionary
			for row in reader:
				newNeighbourhood = Neighbourhood(row["neighbourhood"])
				self.neighbourhoods[row["neighbourhood"]] = newNeighbourhood

	# updates neighbourhood data based on all the listings
	def readListings(self):
		neighbourhoodTotalPrices = {}
		neighbourhoodCount = {}
		with open('./data/important-airbnb-data.csv', newline='', errors='ignore') as listingsFile:
			reader = csv.DictReader(listingsFile, delimiter=',')
			for row in reader:
				# get neighbourhood object
				neighbourhood = self.neighbourhoods[row["neighbourhood_cleansed"]]
				newPrice = float(row["price"].replace(',','').replace('$',''))
				neighbourhood.addListing(row["id"],row["latitude"],row["longitude"],newPrice,row["review_scores_rating"], row["availability_365"])					
					
	# returns array of strings
	def getNeighbourhoods(self):
		return sorted(list(self.neighbourhoods.keys()))

	def getIDs(self, neighbourhood):
		return self.neighbourhoods[neighbourhood].getIDs()
	def getLatitudes(self, neighbourhood):
		return self.neighbourhoods[neighbourhood].getLatitudes()
	def getLongitudes(self, neighbourhood):
		return self.neighbourhoods[neighbourhood].getLongitudes()
	def getPPN(self, neighbourhood = None):
		if neighbourhood is None:
			allPPN = {}
			for neighbourhood in self.neighbourhoods:
				allPPN[neighbourhood] = self.neighbourhoods[neighbourhood].getAveragePPN()
			return allPPN
		else:
			return self.neighbourhoods[neighbourhood].getAveragePPN()

	def getBookedNightsPerPrice(self):
		bookedNightsPerPrice = {}
		for price in self.freeNightsPerPrice:
			if price < 600:
				numberListingsPerPrice = len(self.listingsPerPrice[price])
				bookedNightsPerPrice[price] = (178 - float(self.freeNightsPerPrice[price]/numberListingsPerPrice))/26
		return bookedNightsPerPrice

	def getReviewScoresPerNeighbourhood(self):
		reviewScoresPerNeighbourhood = {}
		for neighbourhood in self.neighbourhoods:
			reviewScoresPerNeighbourhood[neighbourhood] = self.neighbourhoods[neighbourhood].getAverageReviewScore()
		return reviewScoresPerNeighbourhood

	def getAverageWeeklyIncome(self, neighbourhood):
		return self.neighbourhoods[neighbourhood].getAverageWeeklyIncome()

	def getAverageBookingsPerWeek(self, neighbourhood):
		return self.neighbourhoods[neighbourhood].getAverageNumberNightsBookedPerWeek()

	def getOptimalPrice(self, neighbourhood):
		return self.neighbourhoods[neighbourhood].getIdealPPN()

	def getNumberListingsPerNeighbourhood(self):
		numberListingsPerNeighbourhood = {}
		for neighbourhood in self.neighbourhoods:
			numberListingsPerNeighbourhood[neighbourhood] = self.neighbourhoods[neighbourhood].getNumberListings()
		return numberListingsPerNeighbourhood


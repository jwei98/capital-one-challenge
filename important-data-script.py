import csv


def main():
	singleEntryDictionary = {}
	fieldnames = ['id', 'latitude', 'longitude', 'price', 'neighbourhood_cleansed', 'review_scores_rating', 'availability_365']

	# write loop
	with open('./data/important-airbnb-data.csv', 'w') as csvfile:

		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()

		# read listings and read relevant info into new file
		with open('./data/listings.csv', newline='', errors='ignore') as listingsFile:
			reader = csv.DictReader(listingsFile, delimiter=',')
			for row in reader:
				if row["id"] and row["latitude"] and row["longitude"] and row["price"] and row["neighbourhood_cleansed"] and row["review_scores_rating"] and row['availability_365']:
					if int(row["availability_365"]) >= 3:
						# put relevant fields into dictionary
						for field in fieldnames:
							singleEntryDictionary[field] = row[field]

						# write row using dictionary
						writer.writerow(singleEntryDictionary)

if __name__ == "__main__":
	main()



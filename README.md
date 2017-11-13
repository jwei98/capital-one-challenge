# capital-one-challenge

Live link: https://my-airbnb-calculator.herokuapp.com/
Github: https://github.com/jwei98/capital-one-challenge


**Meeting the Specs**:
1. Visualization of data- Firstly, I mapped all the Airbnb listings onto a map for the user to have a geographical representation of the data. I also have 4 charts that help visualize interesting metrics, such as the number of listings per neighbourhood, the average price per night of each neighbourhood, the average review score of each neighbourhood (popularity), and the average overall value of each neighbourhood.
2. To estimate the price a homeowner can make, given a latitude and longitude, I first mapped their geolocation to a neighbourhood in SF. Then, calculating the estimated weekly revenue is just equal to (average revenue) * (average weekly bookings)... (see Assumption #1).
3. To suggest an optimal price for the owner, I mapped prices of listings to average number of bookings per week. Then, to get the optimal listing price, I calculated the expected weekly income of each price (price) * (average weekly bookings for that price), found which price yielded the maximum value, and recommended this price. For this part, I eliminated options where there was only 1 listing at a certain price in order to reduce the effect of outliers.


**Assumptions // Thoughts about the data**:
1. For certain calculations, we need to know the average number of bookings in a week for a neighbourhood. The only relevant pieces of data we are given are the number of days available in the future for each listing, as well as the number of reviews. Though neither of these are great indicators of whether the listing is actually booked or not, I make the assumption that the number of bookings in a year for a listing is 365-(number of days available). Justifying the number of days booked for an airbnb by only using the number of days available alonem is problematic/unrealistic, as it does not account for all the reasons why a house might not be available, but it is the best indicator we have.


**Important notes about my web app // Design decisions**:
1. In order to decrease the runtime and space complexity of my web application, I wrote a script (important-data-script.py) to write to a CSV file (important-airbnb-data.csv) that summarized only the necessary data that I used in my application, rather than having to parse the big files every time.
2. I use a ListingsTracker object (which uses Neighbourhood objects) to handle data calculations, and simply call methods from app.py to retrieve the necessary information to display. This separates the view (app.py) from the data analysis/logic. My callback logic, though, had to be handled in app.py.
3. Because the neighbourhood geocoding of geopy does not map exactly onto the neighbourhood names that were provided, I added a feature to my web application that allows the web app to employ user faciliation to identify which neighbourhood a listing is located in, if the web app cannot do it itself.
4. Once the neighbourhood of your listing is identified, the outline of the results in the Calculator section matches the neighbourhood color. Everything is color coded, and it's really cool to be able to see the listings grouped by neighbourhood :)



**References**:
1. Dash
2. Flask
3. Geopy
4. Mapbox


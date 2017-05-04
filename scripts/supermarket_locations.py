# ------------------------------
#    supermarket_locations.py
#
#    Gets the location of all supermarkets in the Flushing directory of Yelp.
#    Plots these locations on a map.
# ------------------------------

import requests
import re
import folium
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster
import time
from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderServiceError

#Generate all the links
numRestaurants = 471
links = []

for i in list(range(0,numRestaurants,10)):
	link = "https://www.yelp.com/search?find_desc=supermarkets&find_loc=Flushing,+Queens,+NY&start=" + str(i)
	links.append(link)

#Scrape for all addresses
addresses = []

for i in links:
	html = requests.get(i).text
	lines = html.split("\n")

	for index,line in enumerate(lines):
		match = re.search(r"<address>", line)
		if match == None:
			pass
		else:
			#address is always on the next line
			address = lines[index+1]
			#some address on the html that is on every single page and it obviously does not belong
			if address == "        14692 Guy R Brewer Blvd<br>Jamaica, NY 11434":
				pass
			else:
				address = address.replace("        ","")
				address = address.replace("<br>", ", ")
				print(address)
				addresses.append(address)

#Map all addresses
coords = []
NoneType = []
geolocator = Nominatim()

for i in addresses:
	try: 
		try:
			location = geolocator.geocode(i)
			if type(location) != type(None):
				coords.append([location.latitude, location.longitude])
				print("Valid count: %d, address: %s"%(len(coords),i))
				time.sleep(1)
			#Improper formatting of addresses cannot be mapped (thanks Yelp)
			else:
				NoneType.append(i)
				print("Invalid count: %d, address: %s"%(len(NoneType),i))
				time.sleep(1)
		except GeocoderTimedOut as e:
			print("Timed out with address %s"%i)
	except GeocoderServiceError as e:
		print("Server bugged with address %s"%i)

mapRestaurants = folium.Map(location=[40.77, -73.83], zoom_start=13, tiles="Cartodb Positron")
mapRestaurants.add_children(MarkerCluster(locations=coords))
mapRestaurants.save(outfile="supermarket_locations.html")




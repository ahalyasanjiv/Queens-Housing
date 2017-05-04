# ------------------------------
#    supermarket_locations.py
#
#    Gets the location of all supermarkets in the Flushing directory of Yelp.
#    Plots these locations on a map.
# ------------------------------

import requests
import re
import folium
from geopy import GoogleV3
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster
import time
from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderServiceError

#Generate all the links
numRestaurants = 60
links = []

for i in list(range(0,numRestaurants,10)):
	link = "https://www.yelp.com/search?find_desc=supermarkets&find_loc=11354,11355,+New+York,+NY&start=" + str(i)
	links.append(link)

#Scrape for all addresses and names of supermarket
addresses = []
names = []

#All supermarkets have a name
#Some supermarkets are located within other supermarkets (i.e. within New World Mall)
#In these specific cases, there is no given address for the supermarket
#In order to keep a 1-to-1 correspondence of names and addresses so we have a proper map, we discard these no address supermarkets
#They are still mapped however, since the host supermarket is still mapped (i.e. New World Mall is still mapped)
haveNameLFaddress = False

for i in links:
	html = requests.get(i).text
	lines = html.split("\n")

	#Used when searching for names
	beginIndex = len("><span >")
	endIndex = len("</span></a>")

	for index,line in enumerate(lines):

		matchName = re.search(r"><span >(.*)/span></a>", line)
		if matchName != None:
			name = str(matchName.group())
			#some name (below) is on the html of every single page, we ignore this
			if name == "><span >NY Convenience Store &amp; Deli</span></a>":
				pass
			else:
				if haveNameLFaddress == False:
					#Take out the front and end tags we searched for
					name = name[beginIndex:len(name)-endIndex]
					#Convert remaining html elements to English
					name = name.replace('<span class="highlighted">', "")
					name = name.replace('</span>', "")
					name = name.replace('&amp;', "&")
					names.append(name)
					haveNameLFaddress = True
					print(name + " -> ", end="")

		matchAddress = re.search(r"<address>", line)	
		if matchAddress != None:
			#address is always on the next line
			address = lines[index+1]
			#some address (below) is on the html of every single page and it obviously does not belong (Jamaica)
			if address == "        14692 Guy R Brewer Blvd<br>Jamaica, NY 11434":
				pass
			else:
				address = address.replace("        ","")
				address = address.replace("<br>", ", ")
				addresses.append(address)
				haveNameLFaddress = False #found address for previous name of supermarket
				print(address)

#Map all addresses
coords = []
NoneType = []
geolocator = GoogleV3() # Nominatim()

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
mapRestaurants.add_children(MarkerCluster(locations=coords, popups=names))
mapRestaurants.save(outfile="supermarket_locations.html")




"""
This program produces a map of the retail food stores in the following 
zip codes: 11368, 11354, 11355. The neighborhoods corresponding to 
these zip codes are Corona, Willets Point, and Flushing.

csv file was from https://data.ny.gov/Economic-Development/Retail-Food-Stores/9a8c-vfzj
"""

import pandas as pd
import folium

# used to get coordinates from address if coordinates are not given
from geopy.geocoders import Nominatim
geolocator = Nominatim()

stores = pd.read_csv('../data/Retail_Food_Stores.csv')
# # display column names and data types
# print(stores.dtypes)

# filter the stores
queensStores = stores[stores['County'] == 'Queens']
storesNearWP = queensStores[(queensStores['Zip Code'] == 11368)
                | (queensStores['Zip Code'] == 11354)
                | (queensStores['Zip Code'] == 11355)]
# print(storesNearWP)

storesMap = folium.Map(location=[40.7599029,-73.843553], zoom_start=13)

for index, row in storesNearWP.iterrows():
    loc = row['Location'].split('\n')
    coord = loc[2].split(', ')
    name = row['DBA Name'] # DBA = 'Doing business as'
    try:
        lat = float(coord[0][1:])
        lon = float(coord[1][:-1])
        storesMap.add_child(folium.Marker(location=[lat,lon],
                            popup=(folium.Popup(name))))
    except:
        try:
            # fix the addresses that are missing a dash between the numbers
            # because Queens addresses are weird like that
            address = loc[0].split(' ')
            num = address[0] + '-' + address[1]
            address[0] = num
            del address[1]
            loc[0] = ' '.join(address)

            # get the coordinates using geopy
            geoloc = geolocator.geocode(loc[0] + ' ' + loc[1])
            if geoloc:
                lat = geoloc.latitude
                lon = geoloc.longitude
                storesMap.add_child(folium.Marker(location=[lat,lon],
                                    popup=(folium.Popup(name))))
        except:
            continue

storesMap.save(outfile='../html/food-stores-near-willets-point.html')
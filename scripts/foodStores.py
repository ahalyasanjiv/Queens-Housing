"""
This program produces a map of the retail food stores in the following 
zip codes: 11368, 11354, 11355. The neighborhoods corresponding to 
these zip codes are Corona, Willets Point, and Flushing.

csv file was from https://data.ny.gov/Economic-Development/Retail-Food-Stores/9a8c-vfzj
"""

import pandas as pd
import folium
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
from geojson import FeatureCollection, Feature, Polygon
from geopy.geocoders import Nominatim
import requests
import re
from geopy.geocoders import GoogleV3
import time
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def filterDist(dist):
    if "PARK" in dist:
        return 0
    elif "R" in dist:
        retVal = ""
        for char in dist:
            if char=='-':
                break
            if char.isdigit():
                retVal+=char
        return int(retVal)
    elif "C" in dist:
        return 0
    else:
        return 0

# initialize lists for voronoi
point_voronoi_list = []
feature_list = []

zones = pd.read_csv('../data/zoneDist.csv')
zones['Residential Densities'] = zones['Zoning Districts'].apply(filterDist)

def main():
    settings = 0
    while(not(1<=settings<=3)):
        settings = int(input("Generate Corona (1), Flushing(2), or both(3)?: "))

        if settings == 1:
            corona()
        elif settings == 2:
            flushing()
        else:
            corona(); flushing()

def corona():
    global zones
    global point_voronoi_list
    global feature_list

    # used to get coordinates from address if coordinates are not given
    geolocator = Nominatim()

    stores = pd.read_csv('../data/Retail_Food_Stores.csv')

    # filter the stores
    queensStores = stores[stores['County'] == 'Queens']
    storesNearCorona = queensStores[(queensStores['Zip Code'] == 11368)]

    storesCoronaMap = folium.Map(location=[40.7599029,-73.843553], zoom_start=13)
    # store coords for voronoi
    coordsCorona = []

    for index, row in storesNearCorona.iterrows():
        loc = row['Location'].split('\n')
        coord = loc[2].split(', ')
        name = row['DBA Name'] # DBA = 'Doing business as'
        try:
            lat = coord[0][1:]
            lon = coord[1][:-1]
            storesCoronaMap.add_child(folium.Marker(location=[lat,lon],
                                popup=(folium.Popup(name))))
            coordsCorona.append([lat,lon])
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
                    storesCoronaMap.add_child(folium.Marker(location=[lat,lon],
                                        popup=(folium.Popup(name))))
                    coordsCorona.append([lat,lon])
            except:
                continue

    vorCorona = Voronoi(coordsCorona)
    coronaJSON = open('coronaVor.json', 'w')
    
    point_voronoi_list.clear()
    feature_list.clear()
    for region in range(len(vorCorona.regions)-1):
        vertex_list = []
        for x in vorCorona.regions[region]:
            # ignore "infinite" point
            if x == -1:
                break
            else:
                # flip order of vertices
                vertex = vorCorona.vertices[x]
                vertex = (vertex[1], vertex[0])
            vertex_list.append(vertex)
        # save vertices as polygon
        polygon = Polygon([vertex_list])
        feature = Feature(geometry=polygon, properties={})
        feature_list.append(feature)

    feature_collection = FeatureCollection(feature_list)
    print(feature_collection, file=coronaJSON)
    coronaJSON.close()

    storesCoronaMap.choropleth(geo_path="../data/zoningIDs.json", fill_color='GnBu', fill_opacity=0.7, line_color='white', line_weight=1, 
        #threshold_scale=[1,2,3,4,5,6,7,8,9,10], 
        data=zones,
        key_on='feature.properties.arbID', 
        columns=['arbID', 'Residential Densities'])

    storesCoronaMap.geo_json(geo_path='coronaVor.json', fill_color = "BuPu", fill_opacity=0.10, line_opacity=1.00)
    storesCoronaMap.save(outfile='../html/voronoi-food-stores-corona.html')


def flushing():
    global zones
    global point_voronoi_list
    global feature_list

    storesFlushingMap = folium.Map(location=[40.7599029,-73.843553], zoom_start=13)

    # store coords for voronoi
    coordsFlushing = []

    #Generate all the links for Flushing restaurants
    numRestaurants = 92
    links = []

    for i in list(range(0,numRestaurants,10)):
        link = "https://www.yelp.com/search?find_desc=supermarkets&find_loc=11354,11355,+New+York,+NY&start=" + str(i)
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

    #Hold NoneTypes
    NoneType = []
    geolocator = GoogleV3() # Nominatim()

    for i in addresses:
        try: 
            try:
                location = geolocator.geocode(i)
                if type(location) != type(None):
                    print("Valid count: %d, address: %s"%(len(coordsFlushing),i))
                    coordsFlushing.append([location.latitude, location.longitude])
                    storesFlushingMap.add_child(folium.Marker(location=[location.latitude, location.longitude],
                                            popup =(folium.Popup("WHEREISVINCENT"))))
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

    vorFlushing = Voronoi(coordsFlushing)
    flushingJSON = open('flushingVor.json', 'w')

    point_voronoi_list.clear()
    feature_list.clear()
    for region in range(len(vorFlushing.regions)-1):
        vertex_list = []
        for x in vorFlushing.regions[region]:
            # ignore "infinite" point
            if x == -1:
                break
            else:
                # flip order of vertices
                vertex = vorFlushing.vertices[x]
                vertex = (vertex[1], vertex[0])
            vertex_list.append(vertex)
        #save vertices as polygon
        polygon = Polygon([vertex_list])
        feature =Feature(geometry=polygon, properties={})
        feature_list.append(feature)

    feature_collection = FeatureCollection(feature_list)
    print(feature_collection, file=flushingJSON)
    flushingJSON.close()

    storesFlushingMap.choropleth(geo_path="../data/zoningIDs.json", fill_color='GnBu', fill_opacity=0.7, line_color='white', line_weight=1,
        #threshold_scale=[1,2,3,4,5,6,7,8,9,10], 
        data=zones,
        key_on='feature.properties.arbID',
        columns=['arbID', 'Residential Densities']) 

    storesFlushingMap.geo_json(geo_path='flushingVor.json', fill_color = "BuPu", fill_opacity=0.10, line_opacity=1.00)
    storesFlushingMap.save(outfile='../html/voronoi-food-stores-flushing.html')



if __name__ == "__main__":
    main()

# PREVIOUS METHOD FOR FLUSHING
# for index, row in storesNearFlushing.iterrows():
#     loc = row['Location'].split('\n')
#     coord = loc[2].split(', ')
#     name = row['DBA Name'] # DBA = 'Doing business as'
#     try:
#         lat = coord[0][1:]
#         lon = coord[1][:-1]
#         storesFlushingMap.add_child(folium.Marker(location=[lat,lon],
#                             popup=(folium.Popup(name))))
#         coordsFlushing.append([lat,lon])
#     except:
#         try:
#             address = row['Street Number'] + ' ' + row['Street Name'] + ' ' + row['Address Line 2'] + ' ' + row['Address Line 3'] + ' ' \
#             + row['City'] + ' ' + row['State'] + ' ' + str(row['Zip Code'])
#             # get the coordinates using geopy
#             geoloc = geolocator.geocode(address)
#             if geoloc:
#                 lat = geoloc.latitude
#                 lon = geoloc.longitude
#                 storesFlushingMap.add_child(folium.Marker(location=[lat,lon],
#                                     popup=(folium.Popup(name))))
#                 coordsFlushing.append([lat,lon])
#         except:
#             continue
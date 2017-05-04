"""
This program maps out the libraries located in Queens. Their markers are green 
if they are active and red if they are closed. The data was last updated in 
September 2014.

csv file was from https://nycopendata.socrata.com/Recreation/Queens-Library-Branches/kh3d-xhq7
"""

import pandas as pd
import folium
from pygeocoder import Geocoder

def isClosed(row):
    return row['Mn'] == row['Tu'] == row['We'] == \
    row['Th'] == row['Fr'] == row['Sa'] == row['Su'] == 'closed'

def fixAddress(address):
    tmp = address.split(' ')
    if (tmp[0].isnumeric() and tmp[1].isnumeric()):
        tmp[0] = tmp[0] + '-' + tmp[1]
    del tmp[1]
    return ' '.join(tmp)

libraries = pd.read_csv('../data/Queens_Library_Branches.csv')
librariesMap = folium.Map(location=[40.7599029,-73.843553], zoom_start=15)

for index, row in libraries.iterrows():
    loc = row['Location 1'].split('\n')
    name = row['name']

    results = Geocoder.geocode(loc[0] + " " + loc[1])
    # print(type(results[0].coordinates))
    coords = results[0].coordinates
    lat = coords[0]
    lon = coords[1]

    closed = isClosed(row)

    if closed:
        color = 'red'
    else:
        color = 'green'

    librariesMap.add_child(folium.Marker(location=[lat, lon],
        popup=(folium.Popup(name)),
        icon=folium.Icon(color=color)))

librariesMap.save(outfile='../html/queens-libraries.html')
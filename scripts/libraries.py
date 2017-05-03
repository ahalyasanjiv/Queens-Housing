"""
This program maps out the libraries located in Queens. Their markers are green 
if they are active and red if they are closed. The data was last updated in 
September 2014.

csv file was from https://nycopendata.socrata.com/Recreation/Queens-Library-Branches/kh3d-xhq7
"""

import pandas as pd
import folium

def isClosed(row):
    return row['Mn'] == row['Tu'] == row['We'] == \
    row['Th'] == row['Fr'] == row['Sa'] == row['Su'] == 'closed'

libraries = pd.read_csv('../data/Queens_Library_Branches.csv')
librariesMap = folium.Map(location=[40.7599029,-73.843553], zoom_start=15)

for index, row in libraries.iterrows():
    loc = row['Location 1'].split('\n')
    coords = loc[2].split(', ')
    lat = float(coords[0][1:])
    lon = float(coords[1][:-1])
    name = row['name']
    closed = isClosed(row)

    if closed:
        color = 'red'
    else:
        color = 'green'

    librariesMap.add_child(folium.Marker(location=[lat, lon],
        popup=(folium.Popup(name)),
        icon=folium.Icon(color=color)))

librariesMap.save(outfile='../html/queens-libraries.html')
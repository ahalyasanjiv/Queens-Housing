"""
This program maps all of the DOE schools and the school districts 
they belong to. The markers are colored to classify schools of certain
types:
- Early Childhood
- District Pre-K Center
- Elementary
- Junior High-Intermediate-Middle
- High school
- K-8
- K-12 all grades
- Secondary School

csv file was from http://schools.nyc.gov/Offices/EnterpriseOperations/DIIT/OOD/default.htm
"""

import pandas as pd
import folium

schools = pd.read_csv('../data/DOE_Schools_Report.csv')
queensSchools = schools[schools['City'] == 'QUEENS']
schoolsMap = folium.Map(location=[40.7599029,-73.843553], zoom_start=15)

for index, row in queensSchools.iterrows():
    lat = row['Latitude']
    lon = row['Longitude']
    name = row['Location Name']
    level = row['Location Category Description']

    if level == 'Early Childhood':
        color = 'pink'
    elif level == 'District Pre-K Center':
        color == 'red'
    elif level == 'Elementary':
        color = 'orange'
    elif level == 'Junior High-Intermediate-Middle':
        color = 'yellow'
    elif level == 'High school':
        color = 'green'
    elif level == 'K-8':
        color = 'blue'
    elif level == 'K-12 all grades':
        color = 'purple'
    elif level == 'Secondary School':
        color = 'darkblue'
    else: # just in case we missed a type of school
        print(level)
        continue

    schoolsMap.add_child(folium.Marker(location=[lat, lon],
        popup=(folium.Popup(name)),
        icon=folium.Icon(color=color)))

schoolsMap.choropleth(geo_path='../data/2014-2015_School_Zones.geojson',
                    fill_color='grey', fill_opacity=0.15, line_opacity=0.3)

schoolsMap.save(outfile='../html/nyc-schools.html')

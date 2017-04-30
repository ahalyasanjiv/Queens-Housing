"""
This program prints out the top 10 311 complaints in three neighborhoods:
- Willets Point, Queens
- Corona, Queens
- Flushing, Queens

csv file was from https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9/data
Filtered by 'Incident Zip' for 11368, 11354, and 11355
"""

import pandas as pd
import folium
from folium.plugins import MarkerCluster
import math

complaints = pd.read_csv('../data/311_Service_Requests_from_2010_to_Present.csv', low_memory=False)
# # display column names and data types
# print(complaints.dtypes)

# filter complaints by location
wpComplaints = complaints[(complaints['Incident Zip'] == 11368)
                        & (complaints['Latitude'] >= 40.754474)
                        & (complaints['Longitude'] >= -73.845720)]
coronaComplaints = complaints[(complaints['Incident Zip'] == 11368)
                    & (complaints['Longitude'] <= -73.8551671)]
flushingComplaints = complaints[(complaints['Incident Zip'] == 11354)
                    | (complaints['Incident Zip'] == 11355)]

# print top 10 complaints for each location
wpComplaintTypes = wpComplaints['Complaint Type'].value_counts()
print("Willets Point Top Complaints")
for i in range(10):
    print(wpComplaintTypes.keys()[i], wpComplaintTypes.get(i))

print()

coronaComplaintTypes = coronaComplaints['Complaint Type'].value_counts()
print("Corona Top Complaints")
for i in range(10):
    print(coronaComplaintTypes.keys()[i], coronaComplaintTypes.get(i))

print()

flushingComplaintTypes = flushingComplaints['Complaint Type'].value_counts()
print("Flushing Top Complaints")
for i in range(10):
    print(flushingComplaintTypes.keys()[i], flushingComplaintTypes.get(i))

# ~~~~~~~~~~~~~ RESULTS ~~~~~~~~~~~~~
# Willets Point Top Complaints
# Street Condition 636
# Street Light Condition 574
# Noise - Street/Sidewalk 242
# Water System 232
# Derelict Vehicles 211
# Traffic Signal Condition 174
# Highway Condition 122
# Sewer 110
# Illegal Parking 108
# Sanitation Condition 85

# Corona Top Complaints
# Blocked Driveway 14443
# Noise - Residential 10427
# Water System 4913
# HEAT/HOT WATER 4535
# HEATING 3924
# Illegal Parking 3168
# PLUMBING 2867
# Street Light Condition 2749
# Dirty Conditions 2669
# Street Condition 2596

# Flushing Top Complaints
# Blocked Driveway 13675
# Street Condition 10709
# Noise - Residential 8989
# Street Light Condition 6904
# HEAT/HOT WATER 6413
# HEATING 6241
# Illegal Parking 6209
# Building/Use 5674
# Broken Muni Meter 5582
# Water System 4117
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# making map for Willets Point
wpMap = folium.Map(location=[40.7599029,-73.843553], zoom_start=16)
# take a random sample of 1000 complaints
wpComplaints1000 = wpComplaints.sample(n=1000)

for index, row in wpComplaints1000.iterrows():
    lat = row['Latitude']
    lon = row['Longitude']
    name = row['Complaint Type']

    if name == 'Street Condition':
        color = 'darkred'
    elif name == 'Street Light Condition':
        color = 'red'
    elif name == 'Noise - Street/Sidewalk':
        color='lightred'
    elif name == 'Water System':
        color = 'orange'
    elif name == 'Derelict Vehicles':
        color = 'darkblue'
    elif name == 'Traffic Signal Condition':
        color = 'blue'
    elif name == 'Highway Condition':
        color = 'lightblue'
    elif name == 'Sewer':
        color = 'darkpurple'
    elif name == 'Illegal Parking':
        color = 'purple'
    elif name == 'Sanitation Condition':
        color = 'pink'
    else:
        continue

    wpMap.add_child(folium.Marker(location=[lat,lon],
        popup=(folium.Popup(name)),
        icon=folium.Icon(color=color)))

wpMap.save(outfile='../html/willets-point-311-calls.html')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# making map for Corona
coronaMap = folium.Map(location=[40.7471803,-73.8662563], zoom_start=15)
coronaComplaints1000 = coronaComplaints.sample(n=1000)

for index, row in coronaComplaints1000.iterrows():
    lat = row['Latitude']
    lon = row['Longitude']
    name = row['Complaint Type']

    if name == 'Blocked Driveway':
        color = 'darkred'
    elif name == 'Noise - Residential':
        color = 'red'
    elif name == 'Water System':
        color='lightred'
    elif name == 'HEAT/HOT WATER':
        color = 'orange'
    elif name == 'HEATING':
        color = 'darkblue'
    elif name == 'Illegal Parking':
        color = 'blue'
    elif name == 'PLUMBING':
        color = 'lightblue'
    elif name == 'Street Light Condition':
        color = 'darkpurple'
    elif name == 'Dirty Conditions':
        color = 'purple'
    elif name == 'Street Condition':
        color = 'pink'
    else:
        continue

    coronaMap.add_child(folium.Marker(location=[lat,lon],
        popup=(folium.Popup(name)),
        icon=folium.Icon(color=color)))

coronaMap.save(outfile='../html/corona-311-calls.html')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# making map for Flushing
flushingMap = folium.Map(location=[40.7609728,-73.8371958], zoom_start=14)
flushingComplaints1000 = flushingComplaints.sample(n=1000)

for index, row in flushingComplaints1000.iterrows():
    if (not math.isnan(row['Latitude'])):
        lat = row['Latitude']
        lon = row['Longitude']
        name = row['Complaint Type']

        if name == 'Blocked Driveway':
            color = 'darkred'
        elif name == 'Street Condition':
            color = 'red'
        elif name == 'Noise - Residential':
            color='lightred'
        elif name == 'Street Light Condition':
            color = 'orange'
        elif name == 'HEAT/HOT WATER':
            color = 'darkblue'
        elif name == 'HEATING':
            color = 'blue'
        elif name == 'Illegal Parking':
            color = 'lightblue'
        elif name == 'Building/Use':
            color = 'darkpurple'
        elif name == 'Broken Muni Meter':
            color = 'purple'
        elif name == 'Water System':
            color = 'pink'
        else:
            continue

        flushingMap.add_child(folium.Marker(location=[lat,lon],
            popup=(folium.Popup(name)),
            icon=folium.Icon(color=color)))
    else:
        # add another row to make up for the one that lacks coordinate info
        # make sure the new row is not already in the sample
        otherFlushingComplaints = flushingComplaints.loc[~flushingComplaints.index.isin(flushingComplaints1000.index)]
        randomRow = otherFlushingComplaints.sample(n=1)
        flushingComplaints1000 = flushingComplaints1000.append(randomRow)

flushingMap.save(outfile='../html/flushing-311-calls.html')
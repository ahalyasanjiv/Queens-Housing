import pandas as pd

complaints = pd.read_csv('../data/311_Service_Requests_from_2010_to_Present.csv', low_memory=False)

# # display column names and data types
# print(complaints.dtypes)

# filter complaints by location
willetsPointComplaints = complaints[(complaints['Incident Zip'] == 11368)
                        & (complaints['Latitude'] >= 40.754474)
                        & (complaints['Longitude'] >= -73.845720)]
coronaComplaints = complaints[(complaints['Incident Zip'] == 11368)
                    & (complaints['Longitude'] <= -73.8551671)]
flushingComplaints = complaints[(complaints['Incident Zip'] == 11354)
                    | (complaints['Incident Zip'] == 11355)]

# print top 10 complaints for each location
wpComplaintTypes = willetsPointComplaints['Complaint Type'].value_counts()
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

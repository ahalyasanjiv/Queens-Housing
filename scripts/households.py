"""
households.py
This program makes choropleth maps of amount of households and household median income by
owners and renters for 2010 Census Tracts in the following neighborhoods:
- Willets Point
- Flushing, East Flushing, College Point, Murray Hill
- Corona, North Corona

Note that the median income of each Census Tract is the average of the median incomes
of the Census Blocks in the Census Tract.

Census Tracts by Neighborhoods (nyc2010census_tabulation_equiv.csv)
https://www1.nyc.gov/site/planning/data-maps/open-data/dwn-nynta.page

Census Block + Tract Equivalencies 
https://www2.census.gov/geo/maps/dc10map/GUBlock/st36_ny/county/c36081_queens/DC10BLK_C36081_BLK2MS.txt

Data - Location_Affordability_Index_v_2.0 (from US Department of Housing and Urban Development):
https://egis-hud.opendata.arcgis.com/datasets/7dc10bc22f204e03bd0bebe257b5986d_0
***NOTE: the CSV used will be filtered from the larger data set

GEOjson (Census Tracts 2010 (Clipped to Shoreline)):
http://www1.nyc.gov/site/planning/data-maps/open-data/districts-download-metadata.page
"""

import folium
import pandas as pd 

# ===== Filter data by State 36 (NY) and County 81 (Queens) ======
# allData = pd.read_csv("../data/Location_Affordability_Index_v_2.0.csv")
# filteredData = pd.DataFrame()
# filteredData = allData[(allData["BlockGroups_STATEFP10"]==36)
# 						& (allData["BlockGroups_COUNTYFP10"]==81)]
# filteredData.to_csv('../data/LAIFiltered.csv')

# ===== Get census tracts by neighborhood ======
neighborhoods = pd.read_csv("../data/nyc2010census_tabulation_equiv.csv", skiprows=4)
censusTracts = neighborhoods[(neighborhoods["Name"] == "Flushing")
				| (neighborhoods["Name"] == "East Flushing")
				| (neighborhoods["Name"] == "College Point")
				| (neighborhoods["Name"] == "Murray Hill")
				| (neighborhoods["Name"] == "Corona")
				| (neighborhoods["Name"] == "North Corona")]

# choropleth needs the missing census tracts to work properly -_-
otherTracts = neighborhoods[(neighborhoods["Name"] != "Flushing")
				& (neighborhoods["Name"] != "East Flushing")
				& (neighborhoods["Name"] != "College Point")
				& (neighborhoods["Name"] != "Murray Hill")
				& (neighborhoods["Name"] != "Corona")
				& (neighborhoods["Name"] != "North Corona")]

# eastFlushing = neighborhoods[neighborhoods["Name"] == "East Flushing"]
# collegePoint = neighborhoods[neighborhoods["Name"] == "College Point"]
# murrayHill = neighborhoods[neighborhoods["Name"] == "Murray Hill"]

# corona = neighborhoods[neighborhoods["Name"] == "Corona"]
# northCorona = neighborhoods[neighborhoods["Name"] == "North Corona"]

# print(censusTracts["Unnamed: 3"])

# ===== Get household median incomes and amount of households ======
# dataframe to store all the information
data = pd.DataFrame(columns = ['Census Tract', 'Number of Households',
								'Median Income for Owners',
								'Median Income for Renters']) 

lai = pd.read_csv("../data/LAIFiltered.csv")

for index, row in censusTracts.iterrows():
	tract = row["Unnamed: 3"]
	laiTract = lai[lai["BlockGroups_TRACTCE10"]==tract] #select the data by tract
	
	numberHouseholds = laiTract["households"].sum()
	# average the incomes of each census block
	ownerIncome = laiTract["blkgrp_median_income_owners"].mean()
	renterIncome = laiTract["blkgrp_median_income_renters"].mean()

	data.loc[len(data)] = [tract, numberHouseholds, ownerIncome, renterIncome]

# ===== Make choropleth map for number of households ======
#function used to format census tract to match json file
def toStr(GEO_ID):
	num = str(GEO_ID)
	num = num[:-2]
	while len(num) < 6:
		num = "0" + num
	return "4"+ num

data["Boro Census Tract"] = data["Census Tract"].apply(toStr)

#need to fill in out other census tracts to make choropleth happy
for index, row in otherTracts.iterrows():
	num = str(row["Unnamed: 3"])
	while len(num) < 6:
		num = "0" + num
	tract = str(row["Unnamed: 2"]) + num
	data.loc[len(data)] = [row["Unnamed: 3"], 0, 0, 0, tract]

houseMap = folium.Map(location=[40.7609728,-73.8371958], zoom_start=13, tiles ='Cartodb Positron')

houseMap.choropleth(geo_path="../data/censusTract2010.json",
					data = data,
					columns = ["Boro Census Tract", "Number of Households"],
					key_on = "feature.properties.BoroCT2010",
					threshold_scale=[0,400,900,1300,1800,2300],
					fill_color="RdPu", fill_opacity=0.7, line_opacity=0.3)

houseMap.save(outfile='../html/houseMap.html')

# ===== Make choropleth map for owner median income ======
ownerIncomeMap = folium.Map(location=[40.7609728,-73.8371958], zoom_start=13, tiles ='Cartodb Positron')
ownerIncomeMap.choropleth(geo_path="../data/censusTract2010.json",
					data = data,
					columns = ["Boro Census Tract", "Median Income for Owners"],
					key_on = "feature.properties.BoroCT2010",
					threshold_scale=[0,20000,40000,60000,80000,130000],
					fill_color="GnBu", fill_opacity=0.7, line_opacity=0.3)

ownerIncomeMap.save(outfile='../html/ownerIncomeMap.html')

# ===== Make choropleth map for renter median income ======
renterIncomeMap = folium.Map(location=[40.7609728,-73.8371958], zoom_start=13, tiles ='Cartodb Positron')
renterIncomeMap.choropleth(geo_path="../data/censusTract2010.json",
					data = data,
					columns = ["Boro Census Tract", "Median Income for Renters"],
					key_on = "feature.properties.BoroCT2010",
					threshold_scale=[0,20000,40000,60000,80000,130000],
					fill_color="YlGn", fill_opacity=0.7, line_opacity=0.3)

renterIncomeMap.save(outfile='../html/renterIncomeMap.html')

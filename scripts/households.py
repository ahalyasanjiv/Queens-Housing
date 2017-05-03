"""
households.py
This program makes choropleth maps of amount of households and household median income 
by 2010 Census Tracts in the following neighborhoods:
- Flushing, East Flushing, College Point, Murray Hill
- Corona, North Corona

State: 36
County: 81

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
flushing = neighborhoods[neighborhoods["Name"] == "Flushing"]
eastFlushing = neighborhoods[neighborhoods["Name"] == "East Flushing"]
collegePoint = neighborhoods[neighborhoods["Name"] == "College Point"]
murrayHill = neighborhoods[neighborhoods["Name"] == "Murray Hill"]

corona = neighborhoods[neighborhoods["Name"] == "Corona"]
northCorona = neighborhoods[neighborhoods["Name"] == "North Corona"]

# print(flushing["Unnamed: 3"])

# ===== Get household median income and amount of households ======
data = pd.Dataframe() # dataframe to store all the information
lai = pd.read_csv("../data/LAIFiltered.csv")










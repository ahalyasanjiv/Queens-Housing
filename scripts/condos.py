"""
csv files were from https://data.ny.gov/browse?q=DOF%3A%20Condominium%20Comparable%20Rental%20Income%20queens&sortBy=relevance
"""

import pandas as pd

condo1 = pd.read_csv('../data/DOF__Condominium_Comparable_Rental_Income___Queens___FY_2008_2009.csv')
condo2 = pd.read_csv('../data/DOF__Condominium_Comparable_Rental_Income___Queens___FY_2009_2010.csv')
condo3 = pd.read_csv('../data/DOF__Condominium_comparable_rental_income___Queens_-_FY_2010_2011.csv')
condo4 = pd.read_csv('../data/DOF__Condominium_Comparable_Rental_Income___Queens___FY_2011_2012.csv')

# concatenate the dataframes for the three fiscal years
frames = [condo1, condo2, condo3, condo4]
condo = pd.concat(frames)
print(condo.dtypes)

condosNearWP = condo[(condo['COMPARABLE RENTAL 1  Neighborhood'] == 'CORONA')
            | (condo['COMPARABLE RENTAL 1  Neighborhood'] == 'FLUSHING-NORTH')
            | (condo['COMPARABLE RENTAL 1  Neighborhood'] == 'FLUSHING-SOUTH')]

# print(condosNearWP)

# for index, row in condo[:1].iterrows():
#     print(row)
import folium

willetsPointMap = folium.Map(location=[40.7609728,-73.8371958], zoom_start=13)
willetsPointMap.choropleth(geo_path="../data/willetsPoint.json")
willetsPointMap.save(outfile='../html/willetsPointMap.html')
import geopandas as gpd

# Leer el archivo shapefile
shapefile_path = "C:/Users/Diego/Desktop/Valencia_crime_hull.shp"
gdf = gpd.read_file(shapefile_path)

# Mostrar los primeros registros
print(gdf.head())

import matplotlib.pyplot as plt

# Plotear el shapefile
gdf.plot()
plt.title("Mapa de la región espacial")
plt.show()

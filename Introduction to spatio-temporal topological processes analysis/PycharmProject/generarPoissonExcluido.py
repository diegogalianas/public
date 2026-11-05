import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Leer el archivo shapefile
shapefile_path = "C:/Users/Diego/Desktop/Valencia_crime_hull.shp"
gdf = gpd.read_file(shapefile_path)

# Obtener los límites del shapefile
minx, miny, maxx, maxy = gdf.total_bounds

# Generar puntos aleatorios usando un proceso de Poisson
num_points = 95  # Número de puntos a generar
points = []

while len(points) < num_points:
    point = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
    if gdf.contains(point).any():
        points.append(point)

# Crear un GeoDataFrame con los puntos generados
points_gdf = gpd.GeoDataFrame(geometry=points, crs=gdf.crs)

# Plotear el shapefile y los puntos generados
fig, ax = plt.subplots()
gdf.plot(ax=ax, color='white', edgecolor='black')
points_gdf.plot(ax=ax, color='red', markersize=5)
plt.show()

# Convertir el GeoDataFrame a DataFrame para guardar en CSV
points_df = pd.DataFrame(points_gdf.geometry.apply(lambda p: (p.x, p.y)).tolist(), columns=['crime_lon', 'crime_lat'])

# Guardar los puntos generados en un archivo CSV
points_df.to_csv('Random_1_AlarmasMujer2018-2019.csv', index=False)

print("Los puntos generados se han guardado en 'Random_2_AlarmasMujer2018-2019.csv'.")

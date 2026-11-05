import pandas as pd

# Cargar el dataset
file_path = "Valencia.csv"
data = pd.read_csv(file_path)

# Columnas de distancias que quieres analizar
columns_of_interest = ['atm_dist', 'bank_dist', 'bar_dist', 'cafe_dist', 'industrial_dist',
                       'market_dist', 'nightclub_dist', 'police_dist', 'pub_dist',
                       'restaurant_dist', 'taxi_dist']

# Obtener los valores mínimos y máximos en general
min_value = data[columns_of_interest].min().min()
max_value = data[columns_of_interest].max().max()

print(f"Distancia mínima en general: {min_value}")
print(f"Distancia máxima en general: {max_value}")

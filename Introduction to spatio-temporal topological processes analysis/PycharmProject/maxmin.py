import pandas as pd

# Cargar el dataset
df = pd.read_csv('Valencia.csv')

# Obtener los valores mínimos y máximos de las columnas 'crime_lon' y 'crime_lat'
min_lon = df['crime_lon'].min()
max_lon = df['crime_lon'].max()
min_lat = df['crime_lat'].min()
max_lat = df['crime_lat'].max()

# Imprimir los resultados
print(f"Min 'crime_lon': {min_lon}")
print(f"Max 'crime_lon': {max_lon}")
print(f"Min 'crime_lat': {min_lat}")
print(f"Max 'crime_lat': {max_lat}")

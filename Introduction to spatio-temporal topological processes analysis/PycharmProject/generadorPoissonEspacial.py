import numpy as np
import pandas as pd
np.random.seed(42)
# Definir los valores mínimos y máximos
min_lon = -0.429603785
max_lon = -0.320845962
min_lat = 39.41541672
max_lat = 39.53095627

# Parámetros
n = 95
m = 2

# Generar m archivos CSV
for i in range(1, m + 1):
    # Generar coordenadas aleatorias entre los valores mínimos y máximos
    crime_lon = np.random.uniform(min_lon, max_lon, n)
    crime_lat = np.random.uniform(min_lat, max_lat, n)

    # Crear un dataframe con los datos generados
    df = pd.DataFrame({
        'crime_lon': crime_lon,
        'crime_lat': crime_lat
    })

    # Nombre del archivo CSV (con índice i para diferenciarlos)
    filename = f'Random_{i}_AlarmasMujer2018-2019.csv'

    # Guardar el dataframe en un archivo CSV
    df.to_csv(filename, index=False)

    print(f"Archivo {filename} generado con {n} entradas.")

print(f"{m} archivos CSV generados.")

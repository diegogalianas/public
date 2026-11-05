import pandas as pd
archivo = 'Valencia_2015_AlarmasMujer.csv'

df = pd.read_csv(archivo)  # Leer el archivo CSV
num_rows = len(df)  # Contar el número de filas
# Extraer el año del nombre del archivo

print(f'{archivo}: {num_rows} entradas')  # Imprimir el número de filas
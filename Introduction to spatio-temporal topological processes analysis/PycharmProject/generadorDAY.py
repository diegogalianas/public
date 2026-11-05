import pandas as pd

# Cargar el dataset CSV
df = pd.read_csv('Valencia_2019_AlarmasMujer.csv')

# Eliminar filas duplicadas basadas en 'crime_lon', 'crime_lat' y 'day'
df_unique = df.drop_duplicates(subset=['crime_lon', 'crime_lat', 'day'])

# Ordenar por la columna 'day' de menor a mayor
df_unique_sorted = df_unique.sort_values(by='day')

# Guardar el resultado en un nuevo archivo CSV si lo deseas
df_unique_sorted.to_csv('Valencia_2019_AlarmasMujer_DAY_sorted.csv', index=False)
df_top_94 = df_unique_sorted.head(93)

# Si prefieres usar iloc:
# df_top_94 = df_unique_sorted.iloc[:94]

# Guardar el resultado en un nuevo archivo CSV si lo deseas
df_top_94.to_csv('Valencia_2019_AlarmasMujer_DAY_sorted.csv', index=False)
# Mostrar las primeras filas para comprobar el resultado
print(df_unique_sorted.head())

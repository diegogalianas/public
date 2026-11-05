import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv('Valencia_2015.csv')

# Eliminar filas duplicadas basadas en las columnas 'utm_x', 'utm_y', y 'day'
df_unique = df.drop_duplicates(subset=['utm_x', 'utm_y', 'day'])

# Guardar el nuevo dataframe con las tuplas únicas en un nuevo archivo CSV
df_unique.to_csv('Valencia_2015_DAY.csv', index=False)

print("Se ha generado un nuevo archivo CSV con las tuplas únicas.")

import pandas as pd

# Leer el archivo CSV
file_path = 'Valencia.csv'
df = pd.read_csv(file_path)

# Convertir la columna 'crime_date' a formato de fecha
df['crime_date'] = pd.to_datetime(df['crime_date'])

# Filtrar los datos para que contenga solo las fechas entre el 1 de marzo y el 19 de marzo
df_filtered = df[(df['crime_date'].dt.month == 3) & (df['crime_date'].dt.day >= 1) & (df['crime_date'].dt.day <= 19)]

# Filtrar los datos para que contenga solo los años entre 2010 y 2019
df_filtered = df_filtered[(df_filtered['year'] >= 2010) & (df_filtered['year'] <= 2019)]

# Guardar los datos filtrados en un único archivo CSV
output_file = 'Valencia_Fallas.csv'
df_filtered.to_csv(output_file, index=False)
print(f'Archivo {output_file} guardado correctamente.')

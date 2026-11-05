import pandas as pd

# Leer el archivo CSV
file_path = 'Valencia.csv'
df = pd.read_csv(file_path)

# Filtrar los datos para que contenga solo los años entre 2010 y 2020
df_filtered = df[(df['year'] >= 2010) & (df['year'] <= 2020)]

# Crear un archivo CSV separado por cada año
for year in range(2010, 2021):
    df_year = df_filtered[df_filtered['year'] == year]
    output_file = f'Valencia_{year}.csv'
    df_year.to_csv(output_file, index=False)
    print(f'Archivo {output_file} guardado correctamente.')

import pandas as pd

# Leer el archivo CSV
file_path = 'Valencia.csv'
df = pd.read_csv(file_path)

# Mostrar el número total de filas en el archivo original
total_rows = len(df)
print(f'Total de entradas en Valencia.csv: {total_rows} entradas')

# Filtrar los datos para que contenga solo los años entre 2010 y 2020
df_filtered = df[(df['year'] >= 2010) & (df['year'] <= 2020)]

# Crear un archivo CSV separado por cada año y contar las filas
for year in range(2010, 2021):
    df_year = df_filtered[df_filtered['year'] == year]
    num_rows = len(df_year)
    output_file = f'Valencia_{year}.csv'
    df_year.to_csv(output_file, index=False)

    # Mostrar el número de filas para cada año
    print(f'Año {year}: {num_rows} entradas')

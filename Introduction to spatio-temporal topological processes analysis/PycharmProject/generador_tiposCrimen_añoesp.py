import pandas as pd

# Definir los tipos de crímenes
crime_types = ['Agresion', 'Sustraccion', 'AlarmasMujer', 'Otros']

# Iterar por cada año del 2010 al 2020
for month in range(1, 13):
    # Leer el CSV correspondiente a cada año
    file_path = f'Valencia_2015_Month_{month}.csv'
    df_year = pd.read_csv(file_path)

    # Para cada tipo de crimen, crear un CSV separado
    for crime_type in crime_types:
        df_crime = df_year[df_year['crime_type'] == crime_type]

        # Crear el nombre del archivo en base al año y el tipo de crimen
        output_file = f'Valencia_2015_Month_{month}_{crime_type}.csv'
        df_crime.to_csv(output_file, index=False)

        # Mostrar el número de filas para cada tipo de crimen por año
        num_rows = len(df_crime)
        print(f'Mes {month}, Tipo de Crimen: {crime_type}, Entradas: {num_rows}')

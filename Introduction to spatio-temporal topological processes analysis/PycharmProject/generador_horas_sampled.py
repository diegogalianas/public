import pandas as pd

df_2015 = pd.read_csv('Valencia.csv')

# Iterar sobre las 24 horas (0 a 23)
for hour in range(0, 24):
    # Filtrar las filas de la hora correspondiente
    df_hour = df_2015[df_2015['crime_hour'] == hour]

    # Crear el nombre del archivo CSV para cada hora
    output_file = f'Valencia_Hour_{hour}.csv'

    # Guardar las filas correspondientes a esa hora en un archivo CSV
    df_hour.to_csv(output_file, index=False)

    # Imprimir el número de filas para cada hora
    num_rows = len(df_hour)
    print(f'Hora {hour}: {num_rows} entradas')

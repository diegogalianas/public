import pandas as pd

df_2015 = pd.read_csv('Valencia.csv')

# Iterar sobre los 12 meses (1 a 12)
for month in range(1, 13):
    # Filtrar las filas del mes correspondiente
    df_month = df_2015[df_2015['month'] == month]

    # Crear el nombre del archivo CSV para cada mes
    output_file = f'Valencia_Month_{month}.csv'

    # Guardar las filas correspondientes a ese mes en un archivo CSV
    df_month.to_csv(output_file, index=False)

    # Imprimir el número de filas para cada mes
    num_rows = len(df_month)
    print(f'Mes {month}: {num_rows} entradas')

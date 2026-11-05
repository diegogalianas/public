import pandas as pd

# Cargar el archivo CSV original
df_2015 = pd.read_csv('Valencia_2018_AlarmasMujer.csv')

# Obtener la lista única de nombres de días de la semana
week_days = df_2015['week_day_name'].unique()

# Iterar sobre cada día de la semana
for day in week_days:
    # Filtrar las filas del día correspondiente
    df_day = df_2015[df_2015['week_day_name'] == day]

    # Crear el nombre del archivo CSV para cada día de la semana
    output_file = f'Valencia_Otros_{day}.csv'

    # Guardar las filas correspondientes a ese día en un archivo CSV
    df_day.to_csv(output_file, index=False)

    # Imprimir el número de filas para cada día
    num_rows = len(df_day)
    print(f'Día {day}: {num_rows} entradas')

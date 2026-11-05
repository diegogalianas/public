import pandas as pd

# Cargar el archivo CSV original
df_2015 = pd.read_csv('Valencia_2015.csv')

# Definir los días de entre semana y fin de semana
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday']
weekend = ['Friday', 'Saturday', 'Sunday']

# Filtrar las filas correspondientes a los días de entre semana
df_weekdays = df_2015[df_2015['week_day_name'].isin(weekdays)]

# Filtrar las filas correspondientes a los días de fin de semana
df_weekend = df_2015[df_2015['week_day_name'].isin(weekend)]

# Guardar los datasets en archivos CSV separados
df_weekdays.to_csv('Valencia_2015_EntreSemana.csv', index=False)
df_weekend.to_csv('Valencia_2015_FinDeSemana.csv', index=False)

# Imprimir el número de filas en cada dataset
print(f'Entre semana: {len(df_weekdays)} entradas')
print(f'Fin de semana: {len(df_weekend)} entradas')

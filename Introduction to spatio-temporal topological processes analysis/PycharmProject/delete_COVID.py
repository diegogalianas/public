import pandas as pd

# Definir la fecha límite: 1 de marzo de 2020
fecha_limite = '2020-03-01'

# Archivos correspondientes al año 2020
archivos_2020 = [
    'Valencia_2020.csv',
    'Valencia_2020_Agresion.csv',
    'Valencia_2020_Sustraccion.csv',
    'Valencia_2020_AlarmasMujer.csv',
    'Valencia_2020_Otros.csv'
]

# Iterar por cada archivo del año 2020
for archivo in archivos_2020:
    # Leer el archivo
    df = pd.read_csv(archivo)

    # Filtrar las filas cuya fecha sea anterior al 1 de marzo de 2020
    df['crime_date'] = pd.to_datetime(df['crime_date'])  # Convertir la columna de fecha a datetime
    df_filtered = df[df['crime_date'] < fecha_limite]  # Filtrar las fechas anteriores al 1 de marzo

    # Guardar el archivo filtrado
    df_filtered.to_csv(archivo, index=False)

    # Mostrar cuántas entradas quedaron después del filtro
    num_rows = len(df_filtered)
    print(f'Archivo {archivo}: {num_rows} entradas después del filtro')

import pandas as pd

# Definir la lista de meses y la ruta base de los archivos
months = range(0, 24)
base_filename = 'Valencia_Hour_'

# Número objetivo de entradas
num_entries = 1745

# Procesar cada mes
for month in months:
    # Cargar el CSV del mes
    file_path = f'{base_filename}{month}.csv'
    df = pd.read_csv(file_path)

    # Seleccionar las primeras 52 entradas
    sampled_df = df.head(num_entries)

    # Guardar el nuevo CSV
    sampled_file_path = f'{base_filename}{month}_sampled.csv'
    sampled_df.to_csv(sampled_file_path, index=False)

    # Imprimir el número de entradas del nuevo CSV
    print(f'Archivo {sampled_file_path} creado con {len(sampled_df)} entradas.')


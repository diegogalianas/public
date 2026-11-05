import pandas as pd

# Definir la lista de meses y la ruta base de los archivos
months = range(1, 13)
base_filename = 'Valencia_2015_Month_'

# Número objetivo de entradas
num_entries = 526

# Procesar cada mes
for month in months:
    # Cargar el CSV del mes
    file_path = f'{base_filename}{month}.csv'
    df = pd.read_csv(file_path)

    # Muestrear aleatoriamente 526 entradas
    sampled_df = df.sample(n=num_entries, random_state=1)  # Usar el mismo random_state para reproducibilidad

    # Guardar el nuevo CSV
    sampled_file_path = f'{base_filename}{month}_sampled.csv'
    sampled_df.to_csv(sampled_file_path, index=False)

    # Imprimir el número de entradas del nuevo CSV
    print(f'Archivo {sampled_file_path} creado con {len(sampled_df)} entradas.')
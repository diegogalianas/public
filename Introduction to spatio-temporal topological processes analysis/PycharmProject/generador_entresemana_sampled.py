import pandas as pd

# Definir la lista de meses y la ruta base de los archivos

file_path = ['Valencia_2015_EntreSemana', 'Valencia_2015_FinDeSemana']

# Número objetivo de entradas
num_entries = 3794

# Procesar cada mes
for file in file_path:
    # Cargar el CSV del mes
    df = pd.read_csv(f'{file}.csv')

    sampled_df = df.head(num_entries)

    # Guardar el nuevo CSV
    sampled_file_path = f'{file}_sampled.csv'
    sampled_df.to_csv(sampled_file_path, index=False)

    # Imprimir el número de entradas del nuevo CSV
    print(f'Archivo {sampled_file_path} creado con {len(sampled_df)} entradas.')
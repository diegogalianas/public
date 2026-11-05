import pandas as pd

# Definir la lista de años y la ruta base de los archivos
years = range(2010, 2020)
base_filename = 'Valencia_'

# Número objetivo de entradas
num_entries = 3749

# Procesar cada año
for year in years:
    # Cargar el CSV del año
    file_path = f'{base_filename}{year}_Agresion.csv'
    df = pd.read_csv(file_path)

    # Seleccionar las primeras 7538 entradas
    sampled_df = df.head(num_entries)

    # Guardar el nuevo CSV
    sampled_file_path = f'{base_filename}{year}_Agresion_sampled.csv'
    sampled_df.to_csv(sampled_file_path, index=False)

    # Imprimir el número de entradas del nuevo CSV
    print(f'Archivo {sampled_file_path} creado con {len(sampled_df)} entradas.')

import pandas as pd

base_filename = 'Valencia_Otros_'
df_2015 = pd.read_csv('Valencia.csv')

# Obtener la lista única de nombres de días de la semana
week_days = df_2015['week_day_name'].unique()

# Número objetivo de entradas
num_entries = 1028

# Procesar cada mes
for day in week_days:
    # Cargar el CSV del mes
    file_path = f'{base_filename}{day}.csv'
    df = pd.read_csv(file_path)

    # Muestrear aleatoriamente 526 entradas
    sampled_df = df.head(num_entries)

    # Guardar el nuevo CSV
    sampled_file_path = f'{base_filename}{day}_sampled.csv'
    sampled_df.to_csv(sampled_file_path, index=False)

    # Imprimir el número de entradas del nuevo CSV
    print(f'Archivo {sampled_file_path} creado con {len(sampled_df)} entradas.')
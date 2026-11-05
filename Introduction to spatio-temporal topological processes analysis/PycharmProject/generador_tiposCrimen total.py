import pandas as pd

# Definir los tipos de crímenes
crime_types = ['Agresion', 'Sustraccion', 'AlarmasMujer', 'Otros']


file_path = f'Valencia.csv'
df_year = pd.read_csv(file_path)

for crime_type in crime_types:
    df_crime = df_year[df_year['crime_type'] == crime_type]
    # Crear el nombre del archivo en base al año y el tipo de crimen
    output_file = f'Valencia_{crime_type}.csv'
    df_crime.to_csv(output_file, index=False)
    num_rows = len(df_crime)
    print(f'Tipo de Crimen: {crime_type}, Entradas: {num_rows}')

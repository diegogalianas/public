import pandas as pd
import os

# Definir todos los archivos (años y subdivisiones por tipo de crimen)
archivos_generales = [
    'Valencia_2010.csv', 'Valencia_2011.csv', 'Valencia_2012.csv', 'Valencia_2013.csv',
    'Valencia_2014.csv', 'Valencia_2015.csv', 'Valencia_2016.csv', 'Valencia_2017.csv',
    'Valencia_2018.csv', 'Valencia_2019.csv', 'Valencia_2020.csv',
    'Valencia_2010_Agresion.csv', 'Valencia_2010_Sustraccion.csv', 'Valencia_2010_AlarmasMujer.csv', 'Valencia_2010_Otros.csv',
    'Valencia_2011_Agresion.csv', 'Valencia_2011_Sustraccion.csv', 'Valencia_2011_AlarmasMujer.csv', 'Valencia_2011_Otros.csv',
    'Valencia_2012_Agresion.csv', 'Valencia_2012_Sustraccion.csv', 'Valencia_2012_AlarmasMujer.csv', 'Valencia_2012_Otros.csv',
    'Valencia_2013_Agresion.csv', 'Valencia_2013_Sustraccion.csv', 'Valencia_2013_AlarmasMujer.csv', 'Valencia_2013_Otros.csv',
    'Valencia_2014_Agresion.csv', 'Valencia_2014_Sustraccion.csv', 'Valencia_2014_AlarmasMujer.csv', 'Valencia_2014_Otros.csv',
    'Valencia_2015_Agresion.csv', 'Valencia_2015_Sustraccion.csv', 'Valencia_2015_AlarmasMujer.csv', 'Valencia_2015_Otros.csv',
    'Valencia_2016_Agresion.csv', 'Valencia_2016_Sustraccion.csv', 'Valencia_2016_AlarmasMujer.csv', 'Valencia_2016_Otros.csv',
    'Valencia_2017_Agresion.csv', 'Valencia_2017_Sustraccion.csv', 'Valencia_2017_AlarmasMujer.csv', 'Valencia_2017_Otros.csv',
    'Valencia_2018_Agresion.csv', 'Valencia_2018_Sustraccion.csv', 'Valencia_2018_AlarmasMujer.csv', 'Valencia_2018_Otros.csv',
    'Valencia_2019_Agresion.csv', 'Valencia_2019_Sustraccion.csv', 'Valencia_2019_AlarmasMujer.csv', 'Valencia_2019_Otros.csv',
    'Valencia_2020_Agresion.csv', 'Valencia_2020_Sustraccion.csv', 'Valencia_2020_AlarmasMujer.csv', 'Valencia_2020_Otros.csv'
]

# Iterar sobre cada archivo
for archivo in archivos_generales:
    if os.path.exists(archivo):  # Comprobar si el archivo existe
        df = pd.read_csv(archivo)  # Leer el archivo CSV
        num_rows = len(df)  # Contar el número de filas
        print(f'Archivo {archivo}: {num_rows} entradas')  # Imprimir el número de filas
    else:
        print(f'Archivo {archivo} no encontrado')

import pandas as pd
import os

# Definir solo los archivos de agresión de 2010 a 2020
archivos_agresion = [
    'Valencia_2015_Month_1.csv', 'Valencia_2015_Month_2.csv', 'Valencia_2015_Month_3.csv',
    'Valencia_2015_Month_4.csv', 'Valencia_2015_Month_5.csv', 'Valencia_2015_Month_6.csv',
    'Valencia_2015_Month_7.csv', 'Valencia_2015_Month_8.csv', 'Valencia_2015_Month_9.csv',
    'Valencia_2015_Month_10.csv', 'Valencia_2015_Month_11.csv', 'Valencia_2015_Month_12.csv'
]

archivos_agresion2 = [
    'Valencia_2010_Sustraccion.csv', 'Valencia_2011_Sustraccion.csv', 'Valencia_2012_Sustraccion.csv',
    'Valencia_2013_Sustraccion.csv', 'Valencia_2014_Sustraccion.csv', 'Valencia_2015_Sustraccion.csv',
    'Valencia_2016_Sustraccion.csv', 'Valencia_2017_Sustraccion.csv', 'Valencia_2018_Sustraccion.csv',
    'Valencia_2019_Sustraccion.csv', 'Valencia_2020_Sustraccion.csv'
]

# Iterar sobre los archivos que son únicamente de agresión y del 2010 al 2020
for archivo in archivos_agresion:
    if os.path.exists(archivo):  # Comprobar si el archivo existe
        df = pd.read_csv(archivo)  # Leer el archivo CSV
        num_rows = len(df)  # Contar el número de filas
        # Extraer el año del nombre del archivo
        year = archivo.split('_')[1]
        print(f'Valencia_{year}_Sustraccion.csv: {num_rows} entradas')  # Imprimir el número de filas
    else:
        print(f'Archivo {archivo} no encontrado')

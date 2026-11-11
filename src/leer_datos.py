import pandas as pd

df = pd.read_excel("input/ventas.xlsx") # Carga el excel en un tabla

print(df.shape)     # (Cantidad de filas, Cantidad de columnas)
print(df.head())    # Primeras 5 filas
df.info()           # Tipos de datos y cantidad de no nulos por columna
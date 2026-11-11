import pandas as pd

df = pd.read_excel("output/ventas_limpias.xlsx") # Antes: input/ventas.xlsx

# Cuentas los vacios por columnas
print("Vacíos por columnas: ")
print(df.isna().sum())

# Muestra las filas que tienen algun vacio
print("\nFilas con vacíos: ")
print(df[df.isna().any(axis=1)])

# Marca las filas repetidas (True = ya apareció antes)
duplicadas = df.duplicated()
print(f"\nCantidad de filas duplicadas: {duplicadas.sum()}")
print(df[duplicadas])

# Muestra cada valor de región entre comillas, con cuántas veces aparece
print("\nValores de region: ")
print(df["region"].value_counts(dropna=False))
print([repr(v) for v in df["region"].unique()])
import pandas as pd

df = pd.read_excel("output/ventas_validas.xlsx")

df.to_excel("output/ventas_limpias.xlsx", index=False) # Guarda sin el índice
print(f"Archivo limpio guardado con {len(df)} filas.")
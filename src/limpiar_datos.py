import pandas as pd

df = pd.read_excel("input/ventas.xlsx")

# Limpia el texto de región: sin espacios de más, sin "!" y con mayúscula inicial
df["region"] = (
    df["region"]
    .str.strip()                        # Quita espacios al inicio y al final
    .str.replace("!", "", regex=False)  # Quita los signos de exclamacion
    .str.strip()                        # Quita los espacios que quedaron
    .str.title()                        # "NORTE" -> "Norte"
)


filas_antes = len(df)
df = df.drop_duplicates() # Elimina filas repetidas, conserva la primera
print(f"Duplicados eliminados: {filas_antes - len(df)}")

filas_antes = len(df)
df = df.dropna(subset = ["fecha", "region", "producto", "cantidad", "precio_unitario"])  # Descarta filas incompletas
print(f"Filas con vacíos eliminadas: {filas_antes - len(df)}")

df.to_excel("output/ventas_limpias.xlsx", index=False) # Guarda sin el índice
print(f"Archivo limpio guardado con {len(df)} filas.")
import shutil
from datetime import datetime
from pathlib import Path

# Carpeta con la fecha de hoy, por ejemplo output/2026-11-09
hoy = datetime.now().strftime("%Y-%m-%d")
carpeta = Path("output") / hoy
carpeta.mkdir(parents=True, exist_ok=True) # La crea si no existe

# Copia el reporte dentro de esa carpeta
shutil.copy("output/reporte_ventas.xlsx", carpeta / "reporte_ventas.xlsx")

print(f"Reporte copiado en: {carpeta}")

# Mueve el archivo original a input/procesados/AAAA-MM-DD
destino = Path("input") / "procesados" / hoy
destino.mkdir(parents=True, exist_ok=True) # La crea si no existe

shutil.move("input/ventas.xlsx", destino / "ventas.xlsx")

print(f"Original movido a: {destino}")


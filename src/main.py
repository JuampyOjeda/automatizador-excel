import logging
import subprocess
import sys
from pathlib import Path

# Crea la carpeta logs/ si no existe
Path("logs").mkdir(exist_ok=True)

# Registra en archivo y tambien en pantalla
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/proceso.log", encoding="utf=8"),
        logging.StreamHandler(),
    ],
)

# Pasos del flujo, en orden
PASOS = [
    "src/generar_datos.py",
    "src/limpiar_datos.py",
    "src/generar_reporte.py",
    "src/organizar_archivos.py",
]

for paso in PASOS:
    logging.info(f"Ejecutando {paso}")
    try:
        subprocess.run([sys.executable, paso], check=True)
        logging.info(f"OK: {paso}")
    except subprocess.CalledProcessError:
        logging.error(f"FALLÓ: {paso}")
        break # Corta el flujo si un paso falla

logging.info("Proceso terminado")
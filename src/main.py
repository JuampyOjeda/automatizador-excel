import logging
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"

# Crea la carpeta logs/ si no existe
LOG_DIR.mkdir(exist_ok=True)

# Registra en archivo y tambien en pantalla
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "proceso.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

# Pasos del flujo, en orden
PASOS = [
    BASE_DIR / "src" / "generar_datos.py",
    BASE_DIR / "src" / "limpiar_datos.py",
    BASE_DIR / "src" / "generar_reporte.py",
    BASE_DIR / "src" / "organizar_archivos.py",
]

for paso in PASOS:
    logging.info(f"Ejecutando {paso.name}")
    try:
        subprocess.run([sys.executable, str(paso)], 
                       check=True,
                       cwd=BASE_DIR
                       )
        logging.info(f"OK: {paso.name}")
    except subprocess.CalledProcessError as error:
        logging.error(
            f"FALLÓ: {paso.name} | Código de salida: {error.returncode}")
        sys.exit(error.returncode)

logging.info("Proceso terminado correctamente")
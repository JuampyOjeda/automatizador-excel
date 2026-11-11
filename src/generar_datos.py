import random
import pandas as pd
from faker import Faker

fake = Faker("es_AR") # Generador de datos falsos en español

REGIONES = ["Norte", "Sur", "Este", "Oeste"]
PRODUCTOS = ["Laptop", "Mouse", "Teclado", "Monitor", "Auriculares"]

def generar_filas(cantidad=100):
    """Crea una lista de ventas falsas (cada venta es un diccionario)"""
    filas = []
    for _ in range(cantidad):
        fila = {
            "fecha": fake.date_this_year(),
            "region": random.choice(REGIONES),
            "producto": random.choice(PRODUCTOS),
            "cantidad": random.randint(1, 10),
            "precio_unitario": round(random.uniform(10, 500), 2),
        }
        filas.append(fila)
    return filas


def agregar_errores(filas):
    """Ensucia los datos a proposito: vacios, duplicados y texto sucio."""
    for fila in filas:
        # 5% de las veces, deja campo vacio
        if random.random() < 0.05:
            campo = random.choice(list(fila.keys()))
            fila[campo] = None
        # 5% de las veces, ensucia el texto de la region
        if random.random() < 0.05:
            fila["region"] = " " + fila["region"].upper() + "!! "
    
    # Agrega una fila duplicada al final
    filas.append(filas[0].copy())
    return filas


if __name__ == "__main__":
    filas = agregar_errores(generar_filas())  # ensucia los datos
    df = pd.DataFrame(filas)
    df.to_excel("input/ventas.xlsx", index=False) # guarda sin el indice numerico
    print(f"Archivo creado con {len(df)} filas.")

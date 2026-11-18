import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ARCHIVO_ENTRADA = BASE_DIR / "input" / "ventas.xlsx"
ARCHIVO_VALIDOS = BASE_DIR / "output" / "ventas_validas.xlsx"
ARCHIVOS_RECHAZADOS = BASE_DIR / "output" / "ventas_rechazadas.xlsx"

COLUMNAS_REQUERIDAS = [
    "fecha",
    "region",
    "producto",
    "cantidad",
    "precio_unitario",
]
REGIONES_VALIDAS = ["Norte", "Sur", "Este", "Oeste"]

PRODUCTOS_VALIDOS = [
    "Laptop",
    "Mouse",
    "Teclado",
    "Monitor",
    "Auriculares",
]

def cargar_datos():
    """Carga el Excel y verifica que tenga las columnas requeridas"""
    if not ARCHIVO_ENTRADA.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo: {ARCHIVO_ENTRADA}"
        )
    df = pd.read_excel(ARCHIVO_ENTRADA)
    columnas_faltantes = [
        columna
        for columna in COLUMNAS_REQUERIDAS
        if columna not in df.columns
    ]
    if columnas_faltantes:
        raise ValueError(
            f"Faltan columnas obligatorias: {columnas_faltantes}"
        )
    return df

def normalizar_textos(df):
    """Normaliza los campos de texto antes de validarlos"""

    for columna in ["region", "producto"]:
        df[columna] = (
            df[columna]
            .astype("string")                  # Convierte el contenido en texto
            .str.strip()                        # Elimina espacios al inicio y al final
            .str.replace("!", "", regex=False)  # Elimina los signos
            .str.strip()
            .str.title()                        # Coloca mayuscula inicial
        )
    return df

def validar_catalogos(df):
    """Identifica regiones y productos que no pertenecen a los catalogos"""
    region_invalida = (
        df["region"].isna() | ~df["region"].isin(REGIONES_VALIDAS)
    )
    producto_invalido = (
        df["producto"].isna() | ~df["producto"].isin(PRODUCTOS_VALIDOS)
    )
    return region_invalida, producto_invalido

def validar_valores_numericos(df):
    """Comprueba que cantidades y precios sean válidos."""
    cantidad = pd.to_numeric(df["cantidad"], errors="coerce")
    precio = pd.to_numeric(df["precio_unitario"], errors="coerce")
    cantidad_invalida = (
        cantidad.isna()
        | (cantidad <= 0)
        | (cantidad % 1 != 0)
    )
    precio_invalido = (
        precio.isna()
        | (precio <= 0)
    )
    return cantidad_invalida, precio_invalido

def validar_fechas(df):
    """Comprueba que las fechas sean válidas y no estén vacías."""
    fechas = pd.to_datetime(df["fecha"], errors="coerce")
    fecha_invalida = fechas.isna()
    return fecha_invalida

CLAVE_DUPLICADOS = [
    "fecha",
    "region",
    "producto",
    "cantidad",
    "precio_unitario",
]

def detectar_duplicados(df):
    """Identifica registros duplicados según la clave definida."""
    duplicado = df.duplicated(
        subset=CLAVE_DUPLICADOS,
        keep="first"            # Conserva la primera aparicion del registro y marca las siguientes como duplicadas
    )
    return duplicado

def construir_motivos_rechazo(
    region_invalida,
    producto_invalido,
    cantidad_invalida,
    precio_invalido,
    fecha_invalida,
    duplicado,
):
    """Construye una lista de motivos para cada registro."""
    motivos = []
    for i in range(len(region_invalida)):
        errores = []
        if region_invalida.iloc[i]:
            errores.append("Región inválida")
        if producto_invalido.iloc[i]:
            errores.append("Producto inválido")
        if cantidad_invalida.iloc[i]:
            errores.append("Cantidad inválida")
        if precio_invalido.iloc[i]:
            errores.append("Precio unitario inválido")
        if fecha_invalida.iloc[i]:
            errores.append("Fecha inválida")
        if duplicado.iloc[i]:
            errores.append("Registro duplicado")
        motivos.append("; ".join(errores)
        )
    return motivos

def validar_datos(df):
    """Ejecuta todas las reglas y clasifica los registros."""
    df = normalizar_textos(df.copy()
                           )
    region_invalida, producto_invalido = validar_catalogos(df)
    cantidad_invalida, precio_invalido = validar_valores_numericos(df)
    fecha_invalida = validar_fechas(df)
    duplicado = detectar_duplicados(df)
    motivos = construir_motivos_rechazo(
        region_invalida,
        producto_invalido,
        cantidad_invalida,
        precio_invalido,
        fecha_invalida,
        duplicado,
    )
    df["motivo_rechazo"] = motivos
    validos = df[df["motivo_rechazo"] == ""].copy()     # Usamos df.copy() para evitar modificar el DataFrame original
    rechazados = df[df["motivo_rechazo"] != ""].copy()

    return validos, rechazados

def guardar_resultados(validos, rechazados):
    """Guarda los registros válidos y rechazados en Excel."""
    ARCHIVO_VALIDOS.parent.mkdir(parents=True, exist_ok=True)
    validos = validos.drop(columns=["motivo_rechazo"])
    validos.to_excel(ARCHIVO_VALIDOS, index=False)
    rechazados.to_excel(ARCHIVOS_RECHAZADOS, index=False)

    print(f"Registros válidos: {len(validos)}")
    print(f"Registros rechazados: {len(rechazados)}")

if __name__ == "__main__":
    df = cargar_datos()
    validos, rechazados = validar_datos(df)
    guardar_resultados(validos, rechazados)
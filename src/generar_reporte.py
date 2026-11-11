import pandas as pd

df = pd.read_excel("output/ventas_limpias.xlsx")

# Columna nueva: total de cada venta
df["total"] = df["cantidad"] * df["precio_unitario"]

# Resumen por región: unidades vendidas y ventas totales
por_region = df.groupby("region").agg(
    unidades = ("cantidad", "sum"),
    ventas_totales = ("total", "sum")
).round(2).reset_index()

print(por_region)

# Resumen por producto
por_producto = df.groupby("producto").agg(
    unidades = ("cantidad", "sum"),
    ventas_totales = ("total", "sum")
).round(2).reset_index()

# Resumen por mes (ordenado cronologicamente)
df["mes"] = df["fecha"].dt.to_period("M").astype(str)
por_mes = df.groupby("mes").agg(
    unidades = ("cantidad", "sum"),
    ventas_totales = ("total", "sum")
).round(2).reset_index()

print(por_producto)
print(por_mes)

# Guarda las tres tablas en un solo Excel, una hoja por resumen
with pd.ExcelWriter("output/reporte_ventas.xlsx") as escritor:
    por_region.to_excel(escritor, sheet_name="Por región", index=False)
    por_producto.to_excel(escritor, sheet_name="Por producto", index=False)
    por_mes.to_excel(escritor,sheet_name="Por mes", index=False)

print("Reporte creado: output/reporte_ventas.xlsx")


from openpyxl import load_workbook
from openpyxl.styles import Font

# Abre el reporte ya creado para darle formato
libro = load_workbook("output/reporte_ventas.xlsx")

for hoja in libro.worksheets:
    # Encabezado en negrita
    for celda in hoja[1]:
        celda.font = Font(bold=True)

    # Ancho de las columnas
    for columna in hoja.columns:
        hoja.column_dimensions[columna[0].column_letter].width = 18

    # Formato de moneda en la columna C (ventas totales)
    for fila in hoja.iter_rows(min_row=2, min_col=3, max_col=3):
        for celda in fila:
            celda.number_format = '"$"#,##0.00'

libro.save("output/reporte_ventas.xlsx")
print("Formato aplicado")
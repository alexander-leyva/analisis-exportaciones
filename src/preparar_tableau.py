import pandas as pd

exportaciones = pd.read_csv("data/exportaciones_limpio.csv")

# Los guiones "-" se convierten en 0 para que Tableau lea la columna como numero
exportaciones["value"] = pd.to_numeric(exportaciones["value"], errors="coerce").fillna(0)
exportaciones = exportaciones.rename(columns={"value": "exportaciones_millones_usd"})

exportaciones.to_csv("data/exportaciones_tableau.csv", index=False)

print(f"Filas: {len(exportaciones)}")
print("Archivo guardado: data/exportaciones_tableau.csv")
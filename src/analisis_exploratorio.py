import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

sns.set_style("whitegrid")

conexion = sqlite3.connect("database/datos_socioeconomicos.db")

exportaciones = pd.read_sql("SELECT * FROM exportaciones", conexion)
poblacion = pd.read_sql("SELECT * FROM poblacion", conexion)
empleo = pd.read_sql("SELECT * FROM empleo", conexion)
esperanza = pd.read_sql("SELECT * FROM esperanza_de_vida", conexion)
conexion.close()

# La columna value a veces tiene un guion "-" cuando no hubo exportaciones ese anio/rubro
# Lo convertimos a numero y tratamos los guiones como 0
exportaciones["value"] = pd.to_numeric(exportaciones["value"], errors="coerce").fillna(0)

# Sumamos todos los rubros para tener el total exportado por provincia y anio
exportaciones_totales = exportaciones.groupby(["provincia", "anio"])["value"].sum().reset_index()
exportaciones_totales = exportaciones_totales.rename(columns={"value": "exportaciones_total"})

print("Exportaciones totales por provincia y anio (primeras filas):")
print(exportaciones_totales.head())

# GRAFICA 1: Evolucion de exportaciones a lo largo del tiempo, para las 5 provincias con mas exportaciones
top5_provincias = (
    exportaciones_totales.groupby("provincia")["exportaciones_total"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
)

plt.figure(figsize=(10, 6))
for provincia in top5_provincias:
    datos_prov = exportaciones_totales[exportaciones_totales["provincia"] == provincia]
    plt.plot(datos_prov["anio"], datos_prov["exportaciones_total"], marker="o", label=provincia)

plt.title("Evolucion de exportaciones (Top 5 provincias) 2005-2020")
plt.xlabel("Anio")
plt.ylabel("Exportaciones (millones de USD)")
plt.legend()
plt.tight_layout()
plt.savefig("data/grafica_evolucion_exportaciones.png", dpi=150)
plt.close()
print("\nGuardada: data/grafica_evolucion_exportaciones.png")

# GRAFICA 2: Composicion de exportaciones por rubro a nivel nacional (ultimo anio disponible)
ultimo_anio = exportaciones["anio"].max()
exp_ultimo_anio = exportaciones[
    (exportaciones["anio"] == ultimo_anio) & (exportaciones["rubro"] != "Total")
]
composicion = exp_ultimo_anio.groupby("rubro")["value"].sum().sort_values(ascending=False)

plt.figure(figsize=(9, 6))
sns.barplot(x=composicion.values, y=composicion.index, palette="viridis")
plt.title(f"Composicion de exportaciones por rubro ({ultimo_anio})")
plt.xlabel("Exportaciones (millones de USD)")
plt.ylabel("Rubro")
plt.tight_layout()
plt.savefig("data/grafica_composicion_rubros.png", dpi=150)
plt.close()
print("Guardada: data/grafica_composicion_rubros.png")

# GRAFICA 3: Relacion entre exportaciones y empleo por provincia (ultimo anio con datos cruzados)
empleo_anual = empleo.groupby(["provincia", "anio"])["empleados_registrados_miles"].mean().reset_index()
cruce = pd.merge(exportaciones_totales, empleo_anual, on=["provincia", "anio"], how="inner")
cruce = cruce[cruce["provincia"] != "Total País"]

plt.figure(figsize=(9, 7))
sns.scatterplot(data=cruce, x="empleados_registrados_miles", y="exportaciones_total", hue="provincia", legend=False, s=60)
plt.title("Relacion entre empleo registrado y exportaciones por provincia")
plt.xlabel("Empleados registrados (miles)")
plt.ylabel("Exportaciones (millones de USD)")
plt.tight_layout()
plt.savefig("data/grafica_empleo_vs_exportaciones.png", dpi=150)
plt.close()
print("\nListo. Se generaron 3 graficas en la carpeta data/")
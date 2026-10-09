import sqlite3
import numpy as np
import pandas as pd

conexion = sqlite3.connect("database/datos_socioeconomicos.db")
exportaciones = pd.read_sql("SELECT * FROM exportaciones", conexion)
poblacion = pd.read_sql("SELECT * FROM poblacion", conexion)
empleo = pd.read_sql("SELECT * FROM empleo", conexion)
esperanza = pd.read_sql("SELECT * FROM esperanza_de_vida", conexion)
hogares = pd.read_sql("SELECT * FROM hogares", conexion)
conexion.close()

# Exportaciones: convertir a numero (los guiones cuentan como 0) y sumar por provincia y anio
exportaciones["value"] = pd.to_numeric(exportaciones["value"], errors="coerce").fillna(0)
exportaciones_limpio = exportaciones[
    (exportaciones["rubro"] != "Total") & (exportaciones["provincia"] != "Total País")
]
exportaciones_totales = (
    exportaciones_limpio.groupby(["provincia", "anio"])["value"].sum().reset_index()
)
exportaciones_totales = exportaciones_totales.rename(columns={"value": "exportaciones_total"})

empleo_anual = empleo.groupby(["provincia", "anio"])["empleados_registrados_miles"].mean().reset_index()

# Unimos todo (esperanza de vida solo existe para 2015 y 2020)
datos = exportaciones_totales.merge(poblacion, on=["provincia", "anio"], how="inner")
datos = datos.merge(empleo_anual, on=["provincia", "anio"], how="inner")
datos = datos.merge(esperanza, on=["provincia", "anio"], how="inner")
datos = datos.merge(hogares, on="provincia", how="inner")
datos = datos[datos["provincia"] != "Total País"].reset_index(drop=True)

print(f"Filas disponibles para el modelo: {len(datos)}")

columnas_x = [
    "poblacion_total",
    "empleados_registrados_miles",
    "mujeres",
    "varones",
    "hogares",
    "superficie_km2",
]
X = datos[columnas_x].astype(float).values
y = datos["exportaciones_total"].values


def ajustar(X, y):
    """Regresion lineal multiple con variables estandarizadas."""
    media = X.mean(axis=0)
    desv = X.std(axis=0)
    desv[desv == 0] = 1
    A = np.column_stack([np.ones(len(X)), (X - media) / desv])
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return media, desv, coef


def predecir(modelo, X):
    media, desv, coef = modelo
    A = np.column_stack([np.ones(len(X)), (X - media) / desv])
    return A @ coef


def r2(y_real, y_pred):
    return 1 - ((y_real - y_pred) ** 2).sum() / ((y_real - y_real.mean()) ** 2).sum()


# Modelo con todos los datos
modelo = ajustar(X, y)
pred = predecir(modelo, X)

print("\n--- Regresion lineal multiple (todos los datos) ---")
print(f"R2: {r2(y, pred):.3f}")
print(f"Error absoluto medio: {np.abs(y - pred).mean():.2f}")

# Validacion dejando una provincia completa afuera cada vez
pred_cv = np.zeros(len(y))
for prov in datos["provincia"].unique():
    es_prueba = (datos["provincia"] == prov).values
    modelo_cv = ajustar(X[~es_prueba], y[~es_prueba])
    pred_cv[es_prueba] = predecir(modelo_cv, X[es_prueba])

print("\n--- Validacion (una provincia afuera a la vez) ---")
print(f"R2: {r2(y, pred_cv):.3f}")
print(f"Error absoluto medio: {np.abs(y - pred_cv).mean():.2f}")

# Que variables pesan mas (coeficientes estandarizados) y correlacion simple
coeficientes = modelo[2][1:]
print("\nPeso de cada variable (coeficiente estandarizado) y correlacion con exportaciones:")
tabla = []
for i, col in enumerate(columnas_x):
    corr = np.corrcoef(X[:, i], y)[0, 1]
    tabla.append((col, coeficientes[i], corr))
for col, coef, corr in sorted(tabla, key=lambda t: -abs(t[1])):
    print(f"  {col}: coeficiente {coef:.1f} | correlacion {corr:.2f}")

resultados = pd.DataFrame(tabla, columns=["variable", "coeficiente_estandarizado", "correlacion"])
resultados.to_csv("data/resultados_modelo.csv", index=False)
print("\nResultados guardados en data/resultados_modelo.csv")
print("Listo.")
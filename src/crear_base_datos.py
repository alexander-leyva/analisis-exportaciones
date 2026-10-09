import sqlite3
import pandas as pd

# Cargamos los archivos ya limpios
exportaciones = pd.read_csv("data/exportaciones_limpio.csv")
poblacion = pd.read_csv("data/poblacion_limpio.csv")
hogares = pd.read_csv("data/hogares_limpio.csv")
esperanza = pd.read_csv("data/esperanza_limpio.csv")
empleo = pd.read_csv("data/empleo_limpio.csv")

# Creamos (o reemplazamos) la base de datos
conexion = sqlite3.connect("database/datos_socioeconomicos.db")

# Guardamos cada dataset como una tabla
exportaciones.to_sql("exportaciones", conexion, if_exists="replace", index=False)
poblacion.to_sql("poblacion", conexion, if_exists="replace", index=False)
hogares.to_sql("hogares", conexion, if_exists="replace", index=False)
esperanza.to_sql("esperanza_de_vida", conexion, if_exists="replace", index=False)
empleo.to_sql("empleo", conexion, if_exists="replace", index=False)

print("Base de datos creada con 5 tablas:")
print("  - exportaciones")
print("  - poblacion")
print("  - hogares")
print("  - esperanza_de_vida")
print("  - empleo")

# Verificamos que todo quedo bien, contando filas de cada tabla
cursor = conexion.cursor()
for tabla in ["exportaciones", "poblacion", "hogares", "esperanza_de_vida", "empleo"]:
    cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
    cantidad = cursor.fetchone()[0]
    print(f"Tabla '{tabla}': {cantidad} filas")

conexion.close()
import glob
import pandas as pd


def cargar(palabra_clave):
    archivos = glob.glob(f"data/*{palabra_clave}*.csv")
    if not archivos:
        raise FileNotFoundError(f"No encontre ningun archivo con '{palabra_clave}' en data/")
    return pd.read_csv(archivos[0], encoding="latin1")


# Cargamos los cinco archivos originales
poblacion = cargar("poblacion")
hogares = cargar("hogares")
exportaciones = cargar("exportaciones")
esperanza = cargar("esperanza")
empleo = cargar("empleo")

print("Filas antes de limpiar:")
print(f"  Exportaciones: {len(exportaciones)}")

# En exportaciones, quitamos la fila de rubro 'Total' (ya es la suma de los otros rubros)
# y la fila de provincia 'Total Pais' (ya es la suma de las provincias)
exportaciones_limpio = exportaciones[
    (exportaciones["rubro"] != "Total") & (exportaciones["provincia"] != "Total País")
].copy()

print(f"  Exportaciones despues de limpiar: {len(exportaciones_limpio)}")

# Revisamos si hay valores nulos en cada dataset
print("\nValores nulos por dataset:")
print(f"  Poblacion: {poblacion.isnull().sum().sum()}")
print(f"  Hogares: {hogares.isnull().sum().sum()}")
print(f"  Exportaciones: {exportaciones_limpio.isnull().sum().sum()}")
print(f"  Esperanza de vida: {esperanza.isnull().sum().sum()}")
print(f"  Empleo: {empleo.isnull().sum().sum()}")

# Guardamos las versiones limpias
exportaciones_limpio.to_csv("data/exportaciones_limpio.csv", index=False)
poblacion.to_csv("data/poblacion_limpio.csv", index=False)
hogares.to_csv("data/hogares_limpio.csv", index=False)
esperanza.to_csv("data/esperanza_limpio.csv", index=False)
empleo.to_csv("data/empleo_limpio.csv", index=False)

print("\nArchivos limpios guardados en la carpeta data/")
import glob
import pandas as pd


def cargar(palabra_clave):
    """Busca en la carpeta data el CSV que contenga la palabra clave."""
    archivos = glob.glob(f"data/*{palabra_clave}*.csv")
    if not archivos:
        raise FileNotFoundError(f"No encontre ningun archivo con '{palabra_clave}' en data/")
    print(f"Cargando: {archivos[0]}")
    return pd.read_csv(archivos[0], encoding="latin1")


# Cargamos los cinco archivos
poblacion = cargar("poblacion")
hogares = cargar("hogares")
exportaciones = cargar("exportaciones")
esperanza = cargar("esperanza")
empleo = cargar("empleo")

datasets = {
    "Poblacion": poblacion,
    "Hogares y vivienda": hogares,
    "Exportaciones": exportaciones,
    "Esperanza de vida": esperanza,
    "Empleo": empleo,
}

for nombre, df in datasets.items():
    print("=" * 50)
    print(f"Dataset: {nombre}")
    print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
    print(f"Columnas: {list(df.columns)}")
    print(df.head(3))
    print()

print("TERMINE SIN ERRORES")
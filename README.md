# Análisis de Exportaciones por Provincia y Rubro (Argentina, 2005-2020)

## Contexto del proyecto

Este proyecto surge a partir de un caso real de consultoría: una empresa multinacional evalúa instalarse en el país y necesita entender qué provincias y qué rubros lideran las exportaciones, cómo evolucionaron en el tiempo, y qué factores socioeconómicos se relacionan con ese desempeño exportador.

El proyecto combina limpieza y análisis de datos con Python, una base de datos relacional en SQL, un modelo de machine learning y visualizaciones interactivas en Tableau Public.

## Dashboard interactivo

[Ver el dashboard en Tableau Public](https://public.tableau.com/app/profile/alexander.leyva.saturnino/viz/Anlisisdeexportacionesporprovincia-Argentina2005-2020/Anlisisdeexportacionesporprovinciayrubro#1)

## Problema que resuelve

A partir de datos públicos abiertos (exportaciones, población, empleo, esperanza de vida y vivienda por provincia), el proyecto responde:

- ¿Qué provincias concentran más exportaciones y de qué rubros?
- ¿Cómo evolucionaron las exportaciones entre 2005 y 2020?
- ¿Qué tan bien explican variables como población, empleo y vivienda las diferencias de exportaciones entre provincias?

## Fuentes de datos

Datos públicos abiertos del Estado, en formato CSV:

- Exportaciones por provincia, rubro y año
- Población por provincia y año
- Empleo registrado por provincia, año y mes
- Esperanza de vida por provincia, año y sexo
- Hogares, viviendas y superficie por provincia

## Metodología

**1. Limpieza de datos (Python/pandas)**
Se filtraron las filas de "Total" y "Total País" en el dataset de exportaciones para evitar duplicar valores al sumar. Se convirtieron columnas numéricas guardadas como texto (incluyendo valores con guion "-", tratados como cero). Se verificó la ausencia de valores nulos en los cinco datasets.

**2. Base de datos (SQLite)**
Se construyó una base de datos relacional con las cinco tablas limpias, unidas por provincia y año, para facilitar consultas y análisis posteriores.

**3. Análisis exploratorio (Python/seaborn/matplotlib)**
Se generaron visualizaciones de evolución temporal de exportaciones por las provincias líderes, composición por rubro, y relación entre empleo y exportaciones.

**4. Modelo de machine learning (regresión lineal múltiple)**
Se entrenó un modelo para explicar las exportaciones por provincia a partir de población, empleo, hogares y superficie. El modelo ajusta bien con todos los datos (R² de 0.85), pero al validarlo dejando cada provincia afuera del entrenamiento, el desempeño cae notablemente. Esto evidencia una limitación real y esperable: con apenas 48 observaciones y variables correlacionadas entre sí (como población y hogares), el modelo memoriza en vez de generalizar. Esta validación honesta es, en sí misma, parte del valor del análisis.

**5. Visualizaciones en Tableau Public**
Se construyeron dos visualizaciones: evolución de exportaciones por rubro (2005-2020) y exportaciones totales por provincia, integradas en un dashboard público.

## Tecnologías utilizadas

Python (pandas, numpy, matplotlib, seaborn), SQLite, Tableau Public.

## Estructura del proyecto

```
analisis-exportaciones/
  data/              archivos CSV originales, limpios y gráficas generadas
  database/          base de datos SQLite
  src/
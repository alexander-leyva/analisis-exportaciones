[33mcommit 5941fdd0e5a9b750d733dbfb7d14c2987e9d4e1c[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mmain[m[33m, [m[1;31morigin/main[m[33m)[m
Author: Alexander Leyva <alexander1108le@gmail.com>
Date:   Fri Oct 9 15:02:52 2026 -0600

    Proyecto de analisis de exportaciones

 data/empleo.csv                          | 3697 [32m++++++++++++++++++++++++++++++[m
 data/empleo_limpio.csv                   | 3697 [32m++++++++++++++++++++++++++++++[m
 data/esperanza_de_vida.csv               |  145 [32m++[m
 data/esperanza_limpio.csv                |  145 [32m++[m
 data/exportaciones.csv                   | 2001 [32m++++++++++++++++[m
 data/exportaciones_limpio.csv            | 1537 [32m+++++++++++++[m
 data/exportaciones_tableau.csv           | 1537 [32m+++++++++++++[m
 data/grafica_composicion_rubros.png      |  Bin [31m0[m -> [32m37181[m bytes
 data/grafica_empleo_vs_exportaciones.png |  Bin [31m0[m -> [32m73021[m bytes
 data/grafica_evolucion_exportaciones.png |  Bin [31m0[m -> [32m128138[m bytes
 data/hogares_limpio.csv                  |   25 [32m+[m
 data/hogares_viviendas_superficie.csv    |   25 [32m+[m
 data/poblacion.csv                       |  776 [32m+++++++[m
 data/poblacion_limpio.csv                |  776 [32m+++++++[m
 data/resultados_modelo.csv               |    7 [32m+[m
 database/datos_socioeconomicos.db        |  Bin [31m0[m -> [32m274432[m bytes
 src/.gitignore                           |    3 [32m+[m
 src/README.md                            |   58 [32m+[m
 src/analisis_exploratorio.py             |   82 [32m+[m
 src/crear_base_datos.py                  |   35 [32m+[m
 src/explorar_datos.py                    |   37 [32m+[m
 src/limpiar_datos.py                     |   45 [32m+[m
 src/modelo_prediccion.py                 |   98 [32m+[m
 src/preparar_tableau.py                  |   12 [32m+[m
 24 files changed, 14738 insertions(+)

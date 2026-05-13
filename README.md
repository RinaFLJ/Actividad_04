# Actividad 4 - Infraestructura para C. de Datos 

Este proyecto documenta el diseño e implementación de una infraestructura de procesamiento masivo orientada al análisis de telemetría de videojuegos. Se evalúan estrategias de carga incremental y optimización de formatos de archivos para manejar un dataset de 1,000,000 de registros de Overwatch 2.


**Configuración de Hardware** 

Los experimentos y métricas de rendimiento fueron obtenidos en la siguiente configuración:

* 
**CPU:** AMD Ryzen 5 5500 (12 hilos lógicos) 


* 
**GPU:** MSI NVIDIA GeForce RTX 3050 6GB 


* 
**RAM:** 32 GB 



## Estructura del Proyecto

* 
**codigo/**: Scripts de Python para cada experimento 


* **datos/**: Almacenamiento de telemetría original (CSV) y procesada (Parquet)
* **resultados/**: Reportes técnicos generados automáticamente (.txt)
* **visualizaciones/**: Gráficos comparativos de rendimiento y métricas

## Requisitos

```bash
pip install pandas matplotlib psutil pyarrow fastparquet

```

Resumen de Experimentos 

1. Experimento A: Generación de Datos 

Construcción de un motor de telemetría sintética para generar 1,000,000 de registros únicos.

* 
**Tamaño inicial (CSV):** 82.20 MB 



2. Experimento B: Diagnóstico de Carga (Monolítica vs Chunks) 

Evaluación del uso de memoria RAM y tiempos de respuesta:

* **Carga Monolítica:** 1.53s | 174.91 MB 


* **Chunk 100k (Punto Óptimo):** 1.62s | 16.89 MB 



3. Experimento C: Analítica Incremental 

Cálculo de sanación total para héroes de soporte en rangos Diamond/Master:

* 
**Ana:** 1,257,006,595 pts 


* 
**Juno:** 1,260,549,969 pts 


* 
**Kiriko:** 1,262,123,433 pts 


* 
**Mercy:** 1,255,327,763 pts 


* 
**Mizuki:** 1,258,292,276 pts 



4. Experimento D: Optimización Columnar (Parquet) 

Migración de arquitectura de CSV a Parquet:

* 
**Reducción de espacio:** 72.54% (de 82.20 MB a 22.57 MB) 


* 
**Aceleración de lectura:** Acceso selectivo a columnas 9.17 veces más rápido que en CSV 


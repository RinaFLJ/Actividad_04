import pandas as pd
import os
import time
import matplotlib.pyplot as plt

# --- RUTAS ---
RUTA_CSV = '../datos/original/telemetria_rendimiento_ow.csv'
CARPETA_PROCESADOS = '../datos/procesados'
RUTA_PARQUET = os.path.join(CARPETA_PROCESADOS, 'telemetria_ow.parquet')
RUTA_VISUALIZACIONES = '../visualizaciones'
RUTA_RESULTADOS = '../resultados' # <-- Aquí está la corrección

# Aseguramos que todas las carpetas existan antes de guardar nada
os.makedirs(CARPETA_PROCESADOS, exist_ok=True)
os.makedirs(RUTA_RESULTADOS, exist_ok=True)
os.makedirs(RUTA_VISUALIZACIONES, exist_ok=True)

def ejecutar_experimento_d():
    print("Iniciando Experimento D: Optimización Columnar y Lakehouse...")
    
    # 1. CONVERSIÓN A PARQUET
    print("Convirtiendo CSV a Parquet con compresión Snappy...")
    df = pd.read_csv(RUTA_CSV, sep=';')
    df.to_parquet(RUTA_PARQUET, engine='pyarrow', compression='snappy')
    
    # 2. COMPARATIVA DE TAMAÑO EN DISCO
    size_csv = os.path.getsize(RUTA_CSV) / (1024 * 1024)
    size_parquet = os.path.getsize(RUTA_PARQUET) / (1024 * 1024)
    reduccion_pct = ((size_csv - size_parquet) / size_csv) * 100

    # 3. PRUEBA DE RENDIMIENTO: LECTURA DE UNA SOLA COLUMNA
    print("Comparando velocidad de lectura de una columna específica...")
    
    # Leer columna del CSV
    t0 = time.time()
    _ = pd.read_csv(RUTA_CSV, sep=';', usecols=['hero_played'])
    t_csv_col = time.time() - t0
    
    # Leer columna del Parquet
    t0 = time.time()
    _ = pd.read_parquet(RUTA_PARQUET, columns=['hero_played'])
    t_parquet_col = time.time() - t0

    # 4. PARTICIONAMIENTO TIPO DATA LAKE
    print("Particionando datos por rango (match_tier)...")
    ruta_particionada = os.path.join(CARPETA_PROCESADOS, 'ow_by_tier')
    df.to_parquet(ruta_particionada, engine='pyarrow', partition_cols=['match_tier'])
    
    # --- GUARDAR REPORTE ---
    ruta_txt = os.path.join(RUTA_RESULTADOS, 'registro_experimento_D.txt')
    with open(ruta_txt, 'w', encoding='utf-8') as f:
        f.write("============================================================\n")
        f.write("EXPERIMENTO D: ANÁLISIS DE FORMATO COLUMNAR Y PARTICIONES\n")
        f.write("============================================================\n")
        f.write(f"Tamaño CSV     : {size_csv:.2f} MB\n")
        f.write(f"Tamaño Parquet : {size_parquet:.2f} MB\n")
        f.write(f"Reducción disco: {reduccion_pct:.2f}%\n\n")
        f.write("Tiempo lectura columna 'hero_played':\n")
        f.write(f"- Desde CSV    : {t_csv_col:.4f} segundos\n")
        f.write(f"- Desde Parquet: {t_parquet_col:.4f} segundos\n")

    # --- VISUALIZACIÓN 4: TAMAÑO Y VELOCIDAD ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Gráfico Izquierdo: Tamaño
    ax1.bar(['CSV', 'Parquet'], [size_csv, size_parquet], color=['#95a5a6', '#2ecc71'])
    ax1.set_title('Tamaño de Almacenamiento', fontweight='bold')
    ax1.set_ylabel('Megabytes (MB)')
    for i, v in enumerate([size_csv, size_parquet]):
        ax1.text(i, v + 2, f"{v:.1f} MB", ha='center', fontweight='bold')

    # Gráfico Derecho: Velocidad
    ax2.bar(['Lectura CSV', 'Lectura Parquet'], [t_csv_col, t_parquet_col], color=['#e74c3c', '#3498db'])
    ax2.set_title('Velocidad de Lectura (1 Columna)', fontweight='bold')
    ax2.set_ylabel('Segundos')
    
    plt.suptitle('Figura 4: Eficiencia del Formato Columnar (Parquet)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(RUTA_VISUALIZACIONES, 'exp_D_parquet_analisis.png'), dpi=300)
    plt.close()

    print("\n¡Experimento D terminado exitosamente!")
    print(f"Reporte guardado en: {ruta_txt}")

if __name__ == "__main__":
    ejecutar_experimento_d()
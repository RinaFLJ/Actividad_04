import pandas as pd
import os
import time
import matplotlib.pyplot as plt

# --- RUTAS ---
RUTA_CSV = '../datos/original/telemetria_rendimiento_ow.csv'
RUTA_RESULTADOS = '../resultados'
RUTA_VISUALIZACIONES = '../visualizaciones'

def ejecutar_experimento_c():
    print("Iniciando Experimento C: Procesamiento Incremental (Split-Apply-Combine)...")
    
    # Héroes a analizar
    soportes = ['Mercy', 'Juno', 'Ana', 'Mizuki', 'Kiriko']
    resultados_parciales = []
    
    inicio_t = time.time()
    num_chunk = 1
    filas_procesadas = 0

    print("Procesando archivo CSV por fragmentos de 100k filas...")
    
    # 1. SPLIT (Dividir): Leemos el archivo en pedazos manejables
    for chunk in pd.read_csv(RUTA_CSV, sep=';', chunksize=100000):
        print(f"  -> Procesando fragmento {num_chunk}...")
        
        # 2. APPLY (Aplicar): Filtramos y calculamos en este pedazo específico
        mask = (chunk['hero_played'].isin(soportes)) & (chunk['match_tier'].isin(['Diamond', 'Master']))
        filtrado = chunk[mask]
        
        # Sumamos la sanación agrupada por héroe
        agrupado = filtrado.groupby('hero_played')['healing_per_10min'].sum()
        resultados_parciales.append(agrupado)
        
        filas_procesadas += len(chunk)
        num_chunk += 1

    # 3. COMBINE (Combinar): Unimos los resultados de todos los fragmentos
    print("Consolidando resultados globales...")
    resultado_final = pd.concat(resultados_parciales).groupby(level=0).sum()
    
    tiempo_total = time.time() - inicio_t

    # --- GUARDAR REPORTE ---
    ruta_txt = os.path.join(RUTA_RESULTADOS, 'registro_experimento_C.txt')
    with open(ruta_txt, 'w', encoding='utf-8') as f:
        f.write("============================================================\n")
        f.write("EXPERIMENTO C: PROCESAMIENTO INCREMENTAL\n")
        f.write("============================================================\n")
        f.write(f"Filas totales evaluadas : {filas_procesadas:,}\n")
        f.write(f"Tiempo de procesamiento : {tiempo_total:.2f} segundos\n\n")
        f.write("Total de sanación en rangos Diamond/Master:\n")
        f.write(resultado_final.to_string())

    # --- VISUALIZACIÓN ---
    plt.figure(figsize=(10, 6))
    resultado_final.sort_values(ascending=False).plot(kind='bar', color='#9b59b6', edgecolor='black')
    plt.title('Figura 3: Sanación Total Acumulada por Héroe (High Tier)', fontweight='bold')
    plt.ylabel('Puntos de Sanación (Millones)')
    plt.xlabel('Héroe de Soporte')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(RUTA_VISUALIZACIONES, 'exp_C_metricas_soporte.png'), dpi=300)
    plt.close()

    print(f"Procesadas {filas_procesadas} filas en {tiempo_total:.2f}s.")

if __name__ == "__main__":
    ejecutar_experimento_c()
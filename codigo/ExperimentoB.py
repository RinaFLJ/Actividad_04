import pandas as pd
import time
import os
import psutil
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE RUTAS ---
CARPETA_DATOS = '../datos/original'
CARPETA_RESULTADOS = '../resultados'
CARPETA_VISUALIZACIONES = '../visualizaciones'
ruta_csv = os.path.join(CARPETA_DATOS, 'telemetria_rendimiento_ow.csv')

# Aseguramos que existan las carpetas necesarias
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
os.makedirs(CARPETA_VISUALIZACIONES, exist_ok=True)

def medir_memoria():
    # Retorna la memoria RAM usada por el proceso actual en MB
    proceso = psutil.Process(os.getpid())
    return proceso.memory_info().rss / (1024 * 1024)

def ejecutar_experimento_b():
    print("Iniciando Experimento B: Análisis de Rendimiento (Monolítico vs Chunks)...")
    
    etiquetas = ['Monolítica']
    tiempos = []
    memorias = []
    lineas_reporte = []

    # 1. LECTURA MONOLÍTICA (Carga completa)
    print("Ejecutando carga completa...")
    mem_base = medir_memoria()
    inicio_t = time.time()
    
    try:
        # Usamos sep=';' como acordamos para evitar errores de celdas en Excel
        df = pd.read_csv(ruta_csv, sep=';')
        tiempos.append(time.time() - inicio_t)
        memorias.append(medir_memoria() - mem_base)
        print(f"✅ Monolítica terminada: {tiempos[0]:.2f}s")
        del df # Liberar RAM inmediatamente
    except MemoryError:
        print("❌ Error: Memoria insuficiente para carga monolítica.")
        tiempos.append(0)
        memorias.append(0)

    # 2. LECTURA POR FRAGMENTOS (Chunks)
    tamanos_chunk = [50000, 100000, 200000]
    for size in tamanos_chunk:
        etiquetas.append(f'Chunk\n{size//1000}k')
        mem_base_chunk = medir_memoria()
        inicio_t = time.time()
        
        # Simulación de lectura incremental
        for chunk in pd.read_csv(ruta_csv, sep=';', chunksize=size):
            pass
            
        t_final = time.time() - inicio_t
        tiempos.append(t_final)
        # abs() para evitar valores negativos ínfimos por recolección de basura
        memorias.append(abs(medir_memoria() - mem_base_chunk))
        print(f"✅ Chunk {size} terminado: {t_final:.2f}s")

    # --- GUARDAR REPORTE EN TXT (AUTOMATIZADO) ---
    ruta_txt = os.path.join(CARPETA_RESULTADOS, 'registro_experimento_B.txt')
    with open(ruta_txt, 'w', encoding='utf-8') as f:
        f.write("============================================================\n")
        f.write("RESULTADOS TÉCNICOS - EXPERIMENTO B (TIEMPO Y RAM)\n")
        f.write("============================================================\n")
        for i, etiqueta in enumerate(etiquetas):
            f.write(f"Estrategia: {etiqueta.replace('\\n', ' ')} | Tiempo: {tiempos[i]:.2f}s | RAM: {memorias[i]:.2f} MB\n")

    # --- GENERAR LOS 2 GRÁFICOS EN UNA SOLA FOTO (SUBPLOTS) ---
    print("\nGenerando imagen comparativa...")
    
    # Creamos una figura con 2 subplots (1 fila, 2 columnas)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Gráfico de la Izquierda: TIEMPO
    ax1.bar(etiquetas, tiempos, color=['#e74c3c', '#3498db', '#3498db', '#3498db'], alpha=0.8)
    ax1.set_title('Comparación de Tiempo de Lectura', fontweight='bold')
    ax1.set_ylabel('Segundos')
    ax1.grid(axis='y', linestyle='--', alpha=0.6)

    # Gráfico de la Derecha: MEMORIA
    ax2.bar(etiquetas, memorias, color=['#e74c3c', '#2ecc71', '#2ecc71', '#2ecc71'], alpha=0.8)
    ax2.set_title('Uso de Memoria RAM Adicional', fontweight='bold')
    ax2.set_ylabel('Megabytes (MB)')
    ax2.grid(axis='y', linestyle='--', alpha=0.6)

    plt.suptitle('Análisis de Rendimiento: Carga Monolítica vs. Incremental', fontsize=16, fontweight='bold')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Ajuste para que el título no tape los gráficos

    # Guardamos la "foto" única
    ruta_imagen = os.path.join(CARPETA_VISUALIZACIONES, 'exp_B_comparativa_rendimiento.png')
    plt.savefig(ruta_imagen, dpi=300)
    plt.close()

    print(f"\n✅ ¡Listo! Registro guardado en: {ruta_txt}")
    print(f"✅ ¡Listo! Los 2 gráficos se guardaron en una sola foto: {ruta_imagen}")

if __name__ == "__main__":
    ejecutar_experimento_b()
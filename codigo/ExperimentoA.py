import pandas as pd
import numpy as np
import os
import uuid
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE RUTAS ---
# Subimos un nivel de 'codigo' y entramos a las carpetas correspondientes
CARPETA_DATOS = '../datos/original'
CARPETA_RESULTADOS = '../resultados'

# Nos aseguramos de que las carpetas existan (por si acaso)
os.makedirs(CARPETA_DATOS, exist_ok=True)
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

def generar_datos_unicos_ow(num_filas=1_000_000, nombre_archivo='telemetria_rendimiento_ow.csv'):
    print(f"Generando {num_filas} registros de telemetría...")
    np.random.seed(42) # Reproducibilidad
    
    # 1. Variables Categóricas
    heroes = ['Mercy', 'Juno', 'Ana', 'Mizuki', 'Kiriko', 'Reinhardt', 'Tracer']
    modos_juego = ['Push', 'Control', 'Escort', 'Hybrid', 'Flashpoint']
    secciones_mapa = ['Point A', 'Point B', 'Checkpoint 1', 'Mid-fight', 'Final Stand']
    rangos_partida = ['Diamond', 'Master', 'Grandmaster', 'Platinum']
    
    hero_played = np.random.choice(heroes, num_filas)
    
    # 2. Variables Numéricas
    server_latency_ms = np.random.normal(loc=60, scale=15, size=num_filas).astype(int)
    server_latency_ms = np.clip(server_latency_ms, 15, 250) 
    
    critical_hit_accuracy = np.random.uniform(0.0, 0.45, num_filas).round(3)
    healing_per_10min = np.where(
        np.isin(hero_played, ['Mercy', 'Juno', 'Ana', 'Mizuki', 'Kiriko']),
        np.random.normal(11000, 2000, num_filas),
        np.random.normal(800, 300, num_filas)
    ).astype(int)
    
    mitigated_damage = np.where(hero_played == 'Reinhardt', np.random.normal(15000, 4000, num_filas), 0).astype(int)
    
    # 3. Variable Temporal
    fecha_base = datetime.now()
    segundos_atras = np.random.randint(0, 7 * 24 * 3600, num_filas)
    
    print("Ensamblando el DataFrame...")
    df = pd.DataFrame({
        'match_hash': [uuid.uuid4().hex[:8] for _ in range(num_filas)],
        'event_timestamp': [fecha_base - timedelta(seconds=int(s)) for s in segundos_atras],
        'hero_played': hero_played,
        'game_mode': np.random.choice(modos_juego, num_filas),
        'map_section': np.random.choice(secciones_mapa, num_filas),
        'match_tier': np.random.choice(rangos_partida, num_filas, p=[0.4, 0.4, 0.1, 0.1]),
        'server_latency_ms': server_latency_ms,
        'critical_hit_accuracy': critical_hit_accuracy,
        'healing_per_10min': healing_per_10min,
        'mitigated_damage': mitigated_damage
    })
    
    # --- EXPORTACIÓN CORREGIDA ---
    ruta_csv = os.path.join(CARPETA_DATOS, nombre_archivo)
    print(f"Guardando en CSV con delimitador ';' (esto puede tomar unos momentos)...")
    
    # Agregamos sep=';' para que Excel lo lea perfectamente en columnas
    df.to_csv(ruta_csv, index=False, sep=';')
    
    # --- REGISTRO AUTOMÁTICO ---
    tamano_mb = os.path.getsize(ruta_csv) / (1024 * 1024)
    reporte = f"""============================================================
RESULTADOS OBLIGATORIOS - EXPERIMENTO A
============================================================
Archivo generado   : {ruta_csv}
Tamaño en disco    : {tamano_mb:.2f} MB
Número de filas    : {df.shape[0]:,}
Número de columnas : {df.shape[1]}

Tipos de datos detectados:
{df.dtypes.to_string()}
============================================================"""

    print("\n" + reporte)
    
    # Guardar en la carpeta resultados
    ruta_txt = os.path.join(CARPETA_RESULTADOS, 'registro_experimento_A.txt')
    with open(ruta_txt, 'w', encoding='utf-8') as archivo_texto:
        archivo_texto.write(reporte)
        
    print(f"\nCSV guardado en: {ruta_csv}")
    print(f"Reporte guardado en: {ruta_txt}")
    
    return df

if __name__ == "__main__":
    df_ow = generar_datos_unicos_ow()
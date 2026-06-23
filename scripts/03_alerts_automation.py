import os
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv

# 1. Cargar las variables del archivo .env (subimos un nivel porque el script está en /scripts)
load_dotenv('.env')

# 2. Inyectar la ruta exacta de la llave de Google Cloud
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcp_key.json' 

# Inicializar el cliente oficial de BigQuery
client = bigquery.Client()

def ejecutar_auditoria_presupuesto():
    print("🚀 Iniciando auditoría automática en Google BigQuery...\n")
    
    # 3. Consultar la tabla directamente en la nube
    # Fíjate que usamos tu proyecto real y tu tabla 'marketing_kpis'
    query = """
    SELECT 
        campaign_id, 
        SUM(mark_spent) as total_gasto, 
        SUM(revenue) as total_ingresos
    FROM `mktng-performance-dashboard.data.marketing_kpis` 
    GROUP BY campaign_id;
    """
    
    # Ejecutar la consulta en Google y descargarla como DataFrame
    df = client.query(query).to_dataframe()
    
    # Calcular el ROAS global matemáticamente correcto (Ingresos / Gasto)
    # Usamos fillna(0) para evitar errores si alguna campaña gastó pero generó 0 ingresos
    df['roas_promedio'] = (df['total_ingresos'] / df['total_gasto']).fillna(0)
    
    # 4. Definir las REGLAS DE NEGOCIO para la alerta
    ROAS_LIMITE = 0.70
    GASTO_MINIMO = 1000.0
    
    campanas_criticas = df[(df['roas_promedio'] < ROAS_LIMITE) & (df['total_gasto'] > GASTO_MINIMO)]
    
    # 5. Procesar y disparar las alertas
    if not campanas_criticas.empty:
        print(f"⚠️ ¡ALERTA CRÍTICA DETECTADA! Se encontraron {len(campanas_criticas)} campañas quemando presupuesto:\n")
        print("-" * 65)
        
        for index, fila in campanas_criticas.iterrows():
            id_campana = int(fila['campaign_id'])
            gasto = fila['total_gasto']
            roas = fila['roas_promedio']
            
            # Formateamos un mensaje profesional
            mensaje_alerta = (
                f"🚨 ACCIÓN REQUERIDA: Pausar Campaña ID: {id_campana}\n"
                f"   • Rendimiento actual: ROAS de {roas:.2f} (Umbral mínimo: {ROAS_LIMITE})\n"
                f"   • Dinero en riesgo: Gasto total acumulado de ${gasto:,.2f}"
            )
            print(mensaje_alerta)
            print("-" * 65)
            
        print("\n[INFO] En producción, este script enviaría un mensaje automático a Slack o Teams.")
        
    else:
        print("✅ Auditoría finalizada: Todas las campañas operan dentro de los rangos de ROAS saludables.")

if __name__ == "__main__":
    ejecutar_auditoria_presupuesto()
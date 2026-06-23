import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 1. Cargar las credenciales seguras
load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# 2. Conectarse a la Base de Datos
conexion_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(conexion_url)

def ejecutar_auditoria_presupuesto():
    print("🚀 Iniciando auditoría automática de campañas...\n")
    
    # 3. Consultar la tabla correcta usando tus columnas exactas
    query = """
    SELECT 
        campaign_id, 
        SUM(mark_spent) as total_gasto, 
        SUM(revenue) as total_ingresos
    FROM marketing_data 
    GROUP BY campaign_id;
    """
    df = pd.read_sql(query, engine)
    
    # Calcular el ROAS matemáticamente (Ingresos / Gasto)
    df['roas_promedio'] = df['total_ingresos'] / df['total_gasto']
    
    # 4. Definir las REGLAS DE NEGOCIO para la alerta
    ROAS_LIMITE = 0.70
    GASTO_MINIMO = 1000.0
    
    campanas_criticas = df[(df['roas_promedio'] < ROAS_LIMITE) & (df['total_gasto'] > GASTO_MINIMO)]
    
    # 5. Procesar y disparar las alertas
    if not campanas_criticas.empty:
        print(f"⚠️  ¡ALERTA CRÍTICA DETECTADA! Se encontraron {len(campanas_criticas)} campañas quemando presupuesto:\n")
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
            
        print("\n[INFO] En producción, este script enviaría un mensaje automático a Slack.")
        
    else:
        print("✅ Auditoría finalizada: Todas las campañas operan dentro de los rangos de ROAS saludables.")

if __name__ == "__main__":
    ejecutar_auditoria_presupuesto()
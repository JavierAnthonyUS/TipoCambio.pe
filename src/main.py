"""
main.py - Script principal para ejecución automatizada

Este script ejecuta la extracción de tipo de cambio cada 1 hora
de forma automatizada.

Uso:
    python main.py

Para detener: Ctrl+C

Autor: Equipo TipoCambio.pe
Fecha: Diciembre 2025
"""

import schedule
import time
import logging
from datetime import datetime

from integrador import ejecutar_extraccion

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/tipo_cambio.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def job():
    """
    Tarea programada que se ejecuta cada hora.
    """
    logger.info("⏰ Ejecutando tarea programada...")
    try:
        ejecutar_extraccion(forzar_guardado=False)
    except Exception as e:
        logger.error(f"Error en tarea programada: {e}")


def main():
    """
    Función principal que configura y ejecuta el scheduler.
    """
    print("=" * 60)
    print("  💱 TipoCambio.pe - Sistema de Monitoreo Automatizado")
    print("=" * 60)
    print(f"  Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("  Frecuencia: Cada 1 hora")
    print("  Para detener: Ctrl+C")
    print("=" * 60)
    
    # Ejecutar inmediatamente al iniciar
    logger.info("Ejecutando primera extracción...")
    job()
    
    # Programar ejecución cada hora
    schedule.every(1).hours.do(job)
    
    # También podemos programar cada ciertos minutos para testing:
    # schedule.every(5).minutes.do(job)
    
    logger.info("Scheduler iniciado. Esperando siguiente ejecución...")
    
    # Loop infinito
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Revisar cada minuto si hay tareas pendientes
    except KeyboardInterrupt:
        logger.info("Detenido por el usuario (Ctrl+C)")
        print("\n👋 Sistema detenido correctamente.")


if __name__ == "__main__":
    main()

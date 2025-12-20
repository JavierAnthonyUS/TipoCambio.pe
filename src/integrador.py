"""
integrador.py - Integrador de fuentes de tipo de cambio

Este módulo combina los datos de todas las fuentes (BCRP, Kambista, Rextie)
en un registro único y lo guarda en el archivo CSV histórico.

Autor: Javier Uraco (@JavierAnthonyUS)
Fecha: Diciembre 2024
"""

import os
import logging
from datetime import datetime
from typing import Dict, Optional

# Importar scrapers
from scraper_bcrp import obtener_tipo_cambio_bcrp
from scraper_kambista import obtener_tipo_cambio_kambista
from scraper_rextie import obtener_tipo_cambio_rextie
from utils import (
    obtener_timestamp,
    calcular_spread,
    determinar_mejor_opcion,
    guardar_csv,
    cargar_ultimo_registro,
    hubo_cambio
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rutas de archivos
RUTA_CSV_HISTORICO = "../data/processed/tipo_cambio_historico.csv"


def extraer_todas_las_fuentes() -> Dict:
    """
    Extrae datos de todas las fuentes disponibles.
    
    Returns:
        Dict con los datos combinados de todas las fuentes
    """
    logger.info("Iniciando extracción de todas las fuentes...")
    
    # Obtener datos de cada fuente
    datos_bcrp = obtener_tipo_cambio_bcrp()
    datos_kambista = obtener_tipo_cambio_kambista()
    datos_rextie = obtener_tipo_cambio_rextie()
    
    # Combinar en un solo diccionario
    datos_combinados = {
        'timestamp': obtener_timestamp(),
        
        # BCRP
        'tc_bcrp_compra': datos_bcrp.get('tc_bcrp_compra'),
        'tc_bcrp_venta': datos_bcrp.get('tc_bcrp_venta'),
        
        # Kambista
        'tc_kambista_compra': datos_kambista.get('tc_kambista_compra'),
        'tc_kambista_venta': datos_kambista.get('tc_kambista_venta'),
        
        # Rextie
        'tc_rextie_compra': datos_rextie.get('tc_rextie_compra'),
        'tc_rextie_venta': datos_rextie.get('tc_rextie_venta'),
        
        # Metadatos de extracción
        'bcrp_exito': datos_bcrp.get('exito', False),
        'kambista_exito': datos_kambista.get('exito', False),
        'rextie_exito': datos_rextie.get('exito', False),
    }
    
    return datos_combinados


def calcular_metricas(datos: Dict) -> Dict:
    """
    Calcula métricas adicionales a partir de los datos extraídos.
    
    Args:
        datos: Diccionario con los datos de tipo de cambio
    
    Returns:
        Dict con las métricas calculadas añadidas
    """
    # Calcular spreads
    datos['spread_bcrp'] = calcular_spread(
        datos.get('tc_bcrp_compra'),
        datos.get('tc_bcrp_venta')
    )
    
    datos['spread_kambista'] = calcular_spread(
        datos.get('tc_kambista_compra'),
        datos.get('tc_kambista_venta')
    )
    
    datos['spread_rextie'] = calcular_spread(
        datos.get('tc_rextie_compra'),
        datos.get('tc_rextie_venta')
    )
    
    # Determinar mejor opción para COMPRAR USD (menor tasa de venta)
    tasas_venta = {
        'BCRP': datos.get('tc_bcrp_venta'),
        'Kambista': datos.get('tc_kambista_venta'),
        'Rextie': datos.get('tc_rextie_venta')
    }
    datos['mejor_compra'] = determinar_mejor_opcion(tasas_venta, 'compra')
    
    # Determinar mejor opción para VENDER USD (mayor tasa de compra)
    tasas_compra = {
        'BCRP': datos.get('tc_bcrp_compra'),
        'Kambista': datos.get('tc_kambista_compra'),
        'Rextie': datos.get('tc_rextie_compra')
    }
    datos['mejor_venta'] = determinar_mejor_opcion(tasas_compra, 'venta')
    
    return datos


def preparar_registro_csv(datos: Dict) -> Dict:
    """
    Prepara los datos para guardar en el CSV (solo columnas necesarias).
    """
    columnas = [
        'timestamp',
        'tc_bcrp_compra', 'tc_bcrp_venta',
        'tc_kambista_compra', 'tc_kambista_venta',
        'tc_rextie_compra', 'tc_rextie_venta',
        'spread_bcrp', 'spread_kambista', 'spread_rextie',
        'mejor_compra', 'mejor_venta', 'cambio_detectado'
    ]
    
    return {col: datos.get(col) for col in columnas}


def ejecutar_extraccion(forzar_guardado: bool = False) -> Dict:
    """
    Ejecuta el proceso completo de extracción e integración.
    
    Args:
        forzar_guardado: Si True, guarda aunque no haya cambios
    
    Returns:
        Dict con los datos extraídos y el estado de la operación
    """
    logger.info("=" * 50)
    logger.info("INICIANDO EXTRACCIÓN DE TIPO DE CAMBIO")
    logger.info("=" * 50)
    
    # 1. Extraer datos de todas las fuentes
    datos = extraer_todas_las_fuentes()
    
    # 2. Calcular métricas
    datos = calcular_metricas(datos)
    
    # 3. Verificar si hubo cambios respecto al último registro
    ultimo_registro = cargar_ultimo_registro(RUTA_CSV_HISTORICO)
    cambio = hubo_cambio(datos, ultimo_registro)
    datos['cambio_detectado'] = cambio
    
    # 4. Guardar si hubo cambio o si se fuerza
    if cambio or forzar_guardado:
        registro = preparar_registro_csv(datos)
        exito = guardar_csv(registro, RUTA_CSV_HISTORICO)
        
        if exito:
            logger.info("✅ Datos guardados exitosamente")
        else:
            logger.error("❌ Error al guardar datos")
    else:
        logger.info("ℹ️ Sin cambios detectados, no se guardó nuevo registro")
    
    # 5. Resumen
    logger.info("-" * 50)
    logger.info("RESUMEN DE EXTRACCIÓN:")
    logger.info(f"  Timestamp: {datos['timestamp']}")
    logger.info(f"  BCRP: Compra={datos['tc_bcrp_compra']}, Venta={datos['tc_bcrp_venta']}")
    logger.info(f"  Kambista: Compra={datos['tc_kambista_compra']}, Venta={datos['tc_kambista_venta']}")
    logger.info(f"  Rextie: Compra={datos['tc_rextie_compra']}, Venta={datos['tc_rextie_venta']}")
    logger.info(f"  Mejor para comprar USD: {datos['mejor_compra']}")
    logger.info(f"  Mejor para vender USD: {datos['mejor_venta']}")
    logger.info(f"  Cambio detectado: {datos['cambio_detectado']}")
    logger.info("=" * 50)
    
    return datos


if __name__ == "__main__":
    # Ejecutar extracción
    resultado = ejecutar_extraccion(forzar_guardado=True)
    
    print("\n" + "=" * 50)
    print("DATOS EXTRAÍDOS:")
    print("=" * 50)
    for key, value in resultado.items():
        if not key.endswith('_exito'):
            print(f"  {key}: {value}")

"""
scraper_bcrp.py - Extractor de tipo de cambio del BCRP

Este módulo extrae el tipo de cambio oficial del Banco Central de Reserva
del Perú mediante su API REST pública.

API Documentation: https://estadisticas.bcrp.gob.pe/estadisticas/series/ayuda/api

Series utilizadas:
    - PD04638PD: Tipo de cambio compra
    - PD04639PD: Tipo de cambio venta

Autor: Javier Uraco (@JavierAnthonyUS)
Fecha: Diciembre 2024
"""

import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de la API
BASE_URL = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"
SERIES_COMPRA = "PD04638PD"
SERIES_VENTA = "PD04639PD"
FORMATO = "json"
TIMEOUT = 30  # segundos


def construir_url(fecha_inicio: str, fecha_fin: str) -> str:
    """
    Construye la URL para consultar la API del BCRP.
    
    Args:
        fecha_inicio: Fecha inicial en formato 'YYYY-MM-DD'
        fecha_fin: Fecha final en formato 'YYYY-MM-DD'
    
    Returns:
        str: URL completa para la consulta
    
    Ejemplo:
        >>> construir_url("2024-12-01", "2024-12-13")
        'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PD04638PD-PD04639PD/json/2024-12-01/2024-12-13'
    """
    series = f"{SERIES_COMPRA}-{SERIES_VENTA}"
    url = f"{BASE_URL}/{series}/{FORMATO}/{fecha_inicio}/{fecha_fin}"
    return url


def obtener_tipo_cambio_bcrp() -> Dict[str, Optional[float]]:
    """
    Obtiene el tipo de cambio actual del BCRP.
    
    Consulta la API del Banco Central de Reserva del Perú para obtener
    las tasas de compra y venta del tipo de cambio oficial.
    
    Returns:
        Dict con las claves:
            - 'tc_bcrp_compra': Tipo de cambio de compra (float o None)
            - 'tc_bcrp_venta': Tipo de cambio de venta (float o None)
            - 'fecha_bcrp': Fecha del dato (str o None)
            - 'exito': True si la extracción fue exitosa
            - 'error': Mensaje de error si hubo fallo
    
    Ejemplo:
        >>> datos = obtener_tipo_cambio_bcrp()
        >>> print(datos)
        {
            'tc_bcrp_compra': 3.72,
            'tc_bcrp_venta': 3.76,
            'fecha_bcrp': '2024-12-13',
            'exito': True,
            'error': None
        }
    """
    resultado = {
        'tc_bcrp_compra': None,
        'tc_bcrp_venta': None,
        'fecha_bcrp': None,
        'exito': False,
        'error': None
    }
    
    try:
        # Definir rango de fechas (últimos 7 días para asegurar datos)
        fecha_fin = datetime.now()
        fecha_inicio = fecha_fin - timedelta(days=7)
        
        fecha_inicio_str = fecha_inicio.strftime("%Y-%m-%d")
        fecha_fin_str = fecha_fin.strftime("%Y-%m-%d")
        
        # Construir URL
        url = construir_url(fecha_inicio_str, fecha_fin_str)
        logger.info(f"Consultando BCRP API: {url}")
        
        # Realizar petición
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        
        # Parsear respuesta JSON
        data = response.json()
        
        # Extraer el último periodo disponible
        if 'periods' in data and len(data['periods']) > 0:
            ultimo_periodo = data['periods'][-1]
            
            # Obtener valores
            valores = ultimo_periodo.get('values', [])
            
            if len(valores) >= 2:
                # El primer valor es compra, el segundo es venta
                tc_compra = valores[0]
                tc_venta = valores[1]
                
                # Convertir a float (pueden venir como string)
                if tc_compra and tc_compra != 'n.d.':
                    resultado['tc_bcrp_compra'] = float(tc_compra)
                
                if tc_venta and tc_venta != 'n.d.':
                    resultado['tc_bcrp_venta'] = float(tc_venta)
                
                # Obtener fecha del periodo
                resultado['fecha_bcrp'] = ultimo_periodo.get('name', '')
                resultado['exito'] = True
                
                logger.info(f"BCRP - Compra: {resultado['tc_bcrp_compra']}, Venta: {resultado['tc_bcrp_venta']}")
            else:
                resultado['error'] = "Datos insuficientes en la respuesta"
                logger.warning(resultado['error'])
        else:
            resultado['error'] = "No se encontraron periodos en la respuesta"
            logger.warning(resultado['error'])
    
    except requests.exceptions.Timeout:
        resultado['error'] = f"Timeout al conectar con BCRP API (>{TIMEOUT}s)"
        logger.error(resultado['error'])
    
    except requests.exceptions.HTTPError as e:
        resultado['error'] = f"Error HTTP: {e.response.status_code}"
        logger.error(resultado['error'])
    
    except requests.exceptions.ConnectionError:
        resultado['error'] = "Error de conexión con BCRP API"
        logger.error(resultado['error'])
    
    except json.JSONDecodeError:
        resultado['error'] = "Error parseando respuesta JSON del BCRP"
        logger.error(resultado['error'])
    
    except Exception as e:
        resultado['error'] = f"Error inesperado: {str(e)}"
        logger.error(resultado['error'])
    
    return resultado


def obtener_series_disponibles() -> None:
    """
    Función auxiliar para explorar las series disponibles en el BCRP.
    Útil para debugging y exploración de la API.
    """
    print("Series de Tipo de Cambio del BCRP:")
    print(f"  - {SERIES_COMPRA}: Tipo de cambio compra")
    print(f"  - {SERIES_VENTA}: Tipo de cambio venta")
    print(f"\nURL base: {BASE_URL}")
    print(f"Formato: {FORMATO}")


if __name__ == "__main__":
    # Test del módulo
    print("=" * 50)
    print("TEST: Scraper BCRP")
    print("=" * 50)
    
    obtener_series_disponibles()
    
    print("\nObteniendo tipo de cambio actual...")
    datos = obtener_tipo_cambio_bcrp()
    
    print("\nResultados:")
    for key, value in datos.items():
        print(f"  {key}: {value}")
    
    if datos['exito']:
        print("\n✅ Extracción exitosa!")
    else:
        print(f"\n❌ Error: {datos['error']}")

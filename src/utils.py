"""
utils.py - Funciones auxiliares para el proyecto TipoCambio.pe

Este módulo contiene funciones de utilidad compartidas por los scrapers.

Autor: Sebastián Fernández (@TucoSquare)
Fecha: Diciembre 2024
"""

import os
import csv
import logging
from datetime import datetime
from typing import Dict, Optional, List

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Headers para simular navegador real
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-PE,es;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}


def obtener_timestamp() -> str:
    """
    Obtiene el timestamp actual en formato estándar.
    
    Returns:
        str: Fecha y hora actual en formato 'YYYY-MM-DD HH:MM:SS'
    
    Ejemplo:
        >>> obtener_timestamp()
        '2024-12-13 10:30:00'
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def validar_tipo_cambio(valor: float, nombre: str = "tipo_cambio") -> bool:
    """
    Valida que un tipo de cambio esté dentro del rango esperado.
    
    Args:
        valor: El valor del tipo de cambio a validar
        nombre: Nombre descriptivo para el log
    
    Returns:
        bool: True si el valor es válido, False en caso contrario
    
    Ejemplo:
        >>> validar_tipo_cambio(3.75, "tc_bcrp_compra")
        True
        >>> validar_tipo_cambio(10.5, "tc_invalido")
        False
    """
    RANGO_MIN = 3.0
    RANGO_MAX = 5.0
    
    if valor is None:
        logger.warning(f"{nombre} es None")
        return False
    
    if not isinstance(valor, (int, float)):
        logger.warning(f"{nombre} no es numérico: {valor}")
        return False
    
    if RANGO_MIN <= valor <= RANGO_MAX:
        return True
    else:
        logger.warning(f"{nombre} fuera de rango: {valor} (esperado {RANGO_MIN}-{RANGO_MAX})")
        return False


def calcular_spread(compra: float, venta: float) -> Optional[float]:
    """
    Calcula el spread (diferencia) entre tasa de venta y compra.
    
    Args:
        compra: Tasa de compra
        venta: Tasa de venta
    
    Returns:
        float: El spread calculado, o None si hay error
    
    Ejemplo:
        >>> calcular_spread(3.72, 3.76)
        0.04
    """
    if compra is None or venta is None:
        return None
    
    try:
        spread = round(venta - compra, 4)
        if spread < 0:
            logger.warning(f"Spread negativo detectado: {spread}")
        return spread
    except Exception as e:
        logger.error(f"Error calculando spread: {e}")
        return None


def determinar_mejor_opcion(tasas: Dict[str, float], tipo: str = "compra") -> Optional[str]:
    """
    Determina cuál fuente ofrece la mejor tasa.
    
    Args:
        tasas: Diccionario con {nombre_fuente: tasa}
        tipo: 'compra' o 'venta'
    
    Returns:
        str: Nombre de la fuente con mejor tasa
    
    Ejemplo:
        >>> tasas = {"BCRP": 3.76, "Kambista": 3.75, "Rextie": 3.74}
        >>> determinar_mejor_opcion(tasas, "compra")
        'Rextie'  # Menor tasa de venta = mejor para comprar USD
    """
    # Filtrar valores None
    tasas_validas = {k: v for k, v in tasas.items() if v is not None}
    
    if not tasas_validas:
        return None
    
    if tipo == "compra":
        # Para COMPRAR USD, quiero la menor tasa de VENTA
        return min(tasas_validas, key=tasas_validas.get)
    else:
        # Para VENDER USD, quiero la mayor tasa de COMPRA
        return max(tasas_validas, key=tasas_validas.get)


def guardar_csv(datos: Dict, ruta: str, modo: str = 'a') -> bool:
    """
    Guarda un registro en el archivo CSV.
    
    Args:
        datos: Diccionario con los datos a guardar
        ruta: Ruta del archivo CSV
        modo: 'a' para append, 'w' para sobrescribir
    
    Returns:
        bool: True si se guardó correctamente
    
    Ejemplo:
        >>> datos = {"timestamp": "2024-12-13 10:00:00", "tc_bcrp_compra": 3.72}
        >>> guardar_csv(datos, "data/tipo_cambio.csv")
        True
    """
    try:
        # Crear directorio si no existe
        directorio = os.path.dirname(ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        # Verificar si el archivo existe para decidir si escribir headers
        archivo_existe = os.path.exists(ruta)
        escribir_header = (modo == 'w') or (not archivo_existe)
        
        with open(ruta, modo, newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=datos.keys())
            
            if escribir_header:
                writer.writeheader()
            
            writer.writerow(datos)
        
        logger.info(f"Datos guardados en {ruta}")
        return True
    
    except Exception as e:
        logger.error(f"Error guardando CSV: {e}")
        return False


def cargar_ultimo_registro(ruta: str) -> Optional[Dict]:
    """
    Carga el último registro del archivo CSV.
    
    Args:
        ruta: Ruta del archivo CSV
    
    Returns:
        Dict: Último registro como diccionario, o None si no existe
    
    Ejemplo:
        >>> ultimo = cargar_ultimo_registro("data/tipo_cambio.csv")
        >>> print(ultimo['timestamp'])
        '2024-12-13 09:00:00'
    """
    if not os.path.exists(ruta):
        return None
    
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            registros = list(reader)
            
            if registros:
                return registros[-1]
            return None
    
    except Exception as e:
        logger.error(f"Error cargando último registro: {e}")
        return None


def hubo_cambio(datos_nuevos: Dict, datos_anteriores: Dict) -> bool:
    """
    Compara datos nuevos con los anteriores para detectar cambios.
    
    Args:
        datos_nuevos: Diccionario con datos actuales
        datos_anteriores: Diccionario con datos del último registro
    
    Returns:
        bool: True si hubo algún cambio en las tasas
    
    Ejemplo:
        >>> nuevo = {"tc_bcrp_compra": 3.72, "tc_kambista_compra": 3.74}
        >>> anterior = {"tc_bcrp_compra": 3.72, "tc_kambista_compra": 3.73}
        >>> hubo_cambio(nuevo, anterior)
        True
    """
    if datos_anteriores is None:
        return True  # Primer registro siempre es "cambio"
    
    campos_a_comparar = [
        'tc_bcrp_compra', 'tc_bcrp_venta',
        'tc_kambista_compra', 'tc_kambista_venta',
        'tc_rextie_compra', 'tc_rextie_venta'
    ]
    
    for campo in campos_a_comparar:
        valor_nuevo = datos_nuevos.get(campo)
        valor_anterior = datos_anteriores.get(campo)
        
        # Convertir a float para comparación
        try:
            if valor_nuevo is not None:
                valor_nuevo = float(valor_nuevo)
            if valor_anterior is not None:
                valor_anterior = float(valor_anterior)
        except (ValueError, TypeError):
            pass
        
        if valor_nuevo != valor_anterior:
            logger.info(f"Cambio detectado en {campo}: {valor_anterior} -> {valor_nuevo}")
            return True
    
    return False


def limpiar_numero(texto: str) -> Optional[float]:
    """
    Limpia y convierte un texto a número flotante.
    
    Args:
        texto: Texto que contiene un número (puede tener símbolos)
    
    Returns:
        float: Número extraído, o None si falla
    
    Ejemplo:
        >>> limpiar_numero("S/ 3.7500")
        3.75
        >>> limpiar_numero("3,750.00")
        3750.0
    """
    if texto is None:
        return None
    
    try:
        # Remover símbolos comunes
        limpio = texto.replace('S/', '').replace('$', '').replace(' ', '')
        limpio = limpio.replace(',', '')  # Para formatos como 3,750.00
        limpio = limpio.strip()
        
        return float(limpio)
    
    except (ValueError, AttributeError) as e:
        logger.warning(f"No se pudo convertir '{texto}' a número: {e}")
        return None


if __name__ == "__main__":
    # Tests básicos
    print("=== Tests de utils.py ===")
    
    print(f"\nTimestamp actual: {obtener_timestamp()}")
    
    print(f"\nValidar 3.75: {validar_tipo_cambio(3.75)}")
    print(f"Validar 10.5: {validar_tipo_cambio(10.5)}")
    
    print(f"\nSpread de 3.72 y 3.76: {calcular_spread(3.72, 3.76)}")
    
    tasas_venta = {"BCRP": 3.76, "Kambista": 3.755, "Rextie": 3.75}
    print(f"\nMejor para comprar USD: {determinar_mejor_opcion(tasas_venta, 'compra')}")
    
    tasas_compra = {"BCRP": 3.72, "Kambista": 3.735, "Rextie": 3.73}
    print(f"Mejor para vender USD: {determinar_mejor_opcion(tasas_compra, 'venta')}")
    
    print(f"\nLimpiar 'S/ 3.7500': {limpiar_numero('S/ 3.7500')}")
    
    print("\n=== Tests completados ===")

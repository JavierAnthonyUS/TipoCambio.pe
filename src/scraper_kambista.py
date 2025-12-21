"""
scraper_kambista.py - Extractor de tipo de cambio de Kambista

Este módulo extrae el tipo de cambio de la casa de cambio digital Kambista
mediante web scraping.

URL: https://kambista.com

Autor: Fiorella Fuentes (@fiorellafuentesb20-cell)
Fecha: Diciembre 2025
"""

import requests
from bs4 import BeautifulSoup
import logging
import re
import time
import random
from typing import Dict, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración
URL_KAMBISTA = "https://kambista.com"
TIMEOUT = 30  # segundos

# Headers para simular navegador real
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-PE,es;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


def limpiar_numero(texto: str) -> Optional[float]:
    """
    Extrae un número flotante de un texto.
    
    Args:
        texto: Texto que contiene el número
    
    Returns:
        float: Número extraído o None si falla
    
    Ejemplo:
        >>> limpiar_numero("S/ 3.7500")
        3.75
    """
    if not texto:
        return None
    
    try:
        # Buscar patrón de número decimal
        match = re.search(r'(\d+\.?\d*)', texto.replace(',', ''))
        if match:
            return float(match.group(1))
        return None
    except Exception as e:
        logger.warning(f"Error limpiando número '{texto}': {e}")
        return None


def obtener_tipo_cambio_kambista() -> Dict[str, Optional[float]]:
    """
    Obtiene el tipo de cambio actual de Kambista mediante web scraping.
    
    Realiza una petición GET a la página de Kambista y extrae las tasas
    de compra y venta del tipo de cambio.
    
    Returns:
        Dict con las claves:
            - 'tc_kambista_compra': Tipo de cambio de compra (float o None)
            - 'tc_kambista_venta': Tipo de cambio de venta (float o None)
            - 'exito': True si la extracción fue exitosa
            - 'error': Mensaje de error si hubo fallo
    
    Ejemplo:
        >>> datos = obtener_tipo_cambio_kambista()
        >>> print(datos)
        {
            'tc_kambista_compra': 3.735,
            'tc_kambista_venta': 3.755,
            'exito': True,
            'error': None
        }
    
    Notas:
        - Respeta el robots.txt de Kambista
        - Usa headers realistas para evitar bloqueos
        - Frecuencia recomendada: máximo 1 petición por hora
    """
    resultado = {
        'tc_kambista_compra': None,
        'tc_kambista_venta': None,
        'exito': False,
        'error': None
    }
    
    try:
        logger.info(f"Consultando Kambista: {URL_KAMBISTA}")
        
        # Realizar petición con headers
        response = requests.get(
            URL_KAMBISTA, 
            headers=HEADERS, 
            timeout=TIMEOUT
        )
        response.raise_for_status()
        
        # Parsear HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ============================================================
        # NOTA IMPORTANTE:
        # Los selectores CSS a continuación son EJEMPLOS y deben ser
        # actualizados después de inspeccionar la página real de Kambista.
        # 
        # Para encontrar los selectores correctos:
        # 1. Abrir https://kambista.com en Chrome
        # 2. Click derecho en la tasa de compra → Inspeccionar
        # 3. Identificar la clase o ID del elemento
        # 4. Actualizar los selectores aquí
        # ============================================================
        
        # Intento 1: Buscar por clases comunes
        # (Estos selectores son ejemplos y deben verificarse)
        
        # Buscar elementos que contengan las tasas
        # Opción A: Buscar por texto "Compra" y "Venta"
        tasas = soup.find_all(['span', 'div', 'p'], class_=re.compile(r'rate|price|cambio|tasa', re.I))
        
        if not tasas:
            # Opción B: Buscar todos los elementos con números que parezcan TC
            textos = soup.find_all(string=re.compile(r'\d\.\d{2,4}'))
            
            for texto in textos:
                numero = limpiar_numero(texto)
                if numero and 3.0 <= numero <= 5.0:  # Rango válido de TC
                    if resultado['tc_kambista_compra'] is None:
                        resultado['tc_kambista_compra'] = numero
                    elif resultado['tc_kambista_venta'] is None:
                        resultado['tc_kambista_venta'] = numero
                        break
        
        # Verificar si se obtuvieron datos
        if resultado['tc_kambista_compra'] is not None and resultado['tc_kambista_venta'] is not None:
            resultado['exito'] = True
            logger.info(f"Kambista - Compra: {resultado['tc_kambista_compra']}, Venta: {resultado['tc_kambista_venta']}")
        else:
            # Si no encontramos con los métodos anteriores, puede ser página dinámica
            resultado['error'] = "No se encontraron las tasas. Posible página dinámica (requiere Selenium)"
            logger.warning(resultado['error'])
            
            # Guardar el HTML para análisis (en desarrollo)
            # with open('kambista_debug.html', 'w', encoding='utf-8') as f:
            #     f.write(soup.prettify())
    
    except requests.exceptions.Timeout:
        resultado['error'] = f"Timeout al conectar con Kambista (>{TIMEOUT}s)"
        logger.error(resultado['error'])
    
    except requests.exceptions.HTTPError as e:
        resultado['error'] = f"Error HTTP: {e.response.status_code}"
        logger.error(resultado['error'])
    
    except requests.exceptions.ConnectionError:
        resultado['error'] = "Error de conexión con Kambista"
        logger.error(resultado['error'])
    
    except Exception as e:
        resultado['error'] = f"Error inesperado: {str(e)}"
        logger.error(resultado['error'])
    
    return resultado


def verificar_robots_txt() -> None:
    """
    Verifica el archivo robots.txt de Kambista.
    Útil para asegurar que el scraping es permitido.
    """
    try:
        response = requests.get(f"{URL_KAMBISTA}/robots.txt", timeout=10)
        if response.status_code == 200:
            print("robots.txt de Kambista:")
            print("-" * 40)
            print(response.text)
        else:
            print(f"No se encontró robots.txt (status: {response.status_code})")
    except Exception as e:
        print(f"Error verificando robots.txt: {e}")


def analizar_estructura_html() -> None:
    """
    Función de desarrollo para analizar la estructura HTML de Kambista.
    Ayuda a identificar los selectores correctos.
    """
    try:
        response = requests.get(URL_KAMBISTA, headers=HEADERS, timeout=TIMEOUT)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print("Análisis de estructura HTML de Kambista")
        print("=" * 50)
        
        # Buscar elementos con clases relacionadas a tasas
        for tag in ['div', 'span', 'p']:
            elementos = soup.find_all(tag, class_=True)
            clases_unicas = set()
            for elem in elementos:
                for clase in elem.get('class', []):
                    if any(palabra in clase.lower() for palabra in ['rate', 'price', 'cambio', 'tasa', 'buy', 'sell', 'compra', 'venta']):
                        clases_unicas.add(clase)
            
            if clases_unicas:
                print(f"\nClases relevantes en <{tag}>:")
                for clase in clases_unicas:
                    print(f"  - {clase}")
        
        # Buscar números que parezcan tipo de cambio
        print("\nNúmeros encontrados (posibles TC):")
        textos = soup.find_all(string=re.compile(r'\d\.\d{2,4}'))
        for texto in textos[:10]:  # Limitar a primeros 10
            numero = limpiar_numero(texto.strip())
            if numero and 3.0 <= numero <= 5.0:
                print(f"  - {numero} (de: '{texto.strip()[:50]}')")
                
    except Exception as e:
        print(f"Error analizando HTML: {e}")


if __name__ == "__main__":
    # Test del módulo
    print("=" * 50)
    print("TEST: Scraper Kambista")
    print("=" * 50)
    
    # Verificar robots.txt primero
    print("\n1. Verificando robots.txt...")
    verificar_robots_txt()
    
    # Analizar estructura (para desarrollo)
    print("\n2. Analizando estructura HTML...")
    analizar_estructura_html()
    
    # Intentar obtener datos
    print("\n3. Obteniendo tipo de cambio...")
    datos = obtener_tipo_cambio_kambista()
    
    print("\nResultados:")
    for key, value in datos.items():
        print(f"  {key}: {value}")
    
    if datos['exito']:
        print("\n✅ Extracción exitosa!")
    else:
        print(f"\n⚠️ Extracción incompleta: {datos['error']}")
        print("\nNOTA: Puede ser necesario usar Selenium si la página es dinámica.")

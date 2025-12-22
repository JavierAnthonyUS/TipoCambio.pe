"""
scraper_kambista.py - Extractor de tipo de cambio de Kambista

Este módulo extrae el tipo de cambio de la casa de cambio digital Kambista
mediante web scraping con Selenium (página dinámica).

URL: https://kambista.com

Autor: Fiorella Fuentes (@fiorellafuentesb20-cell)
Fecha: Diciembre 2025
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging
import re
import time
from typing import Dict, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(_name_)

# Configuración
URL_KAMBISTA = "https://kambista.com"
TIMEOUT = 15


def obtener_tipo_cambio_kambista() -> Dict[str, Optional[float]]:
    """
    Obtiene el tipo de cambio actual de Kambista mediante Selenium.
    
    Usa un navegador headless para cargar la página y esperar
    a que se renderice el contenido dinámico con las tasas.
    
    Returns:
        Dict con las claves:
            - 'tc_kambista_compra': Tipo de cambio de compra (float o None)
            - 'tc_kambista_venta': Tipo de cambio de venta (float o None)
            - 'exito': True si la extracción fue exitosa
            - 'error': Mensaje de error si hubo fallo
    """
    resultado = {
        'tc_kambista_compra': None,
        'tc_kambista_venta': None,
        'exito': False,
        'error': None
    }
    
    driver = None
    
    try:
        logger.info(f"Iniciando Selenium para Kambista: {URL_KAMBISTA}")
        
        # Configurar Chrome en modo headless
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        options.add_argument('--log-level=3')
        
        # Iniciar el driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Cargar la página
        driver.get(URL_KAMBISTA)
        
        # Esperar a que cargue el contenido dinámico
        time.sleep(3)
        
        # Obtener el HTML de la página renderizada
        html = driver.page_source
        
        # Buscar todos los números que parezcan tipo de cambio
        patron = r'[\d]+\.[\d]{2,4}'
        matches = re.findall(patron, html)
        
        # Filtrar valores válidos de tipo de cambio
        valores_tc = []
        for m in matches:
            try:
                valor = float(m)
                # Rango típico de tipo de cambio PEN/USD
                if 3.30 <= valor <= 3.50:
                    valor_redondeado = round(valor, 4)
                    if valor_redondeado not in valores_tc:
                        valores_tc.append(valor_redondeado)
            except:
                pass
        
        logger.info(f"Valores de TC encontrados: {valores_tc}")
        
        if len(valores_tc) >= 2:
            # Ordenar valores
            valores_tc_sorted = sorted(valores_tc)
            resultado['tc_kambista_compra'] = valores_tc_sorted[0]
            resultado['tc_kambista_venta'] = valores_tc_sorted[-1]
            resultado['exito'] = True
            logger.info(f"Kambista - Compra: {resultado['tc_kambista_compra']}, Venta: {resultado['tc_kambista_venta']}")
        else:
            resultado['error'] = f"Valores insuficientes encontrados: {valores_tc}"
            logger.warning(resultado['error'])
    
    except Exception as e:
        resultado['error'] = f"Error: {str(e)}"
        logger.error(resultado['error'])
    
    finally:
        if driver:
            driver.quit()
            logger.info("Navegador cerrado")
    
    return resultado


# ============================================================
# EJECUCIÓN PRINCIPAL (para testing)
# ============================================================
if _name_ == "_main_":
    print("\n" + "=" * 50)
    print("   TEST: Scraper Kambista (Selenium)")
    print("=" * 50)
    
    print(f"\n🌐 URL: {URL_KAMBISTA}")
    print("🔄 Iniciando navegador headless...")
    
    datos = obtener_tipo_cambio_kambista()
    
    print("\n📊 RESULTADOS:")
    print("-" * 50)
    print(f"  💵 Tipo Cambio Compra: S/ {datos['tc_kambista_compra']}")
    print(f"  💵 Tipo Cambio Venta:  S/ {datos['tc_kambista_venta']}")
    print(f"  ✓  Éxito:              {datos['exito']}")
    
    if datos['error']:
        print(f"  ❌ Error:              {datos['error']}")
    
    print("-" * 50)
    
    if datos['exito']:
        print("\n✅ SCRAPER KAMBISTA FUNCIONANDO CORRECTAMENTE")
    else:
        print(f"\n❌ ERROR: {datos['error']}")
    
    print("=" * 50 + "\n")

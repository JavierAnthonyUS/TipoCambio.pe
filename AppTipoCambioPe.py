"""
💱 COMPARADOR DE TIPO DE CAMBIO PERÚ
Aplicación Web con NiceGUI

Este módulo proporciona una interfaz web interactiva para visualizar
y comparar tipos de cambio de múltiples fuentes en tiempo real.

Páginas:
    - /         : Página de inicio
    - /demo     : Demo de scrapers en tiempo real
    - /analisis : Análisis comparativo (EN DESARROLLO)
    - /equipo   : Información del equipo

Tecnologías:
    - NiceGUI 3.4+ para la interfaz web
    - Plotly para gráficos interactivos
    - Tailwind CSS para estilos

Autor: Javier Uraco (@JavierAnthonyUS)
Fecha: Diciembre 2025

Uso:
    python AppTipoCambioPe.py
    Abrir navegador en: http://localhost:8080
"""

from nicegui import ui
import asyncio
import os
import sys

# Agregar carpeta src al path para importar scrapers
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Intentar importar scrapers
try:
    from scraper_bcrp import obtener_tipo_cambio_bcrp
    from scraper_kambista import obtener_tipo_cambio_kambista
    from scraper_rextie import obtener_tipo_cambio_rextie
    SCRAPERS_DISPONIBLES = True
except ImportError:
    SCRAPERS_DISPONIBLES = False
    print("⚠️ Scrapers no encontrados. Usando datos demo.")


# =============================================================================
# DATOS DE DEMOSTRACIÓN
# =============================================================================
def obtener_datos_demo():
    """
    Retorna datos de demostración cuando los scrapers no están disponibles.
    
    Returns:
        dict: Diccionario con datos de ejemplo de las 3 fuentes
    """
    return {
        'bcrp': {'compra': 3.7320, 'venta': 3.7350, 'exito': True},
        'kambista': {'compra': 3.7100, 'venta': 3.7550, 'exito': True},
        'rextie': {'compra': 3.7200, 'venta': 3.7480, 'exito': True},
    }


# =============================================================================
# FUNCIONES ASYNC PARA EJECUTAR SCRAPERS
# =============================================================================
async def ejecutar_scraper_bcrp():
    """Ejecuta el scraper de BCRP de forma asíncrona."""
    if SCRAPERS_DISPONIBLES:
        try:
            resultado = obtener_tipo_cambio_bcrp()
            return {
                'compra': resultado.get('tc_bcrp_compra', 0),
                'venta': resultado.get('tc_bcrp_venta', 0),
                'exito': resultado.get('exito', False)
            }
        except Exception as e:
            return {'compra': 0, 'venta': 0, 'exito': False}
    else:
        await asyncio.sleep(1)
        return obtener_datos_demo()['bcrp']


async def ejecutar_scraper_kambista():
    """Ejecuta el scraper de Kambista de forma asíncrona."""
    if SCRAPERS_DISPONIBLES:
        try:
            resultado = obtener_tipo_cambio_kambista()
            return {
                'compra': resultado.get('tc_kambista_compra', 0),
                'venta': resultado.get('tc_kambista_venta', 0),
                'exito': resultado.get('exito', False)
            }
        except Exception as e:
            return {'compra': 0, 'venta': 0, 'exito': False}
    else:
        await asyncio.sleep(2)
        return obtener_datos_demo()['kambista']


async def ejecutar_scraper_rextie():
    """Ejecuta el scraper de Rextie de forma asíncrona."""
    if SCRAPERS_DISPONIBLES:
        try:
            resultado = obtener_tipo_cambio_rextie()
            return {
                'compra': resultado.get('tc_rextie_compra', 0),
                'venta': resultado.get('tc_rextie_venta', 0),
                'exito': resultado.get('exito', False)
            }
        except Exception as e:
            return {'compra': 0, 'venta': 0, 'exito': False}
    else:
        await asyncio.sleep(2)
        return obtener_datos_demo()['rextie']


# =============================================================================
# FUNCIÓN: CALCULAR MEJOR OPCIÓN
# =============================================================================
def calcular_mejor_opcion(datos):
    """
    Determina la mejor opción para comprar y vender dólares.
    
    Args:
        datos: Dict con datos de las 3 fuentes
    
    Returns:
        tuple: (mejor_para_comprar, mejor_para_vender)
    """
    fuentes_validas = []
    
    for nombre, info in datos.items():
        if info is not None and info.get('compra') and info.get('venta') and info['compra'] > 0:
            fuentes_validas.append({
                'nombre': nombre.upper(),
                'compra': info['compra'],
                'venta': info['venta']
            })
    
    if not fuentes_validas:
        return None, None
    
    # Para COMPRAR USD: menor precio de VENTA
    mejor_comprar = min(fuentes_validas, key=lambda x: x['venta'])
    # Para VENDER USD: mayor precio de COMPRA
    mejor_vender = max(fuentes_validas, key=lambda x: x['compra'])
    
    return mejor_comprar, mejor_vender


# =============================================================================
# COMPONENTE: BARRA DE NAVEGACIÓN
# =============================================================================
def crear_navbar():
    """Crea la barra de navegación superior."""
    with ui.row().classes('w-full items-center justify-between p-4 bg-gray-900'):
        with ui.row().classes('items-center gap-3'):
            ui.icon('currency_exchange').classes('text-3xl text-cyan-400')
            ui.link('TipoCambio.pe', '/').classes('text-2xl font-bold text-white no-underline')
        
        with ui.row().classes('gap-4'):
            ui.link('Inicio', '/').classes('text-cyan-400 no-underline hover:text-cyan-300')
            ui.link('Demo', '/demo').classes('text-cyan-400 no-underline hover:text-cyan-300')
            ui.link('Análisis', '/analisis').classes('text-cyan-400 no-underline hover:text-cyan-300')
            ui.link('Equipo', '/equipo').classes('text-cyan-400 no-underline hover:text-cyan-300')


# =============================================================================
# PÁGINA: INICIO
# =============================================================================
@ui.page('/')
def pagina_inicio():
    """Página principal con presentación del proyecto."""
    ui.query('body').classes('bg-gray-900')
    
    crear_navbar()
    
    # Hero section
    with ui.column().classes('w-full items-center py-16 px-8'):
        ui.label('💱').classes('text-8xl mb-4')
        ui.label('Comparador de Tipo de Cambio').classes('text-5xl font-bold text-cyan-400 text-center')
        ui.label('Perú').classes('text-6xl font-bold text-white mt-2')
        ui.label('Encuentra la mejor opción para comprar y vender dólares en tiempo real').classes(
            'text-xl text-gray-400 mt-6 text-center max-w-2xl'
        )
        
        with ui.row().classes('gap-4 mt-8'):
            ui.button('🚀 Ver Demo', on_click=lambda: ui.navigate.to('/demo')).props('push color=cyan size=lg').classes('px-8')
            ui.button('📊 Análisis', on_click=lambda: ui.navigate.to('/analisis')).props('outline color=cyan size=lg').classes('px-8')
    
    # Características
    with ui.row().classes('w-full justify-center gap-8 px-8 pb-16 flex-wrap'):
        with ui.card().classes('w-80 p-6 bg-gray-800'):
            ui.icon('cloud_download').classes('text-4xl text-cyan-400 mb-4')
            ui.label('3 Fuentes de Datos').classes('text-xl font-bold text-white mb-2')
            ui.label('BCRP (API oficial), Kambista y Rextie (Web Scraping con Selenium)').classes('text-gray-400')
        
        with ui.card().classes('w-80 p-6 bg-gray-800'):
            ui.icon('speed').classes('text-4xl text-green-400 mb-4')
            ui.label('Datos en Tiempo Real').classes('text-xl font-bold text-white mb-2')
            ui.label('Extracción automática de tipos de cambio actualizados al momento').classes('text-gray-400')
        
        with ui.card().classes('w-80 p-6 bg-gray-800'):
            ui.icon('analytics').classes('text-4xl text-purple-400 mb-4')
            ui.label('Análisis Inteligente').classes('text-xl font-bold text-white mb-2')
            ui.label('Cálculo de spreads, comparación y recomendación de mejor opción').classes('text-gray-400')
    
    # Problema / Solución
    ui.label('¿Por qué TipoCambio.pe?').classes('text-3xl font-bold text-white text-center mb-8')
    
    with ui.row().classes('w-full justify-center gap-8 px-8 pb-16 flex-wrap'):
        with ui.card().classes('w-96 p-6 bg-gray-800 border-l-4 border-red-500'):
            ui.label('❌ El Problema').classes('text-xl font-bold text-red-400 mb-4')
            ui.label('Cada casa de cambio tiene tasas diferentes. Por cada $1,000 la diferencia puede ser de S/ 50 o más.').classes('text-gray-300')
        
        with ui.card().classes('w-96 p-6 bg-gray-800 border-l-4 border-green-500'):
            ui.label('✅ Nuestra Solución').classes('text-xl font-bold text-green-400 mb-4')
            ui.label('Sistema automatizado que extrae datos de múltiples fuentes y recomienda la mejor opción.').classes('text-gray-300')
    
    # Footer
    with ui.row().classes('w-full justify-center py-6 bg-gray-950'):
        ui.label('💱 TipoCambio.pe | LP2 - UNALM 2025').classes('text-gray-500')


# =============================================================================
# PÁGINA: DEMO DE SCRAPERS
# =============================================================================
@ui.page('/demo')
def pagina_demo():
    """Página de demostración de los scrapers en tiempo real."""
    ui.query('body').classes('bg-gray-900')
    
    crear_navbar()
    
    # Variables para almacenar datos
    datos_locales = {'bcrp': None, 'kambista': None, 'rextie': None}
    
    with ui.column().classes('w-full p-8'):
        with ui.row().classes('items-center gap-3 mb-2'):
            ui.icon('sync').classes('text-3xl text-cyan-400')
            ui.label('Demo de Scrapers').classes('text-3xl font-bold text-white')
        ui.label('Ejecuta los scrapers individualmente o todos a la vez').classes('text-gray-400 mb-8')
        
        with ui.row().classes('w-full gap-6 flex-wrap justify-center'):
            
            # === CARD BCRP ===
            with ui.card().classes('w-80 p-6 bg-gray-800'):
                with ui.row().classes('items-center gap-3 mb-4'):
                    ui.icon('account_balance').classes('text-3xl text-blue-500')
                    ui.label('BCRP').classes('text-xl font-bold text-white')
                    ui.badge('API').props('color=blue')
                
                ui.label('Banco Central de Reserva del Perú').classes('text-gray-400 text-sm mb-4')
                
                with ui.row().classes('w-full justify-around mb-4'):
                    with ui.column().classes('items-center'):
                        ui.label('COMPRA').classes('text-xs text-gray-500')
                        bcrp_compra = ui.label('--').classes('text-2xl font-bold text-green-400')
                    with ui.column().classes('items-center'):
                        ui.label('VENTA').classes('text-xs text-gray-500')
                        bcrp_venta = ui.label('--').classes('text-2xl font-bold text-red-400')
                
                bcrp_spinner = ui.spinner('dots', size='lg').classes('mx-auto')
                bcrp_spinner.visible = False
                
                async def click_bcrp():
                    bcrp_spinner.visible = True
                    bcrp_compra.text = '...'
                    bcrp_venta.text = '...'
                    resultado = await ejecutar_scraper_bcrp()
                    datos_locales['bcrp'] = resultado
                    bcrp_compra.text = f"S/ {resultado['compra']:.4f}"
                    bcrp_venta.text = f"S/ {resultado['venta']:.4f}"
                    bcrp_spinner.visible = False
                    ui.notify('✅ BCRP actualizado', type='positive')
                    actualizar_mejor_opcion()
                
                ui.button('EJECUTAR BCRP', on_click=click_bcrp).props('push color=blue').classes('w-full')
            
            # === CARD KAMBISTA ===
            with ui.card().classes('w-80 p-6 bg-gray-800'):
                with ui.row().classes('items-center gap-3 mb-4'):
                    ui.icon('storefront').classes('text-3xl text-purple-500')
                    ui.label('Kambista').classes('text-xl font-bold text-white')
                    ui.badge('Selenium').props('color=purple')
                
                ui.label('Casa de cambio digital').classes('text-gray-400 text-sm mb-4')
                
                with ui.row().classes('w-full justify-around mb-4'):
                    with ui.column().classes('items-center'):
                        ui.label('COMPRA').classes('text-xs text-gray-500')
                        kambista_compra = ui.label('--').classes('text-2xl font-bold text-green-400')
                    with ui.column().classes('items-center'):
                        ui.label('VENTA').classes('text-xs text-gray-500')
                        kambista_venta = ui.label('--').classes('text-2xl font-bold text-red-400')
                
                kambista_spinner = ui.spinner('dots', size='lg').classes('mx-auto')
                kambista_spinner.visible = False
                
                async def click_kambista():
                    kambista_spinner.visible = True
                    kambista_compra.text = '...'
                    kambista_venta.text = '...'
                    resultado = await ejecutar_scraper_kambista()
                    datos_locales['kambista'] = resultado
                    kambista_compra.text = f"S/ {resultado['compra']:.4f}"
                    kambista_venta.text = f"S/ {resultado['venta']:.4f}"
                    kambista_spinner.visible = False
                    ui.notify('✅ Kambista actualizado', type='positive')
                    actualizar_mejor_opcion()
                
                ui.button('EJECUTAR KAMBISTA', on_click=click_kambista).props('push color=purple').classes('w-full')
            
            # === CARD REXTIE ===
            with ui.card().classes('w-80 p-6 bg-gray-800'):
                with ui.row().classes('items-center gap-3 mb-4'):
                    ui.icon('swap_horiz').classes('text-3xl text-orange-500')
                    ui.label('Rextie').classes('text-xl font-bold text-white')
                    ui.badge('Selenium').props('color=orange')
                
                ui.label('Casa de cambio digital').classes('text-gray-400 text-sm mb-4')
                
                with ui.row().classes('w-full justify-around mb-4'):
                    with ui.column().classes('items-center'):
                        ui.label('COMPRA').classes('text-xs text-gray-500')
                        rextie_compra = ui.label('--').classes('text-2xl font-bold text-green-400')
                    with ui.column().classes('items-center'):
                        ui.label('VENTA').classes('text-xs text-gray-500')
                        rextie_venta = ui.label('--').classes('text-2xl font-bold text-red-400')
                
                rextie_spinner = ui.spinner('dots', size='lg').classes('mx-auto')
                rextie_spinner.visible = False
                
                async def click_rextie():
                    rextie_spinner.visible = True
                    rextie_compra.text = '...'
                    rextie_venta.text = '...'
                    resultado = await ejecutar_scraper_rextie()
                    datos_locales['rextie'] = resultado
                    rextie_compra.text = f"S/ {resultado['compra']:.4f}"
                    rextie_venta.text = f"S/ {resultado['venta']:.4f}"
                    rextie_spinner.visible = False
                    ui.notify('✅ Rextie actualizado', type='positive')
                    actualizar_mejor_opcion()
                
                ui.button('EJECUTAR REXTIE', on_click=click_rextie).props('push color=orange').classes('w-full')
        
        # Botón ejecutar todos
        ui.separator().classes('my-8')
        
        with ui.row().classes('w-full justify-center'):
            async def ejecutar_todos():
                ui.notify('🚀 Ejecutando BCRP...', type='info')
                await click_bcrp()
                ui.notify('🚀 Ejecutando Kambista...', type='info')
                await click_kambista()
                ui.notify('🚀 Ejecutando Rextie...', type='info')
                await click_rextie()
                ui.notify('🏆 ¡Todos completados!', type='positive')
            
            ui.button('🚀 EJECUTAR TODOS', on_click=ejecutar_todos).props('push color=cyan size=xl').classes('px-12')
        
        # Sección Mejor Opción
        ui.separator().classes('my-8')
        
        with ui.card().classes('w-full max-w-4xl mx-auto p-6 bg-gray-800'):
            ui.label('🏆 Mejor Opción').classes('text-2xl font-bold text-white text-center mb-6')
            
            with ui.row().classes('w-full justify-around flex-wrap gap-8'):
                with ui.column().classes('items-center flex-1 min-w-64'):
                    ui.icon('shopping_cart').classes('text-4xl text-green-400 mb-2')
                    ui.label('Para COMPRAR USD').classes('text-xl text-white font-bold')
                    ui.label('(Busca el menor precio de VENTA)').classes('text-xs text-gray-500 mb-4')
                    mejor_comprar_fuente = ui.label('Ejecuta los scrapers').classes('text-2xl font-bold text-yellow-400')
                    mejor_comprar_precio = ui.label('').classes('text-lg text-gray-300')
                    mejor_comprar_ahorro = ui.label('').classes('text-sm text-green-400')
                
                with ui.column().classes('items-center flex-1 min-w-64'):
                    ui.icon('sell').classes('text-4xl text-cyan-400 mb-2')
                    ui.label('Para VENDER USD').classes('text-xl text-white font-bold')
                    ui.label('(Busca el mayor precio de COMPRA)').classes('text-xs text-gray-500 mb-4')
                    mejor_vender_fuente = ui.label('Ejecuta los scrapers').classes('text-2xl font-bold text-yellow-400')
                    mejor_vender_precio = ui.label('').classes('text-lg text-gray-300')
                    mejor_vender_ahorro = ui.label('').classes('text-sm text-cyan-400')
        
        def actualizar_mejor_opcion():
            mejor_comprar, mejor_vender = calcular_mejor_opcion(datos_locales)
            
            if mejor_comprar and mejor_vender:
                mejor_comprar_fuente.text = f"✅ {mejor_comprar['nombre']}"
                mejor_comprar_precio.text = f"Venta: S/ {mejor_comprar['venta']:.4f}"
                
                todas_ventas = [d['venta'] for d in datos_locales.values() if d is not None and d.get('venta')]
                if len(todas_ventas) > 1:
                    ahorro = (max(todas_ventas) - mejor_comprar['venta']) * 1000
                    mejor_comprar_ahorro.text = f"Ahorras S/ {ahorro:.2f} por cada $1,000"
                
                mejor_vender_fuente.text = f"✅ {mejor_vender['nombre']}"
                mejor_vender_precio.text = f"Compra: S/ {mejor_vender['compra']:.4f}"
                
                todas_compras = [d['compra'] for d in datos_locales.values() if d is not None and d.get('compra')]
                if len(todas_compras) > 1:
                    ganancia = (mejor_vender['compra'] - min(todas_compras)) * 1000
                    mejor_vender_ahorro.text = f"Ganas S/ {ganancia:.2f} más por cada $1,000"


# =============================================================================
# PÁGINA: ANÁLISIS (EN DESARROLLO - Fiorella completará)
# =============================================================================
@ui.page('/analisis')
def pagina_analisis():
    """Página de análisis comparativo - EN DESARROLLO."""
    ui.query('body').classes('bg-gray-900')
    
    crear_navbar()
    
    with ui.column().classes('w-full p-8'):
        with ui.row().classes('items-center gap-3 mb-2'):
            ui.icon('analytics').classes('text-3xl text-cyan-400')
            ui.label('Análisis Comparativo').classes('text-3xl font-bold text-white')
        ui.label('Visualización de datos y cálculo de ahorro potencial').classes('text-gray-400 mb-8')
        
        # Placeholder - Fiorella completará esta sección
        with ui.card().classes('w-full max-w-4xl mx-auto p-8 bg-gray-800'):
            ui.label('🚧 Sección en desarrollo').classes('text-2xl font-bold text-yellow-400 text-center mb-4')
            ui.label('Los gráficos comparativos y la calculadora serán agregados próximamente.').classes('text-gray-400 text-center')


# =============================================================================
# PÁGINA: EQUIPO
# =============================================================================
@ui.page('/equipo')
def pagina_equipo():
    """Página con información del equipo de desarrollo."""
    ui.query('body').classes('bg-gray-900')
    
    crear_navbar()
    
    with ui.column().classes('w-full p-8 items-center'):
        ui.label('👥 Nuestro Equipo').classes('text-4xl font-bold text-white mb-2')
        ui.label('Lenguaje de Programación 2 - UNALM 2025').classes('text-gray-400 mb-12')
        
        with ui.row().classes('gap-8 flex-wrap justify-center'):
            with ui.card().classes('w-72 p-6 bg-gray-800 text-center'):
                ui.label('👨‍💻').classes('text-6xl mb-4')
                ui.label('Javier Uraco').classes('text-xl font-bold text-white')
                ui.label('Líder del Proyecto').classes('text-cyan-400 text-sm mb-4')
                ui.label('BCRP, Rextie, Integrador, App Web').classes('text-gray-400 text-sm')
            
            with ui.card().classes('w-72 p-6 bg-gray-800 text-center'):
                ui.label('👩‍💻').classes('text-6xl mb-4')
                ui.label('Fiorella Fuentes').classes('text-xl font-bold text-white')
                ui.label('Desarrolladora').classes('text-purple-400 text-sm mb-4')
                ui.label('Scraper Kambista, App Web').classes('text-gray-400 text-sm')
            
            with ui.card().classes('w-72 p-6 bg-gray-800 text-center'):
                ui.label('👨‍💻').classes('text-6xl mb-4')
                ui.label('Sebastián Fernández').classes('text-xl font-bold text-white')
                ui.label('Documentación').classes('text-orange-400 text-sm mb-4')
                ui.label('README, Docs').classes('text-gray-400 text-sm')
        
        ui.separator().classes('my-12')
        
        with ui.card().classes('w-full max-w-3xl p-8 bg-gray-800'):
            ui.label('📚 Tecnologías').classes('text-2xl font-bold text-white mb-6')
            
            with ui.row().classes('gap-4 flex-wrap'):
                ui.badge('Python 3.10+').props('color=blue')
                ui.badge('Selenium').props('color=green')
                ui.badge('Requests').props('color=orange')
                ui.badge('NiceGUI').props('color=cyan')
                ui.badge('Plotly').props('color=pink')


# =============================================================================
# EJECUTAR APLICACIÓN
# =============================================================================
if __name__ in {"__main__", "__mp_main__"}:
    print("=" * 60)
    print("💱 COMPARADOR DE TIPO DE CAMBIO - PERÚ")
    print("=" * 60)
    print("🚀 Iniciando servidor...")
    print("🌐 Abre tu navegador en: http://localhost:8080")
    print("=" * 60)
    
    ui.run(
        title='TipoCambio.pe - Comparador de Tipo de Cambio',
        favicon='💱',
        dark=True,
        port=8080,
        reload=False
    )

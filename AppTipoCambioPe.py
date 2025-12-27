"""
💱 COMPARADOR DE TIPO DE CAMBIO PERÚ
LP2 - UNALM 2025
"""

from nicegui import ui
import plotly.graph_objects as go
import asyncio
import os
import sys

# Agregar carpeta src al path
sys.path.insert(0, os.path.join(os.path.dirname(_file_), 'src'))

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
# DATOS
# =============================================================================
def obtener_datos_demo():
    return {
        'bcrp': {'compra': 3.7320, 'venta': 3.7350, 'exito': True},
        'kambista': {'compra': 3.7100, 'venta': 3.7550, 'exito': True},
        'rextie': {'compra': 3.7200, 'venta': 3.7480, 'exito': True},
    }

# =============================================================================
# FUNCIONES ASYNC PARA SCRAPERS
# =============================================================================
async def ejecutar_scraper_bcrp():
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
    Para COMPRAR dólares: buscas el MENOR precio de VENTA
    Para VENDER dólares: buscas el MAYOR precio de COMPRA
    """
    fuentes_validas = []
    
    for nombre, info in datos.items():
        # CORREGIDO: Verificar que info no sea None antes de usar .get()
        if info is not None and info.get('compra') and info.get('venta') and info['compra'] > 0:
            fuentes_validas.append({
                'nombre': nombre.upper(),
                'compra': info['compra'],
                'venta': info['venta']
            })
    
    if not fuentes_validas:
        return None, None
    
    mejor_comprar = min(fuentes_validas, key=lambda x: x['venta'])
    mejor_vender = max(fuentes_validas, key=lambda x: x['compra'])
    
    return mejor_comprar, mejor_vender

# =============================================================================
# COMPONENTE: BARRA DE NAVEGACIÓN
# =============================================================================
def crear_navbar():
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
    ui.query('body').classes('bg-gray-900')
    
    crear_navbar()
    
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
    
    ui.label('¿Por qué TipoCambio.pe?').classes('text-3xl font-bold text-white text-center mb-8')
    
    with ui.row().classes('w-full justify-center gap-8 px-8 pb-16 flex-wrap'):
        with ui.card().classes('w-96 p-6 bg-gray-800 border-l-4 border-red-500'):
            ui.label('❌ El Problema').classes('text-xl font-bold text-red-400 mb-4')
            ui.label('Cada casa de cambio tiene tasas diferentes. Por cada $1,000 la diferencia puede ser de S/ 50 o más.').classes('text-gray-300')
        
        with ui.card().classes('w-96 p-6 bg-gray-800 border-l-4 border-green-500'):
            ui.label('✅ Nuestra Solución').classes('text-xl font-bold text-green-400 mb-4')
            ui.label('Sistema automatizado que extrae datos de múltiples fuentes y recomienda la mejor opción.').classes('text-gray-300')
    
    with ui.row().classes('w-full justify-center py-6 bg-gray-950'):
        ui.label('💱 TipoCambio.pe | LP2 - UNALM 2025').classes('text-gray-500')

# =============================================================================
# PÁGINA: DEMO
# =============================================================================
@ui.page('/demo')
def pagina_demo():
    ui.query('body').classes('bg-gray-900')
    
    crear_navbar()
    
    # Variables para los datos
    datos_locales = {'bcrp': None, 'kambista': None, 'rextie': None}
    
    with ui.column().classes('w-full p-8'):
        with ui.row().classes('items-center gap-3 mb-2'):
            ui.icon('sync').classes('text-3xl text-cyan-400')
            ui.label('Demo de Scrapers').classes('text-3xl font-bold text-white')
        ui.label('Ejecuta los scrapers individualmente o todos a la vez').classes('text-gray-400 mb-8')
        
        with ui.row().classes('w-full gap-6 flex-wrap justify-center'):
            
            # === BCRP ===
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
            
            # === KAMBISTA ===
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
            
            # === REXTIE ===
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
        
        # =================================================================
        # SECCIÓN: MEJOR OPCIÓN
        # =================================================================
        ui.separator().classes('my-8')
        
        with ui.card().classes('w-full max-w-4xl mx-auto p-6 bg-gray-800'):
            ui.label('🏆 Mejor Opción').classes('text-2xl font-bold text-white text-center mb-6')
            
            with ui.row().classes('w-full justify-around flex-wrap gap-8'):
                # Para COMPRAR USD
                with ui.column().classes('items-center flex-1 min-w-64'):
                    ui.icon('shopping_cart').classes('text-4xl text-green-400 mb-2')
                    ui.label('Para COMPRAR USD').classes('text-xl text-white font-bold')
                    ui.label('(Busca el menor precio de VENTA)').classes('text-xs text-gray-500 mb-4')
                    
                    mejor_comprar_fuente = ui.label('Ejecuta los scrapers').classes('text-2xl font-bold text-yellow-400')
                    mejor_comprar_precio = ui.label('').classes('text-lg text-gray-300')
                    mejor_comprar_ahorro = ui.label('').classes('text-sm text-green-400')
                
                # Para VENDER USD
                with ui.column().classes('items-center flex-1 min-w-64'):
                    ui.icon('sell').classes('text-4xl text-cyan-400 mb-2')
                    ui.label('Para VENDER USD').classes('text-xl text-white font-bold')
                    ui.label('(Busca el mayor precio de COMPRA)').classes('text-xs text-gray-500 mb-4')
                    
                    mejor_vender_fuente = ui.label('Ejecuta los scrapers').classes('text-2xl font-bold text-yellow-400')
                    mejor_vender_precio = ui.label('').classes('text-lg text-gray-300')
                    mejor_vender_ahorro = ui.label('').classes('text-sm text-cyan-400')
        
        # Función para actualizar (CORREGIDA)
        def actualizar_mejor_opcion():
            mejor_comprar, mejor_vender = calcular_mejor_opcion(datos_locales)
            
            if mejor_comprar and mejor_vender:
                # Actualizar mejor para COMPRAR
                mejor_comprar_fuente.text = f"✅ {mejor_comprar['nombre']}"
                mejor_comprar_precio.text = f"Venta: S/ {mejor_comprar['venta']:.4f}"
                
                # Calcular ahorro
                todas_ventas = [d['venta'] for d in datos_locales.values() if d is not None and d.get('venta')]
                if len(todas_ventas) > 1:
                    ahorro = (max(todas_ventas) - mejor_comprar['venta']) * 1000
                    mejor_comprar_ahorro.text = f"Ahorras S/ {ahorro:.2f} por cada $1,000"
                
                # Actualizar mejor para VENDER
                mejor_vender_fuente.text = f"✅ {mejor_vender['nombre']}"
                mejor_vender_precio.text = f"Compra: S/ {mejor_vender['compra']:.4f}"
                
                # Calcular ganancia
                todas_compras = [d['compra'] for d in datos_locales.values() if d is not None and d.get('compra')]
                if len(todas_compras) > 1:
                    ganancia = (mejor_vender['compra'] - min(todas_compras)) * 1000
                    mejor_vender_ahorro.text = f"Ganas S/ {ganancia:.2f} más por cada $1,000"

# =============================================================================
# PÁGINA: ANÁLISIS
# =============================================================================
@ui.page('/analisis')
def pagina_analisis():
    ui.query('body').classes('bg-gray-900')
    
    crear_navbar()
    
    datos = obtener_datos_demo()
    
    with ui.column().classes('w-full p-8'):
        with ui.row().classes('items-center gap-3 mb-2'):
            ui.icon('analytics').classes('text-3xl text-cyan-400')
            ui.label('Análisis Comparativo').classes('text-3xl font-bold text-white')
        ui.label('Visualización de datos y cálculo de ahorro potencial').classes('text-gray-400 mb-8')
        
        with ui.row().classes('w-full gap-8 flex-wrap justify-center'):
            
            # Gráfico de barras
            with ui.card().classes('flex-1 min-w-96 p-6 bg-gray-800'):
                ui.label('📊 Comparación de Tipos de Cambio').classes('text-xl font-bold text-white mb-4')
                
                fig = go.Figure()
                fuentes = ['BCRP', 'Kambista', 'Rextie']
                compras = [datos['bcrp']['compra'], datos['kambista']['compra'], datos['rextie']['compra']]
                ventas = [datos['bcrp']['venta'], datos['kambista']['venta'], datos['rextie']['venta']]
                
                fig.add_trace(go.Bar(name='Compra', x=fuentes, y=compras, marker_color='#00c853'))
                fig.add_trace(go.Bar(name='Venta', x=fuentes, y=ventas, marker_color='#ff5252'))
                
                fig.update_layout(
                    barmode='group',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    legend=dict(orientation='h', y=1.1),
                    margin=dict(l=20, r=20, t=40, b=20),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                
                ui.plotly(fig).classes('w-full h-80')
                
                with ui.expansion('¿Cómo interpretar?', icon='help').classes('w-full mt-4'):
                    ui.label('• VERDE = Precio COMPRA (lo que te pagan al vender USD)').classes('text-gray-300 text-sm')
                    ui.label('• ROJO = Precio VENTA (lo que pagas al comprar USD)').classes('text-gray-300 text-sm')
            
            # Gráfico de spreads
            with ui.card().classes('flex-1 min-w-96 p-6 bg-gray-800'):
                ui.label('📈 Análisis de Spreads').classes('text-xl font-bold text-white mb-4')
                
                spreads = [
                    datos['bcrp']['venta'] - datos['bcrp']['compra'],
                    datos['kambista']['venta'] - datos['kambista']['compra'],
                    datos['rextie']['venta'] - datos['rextie']['compra']
                ]
                
                fig2 = go.Figure(data=[
                    go.Bar(x=fuentes, y=spreads, marker_color=['#1565c0', '#7b1fa2', '#e65100'],
                           text=[f'S/ {s:.4f}' for s in spreads], textposition='outside')
                ])
                
                fig2.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    margin=dict(l=20, r=20, t=40, b=20),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Spread (S/)')
                )
                
                ui.plotly(fig2).classes('w-full h-80')
                
                with ui.expansion('¿Qué es el spread?', icon='help').classes('w-full mt-4'):
                    ui.label('• Spread = Venta - Compra').classes('text-gray-300 text-sm')
                    ui.label('• Es la ganancia de la casa de cambio').classes('text-gray-300 text-sm')
                    ui.label('• Spread BAJO = Mejor para ti').classes('text-green-400 text-sm')
        
        # Calculadora
        ui.separator().classes('my-8')
        
        with ui.card().classes('w-full max-w-xl mx-auto p-6 bg-gray-800'):
            ui.label('💰 Calculadora de Ahorro').classes('text-2xl font-bold text-white text-center mb-6')
            
            monto = ui.number('Monto en USD', value=1000, min=1, max=100000).classes('w-full mb-4')
            resultado = ui.label('Ingresa un monto y presiona calcular').classes('text-center text-lg text-gray-300 mt-4')
            
            def calcular():
                m = monto.value or 1000
                ventas = [datos['bcrp']['venta'], datos['kambista']['venta'], datos['rextie']['venta']]
                ahorro = (max(ventas) - min(ventas)) * m
                resultado.text = f'💵 Por ${m:,.0f} USD puedes ahorrar hasta S/ {ahorro:.2f}'
            
            ui.button('Calcular Ahorro', on_click=calcular).props('push color=cyan').classes('w-full')

# =============================================================================
# PÁGINA: EQUIPO
# =============================================================================
@ui.page('/equipo')
def pagina_equipo():
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
                ui.label('BCRP, Rextie, App Web').classes('text-gray-400 text-sm')
            
            with ui.card().classes('w-72 p-6 bg-gray-800 text-center'):
                ui.label('👩‍💻').classes('text-6xl mb-4')
                ui.label('Fiorella Fuentes').classes('text-xl font-bold text-white')
                ui.label('Desarrolladora').classes('text-purple-400 text-sm mb-4')
                ui.label('Scraper Kambista').classes('text-gray-400 text-sm')
            
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
# EJECUTAR
# =============================================================================
if _name_ in {"_main", "mp_main_"}:
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
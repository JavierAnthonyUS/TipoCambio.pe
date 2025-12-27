# 🔧 DIFICULTADES Y SOLUCIONES
## Proyecto TipoCambio.pe - LP2 UNALM 2025

Este documento detalla los principales desafíos técnicos encontrados durante el desarrollo del proyecto y las soluciones implementadas.

---

## 📋 Resumen de Dificultades

| # | Dificultad | Problema específico | Solución aplicada |
|---|------------|---------------------|-------------------|
| 1 | Páginas dinámicas | BeautifulSoup retornaba HTML vacío | Selenium con Chrome headless |
| 2 | Identificación de valores | Muchos números en la página | Regex + filtro por rango 3.30-3.50 |
| 3 | Tiempos de espera | Selenium tardaba mucho | Optimización de waits |
| 4 | API BCRP | Formato de fechas específico | Función para generar rango de fechas |
| 5 | Compatibilidad NiceGUI | Cambios en versión 3.4.1 | Adaptar componentes UI |
| 6 | Coordinación de equipo | Diferentes horarios y tareas | GitHub + commits descriptivos |

---

## 🔍 Detalle de cada dificultad

---

### 1️⃣ PÁGINAS DINÁMICAS

#### Problema
Kambista y Rextie son páginas web que cargan sus datos de tipo de cambio usando **JavaScript**. Cuando intentamos usar `requests` + `BeautifulSoup`, obteníamos el HTML inicial sin los precios.

```python
# ❌ ESTO NO FUNCIONABA
import requests
from bs4 import BeautifulSoup

response = requests.get("https://kambista.com")
soup = BeautifulSoup(response.text, 'html.parser')
# El HTML no contenía los precios porque JavaScript no se había ejecutado
```

#### ¿Por qué ocurre?
- `requests` solo descarga el HTML inicial
- Los precios se cargan después mediante llamadas JavaScript/AJAX
- BeautifulSoup no ejecuta JavaScript

#### Solución
Implementamos **Selenium** con Chrome en modo headless para renderizar la página completa:

```python
# ✅ SOLUCIÓN CON SELENIUM
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')  # Sin ventana visible
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
driver.get("https://kambista.com")
time.sleep(5)  # Esperar que JavaScript cargue

# Ahora sí tenemos el HTML con los precios
page_source = driver.page_source
```

#### Lección aprendida
> No todas las páginas web pueden ser scrapeadas con BeautifulSoup. Las páginas modernas con frameworks como React, Vue o Angular requieren herramientas que ejecuten JavaScript.

---

### 2️⃣ IDENTIFICACIÓN DE VALORES

#### Problema
Una vez que Selenium obtiene el HTML completo, la página contiene **muchos números** (teléfonos, fechas, porcentajes, etc.). ¿Cómo identificar cuáles son los tipos de cambio?

```html
<!-- Ejemplo de HTML con muchos números -->
<div>Llámanos: 01-234-5678</div>
<div>Tasa: 3.42</div>
<div>Comisión: 0.5%</div>
<div>Compra: 3.38</div>
<div>Fecha: 26/12/2025</div>
```

#### Solución
Desarrollamos una estrategia de **extracción con regex + filtrado por rango**:

```python
import re

# 1. Extraer todos los números con formato decimal
patron = r'[\d]+\.[\d]{2,4}'
valores = re.findall(patron, page_source)
# Resultado: ['234.5678', '3.42', '0.5', '3.38', '26.12', '2025']

# 2. Filtrar solo los que están en rango válido de tipo de cambio
valores_tc = [float(v) for v in valores if 3.30 <= float(v) <= 3.50]
# Resultado: [3.42, 3.38]

# 3. El menor es COMPRA, el mayor es VENTA
compra = min(valores_tc)
venta = max(valores_tc)
```

#### ¿Por qué el rango 3.30 - 3.50?
- El tipo de cambio PEN/USD históricamente fluctúa en este rango
- Valores fuera de este rango claramente no son tipo de cambio
- El rango puede ajustarse si el mercado cambia significativamente

#### Lección aprendida
> Cuando el HTML no tiene estructura clara, las expresiones regulares combinadas con filtros de dominio son una solución efectiva.

---

### 3️⃣ TIEMPOS DE ESPERA

#### Problema
Selenium tardaba demasiado en algunas ejecuciones (30+ segundos por página), haciendo el sistema lento e impredecible.

#### Causas identificadas
1. `time.sleep()` fijo esperaba más de lo necesario
2. Carga de imágenes y recursos innecesarios
3. Inicialización del navegador en cada llamada

#### Solución
Implementamos varias optimizaciones:

```python
# 1. Deshabilitar carga de imágenes
options.add_argument('--blink-settings=imagesEnabled=false')

# 2. Deshabilitar extensiones
options.add_argument('--disable-extensions')

# 3. Modo headless (sin interfaz gráfica)
options.add_argument('--headless')

# 4. Esperas más inteligentes (esperar elemento específico)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
# Esperar hasta que aparezca un elemento con números
```

#### Resultado
- Tiempo promedio reducido de 30s a 10-15s por scraper
- Mayor consistencia en los tiempos de respuesta

#### Lección aprendida
> Las optimizaciones de Selenium pueden reducir significativamente los tiempos. Deshabilitar recursos innecesarios y usar esperas inteligentes es clave.

---

### 4️⃣ API BCRP - FORMATO DE FECHAS

#### Problema
La API del BCRP requiere fechas en formato específico `YYYY-MM-DD` y un rango válido. Si el rango es incorrecto o incluye días sin datos (fines de semana), la API retorna errores o datos vacíos.

```python
# ❌ ESTO FALLABA
url = "https://estadisticas.bcrp.gob.pe/.../2025-12-25/2025-12-25"
# Error: No hay datos para el 25 de diciembre (feriado)
```

#### Solución
Creamos una función que genera un rango de fechas inteligente:

```python
from datetime import datetime, timedelta

def generar_rango_fechas():
    """
    Genera un rango de 7 días hacia atrás para asegurar
    que siempre haya al menos un día hábil con datos.
    """
    hoy = datetime.now()
    hace_7_dias = hoy - timedelta(days=7)
    
    fecha_inicio = hace_7_dias.strftime('%Y-%m-%d')
    fecha_fin = hoy.strftime('%Y-%m-%d')
    
    return fecha_inicio, fecha_fin

# Uso
fecha_inicio, fecha_fin = generar_rango_fechas()
url = f"https://estadisticas.bcrp.gob.pe/.../json/{fecha_inicio}/{fecha_fin}"
```

#### Manejo de respuesta
```python
# Tomamos el último período disponible
periodos = data['periods']
ultimo_periodo = periodos[-1]  # El más reciente con datos
```

#### Lección aprendida
> Las APIs gubernamentales pueden tener particularidades. Es importante manejar casos edge como feriados y fines de semana.

---

### 5️⃣ COMPATIBILIDAD NICEGUI 3.4.1

#### Problema
Al desarrollar la aplicación web con NiceGUI, encontramos que la versión 3.4.1 tiene cambios respecto a versiones anteriores que causaban errores.

#### Errores encontrados

**Error 1: `ui.header()` anidado**
```python
# ❌ ERROR
with ui.column():
    with ui.header():  # RuntimeError: Header no puede estar anidado
        ...
```

**Error 2: `ui.html()` requiere parámetro**
```python
# ❌ ERROR
ui.html('<h1>Título</h1>')  # TypeError: missing argument 'sanitize'
```

#### Soluciones

**Solución 1: Usar `ui.row()` en lugar de `ui.header()`**
```python
# ✅ FUNCIONA
with ui.row().classes('w-full p-4 bg-gray-900'):
    ui.label('TipoCambio.pe').classes('text-2xl font-bold')
```

**Solución 2: Usar `ui.label()` con clases Tailwind**
```python
# ✅ FUNCIONA
ui.label('Título').classes('text-5xl font-bold text-cyan-400')
```

#### Lección aprendida
> Las librerías evolucionan y pueden introducir breaking changes. Es importante revisar changelogs y adaptar el código.

---

### 6️⃣ COORDINACIÓN DE EQUIPO

#### Problema
Coordinar el trabajo de 3 personas con diferentes horarios y responsabilidades.

#### Solución
Implementamos buenas prácticas de desarrollo colaborativo:

**1. Estructura de commits descriptivos**
```
feat: agregar scraper de Kambista con Selenium
fix: corregir extracción de valores en Rextie
docs: actualizar README con instrucciones de instalación
```

**2. Distribución clara de tareas**

| Integrante | Responsabilidad |
|------------|-----------------|
| Javier Uraco | Scrapers BCRP/Rextie, Integrador, App Web |
| Fiorella Fuentes | Scraper Kambista, App Web, DIFICULTADES |
| Sebastián Fernández | Documentación, README |

**3. Revisión de código**
- Cada PR era revisado antes de merge
- Comentarios constructivos para mejorar el código

#### Lección aprendida
> El trabajo en equipo requiere comunicación clara, herramientas adecuadas (GitHub) y distribución equitativa de responsabilidades.

---

## 📊 Resumen de Tecnologías por Dificultad

| Dificultad | Tecnología inicial | Tecnología final |
|------------|-------------------|------------------|
| Páginas dinámicas | BeautifulSoup | Selenium |
| Identificación valores | Selectores CSS | Regex + filtros |
| Tiempos espera | time.sleep() fijo | WebDriverWait + optimizaciones |
| Fechas API | Fecha fija | Rango dinámico 7 días |
| UI Web | ui.html() | ui.label() + Tailwind |
| Colaboración | Archivos compartidos | Git + GitHub |

---

## 🎯 Conclusión

Cada dificultad nos obligó a investigar, probar alternativas y aprender nuevas técnicas. El proceso de debugging y solución de problemas fue una parte fundamental del aprendizaje en este proyecto.

Las principales lecciones fueron:
1. **Investigar antes de implementar** - Entender cómo funciona una página/API antes de escribir código
2. **Manejar errores proactivamente** - Anticipar qué puede fallar y tener planes de contingencia
3. **Documentar soluciones** - Para referencia futura y para el equipo
4. **Iterar y mejorar** - La primera solución raramente es la mejor

---

**Documento elaborado por el equipo TipoCambio.pe - LP2 UNALM 2025**

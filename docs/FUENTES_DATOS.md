# 📚 Documentación de Fuentes de Datos

## TipoCambio.pe - Fuentes de Información

**Última actualización:** Diciembre 2025
**Investigación realizada por:** Javier Uraco (@JavierAnthonyUS)
**Estado:** ✅ Todas las fuentes operativas

---

## 📋 Resumen de Fuentes

| Fuente | Tipo | Método | Estado | Archivo |
|--------|------|--------|--------|---------|
| **BCRP** | API REST | requests + JSON | ✅ Producción | `scraper_bcrp.py` |
| **Kambista** | Web Scraping | Selenium + regex | ✅ Producción | `scraper_kambista.py` |
| **Rextie** | Web Scraping | Selenium + regex | ✅ Producción | `scraper_rextie.py` |

---

## 1️⃣ BCRP (Banco Central de Reserva del Perú)

### Información General
- **URL Base:** `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/`
- **Tipo:** API REST pública (sin autenticación)
- **Formato respuesta:** JSON
- **Frecuencia de actualización:** Diaria (días hábiles)
- **Estado:** ✅ En producción

### Endpoint Utilizado
```
https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PD04638PD-PD04639PD/json/{fecha_inicio}/{fecha_fin}
```

### Series de Datos
| Código | Descripción |
|--------|-------------|
| `PD04638PD` | Tipo de cambio - Loss compra |
| `PD04639PD` | Tipo de cambio - Loss venta |

### Estructura de Respuesta JSON
```json
{
  "config": {
    "series": ["PD04638PD", "PD04639PD"],
    "names": {"PD04638PD": "TC Compra", "PD04639PD": "TC Venta"}
  },
  "periods": [
    {
      "name": "Dic.2025",
      "values": ["3.3666", "3.3630"]
    }
  ]
}
```

### Implementación
```python
# scraper_bcrp.py - Fragmento principal
import requests
from datetime import datetime, timedelta

def obtener_tipo_cambio_bcrp():
    fecha_fin = datetime.now().strftime("%Y-%m-%d")
    fecha_inicio = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    url = f"https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PD04638PD-PD04639PD/json/{fecha_inicio}/{fecha_fin}"
    
    response = requests.get(url, timeout=30)
    data = response.json()
    
    # Extraer último periodo disponible
    ultimo = data['periods'][-1]
    tc_compra = float(ultimo['values'][0])
    tc_venta = float(ultimo['values'][1])
    
    return {'tc_bcrp_compra': tc_compra, 'tc_bcrp_venta': tc_venta}
```

### Consideraciones
- ✅ Fuente oficial del gobierno peruano
- ✅ No requiere autenticación
- ✅ Datos confiables y estables
- ⚠️ No actualiza fines de semana ni feriados
- ⚠️ Puede haber retraso de 1 día en la publicación

---

## 2️⃣ Kambista

### Información General
- **URL:** `https://kambista.com`
- **Tipo:** Página web dinámica (JavaScript/Angular)
- **Método:** Web scraping con Selenium
- **Frecuencia de actualización:** Tiempo real
- **Estado:** ✅ En producción

### Análisis Técnico Realizado
```
Fecha de análisis: 21 de Diciembre, 2025
Resultado: Página DINÁMICA - requiere Selenium
```

**Hallazgos:**
1. El HTML inicial NO contiene los tipos de cambio
2. Los datos se cargan mediante JavaScript después del renderizado
3. `requests.get()` solo obtiene un HTML vacío
4. Solución: Selenium con Chrome headless

### robots.txt
```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
```
✅ Permite scraping del contenido público

### Implementación Final
```python
# scraper_kambista.py - Fragmento principal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

def obtener_tipo_cambio_kambista():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://kambista.com")
    time.sleep(3)  # Esperar carga de JavaScript
    
    html = driver.page_source
    driver.quit()
    
    # Extraer valores con regex
    patron = r'[\d]+\.[\d]{2,4}'
    matches = re.findall(patron, html)
    
    # Filtrar valores en rango de TC (3.30 - 3.50)
    valores_tc = [float(m) for m in matches if 3.30 <= float(m) <= 3.50]
    valores_tc = sorted(set(valores_tc))
    
    return {
        'tc_kambista_compra': valores_tc[0],   # Menor valor
        'tc_kambista_venta': valores_tc[-1]    # Mayor valor
    }
```

### Consideraciones
- ✅ Casa de cambio digital popular en Perú
- ✅ Actualización en tiempo real
- ⚠️ Requiere Selenium (más lento que API)
- ⚠️ Estructura HTML puede cambiar sin aviso
- ⚠️ Spread típicamente más alto que BCRP

---

## 3️⃣ Rextie

### Información General
- **URL:** `https://rextie.com`
- **Tipo:** Página web dinámica (JavaScript/Angular)
- **Método:** Web scraping con Selenium
- **Frecuencia de actualización:** Tiempo real
- **Estado:** ✅ En producción

### Análisis Técnico Realizado
```
Fecha de análisis: 21 de Diciembre, 2025
Resultado: Página DINÁMICA - requiere Selenium
```

**Hallazgos:**
1. Usa framework Angular
2. Componente principal: `<app-gql-exchange-rate>`
3. Los valores aparecen en elementos con clase `font-semibold text-xs`
4. Formato: `s/ 3.3535` (con prefijo "s/")
5. `requests.get()` no obtiene los valores, requiere Selenium

### Implementación Final
```python
# scraper_rextie.py - Fragmento principal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

def obtener_tipo_cambio_rextie():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://rextie.com")
    time.sleep(3)  # Esperar carga de JavaScript
    
    html = driver.page_source
    driver.quit()
    
    # Extraer valores con regex
    patron = r'[\d]+\.[\d]{2,4}'
    matches = re.findall(patron, html)
    
    # Filtrar valores en rango de TC (3.30 - 3.50)
    valores_tc = [float(m) for m in matches if 3.30 <= float(m) <= 3.50]
    valores_tc = sorted(set(valores_tc))
    
    return {
        'tc_rextie_compra': valores_tc[0],   # Menor valor
        'tc_rextie_venta': valores_tc[-1]    # Mayor valor
    }
```

### Consideraciones
- ✅ Casa de cambio digital con buenos volúmenes
- ✅ Actualización en tiempo real
- ⚠️ Requiere Selenium (más lento que API)
- ⚠️ Framework Angular puede dificultar scraping
- ⚠️ Spread moderado comparado con otras casas

---

## 🔧 Configuración de Selenium

Todas las fuentes dinámicas usan la misma configuración:

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--headless')              # Sin ventana visible
options.add_argument('--disable-gpu')           # Deshabilitar GPU
options.add_argument('--no-sandbox')            # Requerido en algunos sistemas
options.add_argument('--disable-dev-shm-usage') # Evitar problemas de memoria
options.add_argument('--window-size=1920,1080') # Tamaño de ventana
options.add_argument('--log-level=3')           # Reducir logs

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
```

**Dependencias requeridas:**
```
selenium>=4.39.0
webdriver-manager>=4.0.2
```

---

## ⚠️ Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Cambio en estructura HTML | Media | Alto | Logging detallado, monitoreo de errores |
| API BCRP no disponible | Baja | Medio | Reintentos automáticos, uso de cache |
| Bloqueo por exceso de peticiones | Baja | Alto | Respetar intervalos (1 hora), headers realistas |
| Timeout en Selenium | Media | Bajo | Manejo de excepciones, tiempos de espera configurables |

---

## 📜 Consideraciones Éticas

### Cumplimiento Legal
- ✅ BCRP: API pública, datos abiertos del gobierno
- ✅ Kambista: robots.txt permite scraping de contenido público
- ✅ Rextie: Datos públicos visibles sin login

### Buenas Prácticas Implementadas
- Intervalo mínimo de 1 hora entre extracciones
- User-Agent realista en las peticiones
- No se almacenan datos personales
- Uso exclusivamente académico
- Respeto a términos de servicio

---

## 📅 Historial de Cambios

| Fecha | Versión | Cambio |
|-------|---------|--------|
| 20/12/2025 | 1.0 | Documentación inicial con diseño propuesto |
| 21/12/2025 | 1.5 | Análisis técnico: Kambista y Rextie requieren Selenium |
| 21/12/2025 | 2.0 | Implementación completa con Selenium, estado: producción |
| 22/12/2025 | 2.0 | Actualización de documentación final |

---

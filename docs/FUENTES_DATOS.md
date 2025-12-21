# 📚 Documentación de Fuentes de Datos

## TipoCambio.pe - Fuentes de Información

**Última actualización:** Diciembre 2025
**Investigación realizada por:** Javier Uraco (@JavierAnthonyUS)

---

## Resumen Ejecutivo

| Fuente | Tipo | Estado | Método Requerido |
|--------|------|--------|------------------|
| **BCRP** | API REST | ✅ Funcionando | requests + JSON |
| **Kambista** | Página Dinámica | ⚠️ Requiere Selenium | Selenium WebDriver |
| **Rextie** | Página Dinámica | ⚠️ Requiere Selenium | Selenium WebDriver |

---

## 1. API del Banco Central de Reserva del Perú (BCRP)

### Información General

| Atributo | Valor |
|----------|-------|
| **Nombre** | API de Estadísticas BCRP |
| **Tipo** | API REST pública |
| **Formato** | JSON / XML |
| **Autenticación** | No requerida |
| **Estado** | ✅ **FUNCIONANDO** |
| **Documentación** | https://estadisticas.bcrp.gob.pe/estadisticas/series/ayuda/api |

### Endpoint Base
```
https://estadisticas.bcrp.gob.pe/estadisticas/series/api/
```

### Series de Tipo de Cambio

| Código Serie | Descripción | Unidad |
|--------------|-------------|--------|
| `PD04638PD` | Tipo de cambio - Compra | Soles por dólar |
| `PD04639PD` | Tipo de cambio - Venta | Soles por dólar |

### Formato de Consulta
```
https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{series}/{formato}/{fecha_inicio}/{fecha_fin}
```

### Ejemplo de Consulta Exitosa
```
URL: https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PD04638PD-PD04639PD/json/2025-12-13/2025-12-20

Respuesta:
- tc_bcrp_compra: 3.3666
- tc_bcrp_venta: 3.3630
- fecha: 18.Dic.25
```

### Consideraciones

- ✅ **Ventaja:** Fuente oficial del gobierno peruano
- ✅ **Ventaja:** API pública sin autenticación
- ✅ **Ventaja:** Datos confiables y estables
- ⚠️ **Limitación:** Actualización diaria (no intradía)

---

## 2. Kambista

### Información General

| Atributo | Valor |
|----------|-------|
| **Nombre** | Kambista |
| **Tipo** | Casa de cambio digital |
| **URL** | https://kambista.com |
| **Estado** | ⚠️ **REQUIERE SELENIUM** |

### Análisis Técnico (20 Dic 2025)

**Resultado de prueba con requests + BeautifulSoup:**
```
❌ No se encontraron las tasas
Diagnóstico: Página dinámica (contenido cargado con JavaScript)
```

**robots.txt:**
```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
```

### Hallazgos

1. La página utiliza **JavaScript/Angular** para cargar el contenido
2. Las tasas de cambio NO están en el HTML inicial
3. Se cargan dinámicamente después de que la página renderiza
4. **Solución requerida:** Selenium WebDriver para ejecutar JavaScript

### Implementación Recomendada para Fiorella
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar Chrome en modo headless
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)
driver.get("https://kambista.com")

# Esperar a que carguen las tasas (ajustar selector)
wait = WebDriverWait(driver, 10)
# Buscar elementos con las tasas...

driver.quit()
```

---

## 3. Rextie

### Información General

| Atributo | Valor |
|----------|-------|
| **Nombre** | Rextie |
| **Tipo** | Casa de cambio digital |
| **URL** | https://rextie.com |
| **Estado** | ⚠️ **REQUIERE SELENIUM** |

### Análisis Técnico (20 Dic 2025)

**Resultado de prueba con requests + BeautifulSoup:**
```
❌ No se encontraron las tasas con el scraper básico
Diagnóstico: Página dinámica (Angular framework)
```

### Hallazgo Importante

Al analizar el HTML completo de la página, se encontró que **los datos SÍ están presentes** dentro del componente Angular, pero requieren renderización:
```html
<!-- Componente: app-gql-exchange-rate -->
<div class="font-semibold text-xs"> s/ 3.3535 </div>  <!-- Compra -->
<div class="font-semibold text-xs"> s/ 3.3825 </div>  <!-- Venta -->
```

**Datos encontrados en el análisis:**
- Compra: S/ 3.3535
- Venta: S/ 3.3825

### Estructura del HTML (para Sebastián)

La página usa Angular y los datos están en:
- Componente: `app-gql-exchange-rate`
- Clase CSS de los valores: `font-semibold text-xs`
- Los valores incluyen el prefijo "s/ "

### Implementación Recomendada para Sebastián
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

options = webdriver.ChromeOptions()
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)
driver.get("https://rextie.com")

# Esperar a que cargue el componente de tasas
wait = WebDriverWait(driver, 10)
elemento = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "app-gql-exchange-rate"))
)

# Extraer el HTML del componente
html = elemento.get_attribute('innerHTML')

# Buscar los valores con regex
valores = re.findall(r's/\s*([\d.]+)', html)
# valores[0] = compra, valores[1] = venta

driver.quit()
```

---

## 4. Comparación de Fuentes

| Característica | BCRP | Kambista | Rextie |
|----------------|------|----------|--------|
| Tipo de acceso | API REST | Web Scraping | Web Scraping |
| Tecnología requerida | requests | Selenium | Selenium |
| Frecuencia actualización | Diaria | Tiempo real | Tiempo real |
| Confiabilidad datos | Alta | Media | Media |
| Complejidad técnica | Baja | Alta | Alta |
| Riesgo de bloqueo | Ninguno | Medio | Medio |
| Tipo de tasa | Oficial | Comercial | Comercial |

---

## 5. Requisitos de Instalación

### Para BCRP (ya funcionando)
```bash
pip install requests
```

### Para Kambista y Rextie (Selenium)
```bash
pip install selenium webdriver-manager
```

También se necesita Chrome o Firefox instalado.

---

## 6. Consideraciones Éticas

- ✅ Frecuencia baja: máximo 1 petición por hora
- ✅ Respetar robots.txt de cada sitio
- ✅ No sobrecargar los servidores
- ✅ User-agent identificable
- ✅ Uso educativo/informativo

---

## 7. Plan de Contingencia

| Problema | Solución |
|----------|----------|
| API BCRP caída | Registrar como NULL, continuar con otras fuentes |
| Kambista bloqueó acceso | Reducir frecuencia, rotar User-Agent |
| Rextie cambió estructura | Actualizar selectores CSS |
| Selenium no funciona | Verificar versión de Chrome/ChromeDriver |

---

## 8. Conclusiones de la Investigación

1. **BCRP** es la fuente más confiable y fácil de implementar (API oficial)
2. **Kambista** y **Rextie** requieren Selenium debido a su arquitectura JavaScript
3. Los datos de Rextie están presentes en el HTML pero necesitan renderización
4. Se recomienda implementar manejo robusto de errores para las fuentes web

---

*Documento actualizado: 20/12/2025*
*Investigación técnica: Javier Uraco (@JavierAnthonyUS)*
# 📖 Diccionario de Datos

## Proyecto: TipoCambio.pe
---

## 📁 Archivo Principal: `tipo_cambio_historico.csv`

**Ubicación:** `data/processed/tipo_cambio_historico.csv`  
**Formato:** CSV (Comma Separated Values)  
**Encoding:** UTF-8  
**Separador:** Coma (,)

---

## 📊 Estructura de Columnas (13 columnas)

| # | Columna | Tipo | Descripción | Ejemplo |
|---|---------|------|-------------|---------|
| 1 | `timestamp` | datetime | Fecha y hora de la extracción (formato ISO) | `2025-12-21 22:19:22` |
| 2 | `tc_bcrp_compra` | float | Tipo de cambio de compra del BCRP | `3.3666` |
| 3 | `tc_bcrp_venta` | float | Tipo de cambio de venta del BCRP | `3.363` |
| 4 | `tc_kambista_compra` | float | Tipo de cambio de compra de Kambista | `3.33` |
| 5 | `tc_kambista_venta` | float | Tipo de cambio de venta de Kambista | `3.486` |
| 6 | `tc_rextie_compra` | float | Tipo de cambio de compra de Rextie | `3.35` |
| 7 | `tc_rextie_venta` | float | Tipo de cambio de venta de Rextie | `3.392` |
| 8 | `spread_bcrp` | float | Diferencia venta - compra del BCRP | `-0.0036` |
| 9 | `spread_kambista` | float | Diferencia venta - compra de Kambista | `0.156` |
| 10 | `spread_rextie` | float | Diferencia venta - compra de Rextie | `0.042` |
| 11 | `mejor_compra` | string | Fuente recomendada para comprar USD | `BCRP` |
| 12 | `mejor_venta` | string | Fuente recomendada para vender USD | `BCRP` |
| 13 | `cambio_detectado` | boolean | Indica si hubo cambio respecto al registro anterior | `True` |

---

## 📝 Descripción Detallada de Columnas

### 1. `timestamp`
- **Descripción:** Marca temporal del momento exacto de la extracción
- **Formato:** `YYYY-MM-DD HH:MM:SS`
- **Zona horaria:** Hora local de Perú (UTC-5)
- **Generado por:** Función `obtener_timestamp()` en `utils.py`

### 2-3. `tc_bcrp_compra` / `tc_bcrp_venta`
- **Fuente:** API oficial del BCRP
- **Precisión:** 4 decimales
- **Actualización:** Diaria (días hábiles)
- **Valores típicos:** 3.30 - 3.70
- **Valores nulos:** Posibles en feriados o fines de semana

### 4-5. `tc_kambista_compra` / `tc_kambista_venta`
- **Fuente:** Web scraping de kambista.com con Selenium
- **Precisión:** 2-4 decimales
- **Actualización:** Tiempo real
- **Valores típicos:** 3.30 - 3.50
- **Valores nulos:** Posibles si el scraping falla

### 6-7. `tc_rextie_compra` / `tc_rextie_venta`
- **Fuente:** Web scraping de rextie.com con Selenium
- **Precisión:** 2-4 decimales
- **Actualización:** Tiempo real
- **Valores típicos:** 3.30 - 3.50
- **Valores nulos:** Posibles si el scraping falla

### 8-10. `spread_*`
- **Cálculo:** `tasa_venta - tasa_compra`
- **Interpretación:** Representa el margen de ganancia de la entidad
- **Valores típicos:** 
  - Casas de cambio: 0.02 - 0.20 (positivo)
  - BCRP: Puede ser negativo (ver nota)
- **Generado por:** Función `calcular_spread()` en `utils.py`

> ⚠️ **Nota sobre spreads negativos:** El BCRP puede mostrar spreads negativos porque sus tasas de compra y venta son valores de referencia del mercado interbancario, no precios para el público. Esto es normal y no indica un error en la extracción.

### 11. `mejor_compra`
- **Descripción:** Fuente con la tasa de venta más baja (mejor para el usuario que quiere comprar dólares)
- **Valores posibles:** `BCRP`, `Kambista`, `Rextie`
- **Lógica:** `min(tc_*_venta)`
- **Generado por:** Función `determinar_mejor_opcion()` en `utils.py`

### 12. `mejor_venta`
- **Descripción:** Fuente con la tasa de compra más alta (mejor para el usuario que quiere vender dólares)
- **Valores posibles:** `BCRP`, `Kambista`, `Rextie`
- **Lógica:** `max(tc_*_compra)`
- **Generado por:** Función `determinar_mejor_opcion()` en `utils.py`

### 13. `cambio_detectado`
- **Descripción:** Indica si algún valor cambió respecto al registro anterior
- **Valores:** `True` o `False`
- **Uso:** Evita registros duplicados cuando no hay cambios
- **Generado por:** Función `hubo_cambio()` en `utils.py`

---

## 🔍 Validaciones Implementadas

| Validación | Descripción | Implementación |
|------------|-------------|----------------|
| Rango de TC | Valores entre 3.0 y 5.0 | Filtro en scrapers |
| Formato numérico | Solo números con decimales válidos | Regex en scrapers |
| Timestamps únicos | No duplicar extracciones idénticas | `hubo_cambio()` |
| Valores nulos | Se permiten si la fuente falla | Manejo de excepciones |
| Spread | Se permite cualquier valor (positivo o negativo) | Sin restricción |

---

## 📈 Ejemplo de Registro Real

```csv
timestamp,tc_bcrp_compra,tc_bcrp_venta,tc_kambista_compra,tc_kambista_venta,tc_rextie_compra,tc_rextie_venta,spread_bcrp,spread_kambista,spread_rextie,mejor_compra,mejor_venta,cambio_detectado
2025-12-21 22:19:22,3.3666,3.363,3.33,3.486,3.35,3.392,-0.0036,0.156,0.042,BCRP,BCRP,True
```

---

## 🔗 Relación con el Código

| Columna | Función que la genera | Archivo |
|---------|----------------------|---------|
| `timestamp` | `obtener_timestamp()` | `utils.py` |
| `tc_bcrp_*` | `obtener_tipo_cambio_bcrp()` | `scraper_bcrp.py` |
| `tc_kambista_*` | `obtener_tipo_cambio_kambista()` | `scraper_kambista.py` |
| `tc_rextie_*` | `obtener_tipo_cambio_rextie()` | `scraper_rextie.py` |
| `spread_*` | `calcular_spread()` | `utils.py` |
| `mejor_*` | `determinar_mejor_opcion()` | `utils.py` |
| `cambio_detectado` | `hubo_cambio()` | `utils.py` |

---

## 📚 Uso del Archivo

### Cargar en Python (Pandas)
```python
import pandas as pd
df = pd.read_csv('data/processed/tipo_cambio_historico.csv')
```

### Cargar en Excel
1. Abrir Excel
2. Datos → Obtener datos → Desde archivo CSV
3. Seleccionar el archivo
4. Usar coma como delimitador

### Análisis recomendado
- Ver `notebooks/analisis_exploratorio.ipynb` para ejemplos de visualización
- Comparar spreads entre fuentes
- Identificar tendencias en el tiempo
- Calcular ahorro potencial por fuente

---

# 📋 Planificación del Proyecto

## TipoCambio.pe - Diseño y Desarrollo

---

## 1. Objetivos del Proyecto

### Objetivo General
Desarrollar un sistema automatizado de extracción y comparación de tipos de cambio de múltiples fuentes en Perú, generando un dataset histórico estructurado.

### Objetivos Específicos
1. Extraer datos del tipo de cambio oficial del BCRP mediante su API REST
2. Realizar web scraping de casas de cambio digitales (Kambista, Rextie)
3. Integrar las fuentes en un dataset unificado con estructura consistente
4. Automatizar la extracción cada 1 hora con detección de cambios
5. Documentar el código siguiendo buenas prácticas de Python

---

## 2. Cronograma de Desarrollo

| Fase | Tarea | Responsable | Fecha | Estado |
|------|-------|-------------|-------|--------|
| 1 | Crear repositorio GitHub | Javier | 13/12/2024 | ✅ |
| 1 | Definir estructura del proyecto | Equipo | 13/12/2024 | ✅ |
| 2 | Desarrollar scraper BCRP | Javier | 14/12/2024 | ⏳ |
| 2 | Desarrollar scraper Kambista | Fiorella | 14/12/2024 | ⏳ |
| 2 | Desarrollar scraper Rextie | Sebastián | 14/12/2024 | ⏳ |
| 3 | Integrar fuentes | Javier | 15/12/2024 | ⏳ |
| 3 | Testing y correcciones | Equipo | 15/12/2024 | ⏳ |
| 4 | Documentación final | Fiorella | 15/12/2024 | ⏳ |
| 4 | Preparar presentación | Equipo | 16/12/2024 | ⏳ |
| 5 | **Exposición final** | Equipo | 16/12/2024 | ⏳ |

---

## 3. Diseño de la Extracción

### 3.1 Fuente 1: API BCRP

**Endpoint:** 
```
https://estadisticas.bcrp.gob.pe/estadisticas/series/api/[series]/[formato]/[periodo_inicial]/[periodo_final]
```

**Series utilizadas:**
- `PD04638PD` - Tipo de cambio compra
- `PD04639PD` - Tipo de cambio venta

**Proceso:**
1. Construir URL con fecha actual
2. Hacer petición GET con requests
3. Parsear respuesta JSON
4. Extraer valores de compra y venta
5. Retornar diccionario con datos

**Manejo de errores:**
- Timeout de conexión
- Error de parseo JSON
- Datos no disponibles

### 3.2 Fuente 2: Web Scraping Kambista

**URL:** `https://kambista.com`

**Proceso:**
1. Hacer petición GET con headers de navegador
2. Parsear HTML con BeautifulSoup
3. Localizar elementos con tasas de cambio
4. Extraer valores numéricos
5. Retornar diccionario con datos

**Selectores CSS/XPath:**
- Tasa compra: (por definir tras inspección)
- Tasa venta: (por definir tras inspección)

**Consideraciones éticas:**
- Respetar robots.txt
- Frecuencia baja (1 petición/hora)
- User-agent realista

### 3.3 Fuente 3: Web Scraping Rextie

**URL:** `https://rextie.com`

**Proceso:** Similar a Kambista

**Selectores CSS/XPath:**
- Tasa compra: (por definir tras inspección)
- Tasa venta: (por definir tras inspección)

---

## 4. Diseño de Integración de Datos

### 4.1 Flujo de Datos

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  API BCRP   │     │  Kambista   │     │   Rextie    │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌──────────────────────────────────────────────────────┐
│                    INTEGRADOR                         │
│  - Combina datos de 3 fuentes                        │
│  - Calcula spreads                                   │
│  - Determina mejor opción                            │
│  - Detecta cambios vs registro anterior              │
└──────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│              tipo_cambio_historico.csv               │
└──────────────────────────────────────────────────────┘
```

### 4.2 Lógica de Detección de Cambios

```python
def hubo_cambio(datos_nuevos, datos_anteriores):
    """
    Compara datos nuevos con el último registro.
    Retorna True si algún valor cambió.
    """
    campos_a_comparar = [
        'tc_bcrp_compra', 'tc_bcrp_venta',
        'tc_kambista_compra', 'tc_kambista_venta',
        'tc_rextie_compra', 'tc_rextie_venta'
    ]
    
    for campo in campos_a_comparar:
        if datos_nuevos[campo] != datos_anteriores[campo]:
            return True
    return False
```

### 4.3 Cálculo de Métricas

```python
# Spread = Venta - Compra
spread_bcrp = tc_bcrp_venta - tc_bcrp_compra
spread_kambista = tc_kambista_venta - tc_kambista_compra
spread_rextie = tc_rextie_venta - tc_rextie_compra

# Mejor opción para COMPRAR dólares (quiero el precio más bajo de venta)
mejor_compra = min([
    ('BCRP', tc_bcrp_venta),
    ('Kambista', tc_kambista_venta),
    ('Rextie', tc_rextie_venta)
], key=lambda x: x[1])[0]

# Mejor opción para VENDER dólares (quiero el precio más alto de compra)
mejor_venta = max([
    ('BCRP', tc_bcrp_compra),
    ('Kambista', tc_kambista_compra),
    ('Rextie', tc_rextie_compra)
], key=lambda x: x[1])[0]
```

---

## 5. Estructura del CSV Final

### Ejemplo de registro:

```csv
timestamp,tc_bcrp_compra,tc_bcrp_venta,tc_kambista_compra,tc_kambista_venta,tc_rextie_compra,tc_rextie_venta,spread_bcrp,spread_kambista,spread_rextie,mejor_compra,mejor_venta
2024-12-13 10:00:00,3.720,3.760,3.735,3.755,3.730,3.750,0.040,0.020,0.020,Rextie,Kambista
```

---

## 6. Automatización

### Usando schedule (Python)

```python
import schedule
import time

def job():
    print("Ejecutando extracción...")
    ejecutar_extraccion()

# Programar cada 1 hora
schedule.every(1).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 7. Distribución de Trabajo

### Javier Uraco (@JavierAnthonyUS)
- [x] Crear repositorio GitHub
- [ ] Desarrollar `scraper_bcrp.py`
- [ ] Desarrollar `integrador.py`
- [ ] Configurar automatización

### Fiorella Fuentes (@fiorellafuentesb20-cell)
- [ ] Desarrollar `scraper_kambista.py`
- [ ] Documentar fuentes de datos
- [ ] Crear diccionario de datos
- [ ] Revisar README

### Sebastián Fernández (@TucoSquare)
- [ ] Desarrollar `scraper_rextie.py`
- [ ] Desarrollar `utils.py`
- [ ] Testing de scrapers
- [ ] Preparar datos de ejemplo

---

## 8. Riesgos Identificados

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Bloqueo por scraping | Media | Alto | Frecuencia baja, headers realistas |
| Cambio en estructura HTML | Alta | Medio | Código modular, fácil actualización |
| API BCRP caída | Baja | Medio | Try-catch, continuar con otras fuentes |
| Conflictos en Git | Media | Bajo | Comunicación, ramas separadas |

---

## 9. Criterios de Éxito

- ✅ Extracción funcional de 3 fuentes
- ✅ Dataset CSV con al menos 24 registros (1 día de datos)
- ✅ Código documentado con docstrings
- ✅ Commits de todos los integrantes en GitHub
- ✅ Exposición clara de 20-25 minutos

---

*Documento creado: 13/12/2024*
*Última actualización: 13/12/2024*

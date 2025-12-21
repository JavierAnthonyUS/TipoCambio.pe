# 📖 Diccionario de Datos

## TipoCambio.pe - Descripción de Variables

---

## Dataset Principal: `tipo_cambio_historico.csv`

Este archivo contiene el registro histórico consolidado de todos los tipos de cambio extraídos.

---

### Variables del Dataset

| # | Variable | Tipo | Descripción | Ejemplo | Fuente |
|---|----------|------|-------------|---------|--------|
| 1 | `timestamp` | datetime | Fecha y hora exacta de la extracción | `2025-12-13 10:00:00` | Sistema |
| 2 | `tc_bcrp_compra` | float | Tipo de cambio oficial de COMPRA del BCRP | `3.720` | API BCRP |
| 3 | `tc_bcrp_venta` | float | Tipo de cambio oficial de VENTA del BCRP | `3.760` | API BCRP |
| 4 | `tc_kambista_compra` | float | Tasa de COMPRA de Kambista | `3.735` | Web Scraping |
| 5 | `tc_kambista_venta` | float | Tasa de VENTA de Kambista | `3.755` | Web Scraping |
| 6 | `tc_rextie_compra` | float | Tasa de COMPRA de Rextie | `3.730` | Web Scraping |
| 7 | `tc_rextie_venta` | float | Tasa de VENTA de Rextie | `3.750` | Web Scraping |
| 8 | `spread_bcrp` | float | Diferencia entre venta y compra BCRP | `0.040` | Calculado |
| 9 | `spread_kambista` | float | Diferencia entre venta y compra Kambista | `0.020` | Calculado |
| 10 | `spread_rextie` | float | Diferencia entre venta y compra Rextie | `0.020` | Calculado |
| 11 | `mejor_compra` | string | Fuente con mejor tasa para comprar USD | `Rextie` | Calculado |
| 12 | `mejor_venta` | string | Fuente con mejor tasa para vender USD | `Kambista` | Calculado |
| 13 | `cambio_detectado` | boolean | Indica si hubo variación respecto al registro anterior | `True` | Calculado |

---

## Descripción Detallada de Variables

### 1. `timestamp`

- **Tipo:** datetime
- **Formato:** `YYYY-MM-DD HH:MM:SS`
- **Descripción:** Momento exacto en que se realizó la extracción de datos
- **Frecuencia:** Cada 1 hora (si hay cambios detectados)
- **Zona horaria:** Perú (UTC-5)

### 2-3. `tc_bcrp_compra` / `tc_bcrp_venta`

- **Tipo:** float (4 decimales)
- **Unidad:** Soles por dólar (PEN/USD)
- **Rango esperado:** 3.00 - 5.00
- **Fuente:** API oficial del Banco Central de Reserva del Perú
- **Interpretación:**
  - `tc_bcrp_compra`: Precio al que el mercado compra dólares
  - `tc_bcrp_venta`: Precio al que el mercado vende dólares
- **Valores especiales:** `NULL` si la API no está disponible

### 4-5. `tc_kambista_compra` / `tc_kambista_venta`

- **Tipo:** float (4 decimales)
- **Unidad:** Soles por dólar (PEN/USD)
- **Rango esperado:** 3.00 - 5.00
- **Fuente:** Web scraping de https://kambista.com
- **Interpretación:**
  - `tc_kambista_compra`: Precio al que Kambista compra tus dólares
  - `tc_kambista_venta`: Precio al que Kambista te vende dólares
- **Valores especiales:** `NULL` si el scraping falla

### 6-7. `tc_rextie_compra` / `tc_rextie_venta`

- **Tipo:** float (4 decimales)
- **Unidad:** Soles por dólar (PEN/USD)
- **Rango esperado:** 3.00 - 5.00
- **Fuente:** Web scraping de https://rextie.com
- **Interpretación:**
  - `tc_rextie_compra`: Precio al que Rextie compra tus dólares
  - `tc_rextie_venta`: Precio al que Rextie te vende dólares
- **Valores especiales:** `NULL` si el scraping falla

### 8-10. `spread_*`

- **Tipo:** float (4 decimales)
- **Fórmula:** `spread = tasa_venta - tasa_compra`
- **Interpretación:** Margen de ganancia de cada fuente
- **Menor spread = Mejor para el usuario**

### 11. `mejor_compra`

- **Tipo:** string
- **Valores posibles:** `"BCRP"`, `"Kambista"`, `"Rextie"`
- **Lógica:** Fuente con la **menor tasa de VENTA**
- **Interpretación:** Si quieres COMPRAR dólares, esta fuente te cobra menos soles

### 12. `mejor_venta`

- **Tipo:** string
- **Valores posibles:** `"BCRP"`, `"Kambista"`, `"Rextie"`
- **Lógica:** Fuente con la **mayor tasa de COMPRA**
- **Interpretación:** Si quieres VENDER dólares, esta fuente te da más soles

### 13. `cambio_detectado`

- **Tipo:** boolean
- **Valores:** `True` o `False`
- **Lógica:** Compara con el registro inmediatamente anterior
- **Uso:** Permite filtrar solo los momentos de cambio real

---

## Conceptos Clave

### ¿Qué es "Compra" vs "Venta"?

Desde la perspectiva de la **casa de cambio**:

| Término | Significado | Para el usuario |
|---------|-------------|-----------------|
| **Compra** | La casa COMPRA tus dólares | Tú VENDES dólares |
| **Venta** | La casa VENDE dólares | Tú COMPRAS dólares |

### ¿Qué es el Spread?

El **spread** es la diferencia entre la tasa de venta y la tasa de compra. Es la ganancia de la casa de cambio.

```
Spread = Tasa Venta - Tasa Compra
```

**Ejemplo:**
- Kambista compra a 3.735 y vende a 3.755
- Spread = 3.755 - 3.735 = 0.020 (2 centavos por dólar)

---

## Validaciones de Datos

| Regla | Descripción |
|-------|-------------|
| Rango de TC | 3.00 ≤ tipo_cambio ≤ 5.00 |
| Spread positivo | tasa_venta > tasa_compra |
| Timestamp válido | Formato datetime correcto |
| Sin duplicados | Mismo timestamp no debe repetirse |

---

## Ejemplo de Registro

```csv
timestamp,tc_bcrp_compra,tc_bcrp_venta,tc_kambista_compra,tc_kambista_venta,tc_rextie_compra,tc_rextie_venta,spread_bcrp,spread_kambista,spread_rextie,mejor_compra,mejor_venta,cambio_detectado
2025-12-13 10:00:00,3.7200,3.7600,3.7350,3.7550,3.7300,3.7500,0.0400,0.0200,0.0200,Rextie,Kambista,True
2025-12-13 11:00:00,3.7200,3.7600,3.7360,3.7560,3.7300,3.7500,0.0400,0.0200,0.0200,Rextie,Kambista,True
2025-12-13 12:00:00,3.7200,3.7600,3.7360,3.7560,3.7300,3.7500,0.0400,0.0200,0.0200,Rextie,Kambista,False
```

---

*Documento creado: 13/12/2025*
*Última actualización: 13/12/2025*

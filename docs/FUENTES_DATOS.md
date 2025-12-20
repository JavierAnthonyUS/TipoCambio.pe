# 📚 Documentación de Fuentes de Datos

## TipoCambio.pe - Fuentes de Información

---

## 1. API del Banco Central de Reserva del Perú (BCRP)

### Información General

| Atributo | Valor |
|----------|-------|
| **Nombre** | API de Estadísticas BCRP |
| **Tipo** | API REST pública |
| **Formato** | JSON / XML |
| **Autenticación** | No requerida |
| **Documentación** | https://estadisticas.bcrp.gob.pe/estadisticas/series/ayuda/api |

### Endpoint Base

```
https://estadisticas.bcrp.gob.pe/estadisticas/series/api/
```

### Series de Tipo de Cambio

| Código Serie | Descripción | Unidad |
|--------------|-------------|--------|
| `PD04638PD` | Tipo de cambio - Loss – promedio del periodo (S/ por US$) - Compra | Soles por dólar |
| `PD04639PD` | Tipo de cambio - Loss – promedio del periodo (S/ por US$) - Venta | Soles por dólar |

### Formato de Consulta

```
https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{series}/{formato}/{fecha_inicio}/{fecha_fin}
```

**Ejemplo:**
```
https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PD04638PD-PD04639PD/json/2024-12-01/2024-12-13
```

### Estructura de Respuesta JSON

```json
{
  "periods": [
    {
      "name": "Dic.2024",
      "values": ["3.72", "3.76"]
    }
  ],
  "config": {
    "series": [
      {"name": "Tipo de cambio - Compra"},
      {"name": "Tipo de cambio - Venta"}
    ]
  }
}
```

### Consideraciones

- ✅ **Ventaja:** Fuente oficial, datos confiables
- ✅ **Ventaja:** API pública sin autenticación
- ⚠️ **Limitación:** Actualización diaria (no intradía)
- ⚠️ **Limitación:** Puede tener delay de 1 día

---

## 2. Kambista

### Información General

| Atributo | Valor |
|----------|-------|
| **Nombre** | Kambista |
| **Tipo** | Casa de cambio digital |
| **URL** | https://kambista.com |
| **Método de extracción** | Web Scraping |
| **robots.txt** | Verificar antes de scraping |

### Datos a Extraer

| Dato | Descripción | Ubicación en HTML |
|------|-------------|-------------------|
| Tasa de compra | Precio al que Kambista COMPRA dólares | Por inspeccionar |
| Tasa de venta | Precio al que Kambista VENDE dólares | Por inspeccionar |

### Proceso de Inspección

1. Abrir https://kambista.com en navegador
2. Click derecho → "Inspeccionar elemento"
3. Localizar los elementos que muestran las tasas
4. Identificar selectores CSS o XPath
5. Verificar si los datos se cargan estáticamente o con JavaScript

### Verificación Estático vs Dinámico

```python
import requests
response = requests.get("https://kambista.com")
print(response.text)
# Si las tasas aparecen → Estático (usar requests + BeautifulSoup)
# Si NO aparecen → Dinámico (usar Selenium)
```

### Headers Recomendados

```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-PE,es;q=0.9,en;q=0.8"
}
```

### Consideraciones Éticas

- ✅ Frecuencia baja: máximo 1 petición por hora
- ✅ Respetar robots.txt
- ✅ No sobrecargar el servidor
- ✅ User-agent transparente (o realista)

---

## 3. Rextie

### Información General

| Atributo | Valor |
|----------|-------|
| **Nombre** | Rextie |
| **Tipo** | Casa de cambio digital |
| **URL** | https://rextie.com |
| **Método de extracción** | Web Scraping |
| **robots.txt** | Verificar antes de scraping |

### Datos a Extraer

| Dato | Descripción | Ubicación en HTML |
|------|-------------|-------------------|
| Tasa de compra | Precio al que Rextie COMPRA dólares | Por inspeccionar |
| Tasa de venta | Precio al que Rextie VENDE dólares | Por inspeccionar |

### Proceso de Inspección

Similar a Kambista:
1. Abrir https://rextie.com
2. Inspeccionar elementos con tasas
3. Identificar selectores
4. Determinar si es estático o dinámico

### Consideraciones Éticas

Mismas que Kambista:
- Frecuencia baja
- Respetar robots.txt
- No sobrecargar servidor

---

## 4. Comparación de Fuentes

| Característica | BCRP | Kambista | Rextie |
|----------------|------|----------|--------|
| Tipo de acceso | API | Scraping | Scraping |
| Frecuencia actualización | Diaria | Tiempo real | Tiempo real |
| Confiabilidad | Alta | Media | Media |
| Complejidad técnica | Baja | Media | Media |
| Riesgo de bloqueo | Ninguno | Bajo | Bajo |
| Tipo de tasa | Oficial/referencial | Comercial | Comercial |

---

## 5. Flujo de Verificación

Antes de ejecutar el scraper, verificar:

```
□ ¿La URL sigue siendo válida?
□ ¿Los selectores CSS siguen funcionando?
□ ¿Hay cambios en la estructura HTML?
□ ¿El robots.txt permite scraping?
□ ¿Hay algún CAPTCHA o bloqueo?
```

---

## 6. Plan de Contingencia

| Problema | Solución |
|----------|----------|
| API BCRP caída | Registrar como NULL, continuar con otras fuentes |
| Kambista cambió HTML | Actualizar selectores, notificar en logs |
| Rextie bloqueó IP | Usar VPN o reducir frecuencia |
| Datos inconsistentes | Validar rangos (3.5 < TC < 4.5) |

---

## 7. Referencias

- [Documentación API BCRP](https://estadisticas.bcrp.gob.pe/estadisticas/series/ayuda/api)
- [Kambista](https://kambista.com)
- [Rextie](https://rextie.com)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://docs.python-requests.org/)

---

*Documento creado: 13/12/2024*
*Última actualización: 13/12/2024*

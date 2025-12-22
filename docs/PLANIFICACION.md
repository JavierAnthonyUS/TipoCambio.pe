# 📋 Planificación del Proyecto

## TipoCambio.pe - Diseño y Desarrollo
**Última actualización:** 22 de Diciembre, 2025  
**Estado del proyecto:** ✅ COMPLETADO

---

## 👥 Equipo de Trabajo

| Integrante | GitHub | Rol |
|------------|--------|-----|
| Javier Uraco | @JavierAnthonyUS | Líder, BCRP, Rextie, Integrador, Análisis |
| Fiorella Fuentes | @fiorellafuentesb20-cell | Scraper Kambista |
| Sebastián Fernández | @TucoSquare | Documentación |

---

## 📅 Cronograma de Desarrollo

### Fase 1: Planificación y Diseño (16-18 Dic)
| Tarea | Responsable | Estado |
|-------|-------------|--------|
| Definición del tema | Equipo | ✅ Completado |
| Identificación de fuentes | Javier | ✅ Completado |
| Diseño de arquitectura | Javier | ✅ Completado |
| Creación de repositorio GitHub | Javier | ✅ Completado |
| Presentación de propuesta | Equipo | ✅ Completado |

### Fase 2: Desarrollo de Scrapers (19-20 Dic)
| Tarea | Responsable | Estado |
|-------|-------------|--------|
| Scraper BCRP (API) | Javier | ✅ Completado |
| Análisis técnico Kambista/Rextie | Javier | ✅ Completado |
| Scraper Rextie (Selenium) | Javier | ✅ Completado |
| Scraper Kambista (Selenium) | Fiorella | ✅ Completado |

### Fase 3: Integración (20-21 Dic)
| Tarea | Responsable | Estado |
|-------|-------------|--------|
| Módulo integrador | Javier | ✅ Completado |
| Funciones auxiliares (utils.py) | Javier | ✅ Completado |
| Generación de CSV | Javier | ✅ Completado |
| Testing y correcciones | Equipo | ✅ Completado |

### Fase 4: Análisis y Documentación (21-22 Dic)
| Tarea | Responsable | Estado |
|-------|-------------|--------|
| Notebook de análisis | Javier | ✅ Completado |
| Documentación técnica | Sebastián | ✅ Completado |
| README completo | Sebastián | ✅ Completado |
| Revisión final | Equipo | ✅ Completado |

---

## 📊 Distribución de Commits por Integrante

### Javier Uraco (@JavierAnthonyUS)
- [x] Estructura inicial del proyecto
- [x] Scraper BCRP con API
- [x] Documentación de investigación técnica
- [x] Corrección de fechas 2024→2025
- [x] Scraper Rextie con Selenium
- [x] Limpieza de archivos temporales
- [x] Sistema integrador completo
- [x] Notebook de análisis con gráficos

### Fiorella Fuentes (@fiorellafuentesb20-cell)
- [x] Scraper Kambista con Selenium
- [x] Corrección de sintaxis __name__

### Sebastián Fernández (@TucoSquare)
- [x] README mejorado con estructura completa
- [x] Revisión de documentación

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    SISTEMA DE EXTRACCIÓN                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  BCRP API    │  │   Kambista   │  │    Rextie    │       │
│  │  (requests)  │  │  (Selenium)  │  │  (Selenium)  │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │                │
│         └────────────┬────┴────────────────┘                │
│                      │                                       │
│              ┌───────▼───────┐                              │
│              │  INTEGRADOR   │                              │
│              │ (integrador.py)│                              │
│              └───────┬───────┘                              │
│                      │                                       │
│         ┌────────────┼────────────┐                         │
│         │            │            │                         │
│  ┌──────▼──────┐ ┌───▼───┐ ┌─────▼─────┐                   │
│  │ Cálculos    │ │ CSV   │ │ Resumen   │                   │
│  │ (spreads,   │ │ datos │ │ consola   │                   │
│  │  mejor op.) │ │       │ │           │                   │
│  └─────────────┘ └───────┘ └───────────┘                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Diseño Técnico de Scrapers

### BCRP (API REST)
```
Método: requests.get()
Formato: JSON
Autenticación: No requerida
Endpoint: /estadisticas/series/api/{series}/json/{fecha_inicio}/{fecha_fin}
Series: PD04638PD (compra), PD04639PD (venta)
```

### Kambista (Web Scraping Dinámico)
```
Método: Selenium + Chrome headless
Espera: 3 segundos para carga de JavaScript
Extracción: regex sobre page_source
Patrón: [\d]+\.[\d]{2,4}
Filtro: Valores entre 3.30 y 3.50
Resultado: Menor = compra, Mayor = venta
```

### Rextie (Web Scraping Dinámico)
```
Método: Selenium + Chrome headless
Espera: 3 segundos para carga de JavaScript
Extracción: regex sobre page_source
Patrón: [\d]+\.[\d]{2,4}
Filtro: Valores entre 3.30 y 3.50
Resultado: Menor = compra, Mayor = venta
```

---

## 📁 Estructura Final del Proyecto

```
tipo-cambio-peru/
│
├── data/
│   ├── processed/
│   │   └── tipo_cambio_historico.csv    ✅
│   └── raw/
│       └── .gitkeep
│
├── docs/
│   ├── PLANIFICACION.md                  ✅
│   ├── FUENTES_DATOS.md                  ✅
│   └── DICCIONARIO_DATOS.md              ✅
│
├── notebooks/
│   └── analisis_exploratorio.ipynb       ✅
│
├── src/
│   ├── __init__.py                       ✅
│   ├── scraper_bcrp.py                   ✅
│   ├── scraper_kambista.py               ✅
│   ├── scraper_rextie.py                 ✅
│   ├── integrador.py                     ✅
│   ├── main.py                           ✅
│   └── utils.py                          ✅
│
├── logs/
│   └── .gitkeep
│
├── .gitignore                            ✅
├── LICENSE                               ✅
├── README.md                             ✅
└── requirements.txt                      ✅
```

---

## ✅ Criterios de Éxito

| Criterio | Meta | Estado |
|----------|------|--------|
| Fuentes de datos | Mínimo 3 | ✅ 3 fuentes (BCRP, Kambista, Rextie) |
| Métodos de extracción | API + Scraping | ✅ 1 API + 2 Selenium |
| CSV estructurado | Datos válidos | ✅ 13 columnas, datos reales |
| Código documentado | Docstrings | ✅ Todos los archivos |
| Trabajo colaborativo | Commits de todos | ✅ 3 integrantes con commits |
| Análisis de datos | Notebook | ✅ Con gráficos comparativos |
| Documentación | Completa | ✅ README + 3 docs técnicos |

---

## 📈 Métricas del Proyecto

| Métrica | Valor |
|---------|-------|
| Total de archivos Python | 6 |
| Total de archivos de documentación | 4 |
| Total de commits | 12+ |
| Fuentes de datos | 3 |
| Columnas en CSV | 13 |
| Integrantes activos | 3 |

---

## 🎯 Lecciones Aprendidas

1. **Páginas dinámicas:** Kambista y Rextie requirieron Selenium porque cargan datos con JavaScript.

2. **APIs vs Scraping:** BCRP con API es más confiable y rápido. Selenium es necesario pero más frágil.

3. **Trabajo colaborativo:** GitHub permitió coordinar el trabajo entre 3 personas con diferentes horarios.

4. **Documentación:** Documentar el diseño antes de programar ayudó a mantener el proyecto organizado.

5. **Testing:** Probar cada scraper individualmente antes de integrar evitó errores difíciles de depurar.

---
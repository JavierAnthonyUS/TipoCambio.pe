# 💱 Comparador de Tipo de Cambio en Perú

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.39-green.svg)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistema automatizado para extraer, comparar y analizar tipos de cambio de múltiples fuentes en Perú. Desarrollado como proyecto final del curso **Lenguaje de Programación 2 (LP2)** - Universidad Nacional Agraria La Molina (UNALM), semestre 2025-2.

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Equipo](#-equipo)
- [Características](#-características)
- [Fuentes de Datos](#-fuentes-de-datos)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Resultados](#-resultados)
- [Documentación](#-documentación)
- [Dificultades y Soluciones](#-dificultades-y-soluciones)
- [Licencia](#-licencia)

## 📝 Descripción

En Perú existen múltiples casas de cambio con diferentes tasas para compra y venta de dólares. Este proyecto automatiza la extracción de tipos de cambio de 3 fuentes diferentes, permitiendo:

- **Comparar** tasas de cambio en tiempo real
- **Identificar** la mejor opción para comprar o vender dólares
- **Almacenar** datos históricos para análisis
- **Visualizar** diferencias mediante gráficos

## 👥 Equipo

| Integrante | GitHub | Rol | Contribuciones |
|------------|--------|-----|----------------|
| Javier Uraco | [@JavierAnthonyUS](https://github.com/JavierAnthonyUS) | Líder del proyecto | Estructura, BCRP, Rextie, Integrador, Notebook |
| Fiorella Fuentes | [@fiorellafuentesb20-cell](https://github.com/fiorellafuentesb20-cell) | Desarrolladora | Scraper Kambista |
| Sebastián Fernández | [@TucoSquare](https://github.com/TucoSquare) | Documentación | README, documentación técnica |

## ✨ Características

- ✅ Extracción automatizada de 3 fuentes de tipo de cambio
- ✅ Manejo de páginas estáticas (API) y dinámicas (Selenium)
- ✅ Cálculo automático de spreads
- ✅ Identificación de mejor opción compra/venta
- ✅ Almacenamiento histórico en CSV
- ✅ Análisis exploratorio con visualizaciones
- ✅ Código documentado con docstrings
- ✅ Detección de cambios para evitar duplicados

## 📊 Fuentes de Datos

| Fuente | Tipo | Método | URL | Estado |
|--------|------|--------|-----|--------|
| **BCRP** | API Oficial | requests + JSON | [estadisticas.bcrp.gob.pe](https://estadisticas.bcrp.gob.pe) | ✅ Funcionando |
| **Kambista** | Web Scraping | Selenium | [kambista.com](https://kambista.com) | ✅ Funcionando |
| **Rextie** | Web Scraping | Selenium | [rextie.com](https://rextie.com) | ✅ Funcionando |

### ¿Por qué estas fuentes?

- **BCRP**: Fuente oficial del Banco Central de Reserva del Perú. Datos confiables y actualizados diariamente.
- **Kambista**: Casa de cambio digital líder en Perú. Tasas competitivas para el público general.
- **Rextie**: Casa de cambio digital con altos volúmenes. Popular entre empresas y personas naturales.

## 🛠 Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.13 | Lenguaje principal |
| Pandas | 2.2+ | Manipulación de datos |
| Requests | 2.32+ | Consumo de APIs |
| BeautifulSoup4 | 4.12+ | Parsing HTML |
| Selenium | 4.39+ | Web scraping dinámico |
| Webdriver Manager | 4.0+ | Gestión automática de ChromeDriver |
| Matplotlib | 3.10+ | Visualización de datos |
| Jupyter | 1.1+ | Notebooks de análisis |

## 📁 Estructura del Proyecto
```
tipo-cambio-peru/
│
├── 📁 data/
│   ├── 📁 processed/
│   │   └── 📄 tipo_cambio_historico.csv    # Datos integrados
│   └── 📁 raw/                              # Datos crudos
│
├── 📁 docs/
│   ├── 📄 PLANIFICACION.md                  # Cronograma y diseño
│   ├── 📄 FUENTES_DATOS.md                  # Documentación técnica
│   └── 📄 DICCIONARIO_DATOS.md              # Descripción de columnas
│
├── 📁 notebooks/
│   └── 📓 analisis_exploratorio.ipynb       # Análisis con gráficos
│
├── 📁 src/
│   ├── 📄 __init__.py
│   ├── 📄 scraper_bcrp.py                   # Extractor BCRP (API)
│   ├── 📄 scraper_kambista.py               # Extractor Kambista (Selenium)
│   ├── 📄 scraper_rextie.py                 # Extractor Rextie (Selenium)
│   ├── 📄 integrador.py                     # Combina todas las fuentes
│   ├── 📄 main.py                           # Punto de entrada
│   └── 📄 utils.py                          # Funciones auxiliares
│
├── 📁 logs/                                 # Archivos de log
├── 📄 .gitignore
├── 📄 LICENSE                               # MIT License
├── 📄 README.md                             # Este archivo
└── 📄 requirements.txt                      # Dependencias
```

## 🚀 Instalación

### Prerrequisitos

- Python 3.10 o superior
- Google Chrome instalado
- Git

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/JavierAnthonyUS/tipo-cambio-peru.git
cd tipo-cambio-peru
```

2. **Instalar dependencias básicas**
```bash
pip install -r requirements.txt
```

3. **Instalar dependencias para Selenium**
```bash
pip install selenium webdriver-manager
```

4. **Verificar instalación**
```bash
cd src
python scraper_bcrp.py
```

## 💻 Uso

### Extracción completa (recomendado)

Ejecuta el integrador para obtener datos de las 3 fuentes:
```bash
cd src
python integrador.py
```

**Salida esperada:**
```
============================================================
   💱 SISTEMA DE EXTRACCIÓN DE TIPO DE CAMBIO
============================================================
📊 Extrayendo datos de BCRP (API)...
📊 Extrayendo datos de Kambista (Selenium)...
📊 Extrayendo datos de Rextie (Selenium)...

   📈 TIPOS DE CAMBIO:
   ┌────────────────────────────────────────────────────────┐
   │ Fuente       │     Compra │      Venta │     Spread │
   ├────────────────────────────────────────────────────────┤
   │ BCRP         │     3.3666 │      3.363 │    -0.0036 │
   │ Kambista     │       3.33 │      3.486 │      0.156 │
   │ Rextie       │       3.35 │      3.392 │      0.042 │
   └────────────────────────────────────────────────────────┘

   🏆 MEJOR OPCIÓN:
      • Para COMPRAR dólares: BCRP
      • Para VENDER dólares:  BCRP
============================================================
```

### Scrapers individuales
```bash
# Solo BCRP (API)
python scraper_bcrp.py

# Solo Kambista (Selenium)
python scraper_kambista.py

# Solo Rextie (Selenium)
python scraper_rextie.py
```

### Análisis exploratorio

Abre el notebook de Jupyter:
```bash
cd notebooks
jupyter notebook analisis_exploratorio.ipynb
```

## 📈 Resultados

### Estructura del CSV generado

El archivo `data/processed/tipo_cambio_historico.csv` contiene:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| timestamp | datetime | Fecha y hora de extracción |
| tc_bcrp_compra | float | Tipo de cambio compra BCRP |
| tc_bcrp_venta | float | Tipo de cambio venta BCRP |
| tc_kambista_compra | float | Tipo de cambio compra Kambista |
| tc_kambista_venta | float | Tipo de cambio venta Kambista |
| tc_rextie_compra | float | Tipo de cambio compra Rextie |
| tc_rextie_venta | float | Tipo de cambio venta Rextie |
| spread_bcrp | float | Diferencia venta-compra BCRP |
| spread_kambista | float | Diferencia venta-compra Kambista |
| spread_rextie | float | Diferencia venta-compra Rextie |
| mejor_compra | string | Mejor fuente para comprar USD |
| mejor_venta | string | Mejor fuente para vender USD |
| cambio_detectado | boolean | Si hubo cambio respecto al registro anterior |

### Ejemplo de visualización

El notebook genera gráficos comparativos como:

- Comparación de tipos de cambio por fuente (barras horizontales)
- Análisis de spreads por casa de cambio
- Resumen y recomendaciones

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [PLANIFICACION.md](docs/PLANIFICACION.md) | Cronograma, fases del proyecto, distribución de tareas |
| [FUENTES_DATOS.md](docs/FUENTES_DATOS.md) | Documentación técnica de cada fuente, endpoints, selectores |
| [DICCIONARIO_DATOS.md](docs/DICCIONARIO_DATOS.md) | Descripción detallada de cada columna del CSV |

## 🔧 Dificultades y Soluciones

### 1. Páginas dinámicas

**Problema:** Kambista y Rextie cargan datos con JavaScript. El HTML inicial no contiene las tasas.

**Solución:** Implementamos Selenium con Chrome headless para renderizar la página completa antes de extraer datos.

### 2. Identificación de valores

**Problema:** El HTML renderizado contiene muchos números. ¿Cómo identificar cuáles son tipos de cambio?

**Solución:** Usamos expresiones regulares y filtrado por rango válido (3.30 - 3.50 para PEN/USD).

### 3. Manejo de errores

**Problema:** Las páginas web pueden fallar, cambiar estructura o estar caídas.

**Solución:** Implementamos manejo robusto de excepciones con logging detallado.

### 4. Trabajo colaborativo

**Problema:** Coordinar el trabajo entre 3 personas con diferentes horarios.

**Solución:** Usamos GitHub para control de versiones con commits descriptivos y branches.

## 🤝 Contribuciones

Este es un proyecto académico cerrado. Sin embargo, las sugerencias son bienvenidas a través de Issues.

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

**Desarrollado con ❤️ para LP2 - UNALM 2025-2**

# 💱 Comparador de Tipo de Cambio en Perú

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.39-green.svg)](https://www.selenium.dev/)
[![NiceGUI](https://img.shields.io/badge/NiceGUI-3.4-cyan.svg)](https://nicegui.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)]()

Sistema automatizado para extraer, comparar y analizar tipos de cambio de múltiples fuentes en Perú. **Incluye aplicación web interactiva** para visualización en tiempo real. Desarrollado como proyecto final del curso **Lenguaje de Programación 2 (LP2)** - Universidad Nacional Agraria La Molina (UNALM), semestre 2025-2.

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Equipo](#-equipo)
- [Características](#-características)
- [Fuentes de Datos](#-fuentes-de-datos)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Aplicación Web](#-aplicación-web)
- [Resultados](#-resultados)
- [Documentación](#-documentación)
- [Dificultades y Soluciones](#-dificultades-y-soluciones)
- [Licencia](#-licencia)

---

## 📝 Descripción

En Perú existen múltiples casas de cambio con diferentes tasas para compra y venta de dólares. Este proyecto automatiza la extracción de tipos de cambio de 3 fuentes diferentes, permitiendo:

- **Comparar** tasas de cambio en tiempo real
- **Identificar** la mejor opción para comprar o vender dólares
- **Visualizar** diferencias mediante gráficos interactivos
- **Calcular** el ahorro potencial al elegir la mejor opción
- **Interactuar** a través de una aplicación web moderna

---

## 👥 Equipo

| Integrante | GitHub | Rol | Contribuciones |
|------------|--------|-----|----------------|
| Javier Uraco | [@JavierAnthonyUS](https://github.com/JavierAnthonyUS) | Líder del proyecto | BCRP, Rextie, Integrador, App Web, Notebook |
| Fiorella Fuentes | [@fiorellafuentesb20-cell](https://github.com/fiorellafuentesb20-cell) | Desarrolladora | Scraper Kambista | App Web |
| Sebastián Fernández | [@TucoSquare](https://github.com/TucoSquare) | Documentación | README, documentación técnica |

---

## ✨ Características

### Scrapers
- ✅ Extracción automatizada de 3 fuentes de tipo de cambio
- ✅ Manejo de páginas estáticas (API) y dinámicas (Selenium)
- ✅ Cálculo automático de spreads
- ✅ Identificación de mejor opción compra/venta

### Aplicación Web
- ✅ Interfaz moderna con tema oscuro
- ✅ Ejecución de scrapers con un click
- ✅ Gráficos interactivos con Plotly
- ✅ Calculadora de ahorro en tiempo real
- ✅ Recomendación automática de mejor opción
- ✅ 100% Python (sin HTML/CSS/JS manual)

### Datos
- ✅ Almacenamiento histórico en CSV (13 columnas)
- ✅ Análisis exploratorio con visualizaciones
- ✅ Detección de cambios para evitar duplicados

---

## 📊 Fuentes de Datos

| Fuente | Tipo | Método | URL | Estado |
|--------|------|--------|-----|--------|
| **BCRP** | API Oficial | requests + JSON | [estadisticas.bcrp.gob.pe](https://estadisticas.bcrp.gob.pe) | ✅ Producción |
| **Kambista** | Web Scraping | Selenium + regex | [kambista.com](https://kambista.com) | ✅ Producción |
| **Rextie** | Web Scraping | Selenium + regex | [rextie.com](https://rextie.com) | ✅ Producción |

### ¿Por qué estas fuentes?

- **BCRP**: Fuente oficial del Banco Central de Reserva del Perú. Datos confiables y actualizados diariamente.
- **Kambista**: Casa de cambio digital líder en Perú. Tasas competitivas para el público general.
- **Rextie**: Casa de cambio digital con altos volúmenes. Popular entre empresas y personas naturales.

---

## 🛠 Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.10+ | Lenguaje principal |
| **NiceGUI** | 3.4+ | **Aplicación web interactiva** |
| **Plotly** | 6.5+ | **Gráficos interactivos** |
| Pandas | 2.2+ | Manipulación de datos |
| Requests | 2.32+ | Consumo de API BCRP |
| Selenium | 4.39+ | Web scraping de páginas dinámicas |
| Webdriver Manager | 4.0+ | Gestión automática de ChromeDriver |
| Matplotlib | 3.10+ | Visualización en notebooks |

> **Nota:** NiceGUI permite crear aplicaciones web modernas usando solo Python, sin necesidad de HTML, CSS o JavaScript.

---

## 📁 Estructura del Proyecto

```
tipo-cambio-peru/
│
├── 📄 AppTipoCambioPe.py          
├── 📁 data/
│   ├── 📁 processed/
│   │   └── 📄 tipo_cambio_historico.csv
│   └── 📁 raw/
│
├── 📁 docs/
│   ├── 📄 PLANIFICACION.md
│   ├── 📄 FUENTES_DATOS.md
│   └── 📄 DICCIONARIO_DATOS.md
│
├── 📁 notebooks/
│   └── 📓 analisis_exploratorio.ipynb
│
├── 📁 src/
│   ├── 📄 __init__.py
│   ├── 📄 scraper_bcrp.py          # Extractor BCRP (API REST)
│   ├── 📄 scraper_kambista.py      # Extractor Kambista (Selenium)
│   ├── 📄 scraper_rextie.py        # Extractor Rextie (Selenium)
│   ├── 📄 integrador.py            # Combina todas las fuentes
│   └── 📄 utils.py                 # Funciones auxiliares
│
├── 📁 logs/
├── 📄 .gitignore
├── 📄 LICENSE
├── 📄 README.md
└── 📄 requirements.txt
```

---

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

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación web**
```bash
python AppTipoCambioPe.py
```

4. **Abrir en el navegador**
```
http://localhost:8080
```

---

## 💻 Uso

### 🌐 Aplicación Web (Recomendado)

La forma más fácil de usar el proyecto:

```bash
python AppTipoCambioPe.py
```

Luego abre tu navegador en: **http://localhost:8080**

### Scrapers por Terminal

```bash
cd src

# Todos los scrapers
python integrador.py

# Scrapers individuales
python scraper_bcrp.py
python scraper_kambista.py
python scraper_rextie.py
```

### Análisis en Jupyter

```bash
cd notebooks
jupyter notebook analisis_exploratorio.ipynb
```

---

## 🌐 Aplicación Web

### Páginas disponibles

| Página | URL | Descripción |
|--------|-----|-------------|
| **Inicio** | `/` | Presentación del proyecto y características |
| **Demo** | `/demo` | Ejecución de scrapers en tiempo real |
| **Análisis** | `/analisis` | Gráficos comparativos y calculadora |
| **Equipo** | `/equipo` | Información de los integrantes |

### Funcionalidades

#### Página Demo (`/demo`)
- Ejecutar scrapers individualmente o todos a la vez
- Ver resultados en tiempo real
- Sección "Mejor Opción" que se actualiza automáticamente
- Cálculo de ahorro por cada $1,000

#### Página Análisis (`/analisis`)
- Gráfico de barras comparativo (Compra vs Venta)
- Gráfico de spreads por fuente
- Calculadora de ahorro interactiva
- Explicaciones integradas

---

## 📈 Resultados

### Estructura del CSV generado

El archivo `data/processed/tipo_cambio_historico.csv` contiene 13 columnas:

| Columna | Descripción |
|---------|-------------|
| `timestamp` | Fecha y hora de extracción |
| `tc_bcrp_compra` | Tipo de cambio compra BCRP |
| `tc_bcrp_venta` | Tipo de cambio venta BCRP |
| `tc_kambista_compra` | Tipo de cambio compra Kambista |
| `tc_kambista_venta` | Tipo de cambio venta Kambista |
| `tc_rextie_compra` | Tipo de cambio compra Rextie |
| `tc_rextie_venta` | Tipo de cambio venta Rextie |
| `spread_bcrp` | Diferencia venta-compra BCRP |
| `spread_kambista` | Diferencia venta-compra Kambista |
| `spread_rextie` | Diferencia venta-compra Rextie |
| `mejor_compra` | Mejor fuente para comprar USD |
| `mejor_venta` | Mejor fuente para vender USD |
| `cambio_detectado` | Si hubo cambio respecto al registro anterior |

---

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [PLANIFICACION.md](docs/PLANIFICACION.md) | Cronograma, fases del proyecto |
| [FUENTES_DATOS.md](docs/FUENTES_DATOS.md) | Documentación técnica de cada fuente |
| [DICCIONARIO_DATOS.md](docs/DICCIONARIO_DATOS.md) | Descripción de columnas del CSV |

---

## 🔧 Dificultades y Soluciones

### 1. Páginas dinámicas
**Problema:** Kambista y Rextie cargan datos con JavaScript.
**Solución:** Selenium con Chrome headless.

### 2. Identificación de valores
**Problema:** Múltiples números en el HTML.
**Solución:** Regex y filtrado por rango válido (3.30 - 3.50).

### 3. Interfaz de usuario
**Problema:** Crear una interfaz web sin conocimientos de frontend.
**Solución:** NiceGUI permite crear aplicaciones web modernas usando solo Python.

### 4. Compatibilidad NiceGUI 3.4.1
**Problema:** Algunos componentes cambiaron entre versiones.
**Solución:** Usar `ui.row()` en lugar de `ui.header()`, evitar `ui.html()`.

---

## 🤝 Contribuciones

Este es un proyecto académico. Las sugerencias son bienvenidas a través de Issues.

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

**Desarrollado con ❤️ para LP2 - UNALM 2025-2**

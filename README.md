# 💱 TipoCambio.pe

## Sistema Automatizado de Comparación de Tipo de Cambio en Perú

> **Transparencia financiera para 33 millones de peruanos**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![UNALM](https://img.shields.io/badge/UNALM-LP2%202025--1-red.svg)](https://www.lamolina.edu.pe/)

---

## 📋 Descripción

Sistema de web scraping que extrae, compara y registra automáticamente los tipos de cambio de múltiples fuentes en Perú:

- **API BCRP**: Tipo de cambio oficial del Banco Central de Reserva del Perú
- **Kambista**: Casa de cambio digital líder
- **Rextie**: Casa de cambio digital competidora

El sistema actualiza los datos cada hora y genera un dataset histórico en formato CSV para análisis posterior.

---

## 👥 Equipo

| Integrante | GitHub | Rol |
|------------|--------|-----|
| Javier Uraco | [@JavierAnthonyUS](https://github.com/JavierAnthonyUS) | Desarrollador - API BCRP |
| Fiorella Fuentes | [@fiorellafuentesb20-cell](https://github.com/fiorellafuentesb20-cell) | Desarrolladora - Scraper Kambista |
| Sebastián Fernández | [@TucoSquare](https://github.com/TucoSquare) | Desarrollador - Scraper Rextie |

**Curso:** Lenguaje de Programación 2 (LP2) - UNALM 2025-1

---

## 🚀 Características

- ✅ **Extracción automatizada** de 3 fuentes de datos
- ✅ **Actualización cada 1 hora** (polling)
- ✅ **Detección inteligente de cambios** (solo guarda cuando hay variación)
- ✅ **Registro histórico** en CSV estructurado
- ✅ **Código documentado** siguiendo buenas prácticas
- ✅ **Manejo de errores** robusto

---

## 📁 Estructura del Proyecto

```
tipo-cambio-peru/
│
├── README.md                    # Este archivo
├── LICENSE                      # Licencia MIT
├── requirements.txt             # Dependencias del proyecto
├── .gitignore                   # Archivos ignorados por Git
│
├── docs/                        # Documentación
│   ├── PLANIFICACION.md         # Plan de diseño y desarrollo
│   ├── FUENTES_DATOS.md         # Documentación de fuentes
│   └── DICCIONARIO_DATOS.md     # Descripción de variables
│
├── src/                         # Código fuente
│   ├── __init__.py
│   ├── scraper_bcrp.py          # Extractor API BCRP
│   ├── scraper_kambista.py      # Extractor Kambista
│   ├── scraper_rextie.py        # Extractor Rextie
│   ├── integrador.py            # Integra todas las fuentes
│   └── utils.py                 # Funciones auxiliares
│
├── data/                        # Datos extraídos
│   ├── raw/                     # Datos crudos por fuente
│   │   ├── bcrp_raw.csv
│   │   ├── kambista_raw.csv
│   │   └── rextie_raw.csv
│   └── processed/               # Datos integrados
│       └── tipo_cambio_historico.csv
│
├── notebooks/                   # Jupyter notebooks
│   └── analisis_exploratorio.ipynb
│
└── tests/                       # Tests (opcional)
    └── test_scrapers.py
```

---

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/JavierAnthonyUS/tipo-cambio-peru.git
cd tipo-cambio-peru
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 📖 Uso

### Ejecución manual (una vez)

```bash
python src/integrador.py
```

### Ejecución automatizada (cada 1 hora)

```bash
python src/main.py
```

### Ejecutar scraper individual

```python
from src.scraper_bcrp import obtener_tipo_cambio_bcrp
from src.scraper_kambista import obtener_tipo_cambio_kambista
from src.scraper_rextie import obtener_tipo_cambio_rextie

# Obtener tipo de cambio del BCRP
tc_bcrp = obtener_tipo_cambio_bcrp()
print(tc_bcrp)

# Obtener tipo de cambio de Kambista
tc_kambista = obtener_tipo_cambio_kambista()
print(tc_kambista)
```

---

## 📊 Dataset Generado

El archivo `data/processed/tipo_cambio_historico.csv` contiene:

| Variable | Descripción | Tipo |
|----------|-------------|------|
| `timestamp` | Fecha y hora de extracción | datetime |
| `tc_bcrp_compra` | Tipo cambio oficial compra | float |
| `tc_bcrp_venta` | Tipo cambio oficial venta | float |
| `tc_kambista_compra` | Tasa compra Kambista | float |
| `tc_kambista_venta` | Tasa venta Kambista | float |
| `tc_rextie_compra` | Tasa compra Rextie | float |
| `tc_rextie_venta` | Tasa venta Rextie | float |
| `spread_bcrp` | Diferencia venta-compra BCRP | float |
| `spread_kambista` | Diferencia venta-compra Kambista | float |
| `spread_rextie` | Diferencia venta-compra Rextie | float |
| `mejor_compra` | Fuente con mejor tasa compra | string |
| `mejor_venta` | Fuente con mejor tasa venta | string |

---

## 🔗 Fuentes de Datos

| Fuente | Tipo | URL | Método |
|--------|------|-----|--------|
| BCRP | API REST | https://estadisticas.bcrp.gob.pe/estadisticas/series/api/ | requests + JSON |
| Kambista | Web | https://kambista.com | BeautifulSoup |
| Rextie | Web | https://rextie.com | BeautifulSoup |

---

## 🤝 Contribución

Este es un proyecto académico desarrollado de manera colaborativa. Cada integrante es responsable de:

1. **Javier**: API BCRP + Integración
2. **Fiorella**: Scraper Kambista + Documentación
3. **Sebastián**: Scraper Rextie + Testing

### Flujo de trabajo con Git

```bash
# Crear rama para tu feature
git checkout -b feature/nombre-feature

# Hacer cambios y commit
git add .
git commit -m "feat: descripción del cambio"

# Subir cambios
git push origin feature/nombre-feature

# Crear Pull Request en GitHub
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- **UNALM** - Universidad Nacional Agraria La Molina
- **Curso LP2** - Lenguaje de Programación 2
- **BCRP** - Por proveer API pública de datos económicos

---

<p align="center">
  <i>"Hagamos que el mercado cambiario peruano sea más justo y transparente, una línea de código a la vez"</i>
</p>

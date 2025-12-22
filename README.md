# 💱 Comparador de Tipo de Cambio en Perú

Sistema automatizado para extraer, comparar y analizar tipos de cambio de múltiples fuentes en Perú.

## 👥 Equipo - LP2 UNALM 2025-1

| Integrante | GitHub | Rol |
|------------|--------|-----|
| Javier Uraco | @JavierAnthonyUS | Líder, BCRP, Rextie, Integrador, Análisis |
| Fiorella Fuentes | @fiorellafuentesb20-cell | Scraper Kambista |
| Sebastián Fernández | @TucoSquare | Documentación |

## 📊 Fuentes de Datos

| Fuente | Tipo | Método | Estado |
|--------|------|--------|--------|
| **BCRP** | API Oficial | requests + JSON | ✅ |
| **Kambista** | Web Scraping | Selenium | ✅ |
| **Rextie** | Web Scraping | Selenium | ✅ |

## 🚀 Instalación
```bash
git clone https://github.com/JavierAnthonyUS/tipo-cambio-peru.git
cd tipo-cambio-peru
pip install -r requirements.txt
pip install selenium webdriver-manager
```

## 💻 Uso
```bash
cd src
python integrador.py      # Ejecutar extracción completa
python scraper_bcrp.py    # Solo BCRP
python scraper_kambista.py # Solo Kambista
python scraper_rextie.py  # Solo Rextie
```

## 📁 Estructura
```
tipo-cambio-peru/
├── data/processed/          # CSV con datos
├── docs/                    # Documentación
├── notebooks/               # Análisis Jupyter
├── src/                     # Código fuente
│   ├── scraper_bcrp.py
│   ├── scraper_kambista.py
│   ├── scraper_rextie.py
│   ├── integrador.py
│   └── utils.py
└── README.md
```

## 📈 Resultados

El sistema extrae y compara tipos de cambio, identifica la mejor opción para comprar/vender dólares y guarda el histórico en CSV.

## 📝 Licencia

MIT License - 2025

# 🛍️ Tienda Aurelion – Sprint 2  
**Análisis Comercial con Python y Visualización de Datos**

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-green?logo=pandas)](https://pandas.pydata.org/)
[![Matplotlib & Seaborn](https://img.shields.io/badge/Visualizaci%C3%B3n-Matplotlib%20%7C%20Seaborn-orange)](https://matplotlib.org/)

Este repositorio contiene la segunda entrega del proyecto **Tienda Aurelion**, centrado en la **limpieza, análisis estadístico y visualización de datos comerciales** para apoyar la toma de decisiones estratégicas.

---

## 🎯 Objetivo del Sprint 2

Transformar datos crudos en información procesable mediante:
- Limpieza y normalización de datasets
- Cálculo de estadísticas descriptivas
- Identificación de distribuciones y outliers
- Análisis de correlaciones
- Generación de visualizaciones representativas
- Documentación metodológica detallada

---

## 📁 Estructura del Proyecto 
```
 tienda_Aurelion/
├── datos_originales/
│ ├── clientes.csv
│ ├── productos.csv
│ ├── detalle_ventas.csv
│ └── ventas.csv
├── datos_limpios/
│ ├── clientes_limpios.csv
│ ├── productos_limpios.csv
│ ├── detalle_ventas_limpios.csv
│ └── ventas_limpios.csv
├── metodos_de_limpieza.csv
├── documentacion.md
├── programa_actualizado.py
└── README.md 
```

---

## 🧹 Fase 1: Limpieza y Transformación

- Lectura y validación de archivos CSV
- Corrección de errores (valores nulos, duplicados, formatos inconsistentes)
- Normalización para evitar redundancia (modelo en copo de nieve)
- Integración con dimensión calendario
- Registro detallado de cada acción de limpieza en `metodos_de_limpieza.csv`

---

## 📊 Fase 2: Estadística Aplicada

- Estadísticas descriptivas (media, mediana, desviación estándar, etc.)
- Análisis de distribución de variables (histogramas, Q-Q plots)
- Detección de outliers mediante IQR y cuartiles
- Matrices de correlación entre variables clave

---

## 📈 Fase 3: Visualización

- Gráficos con **Matplotlib** y **Seaborn**
- Al menos 3 visualizaciones representativas:
  - Tendencias de ventas
  - Comportamiento por categoría de producto
  - Perfil de cliente (segmentación básica)

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.13**
- **Pandas** – Manipulación y limpieza de datos
- **NumPy** – Cálculos numéricos
- **Matplotlib / Seaborn** – Visualización
- **Markdown** – Documentación estructurada
- **Git** – Control de versiones

---

## 📝 Documentación

Toda la metodología, decisiones técnicas y ejemplos se encuentran en:
- `documentacion.md`: Explica el problema, solución, escalas de medición, pseudocódigo y mejoras con IA.
- `metodos_de_limpieza.csv`: Tabla comparativa con errores detectados, métodos aplicados y ejemplos concretos.

---

## Descripción de archivos y carpetas

- `datos_originales/`: Contiene los datasets sin procesar proporcionados por el negocio.
- `datos_limpios/`: Almacena las versiones depuradas y normalizadas de los datasets.
- `metodos_de_limpieza.csv`: Registro tabular de errores detectados, técnicas aplicadas y ejemplos antes/después.
- `documentacion.md`: Explica la metodología, escalas de medición, pseudocódigo del proceso y mejoras propuestas con IA.
- `programa_actualizado.py`: Script principal en Python que ejecuta la limpieza, análisis estadístico y generación de gráficos.

## Requisitos

- Python 3.13
- Sistema operativo: Windows (compatible con otros sistemas con ajustes mínimos)
- Dependencias:
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - jupyter (opcional)

## Instrucciones de ejecución

1. Clona el repositorio:
   ```bash
   git clone https://github.com/NancyCardozo/sprint_2_tiendaAurelion.git
   cd sprint_2_tiendaAurelion

2. (Opcional) Crea y activa un entorno virtual
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instala las dependencias
   ```bash
   pip install pandas numpy matplotlib seaborn jupyter
   ```

4. Ejecuta el scrit principal
   ```bash   
   python programa_actualizado.py
   ```

## Salidas esperadas

- Archivos limpios en `datos_limpios/`
- Gráficos generados (si el script los exporta)
- Información impresa en consola o en archivos de salida (según implementación)

## Documentación

- La metodología completa se encuentra en `documentacion.md`.
- El registro de limpieza detallado está en `metodos_de_limpieza.csv`.



## 👩‍💻 Autora

**Nancy Cardozo** – Creative Director & Data Analyst  
Proyecto desarrollado como parte del curso **Guayerd IA 2025**.

---

> 💡 *“Los datos sin contexto son ruido. Con análisis, se convierten en insight.”*

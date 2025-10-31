# Descripción de los archivos en la carpeta `estadisticas`

Este archivo contiene una breve explicación (una línea) sobre el propósito de cada CSV generado en la fase de análisis.

- `01_estadisticas_descriptivas.csv` — Estadísticas descriptivas generales (media, mediana, std, mínimos y máximos) para las variables numéricas principales del conjunto de datos de ventas.
- `02_analisis_distribuciones.csv` — Resumen del análisis de distribuciones por variable: asimetría, curtosis y observaciones sobre forma de la distribución (simétrica, sesgada, bi-modal, etc.).
- `03_correlaciones.csv` — Tabla resumen de correlaciones entre pares de variables numéricas, con valores y comentarios sobre relaciones fuertes/relevantes.
- `04_matriz_correlacion_pearson.csv` — Matriz de correlación Pearson completa (coeficientes) entre variables numéricas.
- `05_matriz_correlacion_spearman.csv` — Matriz de correlación Spearman (rank) entre variables, útil cuando las relaciones no son lineales.
- `06_analisis_outliers.csv` — Resultados del análisis de outliers: observaciones marcadas, método usado (IQR, Z-score), y conteo por variable.
- `07_top_outliers_importe.csv` — Listado de las observaciones con mayor importe consideradas outliers (por orden descendente) para facilitar inspección.
- `08_interpretaciones_negocio.csv` — Interpretaciones y conclusiones relevantes para negocio extraídas del análisis estadístico (insights accionables y posibles hipótesis).
- `09_herramientas_metodos.csv` — Registro de herramientas, librerías y métodos estadísticos usados (por ejemplo: pandas, scipy, IQR, Z-score, etc.) y parámetros relevantes.
- `10_stats_por_categoria.csv` — Estadísticas agregadas (ej. suma, media, conteo) por categoría de producto para comparar comportamientos entre categorías.
- `11_stats_por_ciudad.csv` — Estadísticas agregadas por ciudad (ventas totales, promedio por transacción, número de clientes, etc.) para análisis geográfico.
- `12_stats_por_medio_pago.csv` — Estadísticas por medio de pago (efectivo, tarjeta, etc.): distribución de ventas y métricas clave por método.
- `13_stats_temporales.csv` — Resumen de estadísticas temporales: comparativos por mes/día/hora, tendencias y estacionalidad detectada.

Cómo usar

- Todos los archivos son CSV y pueden abrirse con Excel, LibreOffice o cargarse en Python/R para análisis adicional.
- Los archivos fueron generados tras el proceso de limpieza y transformación en `datos_limpios/`.
- Si falta algún archivo o nota, actualizar este README.md con la explicación correspondiente.



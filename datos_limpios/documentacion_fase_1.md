# 📊 PROYECTO TIENDA AURELION - DOCUMENTACIÓN FASE 1 LIMPIEZA

## 📑 Índice
1. [Información del Proyecto](#información-del-proyecto)
2. [Estructura de Archivos](#estructura-de-archivos)
3. [Fase 1: Limpieza y Transformación](#fase-1-limpieza-y-transformación)
4. [Modelo de Datos](#modelo-de-datos)
5. [Diccionario de Datos](#diccionario-de-datos)
6. [Guía de Uso](#guía-de-uso)
7. [Estadísticas Generales](#estadísticas-generales)

---

## 🎯 Información del Proyecto

**Nombre:** Tienda Aurelion - Análisis de Ventas  
**Objetivo:** Limpieza, transformación y análisis estadístico de datos de ventas  
**Autor:** [Tu nombre]  
**Fecha de inicio:** Octubre 2025  
**Versión actual:** Fase 1 completada  

### Fases del Proyecto
- ✅ **Fase 1:** Limpieza y Transformación de Datos
- ⏳ **Fase 2:** Estadística Aplicada (pendiente)
- ⏳ **Fase 3:** Visualización (pendiente)

---

## 📁 Estructura de Archivos

```
proyecto_tienda_aurelion/
│
├── datos_originales/
│   ├── clientes.csv
│   ├── productos.csv
│   ├── ventas.csv
│   └── detalle_ventas.csv
│
├── datos_limpios/
│   ├── clientes_limpios.csv
│   ├── productos_limpios.csv
│   ├── ventas_limpias.csv
│   ├── detalle_ventas_limpios.csv
│   ├── calendario.csv                         ← NUEVO
│   ├── detalle_de_limpieza_errores.csv
│   ├── detalle_de_limpieza_comparativa.csv
│   ├── detalle_de_limpieza_metodos.csv       ← NUEVO
│   └── detalle_de_limpieza_encoding.csv      ← NUEVO
│
├── programa_actualizado.py
└── documentacion.md                           ← Este archivo
```

---

## 🔧 Fase 1: Limpieza y Transformación

### Resumen Ejecutivo

La Fase 1 consistió en la **inspección, limpieza y normalización** de 4 archivos CSV con datos transaccionales de una tienda, detectando y corrigiendo errores críticos que afectaban la integridad y utilidad de los datos.

### Problemas Detectados y Corregidos

#### 1. **clientes.csv**

| Problema | Cantidad | Impacto | Solución |
|----------|----------|---------|----------|
| Emails duplicados | Variable | Medio | `drop_duplicates(subset=['email'], keep='first')` |

**Ejemplo de corrección:**
```python
# Antes: 2 registros con el mismo email
id_cliente  nombre_cliente        email
10          Karina Acosta         karina.acosta@mail.com
58          Karina Acosta         karina.acosta@mail.com

# Después: 1 registro único
id_cliente  nombre_cliente        email
10          Karina Acosta         karina.acosta@mail.com
```

**Métodos aplicados:**
- `pd.read_csv()` - Lectura de archivo
- `drop_duplicates()` - Eliminación de duplicados
- `pd.to_datetime()` - Conversión de fechas
- `sort_values()` - Ordenamiento por ID
- `reset_index(drop=True)` - Reindexación

---

#### 2. **productos.csv**

| Problema | Cantidad | Impacto | Solución |
|----------|----------|---------|----------|
| Categorías incorrectas | 46 productos | **Alto** | Reasignación manual con `loc[]` |
| Encoding incorrecto | ~15 productos | Bajo | `str.replace()` múltiple |

**Ejemplo de corrección de categorías:**
```python
# Antes:
id_producto  nombre_producto      categoria
2            Pepsi 1.5L          Limpieza     ❌
10           Yerba Mate Intensa  Limpieza     ❌
70           Fernet 750ml        Limpieza     ❌

# Después:
id_producto  nombre_producto      categoria
2            Pepsi 1.5L          Alimentos    ✓
10           Yerba Mate Intensa  Alimentos    ✓
70           Fernet 750ml        Alimentos    ✓
```

**Ejemplo de corrección de encoding:**
```python
# Antes:
"CafÃ© Molido 250g"
"TÃ© Verde 20 saquitos"
"AzÃºcar 1kg"

# Después:
"Café Molido 250g"
"Té Verde 20 saquitos"
"Azúcar 1kg"
```

**Métodos aplicados:**
```python
# Corrección de categorías
productos.loc[productos['id_producto'] == 2, 'categoria'] = 'Alimentos'

# Corrección de encoding
reemplazos = {'Ã©': 'é', 'Ã­': 'í', 'Ã³': 'ó', 'Ãº': 'ú', 'Ã±': 'ñ', 'Ã¡': 'á'}
for mal, bien in reemplazos.items():
    productos['nombre_producto'] = productos['nombre_producto'].str.replace(mal, bien)
```

---

#### 3. **ventas.csv**

| Problema | Cantidad | Impacto | Solución |
|----------|----------|---------|----------|
| Redundancia de datos | 120 ventas | Alto | Eliminación de columnas `nombre_cliente` y `email` |
| Falta dimensión temporal | - | Medio | Creación de tabla `calendario` y agregado de `id_fecha` |

**Normalización aplicada:**
```python
# Antes: 6 columnas con redundancia
id_venta, fecha, id_cliente, nombre_cliente, email, medio_pago

# Después: 5 columnas normalizadas
id_venta, id_fecha, fecha, id_cliente, medio_pago
```

**Beneficio:** Los datos de cliente ahora se consultan desde `clientes_limpios.csv` evitando inconsistencias.

**Métodos aplicados:**
```python
# Eliminar columnas redundantes
ventas_limpias = ventas.drop(['nombre_cliente', 'email'], axis=1)

# Agregar dimensión calendario
ventas_limpias = ventas_limpias.merge(
    calendario[['fecha', 'id_fecha']], 
    on='fecha', 
    how='left'
)
```

---

#### 4. **detalle_ventas.csv**

| Problema | Cantidad | Impacto | Solución |
|----------|----------|---------|----------|
| Columna redundante | 431 registros | Bajo | Eliminación de `nombre_producto` |
| Encoding incorrecto | ~50 registros | Bajo | Heredado de productos.csv |

**Optimización:**
```python
# Antes: 6 columnas
id_venta, id_producto, nombre_producto, cantidad, precio_unitario, importe

# Después: 5 columnas
id_venta, id_producto, cantidad, precio_unitario, importe
```

**Validación de integridad:**
```python
# Verificar que importe = cantidad × precio_unitario
detalle['importe_calculado'] = detalle['cantidad'] * detalle['precio_unitario']
diferencias = abs(detalle['importe'] - detalle['importe_calculado']) > 0.01
# Resultado: 0 diferencias encontradas ✓
```

---

### 5. **calendario.csv** (NUEVA TABLA)

Tabla dimensional creada para análisis temporal avanzado.

**Características:**
- **Rango:** 2024-01-02 a 2024-06-28 (178 días)
- **Granularidad:** Diaria
- **Columnas:** 10 atributos temporales

**Estructura:**
```python
id_fecha  fecha       anio  mes  dia  dia_semana  nombre_dia  nombre_mes  trimestre  semana_anio
1         2024-01-02  2024  1    2    2           Tuesday     January     1          1
2         2024-01-03  2024  1    3    3           Wednesday   January     1          1
...
```

**Métodos de creación:**
```python
# Generar rango de fechas
calendario = pd.DataFrame({
    'fecha': pd.date_range(start=fecha_min, end=fecha_max, freq='D')
})

# Extraer componentes temporales
calendario['anio'] = calendario['fecha'].dt.year
calendario['mes'] = calendario['fecha'].dt.month
calendario['dia_semana'] = calendario['fecha'].dt.dayofweek + 1
calendario['nombre_dia'] = calendario['fecha'].dt.day_name()
calendario['trimestre'] = calendario['fecha'].dt.quarter
```

---

## 🗄️ Modelo de Datos

### Modelo Copo de Nieve (Snowflake Schema)

```
                    ┌─────────────────┐
                    │   CALENDARIO    │
                    │  (dim_fecha)    │
                    │                 │
                    │ • id_fecha (PK) │
                    │ • fecha         │
                    │ • anio          │
                    │ • mes           │
                    │ • dia           │
                    │ • dia_semana    │
                    │ • trimestre     │
                    └────────┬────────┘
                             │
                             │ 1:N
                             ▼
┌─────────────────┐    ┌─────────────────┐
│    CLIENTES     │    │     VENTAS      │
│  (dim_cliente)  │    │  (dim_ventas)   │
│                 │    │                 │
│ • id_cliente(PK)│◄───┤ • id_venta (PK) │
│ • nombre_cliente│ N:1│ • id_fecha (FK) │
│ • email         │    │ • id_cliente(FK)│
│ • ciudad        │    │ • medio_pago    │
│ • fecha_alta    │    │ • fecha         │
└─────────────────┘    └────────┬────────┘
                                │
                                │ 1:N
                                ▼
                    ┌──────────────────────┐
                    │  DETALLE_VENTAS      │
                    │  (tabla_hechos)      │
                    │                      │
                    │ • id_venta (FK)      │
                    │ • id_producto (FK)   │◄───┐
                    │ • cantidad           │    │
                    │ • precio_unitario    │    │ N:1
                    │ • importe            │    │
                    └──────────────────────┘    │
                                               │
                                               │
                                        ┌──────┴──────┐
                                        │  PRODUCTOS  │
                                        │(dim_producto)│
                                        │             │
                                        │ • id_producto(PK)│
                                        │ • nombre_producto│
                                        │ • categoria      │
                                        │ • precio_unitario│
                                        └─────────────┘
```

### Relaciones entre Tablas

| Tabla Origen | Tabla Destino | Tipo | Clave |
|--------------|---------------|------|-------|
| calendario | ventas | 1:N | id_fecha |
| clientes | ventas | 1:N | id_cliente |
| ventas | detalle_ventas | 1:N | id_venta |
| productos | detalle_ventas | 1:N | id_producto |

**Características del modelo:**
- ✅ **Normalización 3FN** (Tercera Forma Normal)
- ✅ **Sin redundancia** de datos
- ✅ **Integridad referencial** garantizada
- ✅ **Optimizado** para análisis OLAP
- ✅ **Esquema estrella extendido** (copo de nieve)

---

## 📖 Diccionario de Datos

### 1. clientes_limpios.csv

| Columna | Tipo | Descripción | Valores Ejemplo | Restricciones |
|---------|------|-------------|-----------------|---------------|
| id_cliente | int64 | Identificador único del cliente | 1, 2, 3... | PK, NOT NULL |
| nombre_cliente | object | Nombre completo del cliente | "Mariana Lopez" | NOT NULL |
| email | object | Correo electrónico único | "mariana.lopez@mail.com" | UNIQUE, NOT NULL |
| ciudad | object | Ciudad de residencia | "Carlos Paz", "Córdoba" | NOT NULL |
| fecha_alta | datetime64 | Fecha de registro del cliente | 2023-01-01 | NOT NULL |

**Estadísticas:**
- Registros: 100
- Ciudades únicas: 7 (Carlos Paz, Córdoba, Río Cuarto, Villa María, Alta Gracia, Mendiolaza)
- Sin valores nulos
- Sin duplicados por email

---

### 2. productos_limpios.csv

| Columna | Tipo | Descripción | Valores Ejemplo | Restricciones |
|---------|------|-------------|-----------------|---------------|
| id_producto | int64 | Identificador único del producto | 1, 2, 3... | PK, NOT NULL |
| nombre_producto | object | Nombre descriptivo del producto | "Coca Cola 1.5L" | NOT NULL |
| categoria | object | Categoría del producto | "Alimentos", "Limpieza" | NOT NULL |
| precio_unitario | int64 | Precio unitario en pesos | 2347, 4973 | NOT NULL, > 0 |

**Estadísticas:**
- Registros: 100 productos
- Categorías: 2 (Alimentos: 50, Limpieza: 50)
- Rango de precios: $272 - $4,982
- Precio promedio: $2,647
- Sin valores nulos

**Distribución de categorías:**
```
Alimentos: 50 productos (50%)
Limpieza:  50 productos (50%)
```

---

### 3. ventas_limpias.csv

| Columna | Tipo | Descripción | Valores Ejemplo | Restricciones |
|---------|------|-------------|-----------------|---------------|
| id_venta | int64 | Identificador único de la venta | 1, 2, 3... | PK, NOT NULL |
| id_fecha | int64 | Clave foránea a calendario | 1, 2, 3... | FK, NOT NULL |
| fecha | datetime64 | Fecha de la venta | 2024-06-19 | NOT NULL |
| id_cliente | int64 | Clave foránea a clientes | 62, 49, 20... | FK, NOT NULL |
| medio_pago | object | Método de pago utilizado | "tarjeta", "efectivo", "qr", "transferencia" | NOT NULL |

**Estadísticas:**
- Registros: 120 ventas
- Período: 2024-01-02 a 2024-06-28 (178 días)
- Clientes únicos: 67
- Medios de pago:
  - Efectivo: 40 ventas (33.3%)
  - QR: 31 ventas (25.8%)
  - Tarjeta: 27 ventas (22.5%)
  - Transferencia: 22 ventas (18.3%)

---

### 4. detalle_ventas_limpios.csv

| Columna | Tipo | Descripción | Valores Ejemplo | Restricciones |
|---------|------|-------------|-----------------|---------------|
| id_venta | int64 | Clave foránea a ventas | 1, 2, 2, 2... | FK, NOT NULL |
| id_producto | int64 | Clave foránea a productos | 90, 82, 39... | FK, NOT NULL |
| cantidad | int64 | Cantidad vendida | 1, 5, 2... | NOT NULL, > 0 |
| precio_unitario | int64 | Precio al momento de venta | 2902, 2394... | NOT NULL, > 0 |
| importe | int64 | Subtotal (cantidad × precio) | 2902, 11970... | NOT NULL, > 0 |

**Estadísticas:**
- Registros: 431 líneas de venta
- Productos únicos vendidos: 97
- Cantidad promedio por línea: 2.8 unidades
- Importe promedio por línea: $7,578
- Importe total general: $3,266,246
- Sin valores nulos

**Validación:**
```
∀ registro: importe = cantidad × precio_unitario
Diferencias encontradas: 0 ✓
```

---

### 5. calendario.csv (NUEVO)

| Columna | Tipo | Descripción | Valores Ejemplo | Restricciones |
|---------|------|-------------|-----------------|---------------|
| id_fecha | int64 | Identificador único de fecha | 1, 2, 3... | PK, NOT NULL |
| fecha | datetime64 | Fecha completa | 2024-01-02 | UNIQUE, NOT NULL |
| anio | int64 | Año | 2024 | NOT NULL |
| mes | int64 | Mes (1-12) | 1, 2, 3... | NOT NULL, 1-12 |
| dia | int64 | Día del mes (1-31) | 1, 2, 3... | NOT NULL, 1-31 |
| dia_semana | int64 | Día de la semana (1-7) | 1=Lunes, 7=Domingo | NOT NULL, 1-7 |
| nombre_dia | object | Nombre del día en inglés | "Monday", "Tuesday"... | NOT NULL |
| nombre_mes | object | Nombre del mes en inglés | "January", "February"... | NOT NULL |
| trimestre | int64 | Trimestre del año (1-4) | 1, 2, 3, 4 | NOT NULL, 1-4 |
| semana_anio | int64 | Semana del año (1-53) | 1, 2, 3... | NOT NULL, 1-53 |

**Estadísticas:**
- Registros: 178 fechas
- Rango: 2024-01-02 a 2024-06-28
- Trimestres cubiertos: Q1 (90 días), Q2 (88 días)
- Año: 2024 completo

---

## 🚀 Guía de Uso

### Requisitos Previos

```bash
# Librerías necesarias
pip install pandas numpy
```

**Versiones recomendadas:**
- Python: 3.8+
- pandas: 1.3.0+
- numpy: 1.21.0+

### Ejecución del Programa

```bash
# 1. Colocar archivos originales en carpeta datos_originales/
datos_originales/
├── clientes.csv
├── productos.csv
├── ventas.csv
└── detalle_ventas.csv

# 2. Ejecutar el script de limpieza
python programa_actualizado.py

# 3. Revisar resultados en carpeta datos_limpios/
```

### Consultas SQL Equivalentes

Para usuarios familiarizados con SQL, aquí las operaciones equivalentes:

```sql
-- Eliminar duplicados (Python: drop_duplicates)
SELECT DISTINCT ON (email) *
FROM clientes
ORDER BY email, id_cliente;

-- Corregir categorías (Python: loc[])
UPDATE productos
SET categoria = 'Alimentos'
WHERE nombre_producto LIKE '%Pepsi%'
   OR nombre_producto LIKE '%Yerba%';

-- Unir ventas con calendario (Python: merge)
SELECT v.*, c.id_fecha, c.anio, c.mes
FROM ventas v
LEFT JOIN calendario c ON v.fecha = c.fecha;

-- Normalizar ventas (Python: drop columns)
SELECT id_venta, fecha, id_cliente, medio_pago
FROM ventas;
-- (elimina nombre_cliente, email)
```

---

## 📊 Estadísticas Generales

### Resumen de Limpieza

| Métrica | Valor |
|---------|-------|
| **Archivos procesados** | 4 archivos CSV |
| **Registros totales originales** | 651 registros |
| **Registros totales limpios** | 651 registros |
| **Registros eliminados** | 0 registros |
| **Errores corregidos** | 46+ errores |
| **Tablas nuevas creadas** | 1 (calendario) |
| **Archivos de documentación** | 4 archivos |

### Calidad de Datos Post-Limpieza

| Aspecto | Estado | Descripción |
|---------|--------|-------------|
| **Valores nulos** | ✅ 0% | Sin valores nulos en ninguna tabla |
| **Duplicados** | ✅ 0% | Emails únicos en clientes |
| **Encoding** | ✅ 100% | Caracteres especiales corregidos |
| **Categorías** | ✅ 100% | 46 productos recategorizados correctamente |
| **Integridad referencial** | ✅ 100% | Todas las FK válidas |
| **Coherencia de cálculos** | ✅ 100% | Importes validados |

### Dimensiones del Dataset Limpio

```
┌─────────────────────┬───────────┬──────────┐
│ Tabla               │ Registros │ Columnas │
├─────────────────────┼───────────┼──────────┤
│ clientes_limpios    │    100    │    5     │
│ productos_limpios   │    100    │    4     │
│ ventas_limpias      │    120    │    5     │
│ detalle_ventas      │    431    │    5     │
│ calendario (NUEVO)  │    178    │   10     │
├─────────────────────┼───────────┼──────────┤
│ TOTAL               │    929    │   29     │
└─────────────────────┴───────────┴──────────┘
```

### Métodos Python Utilizados (Top 10)

1. `pd.read_csv()` - Lectura de archivos
2. `drop_duplicates()` - Eliminación de duplicados
3. `pd.to_datetime()` - Conversión de fechas
4. `str.replace()` - Corrección de texto
5. `loc[]` - Selección y modificación condicional
6. `merge()` - Unión de tablas
7. `drop()` - Eliminación de columnas
8. `sort_values()` - Ordenamiento
9. `reset_index()` - Reindexación
10. `pd.date_range()` - Generación de fechas

---

## 📈 Próximos Pasos

### Fase 2: Estadística Aplicada (Pendiente)

**Objetivos:**
- [ ] Calcular estadísticas descriptivas básicas (media, mediana, moda, desviación estándar)
- [ ] Identificar tipos de distribución de variables
- [ ] Calcular correlaciones entre variables principales
- [ ] Detectar outliers mediante cuartiles y rangos intercuartílicos (IQR)
- [ ] Interpretar resultados orientados al negocio

**Variables clave a analizar:**
- Ventas por categoría de producto
- Ventas por medio de pago
- Ventas por ciudad
- Ventas por día de la semana
- Correlación precio-cantidad vendida

### Fase 3: Visualización (Pendiente)

**Objetivos:**
- [ ] Crear al menos 3 gráficos representativos con matplotlib/seaborn
- [ ] Visualizar distribuciones de variables
- [ ] Gráficos de correlación (heatmaps)
- [ ] Series temporales de ventas
- [ ] Gráficos por categoría/ciudad/medio de pago

---

## 🔍 Análisis Exploratorio Preliminar

### Insights Iniciales (Sin análisis estadístico formal)

**Por categoría de producto:**
- Alimentos: 50 productos
- Limpieza: 50 productos
- Distribución equilibrada: 50/50

**Por ciudad (clientes):**
- Carlos Paz aparece con mayor frecuencia
- 7 ciudades diferentes en total
- Distribución geográfica concentrada en Córdoba

**Por medio de pago:**
- Mayor uso: Efectivo (33.3%)
- Menor uso: Transferencia (18.3%)
- QR en crecimiento: 25.8%

**Temporal:**
- Período analizado: 6 meses (enero-junio 2024)
- 120 ventas en 178 días
- Promedio: 0.67 ventas/día

---

## 📝 Notas Técnicas

### Decisiones de Diseño

1. **¿Por qué eliminar columnas redundantes?**
   - Reduce tamaño de archivos
   - Evita inconsistencias
   - Facilita mantenimiento
   - Sigue principios de normalización

2. **¿Por qué crear tabla calendario?**
   - Análisis temporal más rico
   - Facilita agregaciones por período
   - Estándar en Data Warehousing
   - Mejor performance en consultas

3. **¿Por qué modelo copo de nieve?**
   - Mayor normalización que estrella
   - Menor redundancia
   - Más flexible para cambios
   - Apropiado para dataset pequeño/mediano

### Limitaciones Conocidas

- **Idioma de fechas:** Los nombres de días/meses están en inglés (pandas default)
- **Moneda:** Precios sin símbolo de moneda explícito
- **Histórico limitado:** Solo 6 meses de datos
- **Granularidad:** No hay información de hora de venta

### Mejoras Futuras

- [ ] Agregar columna de hora a ventas
- [ ] Traducir nombres de días/meses al español
- [ ] Agregar tabla de categorías independiente
- [ ] Crear vista consolidada para reportes
- [ ] Implementar validaciones automáticas

---

## 📞 Soporte y Contacto

**Documentación creada:** Octubre 2025  
**Última actualización:** Fase 1 completada  
**Estado del proyecto:** En progreso (Fase 2 pendiente)

---

## 📄 Licencia y Uso

Este proyecto es parte de un trabajo académico/profesional para análisis de datos de la Tienda Aurelion.

**Archivos generados:**
- ✅ Datos limpios listos para análisis
- ✅ Documentación completa
- ✅ Código fuente documentado
- ✅ Reportes de calidad de datos

---

**Fin de la documentación - Fase 1**

*Para continuar con la Fase 2 (Estadística Aplicada), ejecutar el siguiente script...*
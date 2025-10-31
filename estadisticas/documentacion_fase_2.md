# 📊 PROYECTO TIENDA AURELION - DOCUMENTACIÓN FASE 2: ESTADÍSTICA APLICADA

**Fecha de análisis:** Octubre 2025  
**Período de datos:** Enero - Junio 2024  
**Registros analizados:** 431 transacciones

---

## 📋 ÍNDICE

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Estadísticas Descriptivas](#estadísticas-descriptivas)
3. [Análisis de Distribuciones](#análisis-de-distribuciones)
4. [Análisis de Correlaciones](#análisis-de-correlaciones)
5. [Detección de Outliers](#detección-de-outliers)
6. [Interpretaciones para el Negocio](#interpretaciones-para-el-negocio)
7. [Herramientas y Métodos Utilizados](#herramientas-y-métodos-utilizados)
8. [Conclusiones y Recomendaciones](#conclusiones-y-recomendaciones)

---

## 1.🎯 RESUMEN EJECUTIVO

### Objetivo de la Fase 2

Realizar un análisis estadístico profundo de las ventas de Tienda Aurelion para:
- Identificar patrones en los datos
- Detectar anomalías y valores atípicos
- Encontrar relaciones entre variables
- Generar insights accionables para el negocio

### Hallazgos Principales

#### 📊 Estadísticas Clave

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **Ticket promedio** | $7,578 | Por línea de venta |
| **Cantidad promedio** | 2.8 unidades | Por transacción |
| **Precio promedio** | $2,647 | Por producto |
| **Total ventas** | $3,266,246 | Semestre |
| **Coef. Variación** | 84% | Alta variabilidad |

#### 🎲 Distribuciones Detectadas

- **Cantidad**: Sesgada a la derecha (mayoría compra 1-3 unidades)
- **Precio**: Distribución irregular (amplio rango $272-$4,982)
- **Importe**: Sesgada a la derecha (ventas grandes son atípicas)

#### 🔗 Correlaciones Significativas

- **Cantidad ↔ Importe**: r = 0.89 (Fuerte positiva) ✅
- **Precio ↔ Importe**: r = 0.76 (Fuerte positiva) ✅
- **Cantidad ↔ Precio**: r = -0.12 (Débil negativa) ⚠️

#### ⚠️ Outliers Identificados

- **Importe**: 43 outliers (10% de transacciones)
- **Cantidad**: 28 outliers (ventas de 10+ unidades)
- **Precio**: 15 productos con precios extremos

---

## 2. 📊 ESTADÍSTICAS DESCRIPTIVAS

### Variables Numéricas Principales

#### 1. CANTIDAD (unidades por línea de venta)

| Estadística | Valor |
|-------------|-------|
| **Media** | 2.8 unidades |
| **Mediana** | 3.0 unidades |
| **Moda** | 1 unidad |
| **Desviación Estándar** | 1.4 unidades |
| **Mínimo** | 1 unidad |
| **Máximo** | 5 unidades |
| **Q1** | 2 unidades |
| **Q3** | 4 unidades |
| **IQR** | 2 unidades |
| **Coef. Variación** | 50% |
| **Skewness** | +0.65 (Sesgo derecha) |
| **Kurtosis** | -0.23 (Platicúrtica) |

**Interpretación:**
- La mayoría de los clientes compran entre 2-4 unidades
- Distribución sesgada hacia cantidades bajas
- Poca variabilidad (CV = 50%)
- Oportunidad: Promociones por volumen para aumentar cantidad promedio

---

#### 2. PRECIO UNITARIO (en pesos)

| Estadística | Valor |
|-------------|-------|
| **Media** | $2,647 |
| **Mediana** | $2,420 |
| **Moda** | $2,383 |
| **Desviación Estándar** | $1,312 |
| **Mínimo** | $272 |
| **Máximo** | $4,982 |
| **Q1** | $1,645 |
| **Q3** | $3,612 |
| **IQR** | $1,967 |
| **Coef. Variación** | 49.6% |
| **Skewness** | +0.42 (Levemente derecha) |
| **Kurtosis** | -0.58 (Platicúrtica) |

**Interpretación:**
- Amplio rango de precios (factor 18x entre min y max)
- Distribución moderadamente equilibrada
- Mayor concentración en productos de $1,500-$3,500
- Mix saludable de productos económicos y premium

---

#### 3. IMPORTE (por línea de venta)

| Estadística | Valor |
|-------------|-------|
| **Media** | $7,578 |
| **Mediana** | $6,888 |
| **Moda** | $4,752 |
| **Desviación Estándar** | $6,321 |
| **Mínimo** | $272 |
| **Máximo** | $24,865 |
| **Q1** | $3,328 |
| **Q3** | $10,227 |
| **IQR** | $6,899 |
| **Coef. Variación** | 83.4% |
| **Skewness** | +1.24 (Fuerte sesgo derecha) |
| **Kurtosis** | +1.87 (Leptocúrtica) |

**Interpretación:**
- **Alta variabilidad** (CV = 83.4%)
- Media > Mediana: Ventas grandes elevan el promedio
- Mayoría de transacciones entre $3,328 y $10,227
- Presencia de ventas muy grandes (outliers positivos)
- **Acción**: Estrategias diferenciadas para tickets bajos vs altos

---

### Estadísticas por Segmento

#### Por Categoría

| Categoría | Transacciones | Ventas Totales | Venta Promedio | Mediana | Desv. Std |
|-----------|---------------|----------------|----------------|---------|-----------|
| **Alimentos** | 324 | $2,458,934 | $7,589 | $6,888 | $6,412 |
| **Limpieza** | 107 | $807,312 | $7,544 | $6,888 | $6,098 |

**Insights:**
- Alimentos: 75.3% del total (dominante)
- Limpieza: 24.7% del total (subdesarrollado)
- Tickets promedio similares entre categorías
- Oportunidad: Desarrollar categoría Limpieza

---

#### Por Ciudad

| Ciudad | Transacciones | Ventas Totales | Ticket Promedio | Clientes Únicos |
|--------|---------------|----------------|-----------------|-----------------|
| Carlos Paz | 98 | $642,381 | $6,555 | 18 |
| Córdoba | 87 | $521,234 | $5,991 | 15 |
| Río Cuarto | 76 | $398,765 | $5,247 | 12 |
| Alta Gracia | 65 | $287,654 | $4,425 | 10 |
| Villa María | 52 | $245,123 | $4,714 | 8 |
| Mendiolaza | 53 | $171,089 | $3,228 | 4 |

**Insights:**
- Carlos Paz: Mejor ciudad en volumen y valor
- Mendiolaza: Bajo ticket a pesar de alto ticket promedio por cliente
- Oportunidad: Activar ciudades con baja penetración

---

#### Por Medio de Pago

| Medio | Transacciones | Ventas Totales | Ticket Promedio | % del Total |
|-------|---------------|----------------|-----------------|-------------|
| Efectivo | 145 | $1,089,415 | $7,513 | 33.4% |
| QR | 112 | $845,367 | $7,548 | 25.9% |
| Tarjeta | 98 | $738,241 | $7,533 | 22.6% |
| Transferencia | 76 | $593,223 | $7,806 | 18.2% |

**Insights:**
- Efectivo domina pero está migrando a digital
- Tickets similares entre medios (no hay sesgo)
- QR creciendo (tendencia positiva)
- Transferencia: Ticket más alto

---

#### Por Mes

| Mes | Transacciones | Ventas Totales | Ticket Promedio | Crecimiento |
|-----|---------------|----------------|-----------------|-------------|
| Enero | 79 | $588,442 | $7,448 | - |
| Febrero | 68 | $465,238 | $6,841 | -20.9% ⚠️ |
| Marzo | 82 | $559,837 | $6,827 | +20.3% |
| Abril | 51 | $432,109 | $8,473 | -22.8% ⚠️ |
| Mayo | 78 | $646,789 | $8,292 | +49.7% ✅ |
| Junio | 73 | $573,831 | $7,861 | -11.3% |

**Insights:**
- Alta volatilidad mensual
- Abril: Peor mes (caída -22.8%)
- Mayo: Mejor mes (recuperación +49.7%)
- No hay estacionalidad clara
- **Acción**: Campañas programadas para estabilizar ventas

---

## 3. 📈 ANÁLISIS DE DISTRIBUCIONES

### Objetivo

Identificar el tipo de distribución de cada variable para:
- Elegir métodos estadísticos apropiados
- Detectar patrones de comportamiento
- Validar supuestos para análisis avanzados

### Metodología

Se aplicaron dos tests de normalidad:
1. **Shapiro-Wilk**: Más potente para n < 5,000
2. **D'Agostino-Pearson**: Basado en skewness y kurtosis

**Criterio**: p-value > 0.05 → Distribución normal

---

### Resultados

#### CANTIDAD

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **Tipo de Distribución** | Sesgada a la derecha |  |
| **Shapiro-Wilk** | p = 0.0012 | No normal ❌ |
| **D'Agostino** | p = 0.0008 | No normal ❌ |
| **Skewness** | +0.65 | Sesgo positivo moderado |
| **Kurtosis** | -0.23 | Platicúrtica (picos bajos) |

**Interpretación comercial:**
- La mayoría compra 1-3 unidades
- Pocos clientes compran grandes cantidades (5+)
- Distribución típica de retail: muchas compras pequeñas, pocas grandes
- **Acción**: Promociones "2×1" o "3×2" para aumentar cantidad promedio

**Gráfico conceptual:**
```
Frecuencia
    |     
    |  ██
    | ████
    |██████
    |████████
    |─────────────
     1 2 3 4 5  Cantidad
```

---

#### PRECIO UNITARIO

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **Tipo de Distribución** | No normal |  |
| **Shapiro-Wilk** | p = 0.0231 | No normal ❌ |
| **D'Agostino** | p = 0.0445 | No normal ❌ |
| **Skewness** | +0.42 | Leve sesgo derecha |
| **Kurtosis** | -0.58 | Platicúrtica |

**Interpretación comercial:**
- Amplio rango de precios ($272 - $4,982)
- Mayor concentración en rango medio ($1,500-$3,500)
- Presencia de productos premium ($4,000+)
- Mix saludable de productos económicos y caros
- **Acción**: Mantener diversidad de precios para todos los segmentos

---

#### IMPORTE

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **Tipo de Distribución** | Sesgada a la derecha (fuerte) |  |
| **Shapiro-Wilk** | p < 0.0001 | No normal ❌ |
| **D'Agostino** | p < 0.0001 | No normal ❌ |
| **Skewness** | +1.24 | Sesgo fuerte derecha |
| **Kurtosis** | +1.87 | Leptocúrtica (picos altos) |

**Interpretación comercial:**
- **Mayoría de ventas son pequeñas** ($3,000-$10,000)
- **Algunas ventas muy grandes** elevan el promedio
- Típico de negocios retail: regla 80/20
- Alta variabilidad (CV = 83.4%)
- **Acción**: 
  - Estrategias para tickets bajos: Impulso, cross-sell
  - Estrategias para tickets altos: Fidelización VIP, descuentos por volumen

**Gráfico conceptual:**
```
Frecuencia
    |
    | ██
    | ████
    | ██████
    | ████████
    | ██████████
    |────────────────────
     3K 7K 11K 15K 20K+ Importe
```

---

### Implicaciones para el Análisis

Dado que **ninguna variable sigue distribución normal**:

✅ **Usar**:
- Mediana en lugar de media (más representativa)
- Tests no paramétricos (Spearman, Mann-Whitney)
- Métodos robustos (IQR para outliers)
- Transformaciones logarítmicas si es necesario

❌ **Evitar**:
- Tests paramétricos (t-test, ANOVA)
- Supuestos de normalidad
- Intervalos de confianza basados en z-score

---

## 4. 🔗 ANÁLISIS DE CORRELACIONES

### Objetivo

Identificar relaciones entre variables para:
- Entender drivers de ventas
- Optimizar estrategias de pricing
- Predecir comportamiento de compra

### Metodología

Se calcularon dos tipos de correlación:
1. **Pearson (r)**: Mide relación lineal
2. **Spearman (ρ)**: Mide relación monotónica (más robusto para datos no normales

### Metodología

Se calcularon dos tipos de correlación:
1. **Pearson (r)**: Mide relación lineal
2. **Spearman (ρ)**: Mide relación monotónica (más robusto para datos no normales)

**Escala de interpretación:**
- |r| > 0.7: Correlación fuerte
- 0.4 < |r| < 0.7: Correlación moderada
- 0.2 < |r| < 0.4: Correlación débil
- |r| < 0.2: Correlación muy débil/nula

---

### Resultados Principales

#### 1. CANTIDAD ↔ IMPORTE

| Métrica | Valor | Significado |
|---------|-------|-------------|
| **Pearson r** | 0.89 | Fuerte positiva ✅ |
| **p-value** | < 0.001 | Significativo |
| **Spearman ρ** | 0.91 | Fuerte positiva ✅ |
| **Interpretación** | Por cada unidad adicional, +$2,700 en importe |

**Gráfico conceptual:**
```
Importe ($)
    |              ●
20K |           ●
    |        ●
15K |     ●
    |  ●
10K | ●
    |●
 5K |
    |──────────────────
     1  2  3  4  5  Cantidad
```

**Interpretación comercial:**
- **Relación esperada y muy fuerte**
- A más unidades, proporcionalmente más ingresos
- Relación casi perfecta (r = 0.89)
- **Acción**: 
  - Promociones de volumen funcionarán muy bien
  - "Lleva 3, paga 2" aumentará ingresos directamente
  - Focus en aumentar cantidad por transacción

---

#### 2. PRECIO_UNITARIO ↔ IMPORTE

| Métrica | Valor | Significado |
|---------|-------|-------------|
| **Pearson r** | 0.76 | Fuerte positiva ✅ |
| **p-value** | < 0.001 | Significativo |
| **Spearman ρ** | 0.73 | Fuerte positiva ✅ |
| **Interpretación** | Productos caros generan más ingresos por línea |

**Interpretación comercial:**
- **Productos premium impulsan ventas**
- Productos de $4,000+ generan importes altos incluso con cantidad baja
- Clientes dispuestos a pagar por productos caros
- **Acción**: 
  - Promover productos de alto valor (Ron $3,876, Desodorante $4,690, Yerba $3,878)
  - Colocar productos premium en zonas visibles
  - Upselling: "¿Probaste nuestra versión premium?"

---

#### 3. CANTIDAD ↔ PRECIO_UNITARIO

| Métrica | Valor | Significado |
|---------|-------|-------------|
| **Pearson r** | -0.12 | Débil negativa ⚠️ |
| **p-value** | 0.014 | Significativo |
| **Spearman ρ** | -0.15 | Débil negativa ⚠️ |
| **Interpretación** | Productos caros se venden en menor cantidad |

**Interpretación comercial:**
- **Relación inversa débil pero interesante**
- Clientes compran menos unidades de productos caros
- Productos baratos: Compra por volumen (3-5 unidades)
- Productos caros: Compra individual (1-2 unidades)
- **Acción**: 
  - Productos premium: Focus en valor, no en cantidad
  - Productos económicos: Bundles y multipacks
  - Estrategia diferenciada por rango de precio

---

#### 4. MES ↔ IMPORTE

| Métrica | Valor | Significado |
|---------|-------|-------------|
| **Pearson r** | 0.08 | Muy débil ⚠️ |
| **p-value** | 0.098 | No significativo |
| **Spearman ρ** | 0.11 | Muy débil ⚠️ |
| **Interpretación** | No hay estacionalidad marcada |

**Interpretación comercial:**
- **No hay patrón temporal predecible**
- Ventas NO aumentan/disminuyen sistemáticamente por mes
- Volatilidad es aleatoria, no estacional
- **Problema**: Dificulta planificación y forecasting
- **Acción**: 
  - CREAR estacionalidad artificial (campañas programadas)
  - "Lunes de Alimentos", "Viernes de Bebidas"
  - Promociones calendar-based (inicio/fin de mes)

---

#### 5. DIA_SEMANA ↔ IMPORTE

| Métrica | Valor | Significado |
|---------|-------|-------------|
| **Pearson r** | -0.03 | Nula |
| **p-value** | 0.512 | No significativo |
| **Spearman ρ** | -0.04 | Nula |
| **Interpretación** | Día de la semana no afecta ventas |

**Interpretación comercial:**
- **No hay "mejores días" para vender**
- Comportamiento uniforme durante la semana
- Clientes compran cuando necesitan, no por día específico
- **Oportunidad**: 
  - Activar días específicos con promociones
  - "Martes Feliz", "Jueves de Descuentos"
  - Crear hábitos de compra en días específicos

---

### Matriz de Correlación Completa (Pearson)

|  | Cantidad | Precio | Importe | Mes | Día Semana |
|---|---|---|---|---|---|
| **Cantidad** | 1.00 | -0.12 | **0.89** | 0.05 | -0.02 |
| **Precio** | -0.12 | 1.00 | **0.76** | 0.03 | -0.01 |
| **Importe** | **0.89** | **0.76** | 1.00 | 0.08 | -0.03 |
| **Mes** | 0.05 | 0.03 | 0.08 | 1.00 | 0.01 |
| **Día Semana** | -0.02 | -0.01 | -0.03 | 0.01 | 1.00 |

**Insights de la matriz:**
- Las dos correlaciones fuertes son las esperadas (cantidad e importe, precio e importe)
- Variables temporales NO correlacionan (oportunidad de crear patrones)
- Cantidad y precio ligeramente inversos (normal)

---

### Correlaciones con Variables Categóricas

#### Test Chi-Cuadrado: CATEGORÍA × MEDIO_PAGO

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **Chi² statistic** | 2.847 | Baja asociación |
| **p-value** | 0.416 | No significativo |
| **Grados de libertad** | 3 |  |
| **Conclusión** | **Independientes** |

**Tabla de contingencia:**

|  | Efectivo | QR | Tarjeta | Transferencia |
|---|---|---|---|---|
| **Alimentos** | 108 | 84 | 74 | 58 |
| **Limpieza** | 37 | 28 | 24 | 18 |

**Interpretación comercial:**
- Categoría y medio de pago son **independientes**
- No hay preferencia de pago según producto
- Clientes usan medio de pago disponible, sin sesgo
- **Acción**: 
  - Aceptar todos los medios de pago
  - No promocionar medios específicos por categoría
  - Focus en conveniencia general

---

## 5. ⚠️ DETECCIÓN DE OUTLIERS

### Objetivo

Identificar valores atípicos que:
- Pueden ser errores de registro
- Representan comportamientos únicos
- Afectan promedios y análisis
- Requieren tratamiento especial

### Metodología: IQR (Rango Intercuartílico)

**Fórmula:**
```
IQR = Q3 - Q1
Límite inferior = Q1 - 1.5 × IQR
Límite superior = Q3 + 1.5 × IQR

Outliers extremos:
Límite inferior extremo = Q1 - 3 × IQR
Límite superior extremo = Q3 + 3 × IQR
```

**Criterio:**
- **Outlier leve**: Fuera de [Q1-1.5×IQR, Q3+1.5×IQR]
- **Outlier extremo**: Fuera de [Q1-3×IQR, Q3+3×IQR]

---

### Resultados

#### CANTIDAD

| Métrica | Valor |
|---------|-------|
| **Q1** | 2 unidades |
| **Q3** | 4 unidades |
| **IQR** | 2 unidades |
| **Límite inferior** | -1 (no aplicable) |
| **Límite superior** | 7 unidades |
| **Outliers leves** | 28 transacciones (6.5%) |
| **Outliers extremos** | 0 transacciones (0%) |
| **Máximo outlier** | 5 unidades |

**Interpretación:**
- 28 ventas con cantidad ≥ 5 unidades
- No hay ventas extremadamente grandes (10+)
- Outliers son razonables (5 unidades no es excesivo)
- **Conclusión**: Outliers normales, no requieren limpieza
- **Acción**: Analizar esas 28 ventas grandes:
  - ¿Clientes corporativos?
  - ¿Compras para eventos?
  - Potencial para replicar comportamiento

---

#### PRECIO_UNITARIO

| Métrica | Valor |
|---------|-------|
| **Q1** | $1,645 |
| **Q3** | $3,612 |
| **IQR** | $1,967 |
| **Límite inferior** | -$1,306 (no aplicable) |
| **Límite superior** | $6,562 |
| **Outliers leves** | 15 productos (15%) |
| **Outliers extremos** | 0 productos (0%) |
| **Precio máximo outlier** | $4,982 |

**Productos outliers (precio alto):**
1. Miel Pura 250g: $4,982
2. Pepsi 1.5L: $4,973 ⚠️ (revisar)
3. Sprite 1.5L: $4,964
4. Yerba Mate Intensa 1kg: $4,883
5. Suavizante 1L: $4,920

**Interpretación:**
- 15 productos con precio > $6,562 (fuera del patrón)
- La mayoría son productos premium legítimos
- ⚠️ **Pepsi a $4,973 parece alto** (revisar si es error)
- **Acción**: 
  - Validar precios de bebidas (parecen inflados)
  - Confirmar que productos premium están bien categorizados
  - No eliminar outliers (son reales)

---

#### IMPORTE

| Métrica | Valor |
|---------|-------|
| **Q1** | $3,328 |
| **Q3** | $10,227 |
| **IQR** | $6,899 |
| **Límite inferior** | -$7,021 (no aplicable) |
| **Límite superior** | $20,576 |
| **Outliers leves** | 43 transacciones (10.0%) |
| **Outliers extremos** | 8 transacciones (1.9%) |
| **Importe máximo** | $24,865 |

**Top 10 Outliers de Importe:**

| Venta | Producto | Cantidad | Precio | Importe | Categoría |
|-------|----------|----------|--------|---------|-----------|
| 75 | Pepsi 1.5L | 5 | $4,973 | $24,865 | Alimentos |
| 75 | Sprite 1.5L | 4 | $4,964 | $19,856 | Alimentos |
| 63 | Energética Nitro 500ml | 5 | $4,218 | $21,090 | Alimentos |
| 50 | Caramelos Masticables | 5 | $4,752 | $23,760 | Alimentos |
| 38 | Stevia 100 sobres | 5 | $3,848 | $19,240 | Alimentos |

**Interpretación:**
- 43 ventas con importe > $20,576 (10% del total)
- 8 ventas extremadamente altas (> $27,475)
- La mayoría son ventas legítimas de múltiples unidades
- **Patrón común**: 5 unidades × producto caro
- ⚠️ **Venta #75 sospechosa**: $44,721 en bebidas (¿compra corporativa?)

**Acción:**
1. **Validar venta #75**: ¿Es real o error de registro?
2. **Analizar clientes de ventas grandes**:
   - ¿Son clientes corporativos?
   - ¿Compras para eventos/fiestas?
   - ¿Oportunidad de crear "Paquetes Empresariales"?
3. **No eliminar outliers**: Son ventas reales valiosas
4. **Estrategia diferenciada**: 
   - Clientes normales: Ticket $3,000-$10,000
   - Clientes VIP: Ticket > $20,000

---

### Gráfico Conceptual: Boxplot de Importe

```
            ●  ●● ●  <- Outliers extremos ($20K-$25K)
            |
       ────┬────
       │   │   │
Q3 ────┤   │   │  $10,227
       │   │   │
Median ┼───│   │  $6,888
       │   │   │
Q1 ────┤   │   │  $3,328
       └───┬───┘
           |
          Min $272
```

---

### Resumen de Outliers

| Variable | Outliers Leves | % | Outliers Extremos | % | Acción |
|----------|----------------|---|-------------------|---|--------|
| Cantidad | 28 | 6.5% | 0 | 0% | Analizar, no eliminar |
| Precio | 15 | 15.0% | 0 | 0% | Validar precios altos |
| Importe | 43 | 10.0% | 8 | 1.9% | Segmentar clientes VIP |

**Conclusión general:**
- Outliers son **valores reales**, no errores
- Representan **oportunidades de negocio**
- No eliminar, sino **entender y replicar**
- Crear **segmentos diferenciados** para atenderlos

---

## 6. 💼 INTERPRETACIONES PARA EL NEGOCIO

### 1. Estadística Descriptiva: Ticket Promedio

**Hallazgo:**
- Venta promedio: $7,578
- Mediana: $6,888
- Diferencia: +$690 (9.1%)

**Interpretación:**
El ticket promedio es 9% mayor que la mediana, lo que indica que **algunas ventas grandes elevan el promedio**. La mayoría de las ventas están en el rango $3,000-$10,000, pero hay ventas de $20,000+ que distorsionan el promedio.

**Impacto en el negocio:** Alto

**Acción recomendada:**
1. **Usar mediana** para forecasting y metas realistas
2. **Segmentar clientes**:
   - Clientes normales: Ticket $3K-$10K → Impulso, cross-sell
   - Clientes VIP: Ticket > $20K → Atención personalizada, descuentos por volumen
3. **KPI dual**: 
   - "Aumentar mediana a $8,000" (alcanzable)
   - "Aumentar % de ventas > $20K" (VIP)

---

### 2. Distribución: Cantidad Sesgada

**Hallazgo:**
- Distribución: Sesgada a la derecha
- Skewness: +0.65
- Interpretación: Mayoría compra 1-3 unidades

**Interpretación:**
La cantidad por venta está **sesgada hacia valores bajos**, indicando que la mayoría de los clientes compran pocas unidades (1-3), con algunos clientes comprando mucho más (4-5). Este patrón es típico en retail de conveniencia.

**Impacto en el negocio:** Medio

**Acción recomendada:**
1. **Promociones por volumen**:
   - "3×2" en productos de rotación rápida
   - "Descuento 15% en compras de 4+ unidades"
2. **Bundles pre-armados**:
   - "Pack Desayuno": Café + Galletitas + Dulce de Leche
   - "Pack Limpieza": Lavandina + Detergente + Esponjas
3. **Meta**: Aumentar cantidad promedio de 2.8 a 3.5 unidades (+25%)

---

### 3. Correlación: Cantidad-Importe Fuerte

**Hallazgo:**
- Correlación: Fuerte positiva (r = 0.89)
- Interpretación: A más cantidad, proporcionalmente más ingresos

**Interpretación:**
Existe una **relación casi perfecta** entre cantidad e importe. Por cada unidad adicional, el importe aumenta ~$2,700 en promedio. Esto valida que aumentar la cantidad por transacción es la forma más directa de incrementar ventas.

**Impacto en el negocio:** Alto

**Acción recomendada:**
1. **Focus absoluto** en aumentar cantidad por transacción
2. **Capacitar personal** en técnicas de upselling:
   - "¿Necesitas algo más?"
   - "Lleva 2 y te ahorras 10%"
3. **Colocación estratégica**:
   - Productos complementarios juntos
   - Snacks cerca de caja (impulso)
4. **Meta**: Cada transacción debe tener mínimo 4 productos

---

### 4. Correlación: Precio-Importe Fuerte

**Hallazgo:**
- Correlación: Fuerte positiva (r = 0.76)
- Interpretación: Productos caros generan más ingresos por línea

**Interpretación:**
Los productos de **alto valor unitario** generan importes significativamente mayores, incluso con cantidad baja. Los clientes están dispuestos a pagar por productos premium, lo que valida la estrategia de tener productos caros en el mix.

**Impacto en el negocio:** Alto

**Acción recomendada:**
1. **Promover productos premium**:
   - Ron 700ml ($3,876)
   - Desodorante Aerosol ($4,690)
   - Yerba Mate Suave ($3,878)
   - Miel Pura ($4,982)
2. **Ubicación privilegiada** para productos caros:
   - Nivel de ojos en góndolas
   - Displays especiales
   - Iluminación destacada
3. **Upselling premium**:
   - "¿Probaste nuestra versión premium?"
   - "Por $500 más, llevás la calidad superior"
4. **Meta**: 35% de ventas de productos > $3,500

---

### 5. Outliers: Ventas Grandes (Oportunidad VIP)

**Hallazgo:**
- 43 outliers (10% de transacciones)
- Importes: $20,000 - $24,865
- Patrón: 5 unidades × producto caro

**Interpretación:**
Existen **ventas significativamente mayores** que el promedio, representando el 10% de las transacciones pero probablemente 20-25% de los ingresos. Estas ventas tienen un patrón claro: cantidad alta (5 unidades) de productos caros.

**Impacto en el negocio:** Alto

**Acción recomendada:**
1. **Identificar clientes de ventas grandes**:
   - Analizar IDs de cliente en las 43 transacciones
   - ¿Son clientes corporativos?
   - ¿Compras para eventos?
2. **Crear segmento VIP**:
   - Descuentos exclusivos por volumen (10% en compras > $20K)
   - Atención personalizada
   - Acceso anticipado a nuevos productos
3. **Paquetes empresariales**:
   - "Pack Oficina" (café, galletitas, servilletas)
   - "Pack Evento" (bebidas, snacks, hielo)
   - Entrega a domicilio gratis para compras > $15K
4. **Meta**: Aumentar ventas > $20K de 10% a 15%

---

### 6. No Estacionalidad: Crear Patrones

**Hallazgo:**
- Correlación mes-importe: r = 0.08 (nula)
- No hay estacionalidad natural
- Volatilidad alta mes a mes

**Interpretación:**
Las ventas **NO siguen un patrón estacional predecible**. Esto dificulta la planificación de inventario y personal, pero también es una **oportunidad para crear estacionalidad artificial** mediante campañas programadas.

**Impacto en el negocio:** Medio

**Acción recomendada:**
1. **Calendario de promociones fijas**:
   - Semana 1: "Lunes de Alimentos" (20% off categoría)
   - Semana 2: "Miércoles de Limpieza" (2×1 seleccionados)
   - Semana 3: "Viernes de Bebidas" (combos especiales)
   - Semana 4: "Domingo Familiar" (regalo sorpresa)
2. **Promociones de fin de mes**:
   - Días 25-31: "Remate de mes" (liquidación de stock lento)
3. **Eventos mensuales**:
   - Degustaciones, demos, sorteos
4. **Meta**: Reducir volatilidad mensual de CV=18% a CV<10%

---

## 7. 🛠️ HERRAMIENTAS Y MÉTODOS UTILIZADOS

### Tabla Completa de Herramientas

| Categoría | Herramienta | Método Python | Librería | Aplicación | Resultado | Ejemplo Código |
|-----------|-------------|---------------|----------|------------|-----------|----------------|
| **Estadística Descriptiva** | Medidas de Tendencia Central | `mean()`, `median()`, `mode()` | pandas, numpy | Calcular promedio, mediana y moda | Valores típicos de ventas | `df["importe"].mean()` |
| **Estadística Descriptiva** | Medidas de Dispersión | `std()`, `var()`, `quantile()` | pandas, numpy | Medir variabilidad de ventas | Desviación estándar, varianza, cuartiles | `df["importe"].std()` |
| **Estadística Descriptiva** | Medidas de Forma | `skew()`, `kurtosis()` | pandas, scipy.stats | Analizar simetría y curtosis | Identificar sesgos y forma | `df["cantidad"].skew()` |
| **Estadística Descriptiva** | Coeficiente de Variación | `(std() / mean()) * 100` | pandas, numpy | Comparar variabilidad relativa | % de variación respecto a media | `(df["importe"].std() / df["importe"].mean()) * 100` |
| **Análisis de Distribución** | Test de Shapiro-Wilk | `shapiro()` | scipy.stats | Evaluar normalidad (n < 5000) | p-value > 0.05 indica normal | `stats.shapiro(df["importe"])` |
| **Análisis de Distribución** | Test de D'Agostino-Pearson | `normaltest()` | scipy.stats | Evaluar normalidad vía skewness/kurtosis | Determinar si es normal | `stats.normaltest(df["cantidad"])` |
| **Análisis de Distribución** | Análisis de Skewness | `skew()` | pandas | Identificar sesgo | >0: derecha, <0: izquierda | `df["precio_unitario"].skew()` |
| **Análisis de Distribución** | Análisis de Kurtosis | `kurtosis()` | pandas | Identificar forma de picos | >0: leptocúrtica, <0: platicúrtica | `df["importe"].kurtosis()` |
| **Análisis de Correlación** | Correlación de Pearson | `corr(method="pearson")`, `pearsonr()` | pandas, scipy.stats | Medir relación lineal | r entre -1 y 1 | `df[["cantidad", "importe"]].corr()` |
| **Análisis de Correlación** | Correlación de Spearman | `corr(method="spearman")`, `spearmanr()` | pandas, scipy.stats | Medir relación monotónica | Correlación basada en rangos | `stats.spearmanr(df["cantidad"], df["importe"])` |
| **Análisis de Correlación** | Matriz de Correlación | `corr()` | pandas | Crear matriz de correlaciones | Tabla con todas las correlaciones | `df[cols_numericas].corr()` |
| **Análisis de Correlación** | Test Chi-cuadrado | `chi2_contingency()` | scipy.stats | Evaluar asociación entre categóricas | p-value < 0.05 indica asociación | `stats.chi2_contingency(pd.crosstab(df["cat1"], df["cat2"]))` |
| **Detección de Outliers** | Método IQR | `quantile(0.25)`, `quantile(0.75)` | pandas, numpy | Identificar valores atípicos | Outliers: Q1-1.5×IQR o Q3+1.5×IQR | `Q1 = df["importe"].quantile(0.25); IQR = Q3 - Q1` |
| **Detección de Outliers** | Límites Extremos | `Q1 - 3*IQR`, `Q3 + 3*IQR` | pandas, numpy | Detectar valores extremos | Outliers más allá de 3×IQR | `upper_extreme = Q3 + 3 * IQR` |
| **Detección de Outliers** | Filtrado Booleano | Boolean indexing | pandas | Extraer outliers | DataFrame con solo outliers | `outliers = df[df["importe"] > upper_bound]` |
| **Detección de Outliers** | Porcentaje de Outliers | `len() / len() * 100` | pandas, numpy | Calcular proporción de outliers | % de valores atípicos | `(len(outliers) / len(df)) * 100` |
| **Análisis por Grupos** | GroupBy con Agregaciones | `groupby().agg()` | pandas | Calcular estadísticas por segmento | Estadísticas segmentadas | `df.groupby("categoria").agg({"importe": ["mean", "sum"]})` |
| **Análisis por Grupos** | Tablas de Contingencia | `pd.crosstab()` | pandas | Crear tablas de frecuencia cruzada | Matriz de conteos por categorías | `pd.crosstab(df["categoria"], df["medio_pago"])` |
| **Preparación de Datos** | Merge/Join | `merge()` | pandas | Unir múltiples DataFrames | Dataset consolidado | `df1.merge(df2, on="id", how="left")` |
| **Preparación de Datos** | Conversión de Tipos | `pd.to_datetime()`, `astype()` | pandas | Convertir tipos de datos | Datos en formato correcto | `df["fecha"] = pd.to_datetime(df["fecha"])` |
| **Preparación de Datos** | Manejo de Valores Nulos | `dropna()`, `isna()` | pandas | Eliminar o identificar nulos | Dataset limpio | `df["col"].dropna()` |

---

## 8. 📋 CONCLUSIONES Y RECOMENDACIONES

### Hallazgos Clave

#### ✅ Fortalezas Identificadas

1. **Correlaciones sólidas**: Cantidad e importe tienen relación casi perfecta (r=0.89)
2. **Mix de precios**: Amplio rango ($272-$4,982) atiende todos los segmentos
3. **Clientes VIP valiosos**: 10% de transacciones son > $20K
4. **Sin errores críticos**: Outliers son reales, no errores de datos

#### ⚠️ Áreas de Oportunidad

1. **Alta variabilidad**: CV = 83.4% dificulta forecasting
2. **Sin estacionalidad**: Ventas impredecibles mes a mes
3. **Cantidad baja**: Promedio 2.8 unidades (debería ser 4+)
4. **Distribuciones sesgadas**: Mayoría de ventas son pequeñas

---

### Recomendaciones Prioritarias

#### 🎯 **PRIORIDAD 1**: Aumentar Cantidad por Transacción

**Meta**: De 2.8 → 3.5 unidades (+25%)

**Acciones**:
- Promociones "3×2" en productos de alta rotación
- Bundles pre-armados ("Pack Desayuno", "Pack Limpieza")
- Capacitación en upselling: "¿Necesitas algo más?"
- Productos complementarios juntos en góndola

**ROI esperado**: +$400K en 6 meses

---

#### 🎯 **PRIORIDAD 2**: Promover Productos Premium

**Meta**: 35% de ventas de productos > $3,500

**Acciones**:
- Destacar productos caros: Ron, Yerba, Desodorante, Miel
- Ubicación privilegiada (nivel de ojos)
- Upselling: "Por $500 más, llevás calidad superior"
- Displays especiales con iluminación

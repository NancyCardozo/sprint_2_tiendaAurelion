"""
PROYECTO TIENDA AURELION - FASE 2
Estadística Aplicada: Análisis Descriptivo, Distribuciones, Correlaciones y Outliers
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import normaltest, shapiro, kstest, chi2_contingency
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
CARPETA_LIMPIOS = 'datos_limpios'
CARPETA_ESTADISTICAS = 'estadisticas'

import os
os.makedirs(CARPETA_ESTADISTICAS, exist_ok=True)

print("="*80)
print("FASE 2: ESTADÍSTICA APLICADA - TIENDA AURELION")
print("="*80)

# ============================================================================
# 1. LECTURA DE DATOS LIMPIOS
# ============================================================================
print("\n1. Cargando datos limpios...")

clientes = pd.read_csv(f'{CARPETA_LIMPIOS}/clientes_limpios.csv')
productos = pd.read_csv(f'{CARPETA_LIMPIOS}/productos_limpios.csv')
ventas = pd.read_csv(f'{CARPETA_LIMPIOS}/ventas_limpias.csv')
detalle_ventas = pd.read_csv(f'{CARPETA_LIMPIOS}/detalle_ventas_limpios.csv')
calendario = pd.read_csv(f'{CARPETA_LIMPIOS}/calendario.csv')

# Convertir fechas
ventas['fecha'] = pd.to_datetime(ventas['fecha'])
calendario['fecha'] = pd.to_datetime(calendario['fecha'])
clientes['fecha_alta'] = pd.to_datetime(clientes['fecha_alta'])

print(f"   ✓ Datos cargados exitosamente")

# ============================================================================
# 2. CONSTRUCCIÓN DE DATASET CONSOLIDADO PARA ANÁLISIS
# ============================================================================
print("\n2. Construyendo dataset consolidado...")

# Unir detalle_ventas con ventas
ventas_completas = detalle_ventas.merge(ventas, on='id_venta', how='left')

# Agregar información de productos (sin precio_unitario para evitar duplicados)
productos_sin_precio = productos.drop('precio_unitario', axis=1)
ventas_completas = ventas_completas.merge(productos_sin_precio, on='id_producto', how='left')

# Agregar información de clientes
ventas_completas = ventas_completas.merge(
    clientes[['id_cliente', 'ciudad']], 
    on='id_cliente', 
    how='left'
)

# Agregar información temporal
ventas_completas = ventas_completas.merge(
    calendario[['fecha', 'anio', 'mes', 'dia_semana', 'nombre_dia']], 
    on='fecha', 
    how='left'
)

print(f"   ✓ Dataset consolidado: {ventas_completas.shape[0]} registros")
print(f"   ✓ Columnas disponibles: {list(ventas_completas.columns)}")

# ============================================================================
# 3. ESTADÍSTICAS DESCRIPTIVAS BÁSICAS
# ============================================================================
print("\n3. Calculando estadísticas descriptivas básicas...")

# 3.1 Variables Numéricas Principales
# Verificar nombres exactos de columnas
print(f"\n   DEBUG: Columnas numéricas encontradas:")
for col in ventas_completas.select_dtypes(include=[np.number]).columns:
    print(f"      - {col}")

variables_numericas = {
    'cantidad': ventas_completas['cantidad'],
    'precio_unitario': ventas_completas['precio_unitario'],  # Del detalle_ventas
    'importe': ventas_completas['importe'],
}

estadisticas_descriptivas = []

for nombre_var, variable in variables_numericas.items():
    stats_dict = {
        'Variable': nombre_var,
        'Count': len(variable),
        'Mean': variable.mean(),
        'Median': variable.median(),
        'Mode': variable.mode()[0] if len(variable.mode()) > 0 else np.nan,
        'Std': variable.std(),
        'Variance': variable.var(),
        'Min': variable.min(),
        'Q1': variable.quantile(0.25),
        'Q2': variable.quantile(0.50),
        'Q3': variable.quantile(0.75),
        'Max': variable.max(),
        'Range': variable.max() - variable.min(),
        'IQR': variable.quantile(0.75) - variable.quantile(0.25),
        'CV': (variable.std() / variable.mean()) * 100,  # Coeficiente de variación
        'Skewness': variable.skew(),
        'Kurtosis': variable.kurtosis()
    }
    estadisticas_descriptivas.append(stats_dict)

df_estadisticas = pd.DataFrame(estadisticas_descriptivas)

# 3.2 Estadísticas por Categoría
print("\n   Calculando estadísticas por categoría...")

stats_por_categoria = ventas_completas.groupby('categoria').agg({
    'importe': ['count', 'sum', 'mean', 'median', 'std'],
    'cantidad': ['sum', 'mean'],
    'id_venta': 'nunique'
}).round(2)

stats_por_categoria.columns = ['_'.join(col).strip() for col in stats_por_categoria.columns]
stats_por_categoria = stats_por_categoria.reset_index()

# 3.3 Estadísticas por Ciudad
stats_por_ciudad = ventas_completas.groupby('ciudad').agg({
    'importe': ['count', 'sum', 'mean', 'median'],
    'id_venta': 'nunique',
    'id_cliente': 'nunique'
}).round(2)

stats_por_ciudad.columns = ['_'.join(col).strip() for col in stats_por_ciudad.columns]
stats_por_ciudad = stats_por_ciudad.reset_index()

# 3.4 Estadísticas por Medio de Pago
stats_por_medio_pago = ventas_completas.groupby('medio_pago').agg({
    'importe': ['count', 'sum', 'mean', 'median', 'std'],
    'id_venta': 'nunique'
}).round(2)

stats_por_medio_pago.columns = ['_'.join(col).strip() for col in stats_por_medio_pago.columns]
stats_por_medio_pago = stats_por_medio_pago.reset_index()

# 3.5 Estadísticas Temporales
stats_temporales = ventas_completas.groupby(['mes']).agg({
    'importe': ['count', 'sum', 'mean'],
    'id_venta': 'nunique',
    'cantidad': 'sum'
}).round(2)

stats_temporales.columns = ['_'.join(col).strip() for col in stats_temporales.columns]
stats_temporales = stats_temporales.reset_index()

print("   ✓ Estadísticas descriptivas calculadas")

# ============================================================================
# 4. IDENTIFICACIÓN DE DISTRIBUCIONES
# ============================================================================
print("\n4. Identificando tipos de distribución...")

distribuciones = []

for nombre_var, variable in variables_numericas.items():
    
    # Test de Normalidad: Shapiro-Wilk (para n < 5000)
    if len(variable) < 5000:
        shapiro_stat, shapiro_p = shapiro(variable)
    else:
        shapiro_stat, shapiro_p = np.nan, np.nan
    
    # Test de Normalidad: D'Agostino-Pearson
    dagostino_stat, dagostino_p = normaltest(variable)
    
    # Determinar tipo de distribución
    if shapiro_p > 0.05 or dagostino_p > 0.05:
        tipo_dist = "Normal (aproximada)"
    else:
        # Analizar skewness y kurtosis
        skew = variable.skew()
        kurt = variable.kurtosis()
        
        if abs(skew) < 0.5 and abs(kurt) < 0.5:
            tipo_dist = "Simétrica (no normal)"
        elif skew > 1:
            tipo_dist = "Sesgada a la derecha (positiva)"
        elif skew < -1:
            tipo_dist = "Sesgada a la izquierda (negativa)"
        elif kurt > 1:
            tipo_dist = "Leptocúrtica (picos altos)"
        elif kurt < -1:
            tipo_dist = "Platicúrtica (picos bajos)"
        else:
            tipo_dist = "No normal"
    
    distribuciones.append({
        'Variable': nombre_var,
        'Tipo_Distribucion': tipo_dist,
        'Shapiro_Wilk_Statistic': shapiro_stat,
        'Shapiro_Wilk_p_value': shapiro_p,
        'Shapiro_Normal': 'Sí' if shapiro_p > 0.05 else 'No',
        'DAgostino_Statistic': dagostino_stat,
        'DAgostino_p_value': dagostino_p,
        'DAgostino_Normal': 'Sí' if dagostino_p > 0.05 else 'No',
        'Skewness': variable.skew(),
        'Kurtosis': variable.kurtosis(),
        'Interpretacion_Skewness': 'Derecha' if variable.skew() > 0.5 else ('Izquierda' if variable.skew() < -0.5 else 'Simétrica'),
        'Interpretacion_Kurtosis': 'Leptocúrtica' if variable.kurtosis() > 1 else ('Platicúrtica' if variable.kurtosis() < -1 else 'Mesocúrtica')
    })

df_distribuciones = pd.DataFrame(distribuciones)

print("   ✓ Distribuciones identificadas")

# ============================================================================
# 5. ANÁLISIS DE CORRELACIONES
# ============================================================================
print("\n5. Calculando correlaciones entre variables...")

# 5.1 Correlación entre variables numéricas
variables_para_correlacion = ventas_completas[['cantidad', 'precio_unitario', 'importe', 'mes', 'dia_semana']]

# Matriz de correlación de Pearson
correlacion_pearson = variables_para_correlacion.corr(method='pearson')

# Matriz de correlación de Spearman (para datos no normales)
correlacion_spearman = variables_para_correlacion.corr(method='spearman')

# 5.2 Correlaciones específicas de interés
correlaciones_clave = []

pares_interes = [
    ('cantidad', 'importe'),
    ('precio_unitario', 'importe'),
    ('cantidad', 'precio_unitario'),
    ('mes', 'importe'),
    ('dia_semana', 'importe')
]

for var1, var2 in pares_interes:
    # Pearson
    pearson_r, pearson_p = stats.pearsonr(
        ventas_completas[var1].dropna(), 
        ventas_completas[var2].dropna()
    )
    
    # Spearman
    spearman_r, spearman_p = stats.spearmanr(
        ventas_completas[var1].dropna(), 
        ventas_completas[var2].dropna()
    )
    
    # Interpretación
    if abs(pearson_r) > 0.7:
        fuerza = "Fuerte"
    elif abs(pearson_r) > 0.4:
        fuerza = "Moderada"
    elif abs(pearson_r) > 0.2:
        fuerza = "Débil"
    else:
        fuerza = "Muy débil/Nula"
    
    direccion = "Positiva" if pearson_r > 0 else "Negativa"
    
    correlaciones_clave.append({
        'Variable_1': var1,
        'Variable_2': var2,
        'Pearson_r': pearson_r,
        'Pearson_p_value': pearson_p,
        'Pearson_Significativo': 'Sí' if pearson_p < 0.05 else 'No',
        'Spearman_r': spearman_r,
        'Spearman_p_value': spearman_p,
        'Spearman_Significativo': 'Sí' if spearman_p < 0.05 else 'No',
        'Fuerza': fuerza,
        'Direccion': direccion,
        'Interpretacion': f"{fuerza} {direccion}"
    })

df_correlaciones = pd.DataFrame(correlaciones_clave)

# 5.3 Correlación con variables categóricas (Chi-cuadrado)
print("\n   Calculando correlaciones con variables categóricas...")

# Chi-cuadrado: Categoría vs Medio de Pago
tabla_contingencia = pd.crosstab(ventas_completas['categoria'], ventas_completas['medio_pago'])
chi2, p_value, dof, expected = chi2_contingency(tabla_contingencia)

correlacion_categoricas = {
    'Test': 'Chi-cuadrado',
    'Variable_1': 'categoria',
    'Variable_2': 'medio_pago',
    'Chi2_Statistic': chi2,
    'p_value': p_value,
    'Grados_Libertad': dof,
    'Asociacion_Significativa': 'Sí' if p_value < 0.05 else 'No'
}

print("   ✓ Correlaciones calculadas")

# ============================================================================
# 6. DETECCIÓN DE OUTLIERS (IQR)
# ============================================================================
print("\n6. Detectando outliers mediante IQR...")

outliers_resultados = []

for nombre_var, variable in variables_numericas.items():
    Q1 = variable.quantile(0.25)
    Q3 = variable.quantile(0.75)
    IQR = Q3 - Q1
    
    # Límites
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Outliers extremos
    lower_extreme = Q1 - 3 * IQR
    upper_extreme = Q3 + 3 * IQR
    
    # Detectar outliers
    outliers_leves = variable[(variable < lower_bound) | (variable > upper_bound)]
    outliers_extremos = variable[(variable < lower_extreme) | (variable > upper_extreme)]
    
    # Porcentajes
    pct_outliers_leves = (len(outliers_leves) / len(variable)) * 100
    pct_outliers_extremos = (len(outliers_extremos) / len(variable)) * 100
    
    outliers_resultados.append({
        'Variable': nombre_var,
        'Q1': Q1,
        'Q3': Q3,
        'IQR': IQR,
        'Limite_Inferior': lower_bound,
        'Limite_Superior': upper_bound,
        'Limite_Inferior_Extremo': lower_extreme,
        'Limite_Superior_Extremo': upper_extreme,
        'Outliers_Leves_Count': len(outliers_leves),
        'Outliers_Leves_Pct': pct_outliers_leves,
        'Outliers_Extremos_Count': len(outliers_extremos),
        'Outliers_Extremos_Pct': pct_outliers_extremos,
        'Min_Outlier': outliers_leves.min() if len(outliers_leves) > 0 else np.nan,
        'Max_Outlier': outliers_leves.max() if len(outliers_leves) > 0 else np.nan,
        'Interpretacion': 'Sin outliers significativos' if pct_outliers_leves < 5 else 'Outliers presentes'
    })

df_outliers = pd.DataFrame(outliers_resultados)

# 6.2 Análisis específico de outliers por variable
print("\n   Analizando outliers en detalle...")

# Outliers en IMPORTE
outliers_importe = ventas_completas[
    (ventas_completas['importe'] > df_outliers[df_outliers['Variable'] == 'importe']['Limite_Superior'].values[0])
]

top_outliers_importe = outliers_importe.nlargest(10, 'importe')[
    ['id_venta', 'nombre_producto', 'cantidad', 'precio_unitario', 'importe', 'categoria']
]

print("   ✓ Outliers detectados")

# ============================================================================
# 7. INTERPRETACIÓN PARA EL NEGOCIO
# ============================================================================
print("\n7. Generando interpretaciones para el negocio...")

interpretaciones = []

# Interpretación 1: Estadísticas Descriptivas
for _, row in df_estadisticas.iterrows():
    if row['Variable'] == 'importe':
        interpretaciones.append({
            'Tipo_Analisis': 'Estadística Descriptiva',
            'Variable': 'Importe',
            'Hallazgo': f"Venta promedio: ${row['Mean']:,.0f} | Mediana: ${row['Median']:,.0f}",
            'Interpretacion': f"El ticket promedio (${row['Mean']:,.0f}) es {'mayor' if row['Mean'] > row['Median'] else 'menor'} que la mediana (${row['Median']:,.0f}), indicando {'ventas grandes que elevan el promedio' if row['Mean'] > row['Median'] else 'distribución equilibrada'}.",
            'Impacto_Negocio': 'Alto',
            'Accion_Recomendada': 'Estrategias de upselling para aumentar ticket promedio' if row['Mean'] < 30000 else 'Mantener estrategia actual de venta'
        })

# Interpretación 2: Distribuciones
for _, row in df_distribuciones.iterrows():
    if row['Variable'] == 'cantidad':
        interpretaciones.append({
            'Tipo_Analisis': 'Distribución',
            'Variable': 'Cantidad',
            'Hallazgo': f"Distribución: {row['Tipo_Distribucion']} | Skewness: {row['Skewness']:.2f}",
            'Interpretacion': f"La cantidad por venta tiene sesgo {row['Interpretacion_Skewness']}, lo que indica que {'la mayoría compra pocas unidades con algunos clientes comprando mucho' if row['Skewness'] > 0.5 else 'las compras son equilibradas'}.",
            'Impacto_Negocio': 'Medio',
            'Accion_Recomendada': 'Promociones por volumen (3x2, descuentos por cantidad)' if row['Skewness'] > 0.5 else 'Mantener estrategia actual'
        })

# Interpretación 3: Correlaciones
for _, row in df_correlaciones.iterrows():
    if row['Variable_1'] == 'cantidad' and row['Variable_2'] == 'importe':
        interpretaciones.append({
            'Tipo_Analisis': 'Correlación',
            'Variable': 'Cantidad-Importe',
            'Hallazgo': f"Correlación {row['Fuerza']} {row['Direccion']} (r={row['Pearson_r']:.3f})",
            'Interpretacion': f"{'Fuerte' if abs(row['Pearson_r']) > 0.7 else 'Moderada'} relación entre cantidad e importe, como se espera. {'Clientes que compran más unidades gastan proporcionalmente más.' if row['Pearson_r'] > 0 else 'Relación inesperada.'}",
            'Impacto_Negocio': 'Bajo',
            'Accion_Recomendada': 'Esperado. Seguir monitoreando.'
        })
    
    if row['Variable_1'] == 'precio_unitario' and row['Variable_2'] == 'importe':
        interpretaciones.append({
            'Tipo_Analisis': 'Correlación',
            'Variable': 'Precio-Importe',
            'Hallazgo': f"Correlación {row['Fuerza']} {row['Direccion']} (r={row['Pearson_r']:.3f})",
            'Interpretacion': f"El precio unitario tiene {'fuerte' if abs(row['Pearson_r']) > 0.7 else 'moderada'} influencia en el importe final. Productos de mayor precio generan {'proporcionalmente' if row['Pearson_r'] > 0.8 else 'moderadamente'} más ingresos.",
            'Impacto_Negocio': 'Alto',
            'Accion_Recomendada': 'Promover productos de alto valor (Ron, Yerba, Desodorante)' if abs(row['Pearson_r']) > 0.5 else 'Revisar estrategia de pricing'
        })

# Interpretación 4: Outliers
for _, row in df_outliers.iterrows():
    if row['Variable'] == 'importe' and row['Outliers_Leves_Pct'] > 5:
        interpretaciones.append({
            'Tipo_Analisis': 'Outliers',
            'Variable': 'Importe',
            'Hallazgo': f"{row['Outliers_Leves_Count']} outliers ({row['Outliers_Leves_Pct']:.1f}%)",
            'Interpretacion': f"Existen {row['Outliers_Leves_Count']} ventas con importes inusualmente altos (>${row['Limite_Superior']:,.0f}). Estas representan el {row['Outliers_Leves_Pct']:.1f}% de las transacciones.",
            'Impacto_Negocio': 'Alto',
            'Accion_Recomendada': 'Analizar estas ventas grandes: ¿Son clientes VIP? ¿Compras corporativas? Replicar comportamiento.'
        })

df_interpretaciones = pd.DataFrame(interpretaciones)

print("   ✓ Interpretaciones generadas")

# ============================================================================
# 8. TABLA DE HERRAMIENTAS Y MÉTODOS UTILIZADOS
# ============================================================================
print("\n8. Documentando herramientas y métodos...")

herramientas_metodos = [
    # ESTADÍSTICAS DESCRIPTIVAS
    {
        'Categoria': 'Estadística Descriptiva',
        'Herramienta': 'Medidas de Tendencia Central',
        'Metodo_Python': 'mean(), median(), mode()',
        'Libreria': 'pandas, numpy',
        'Aplicacion': 'Calcular promedio, mediana y moda de cantidad, precio e importe',
        'Resultado': 'Identificar valores típicos de ventas',
        'Ejemplo_Codigo': 'df["importe"].mean()'
    },
    {
        'Categoria': 'Estadística Descriptiva',
        'Herramienta': 'Medidas de Dispersión',
        'Metodo_Python': 'std(), var(), quantile()',
        'Libreria': 'pandas, numpy',
        'Aplicacion': 'Medir variabilidad de ventas',
        'Resultado': 'Desviación estándar, varianza, cuartiles',
        'Ejemplo_Codigo': 'df["importe"].std()'
    },
    {
        'Categoria': 'Estadística Descriptiva',
        'Herramienta': 'Medidas de Forma',
        'Metodo_Python': 'skew(), kurtosis()',
        'Libreria': 'pandas, scipy.stats',
        'Aplicacion': 'Analizar simetría y curtosis de distribuciones',
        'Resultado': 'Identificar sesgos y forma de la distribución',
        'Ejemplo_Codigo': 'df["cantidad"].skew()'
    },
    {
        'Categoria': 'Estadística Descriptiva',
        'Herramienta': 'Coeficiente de Variación',
        'Metodo_Python': '(std() / mean()) * 100',
        'Libreria': 'pandas, numpy',
        'Aplicacion': 'Comparar variabilidad relativa entre variables',
        'Resultado': 'Porcentaje de variación respecto a la media',
        'Ejemplo_Codigo': '(df["importe"].std() / df["importe"].mean()) * 100'
    },
    
    # DISTRIBUCIONES
    {
        'Categoria': 'Análisis de Distribución',
        'Herramienta': 'Test de Shapiro-Wilk',
        'Metodo_Python': 'shapiro()',
        'Libreria': 'scipy.stats',
        'Aplicacion': 'Evaluar normalidad de variables (n < 5000)',
        'Resultado': 'p-value > 0.05 indica distribución normal',
        'Ejemplo_Codigo': 'stats.shapiro(df["importe"])'
    },
    {
        'Categoria': 'Análisis de Distribución',
        'Herramienta': 'Test de D\'Agostino-Pearson',
        'Metodo_Python': 'normaltest()',
        'Libreria': 'scipy.stats',
        'Aplicacion': 'Evaluar normalidad mediante skewness y kurtosis',
        'Resultado': 'Determinar si sigue distribución normal',
        'Ejemplo_Codigo': 'stats.normaltest(df["cantidad"])'
    },
    {
        'Categoria': 'Análisis de Distribución',
        'Herramienta': 'Análisis de Skewness',
        'Metodo_Python': 'skew()',
        'Libreria': 'pandas',
        'Aplicacion': 'Identificar sesgo de la distribución',
        'Resultado': '>0: derecha, <0: izquierda, ≈0: simétrica',
        'Ejemplo_Codigo': 'df["precio_unitario"].skew()'
    },
    {
        'Categoria': 'Análisis de Distribución',
        'Herramienta': 'Análisis de Kurtosis',
        'Metodo_Python': 'kurtosis()',
        'Libreria': 'pandas',
        'Aplicacion': 'Identificar forma de picos en distribución',
        'Resultado': '>0: leptocúrtica, <0: platicúrtica',
        'Ejemplo_Codigo': 'df["importe"].kurtosis()'
    },
    
    # CORRELACIONES
    {
        'Categoria': 'Análisis de Correlación',
        'Herramienta': 'Correlación de Pearson',
        'Metodo_Python': 'corr(method="pearson"), pearsonr()',
        'Libreria': 'pandas, scipy.stats',
        'Aplicacion': 'Medir relación lineal entre variables numéricas',
        'Resultado': 'r entre -1 y 1 (fuerza y dirección)',
        'Ejemplo_Codigo': 'df[["cantidad", "importe"]].corr()'
    },
    {
        'Categoria': 'Análisis de Correlación',
        'Herramienta': 'Correlación de Spearman',
        'Metodo_Python': 'corr(method="spearman"), spearmanr()',
        'Libreria': 'pandas, scipy.stats',
        'Aplicacion': 'Medir relación monotónica (datos no normales)',
        'Resultado': 'Correlación basada en rangos',
        'Ejemplo_Codigo': 'stats.spearmanr(df["cantidad"], df["importe"])'
    },
    {
        'Categoria': 'Análisis de Correlación',
        'Herramienta': 'Matriz de Correlación',
        'Metodo_Python': 'corr()',
        'Libreria': 'pandas',
        'Aplicacion': 'Crear matriz de correlaciones múltiples',
        'Resultado': 'Tabla con todas las correlaciones',
        'Ejemplo_Codigo': 'df[cols_numericas].corr()'
    },
    {
        'Categoria': 'Análisis de Correlación',
        'Herramienta': 'Test Chi-cuadrado',
        'Metodo_Python': 'chi2_contingency()',
        'Libreria': 'scipy.stats',
        'Aplicacion': 'Evaluar asociación entre variables categóricas',
        'Resultado': 'p-value < 0.05 indica asociación significativa',
        'Ejemplo_Codigo': 'stats.chi2_contingency(pd.crosstab(df["cat1"], df["cat2"]))'
    },
    
    # OUTLIERS
    {
        'Categoria': 'Detección de Outliers',
        'Herramienta': 'Método IQR (Rango Intercuartílico)',
        'Metodo_Python': 'quantile(0.25), quantile(0.75)',
        'Libreria': 'pandas, numpy',
        'Aplicacion': 'Identificar valores atípicos',
        'Resultado': 'Outliers: Q1-1.5*IQR o Q3+1.5*IQR',
        'Ejemplo_Codigo': 'Q1 = df["importe"].quantile(0.25); IQR = Q3 - Q1'
    },
    {
        'Categoria': 'Detección de Outliers',
        'Herramienta': 'Límites de Outliers Extremos',
        'Metodo_Python': 'Q1 - 3*IQR, Q3 + 3*IQR',
        'Libreria': 'pandas, numpy',
        'Aplicacion': 'Detectar valores extremadamente atípicos',
        'Resultado': 'Outliers más allá de 3*IQR',
        'Ejemplo_Codigo': 'upper_extreme = Q3 + 3 * IQR'
    },
    {
        'Categoria': 'Detección de Outliers',
        'Herramienta': 'Filtrado Booleano',
        'Metodo_Python': 'Boolean indexing',
        'Libreria': 'pandas',
        'Aplicacion': 'Extraer registros que son outliers',
        'Resultado': 'DataFrame con solo outliers',
        'Ejemplo_Codigo': 'outliers = df[df["importe"] > upper_bound]'
    },
    {
        'Categoria': 'Detección de Outliers',
        'Herramienta': 'Porcentaje de Outliers',
        'Metodo_Python': 'len() / len() * 100',
        'Libreria': 'pandas, numpy',
        'Aplicacion': 'Calcular proporción de outliers',
        'Resultado': 'Porcentaje de valores atípicos',
        'Ejemplo_Codigo': '(len(outliers) / len(df)) * 100'
    },
    
    # AGRUPACIONES
    {
        'Categoria': 'Análisis por Grupos',
        'Herramienta': 'GroupBy con Agregaciones',
        'Metodo_Python': 'groupby().agg()',
        'Libreria': 'pandas',
        'Aplicacion': 'Calcular estadísticas por categoría/ciudad/etc',
        'Resultado': 'Estadísticas segmentadas',
        'Ejemplo_Codigo': 'df.groupby("categoria").agg({"importe": ["mean", "sum"]})'
    },
    {
        'Categoria': 'Análisis por Grupos',
        'Herramienta': 'Tablas de Contingencia',
        'Metodo_Python': 'pd.crosstab()',
        'Libreria': 'pandas',
        'Aplicacion': 'Crear tablas de frecuencia cruzada',
        'Resultado': 'Matriz de conteos por categorías',
        'Ejemplo_Codigo': 'pd.crosstab(df["categoria"], df["medio_pago"])'
    },
    
    # MANIPULACIÓN DE DATOS
    {
        'Categoria': 'Preparación de Datos',
        'Herramienta': 'Merge/Join',
        'Metodo_Python': 'merge()',
        'Libreria': 'pandas',
        'Aplicacion': 'Unir múltiples DataFrames',
        'Resultado': 'Dataset consolidado para análisis',
        'Ejemplo_Codigo': 'df1.merge(df2, on="id", how="left")'
    },
    {
        'Categoria': 'Preparación de Datos',
        'Herramienta': 'Conversión de Tipos',
        'Metodo_Python': 'pd.to_datetime(), astype()',
        'Libreria': 'pandas',
        'Aplicacion': 'Convertir tipos de datos',
        'Resultado': 'Datos en formato correcto para análisis',
        'Ejemplo_Codigo': 'df["fecha"] = pd.to_datetime(df["fecha"])'
    },
    {
        'Categoria': 'Preparación de Datos',
        'Herramienta': 'Manejo de Valores Nulos',
        'Metodo_Python': 'dropna(), isna()',
        'Libreria': 'pandas',
        'Aplicacion': 'Eliminar o identificar valores nulos',
        'Resultado': 'Dataset limpio para cálculos',
        'Ejemplo_Codigo': 'df["col"].dropna()'
    }
]

df_herramientas = pd.DataFrame(herramientas_metodos)

print("   ✓ Tabla de herramientas documentada")

# ============================================================================
# 9. GUARDAR RESULTADOS
# ============================================================================
print("\n9. Guardando resultados del análisis estadístico...")

# Guardar todas las tablas
df_estadisticas.to_csv(f'{CARPETA_ESTADISTICAS}/01_estadisticas_descriptivas.csv', index=False)
df_distribuciones.to_csv(f'{CARPETA_ESTADISTICAS}/02_analisis_distribuciones.csv', index=False)
df_correlaciones.to_csv(f'{CARPETA_ESTADISTICAS}/03_correlaciones.csv', index=False)
correlacion_pearson.to_csv(f'{CARPETA_ESTADISTICAS}/04_matriz_correlacion_pearson.csv')
correlacion_spearman.to_csv(f'{CARPETA_ESTADISTICAS}/05_matriz_correlacion_spearman.csv')
df_outliers.to_csv(f'{CARPETA_ESTADISTICAS}/06_analisis_outliers.csv', index=False)
top_outliers_importe.to_csv(f'{CARPETA_ESTADISTICAS}/07_top_outliers_importe.csv', index=False)
df_interpretaciones.to_csv(f'{CARPETA_ESTADISTICAS}/08_interpretaciones_negocio.csv', index=False)
df_herramientas.to_csv(f'{CARPETA_ESTADISTICAS}/09_herramientas_metodos.csv', index=False)

# Guardar estadísticas por segmento
stats_por_categoria.to_csv(f'{CARPETA_ESTADISTICAS}/10_stats_por_categoria.csv', index=False)
stats_por_ciudad.to_csv(f'{CARPETA_ESTADISTICAS}/11_stats_por_ciudad.csv', index=False)
stats_por_medio_pago.to_csv(f'{CARPETA_ESTADISTICAS}/12_stats_por_medio_pago.csv', index=False)
stats_temporales.to_csv(f'{CARPETA_ESTADISTICAS}/13_stats_temporales.csv', index=False)

print(f"   ✓ 01_estadisticas_descriptivas.csv")
print(f"   ✓ 02_analisis_distribuciones.csv")
print(f"   ✓ 03_correlaciones.csv")
print(f"   ✓ 04_matriz_correlacion_pearson.csv")
print(f"   ✓ 05_matriz_correlacion_spearman.csv")
print(f"   ✓ 06_analisis_outliers.csv")
print(f"   ✓ 07_top_outliers_importe.csv")
print(f"   ✓ 08_interpretaciones_negocio.csv")
print(f"   ✓ 09_herramientas_metodos.csv")
print(f"   ✓ 10_stats_por_categoria.csv")
print(f"   ✓ 11_stats_por_ciudad.csv")
print(f"   ✓ 12_stats_por_medio_pago.csv")
print(f"   ✓ 13_stats_temporales.csv")

# ============================================================================
# 10. RESUMEN EJECUTIVO DEL ANÁLISIS
# ============================================================================
print("\n" + "="*80)
print("RESUMEN EJECUTIVO - FASE 2: ESTADÍSTICA APLICADA")
print("="*80)

print("\n📊 ESTADÍSTICAS DESCRIPTIVAS CLAVE:")
print("-" * 80)
for _, row in df_estadisticas.iterrows():
    print(f"\n{row['Variable'].upper()}:")
    print(f"  • Media: ${row['Mean']:,.2f}")
    print(f"  • Mediana: ${row['Median']:,.2f}")
    print(f"  • Desviación Std: ${row['Std']:,.2f}")
    print(f"  • Rango: ${row['Min']:,.2f} - ${row['Max']:,.2f}")
    print(f"  • Coeficiente Variación: {row['CV']:.2f}%")
    print(f"  • Skewness: {row['Skewness']:.3f} ({'Derecha' if row['Skewness'] > 0 else 'Izquierda'})")

print("\n📈 DISTRIBUCIONES IDENTIFICADAS:")
print("-" * 80)
for _, row in df_distribuciones.iterrows():
    print(f"\n{row['Variable'].upper()}: {row['Tipo_Distribucion']}")
    print(f"  • Test Shapiro-Wilk: {'Normal' if row['Shapiro_Normal'] == 'Sí' else 'No Normal'} (p={row['Shapiro_Wilk_p_value']:.4f})")
    print(f"  • Test D'Agostino: {'Normal' if row['DAgostino_Normal'] == 'Sí' else 'No Normal'} (p={row['DAgostino_p_value']:.4f})")
    print(f"  • Interpretación: {row['Interpretacion_Skewness']} con curtosis {row['Interpretacion_Kurtosis']}")

print("\n🔗 CORRELACIONES PRINCIPALES:")
print("-" * 80)
for _, row in df_correlaciones.iterrows():
    print(f"\n{row['Variable_1'].upper()} ↔ {row['Variable_2'].upper()}:")
    print(f"  • Pearson r: {row['Pearson_r']:.3f} ({row['Fuerza']} {row['Direccion']})")
    print(f"  • Spearman r: {row['Spearman_r']:.3f}")
    print(f"  • Significativo: {row['Pearson_Significativo']} (p={row['Pearson_p_value']:.4f})")
    print(f"  • Interpretación: {row['Interpretacion']}")

print("\n⚠️  OUTLIERS DETECTADOS:")
print("-" * 80)
for _, row in df_outliers.iterrows():
    print(f"\n{row['Variable'].upper()}:")
    print(f"  • Outliers leves: {row['Outliers_Leves_Count']} ({row['Outliers_Leves_Pct']:.2f}%)")
    print(f"  • Outliers extremos: {row['Outliers_Extremos_Count']} ({row['Outliers_Extremos_Pct']:.2f}%)")
    print(f"  • Límite superior: ${row['Limite_Superior']:,.2f}")
    print(f"  • Límite inferior: ${row['Limite_Inferior']:,.2f}")
    print(f"  • Estado: {row['Interpretacion']}")

print("\n💼 INTERPRETACIONES PARA EL NEGOCIO:")
print("-" * 80)
for i, row in df_interpretaciones.iterrows():
    print(f"\n{i+1}. {row['Tipo_Analisis']} - {row['Variable']}")
    print(f"   Hallazgo: {row['Hallazgo']}")
    print(f"   Interpretación: {row['Interpretacion']}")
    print(f"   Impacto: {row['Impacto_Negocio']}")
    print(f"   Acción: {row['Accion_Recomendada']}")

print("\n📊 ESTADÍSTICAS POR CATEGORÍA:")
print("-" * 80)
print(stats_por_categoria.to_string(index=False))

print("\n🌍 ESTADÍSTICAS POR CIUDAD:")
print("-" * 80)
print(stats_por_ciudad.to_string(index=False))

print("\n💳 ESTADÍSTICAS POR MEDIO DE PAGO:")
print("-" * 80)
print(stats_por_medio_pago.to_string(index=False))

print("\n📅 ESTADÍSTICAS TEMPORALES:")
print("-" * 80)
print(stats_temporales.to_string(index=False))

print("\n" + "="*80)
print("✓ FASE 2 COMPLETADA EXITOSAMENTE")
print(f"✓ {13} archivos generados en '{CARPETA_ESTADISTICAS}/'")
print("="*80)

# ============================================================================
# 11. ANÁLISIS ADICIONAL: INSIGHTS CLAVE
# ============================================================================
print("\n" + "="*80)
print("INSIGHTS CLAVE PARA LA TOMA DE DECISIONES")
print("="*80)

# Insight 1: Productos más rentables
print("\n1. PRODUCTOS MÁS RENTABLES:")
top_productos = ventas_completas.groupby('nombre_producto').agg({
    'importe': 'sum',
    'cantidad': 'sum'
}).sort_values('importe', ascending=False).head(5)
print(top_productos)

# Insight 2: Categoría dominante
print("\n2. VENTAS POR CATEGORÍA:")
ventas_categoria = ventas_completas.groupby('categoria')['importe'].sum()
print(f"   Alimentos: ${ventas_categoria.get('Alimentos', 0):,.0f} ({ventas_categoria.get('Alimentos', 0)/ventas_categoria.sum()*100:.1f}%)")
print(f"   Limpieza: ${ventas_categoria.get('Limpieza', 0):,.0f} ({ventas_categoria.get('Limpieza', 0)/ventas_categoria.sum()*100:.1f}%)")

# Insight 3: Mejor día de la semana
print("\n3. MEJOR DÍA DE LA SEMANA:")
ventas_por_dia = ventas_completas.groupby('nombre_dia')['importe'].sum().sort_values(ascending=False)
print(ventas_por_dia.head(3))

# Insight 4: Mes con más ventas
print("\n4. MES CON MÁS VENTAS:")
meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio'}
ventas_por_mes = ventas_completas.groupby('mes')['importe'].sum().sort_values(ascending=False)
for mes, importe in ventas_por_mes.head(3).items():
    print(f"   {meses.get(mes, mes)}: ${importe:,.0f}")

# Insight 5: Ciudad más rentable
print("\n5. CIUDAD MÁS RENTABLE:")
ventas_por_ciudad = ventas_completas.groupby('ciudad')['importe'].sum().sort_values(ascending=False)
print(ventas_por_ciudad.head(3))

print("\n" + "="*80)
print("FIN DEL ANÁLISIS ESTADÍSTICO")
print("="*80)
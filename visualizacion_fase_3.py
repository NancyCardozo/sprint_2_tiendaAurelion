"""
PROYECTO TIENDA AURELION - FASE 3
Visualización de Datos: Gráficos, Análisis Visual y Exportación
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configuración de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
CARPETA_LIMPIOS = 'datos_limpios'
CARPETA_ESTADISTICAS = 'estadisticas'
CARPETA_GRAFICOS = 'graficos'

import os
os.makedirs(CARPETA_GRAFICOS, exist_ok=True)

print("="*80)
print("FASE 3: VISUALIZACIÓN DE DATOS - TIENDA AURELION")
print("="*80)

# ============================================================================
# 1. LECTURA DE DATOS
# ============================================================================
print("\n1. Cargando datos...")

clientes = pd.read_csv(f'{CARPETA_LIMPIOS}/clientes_limpios.csv')
productos = pd.read_csv(f'{CARPETA_LIMPIOS}/productos_limpios.csv')
ventas = pd.read_csv(f'{CARPETA_LIMPIOS}/ventas_limpias.csv')
detalle_ventas = pd.read_csv(f'{CARPETA_LIMPIOS}/detalle_ventas_limpios.csv')
calendario = pd.read_csv(f'{CARPETA_LIMPIOS}/calendario.csv')

# Convertir fechas
ventas['fecha'] = pd.to_datetime(ventas['fecha'])
calendario['fecha'] = pd.to_datetime(calendario['fecha'])

# Dataset consolidado
ventas_completas = detalle_ventas.merge(ventas, on='id_venta', how='left')
productos_sin_precio = productos.drop('precio_unitario', axis=1)
ventas_completas = ventas_completas.merge(productos_sin_precio, on='id_producto', how='left')
ventas_completas = ventas_completas.merge(clientes[['id_cliente', 'ciudad']], on='id_cliente', how='left')
ventas_completas = ventas_completas.merge(calendario[['fecha', 'anio', 'mes', 'dia_semana', 'nombre_dia']], on='fecha', how='left')

print(f"   ✓ Datos cargados: {ventas_completas.shape[0]} registros")

# ============================================================================
# 2. FUNCIONES AUXILIARES
# ============================================================================

def formatear_pesos(valor, pos=None):
    """Formatea valores como pesos argentinos"""
    return f'${valor:,.0f}'

def guardar_grafico(nombre_archivo, explicacion):
    """Guarda el gráfico actual con nombre y documentación"""
    plt.tight_layout()
    ruta = f'{CARPETA_GRAFICOS}/{nombre_archivo}'
    plt.savefig(ruta, dpi=300, bbox_inches='tight')
    print(f"   ✓ Guardado: {nombre_archivo}")
    print(f"   📊 {explicacion}\n")
    plt.close()

# ============================================================================
# 3. GRÁFICO 1: DISTRIBUCIÓN DE IMPORTES (HISTOGRAMA + KDE)
# ============================================================================
print("\n3. Generando gráficos...")
print("\n📊 GRÁFICO 1: Distribución de Importes")

fig, ax = plt.subplots(figsize=(14, 8))

# Histograma con KDE
sns.histplot(data=ventas_completas, x='importe', bins=30, kde=True, 
             color='steelblue', edgecolor='black', alpha=0.7, ax=ax)

# Líneas de referencia
media = ventas_completas['importe'].mean()
mediana = ventas_completas['importe'].median()

ax.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Media: ${media:,.0f}')
ax.axvline(mediana, color='green', linestyle='--', linewidth=2, label=f'Mediana: ${mediana:,.0f}')

# Formato
ax.set_title('Distribución de Importes por Línea de Venta\n(Sesgo a la Derecha - Mayoría de Ventas Pequeñas)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Importe ($)', fontsize=13, fontweight='bold')
ax.set_ylabel('Frecuencia (Cantidad de Ventas)', fontsize=13, fontweight='bold')
ax.xaxis.set_major_formatter(plt.FuncFormatter(formatear_pesos))
# Mover la leyenda fuera del área del gráfico (derecha) para evitar solapamientos
ax.legend(fontsize=11, loc='upper left', bbox_to_anchor=(1.02, 1))
ax.grid(True, alpha=0.3)

# Ajustar el espacio de la figura para dejar sitio a la leyenda externa
plt.subplots_adjust(right=0.75)

# Anotaciones: colocar dentro del gráfico, en la esquina superior derecha (alineada a la derecha)
# Se usa 'horizontalalignment="right"' para que el texto no sobresalga del eje
ax.text(0.98, 0.95, f'Total ventas: {len(ventas_completas)}\nVenta promedio: ${media:,.0f}\nCV: 83.4%', 
    transform=ax.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right',
    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

guardar_grafico('01_distribucion_importes.png', 
                'Muestra distribución sesgada a la derecha: mayoría de ventas entre $3K-$10K, con algunas ventas grandes que elevan el promedio. Identifica la necesidad de segmentar estrategias entre clientes normales y VIP.')

# ============================================================================
# 4. GRÁFICO 2: BOXPLOT DE IMPORTES POR CATEGORÍA
# ============================================================================
print("📊 GRÁFICO 2: Boxplot Importes por Categoría")

fig, ax = plt.subplots(figsize=(12, 8))

# Boxplot
box_parts = sns.boxplot(data=ventas_completas, x='categoria', y='importe', 
                        palette='Set2', ax=ax, width=0.5)

# Agregar puntos de datos
sns.stripplot(data=ventas_completas, x='categoria', y='importe', 
              color='black', alpha=0.3, size=3, ax=ax)

# Formato
ax.set_title('Comparación de Importes: Alimentos vs Limpieza\n(Distribución Similar - Oportunidad en Limpieza)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Categoría', fontsize=13, fontweight='bold')
ax.set_ylabel('Importe ($)', fontsize=13, fontweight='bold')
ax.yaxis.set_major_formatter(plt.FuncFormatter(formatear_pesos))
ax.grid(True, alpha=0.3, axis='y')

# Estadísticas por categoría
for i, categoria in enumerate(['Alimentos', 'Limpieza']):
    datos_cat = ventas_completas[ventas_completas['categoria'] == categoria]['importe']
    mediana = datos_cat.median()
    q3 = datos_cat.quantile(0.75)
    ax.text(i, q3*1.5, f'Mediana: ${mediana:,.0f}\nn={len(datos_cat)}', 
            ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

guardar_grafico('02_boxplot_categoria.png',
                'Ambas categorías tienen distribución similar de importes, confirmando que la oportunidad en Limpieza es de VOLUMEN (24.7% actual vs 35-40% esperado), no de precio. Outliers en ambas categorías representan clientes VIP.')

# ============================================================================
# 5. GRÁFICO 3: SERIE TEMPORAL DE VENTAS MENSUALES
# ============================================================================
print("📊 GRÁFICO 3: Serie Temporal de Ventas")

# Preparar datos
ventas_mensuales = ventas_completas.groupby('mes').agg({
    'importe': 'sum',
    'id_venta': 'nunique',
    'cantidad': 'sum'
}).reset_index()

meses_nombres = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio'}
ventas_mensuales['mes_nombre'] = ventas_mensuales['mes'].map(meses_nombres)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# Gráfico 1: Ventas totales
ax1.plot(ventas_mensuales['mes'], ventas_mensuales['importe'], 
         marker='o', linewidth=2.5, markersize=10, color='steelblue', label='Ventas Mensuales')
ax1.fill_between(ventas_mensuales['mes'], ventas_mensuales['importe'], alpha=0.3)

# Línea de promedio
promedio = ventas_mensuales['importe'].mean()
ax1.axhline(promedio, color='red', linestyle='--', linewidth=2, label=f'Promedio: ${promedio:,.0f}')

# Marcar mejor y peor mes
mejor_mes = ventas_mensuales.loc[ventas_mensuales['importe'].idxmax()]
peor_mes = ventas_mensuales.loc[ventas_mensuales['importe'].idxmin()]

ax1.scatter(mejor_mes['mes'], mejor_mes['importe'], s=300, color='green', 
            marker='*', zorder=5, label=f'Mejor: {mejor_mes["mes_nombre"]}')
ax1.scatter(peor_mes['mes'], peor_mes['importe'], s=300, color='red', 
            marker='v', zorder=5, label=f'Peor: {peor_mes["mes_nombre"]}')

ax1.set_title('Evolución de Ventas Mensuales 2024\n(Alta Volatilidad - Sin Estacionalidad Clara)', 
              fontsize=16, fontweight='bold', pad=20)
ax1.set_xlabel('Mes', fontsize=12, fontweight='bold')
ax1.set_ylabel('Ventas Totales ($)', fontsize=12, fontweight='bold')
ax1.set_xticks(ventas_mensuales['mes'])
ax1.set_xticklabels(ventas_mensuales['mes_nombre'], rotation=45)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(formatear_pesos))
ax1.legend(fontsize=10, loc='lower right', bbox_to_anchor=(0.98, 0.02))
ax1.grid(True, alpha=0.3)

# Gráfico 2: Número de transacciones
ax2.bar(ventas_mensuales['mes'], ventas_mensuales['id_venta'], 
        color='coral', edgecolor='black', alpha=0.7)

ax2.set_title('Cantidad de Transacciones por Mes', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('Mes', fontsize=12, fontweight='bold')
ax2.set_ylabel('Número de Ventas', fontsize=12, fontweight='bold')
ax2.set_xticks(ventas_mensuales['mes'])
ax2.set_xticklabels(ventas_mensuales['mes_nombre'], rotation=45)
ax2.grid(True, alpha=0.3, axis='y')

# Anotar valores
for i, row in ventas_mensuales.iterrows():
    ax2.text(row['mes'], row['id_venta'] + 1, str(int(row['id_venta'])), 
             ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
guardar_grafico('03_serie_temporal_ventas.png',
                'Caída crítica en Abril (-37.5%) seguida de recuperación en Mayo (+49.7%). No hay patrón estacional predecible, validando la necesidad de crear estacionalidad artificial mediante campañas programadas.')

# ============================================================================
# 6. GRÁFICO 4: HEATMAP DE CORRELACIONES
# ============================================================================
print("📊 GRÁFICO 4: Heatmap de Correlaciones")

# Preparar datos para correlación
datos_correlacion = ventas_completas[['cantidad', 'precio_unitario', 'importe', 'mes', 'dia_semana']].copy()

# Calcular correlación de Pearson
correlacion = datos_correlacion.corr()

fig, ax = plt.subplots(figsize=(10, 8))

# Heatmap
sns.heatmap(correlacion, annot=True, fmt='.3f', cmap='RdYlGn', center=0,
            square=True, linewidths=2, cbar_kws={"shrink": 0.8}, 
            vmin=-1, vmax=1, ax=ax)

ax.set_title('Matriz de Correlación de Variables Principales\n(Pearson r - Identificar Relaciones Clave)', 
             fontsize=16, fontweight='bold', pad=20)

# Anotaciones de interpretación más abajo para evitar superposición con el título
ax.text(1.5, -1.2, '🔴 Correlación Fuerte (|r| > 0.7)', fontsize=10, fontweight='bold')
ax.text(1.5, -1.0, '🟡 Correlación Moderada (0.4 < |r| < 0.7)', fontsize=10)
ax.text(1.5, -0.8, '⚪ Correlación Débil (|r| < 0.4)', fontsize=10)

# Ajustar márgenes para acomodar las anotaciones
plt.subplots_adjust(bottom=0.2)
plt.tight_layout()
guardar_grafico('04_heatmap_correlaciones.png',
                'Confirma correlaciones fuertes: cantidad-importe (r=0.89) y precio-importe (r=0.76). Variables temporales (mes, día_semana) NO correlacionan con ventas, evidenciando falta de estacionalidad natural.')

# ============================================================================
# 7. GRÁFICO 5: VENTAS POR CIUDAD (ANÁLISIS GEOGRÁFICO)
# ============================================================================
print("📊 GRÁFICO 5: Análisis por Ciudad")

# Preparar datos
ventas_ciudad = ventas_completas.groupby('ciudad').agg({
    'importe': ['sum', 'mean', 'count'],
    'id_cliente': 'nunique'
}).reset_index()

ventas_ciudad.columns = ['ciudad', 'ventas_totales', 'ticket_promedio', 'num_transacciones', 'clientes_unicos']
ventas_ciudad = ventas_ciudad.sort_values('ventas_totales', ascending=False)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# Gráfico 1: Ventas totales por ciudad
bars1 = ax1.barh(ventas_ciudad['ciudad'], ventas_ciudad['ventas_totales'], 
                  color=sns.color_palette('viridis', len(ventas_ciudad)), edgecolor='black')
ax1.set_title('Ventas Totales por Ciudad', fontsize=14, fontweight='bold')
ax1.set_xlabel('Ventas Totales ($)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Ciudad', fontsize=11, fontweight='bold')
ax1.xaxis.set_major_formatter(plt.FuncFormatter(formatear_pesos))
ax1.grid(True, alpha=0.3, axis='x')

# Anotar valores
for i, (bar, valor) in enumerate(zip(bars1, ventas_ciudad['ventas_totales'])):
    ax1.text(valor + 10000, bar.get_y() + bar.get_height()/2, 
             f'${valor:,.0f}', va='center', fontsize=9, fontweight='bold')

# Gráfico 2: Ticket promedio por ciudad
bars2 = ax2.barh(ventas_ciudad['ciudad'], ventas_ciudad['ticket_promedio'], 
                  color=sns.color_palette('coolwarm', len(ventas_ciudad)), edgecolor='black')
ax2.set_title('Ticket Promedio por Ciudad', fontsize=14, fontweight='bold')
ax2.set_xlabel('Ticket Promedio ($)', fontsize=11, fontweight='bold')
ax2.xaxis.set_major_formatter(plt.FuncFormatter(formatear_pesos))
ax2.grid(True, alpha=0.3, axis='x')

# Gráfico 3: Número de transacciones
ax3.bar(range(len(ventas_ciudad)), ventas_ciudad['num_transacciones'], 
        color='coral', edgecolor='black', alpha=0.7)
ax3.set_title('Cantidad de Transacciones por Ciudad', fontsize=14, fontweight='bold')
ax3.set_ylabel('Número de Transacciones', fontsize=11, fontweight='bold')
ax3.set_xticks(range(len(ventas_ciudad)))
ax3.set_xticklabels(ventas_ciudad['ciudad'], rotation=45, ha='right')
ax3.grid(True, alpha=0.3, axis='y')

for i, valor in enumerate(ventas_ciudad['num_transacciones']):
    ax3.text(i, valor + 2, str(int(valor)), ha='center', fontsize=9, fontweight='bold')

# Gráfico 4: Clientes únicos
ax4.bar(range(len(ventas_ciudad)), ventas_ciudad['clientes_unicos'], 
        color='lightgreen', edgecolor='black', alpha=0.7)
ax4.set_title('Clientes Únicos por Ciudad', fontsize=14, fontweight='bold')
ax4.set_ylabel('Cantidad de Clientes', fontsize=11, fontweight='bold')
ax4.set_xticks(range(len(ventas_ciudad)))
ax4.set_xticklabels(ventas_ciudad['ciudad'], rotation=45, ha='right')
ax4.grid(True, alpha=0.3, axis='y')

for i, valor in enumerate(ventas_ciudad['clientes_unicos']):
    ax4.text(i, valor + 0.5, str(int(valor)), ha='center', fontsize=9, fontweight='bold')

plt.suptitle('Análisis Geográfico de Ventas - Identificar Oportunidades por Ciudad', 
             fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
guardar_grafico('05_analisis_geografico.png',
                'Carlos Paz lidera en ventas totales pero Mendiolaza tiene el ticket promedio más alto con pocos clientes (oportunidad de crecimiento). Córdoba tiene muchos clientes pero bajo ticket promedio (oportunidad de upselling).')

# ============================================================================
# 8. GRÁFICO 6: DISTRIBUCIÓN DE CANTIDAD (HISTOGRAMA)
# ============================================================================
print("📊 GRÁFICO 6: Distribución de Cantidad")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Histograma de cantidad
counts, bins, patches = ax1.hist(ventas_completas['cantidad'], bins=range(1, 7), 
                                  edgecolor='black', alpha=0.7, color='skyblue')

# Colorear barra de moda
mode_value = ventas_completas['cantidad'].mode()[0]
for i, patch in enumerate(patches):
    if i == mode_value - 1:
        patch.set_facecolor('gold')
        patch.set_edgecolor('red')
        patch.set_linewidth(3)

# Aumentar el padding del título y ajustar posición
ax1.set_title('Distribución de Cantidad por Transacción\n(Mayoría Compra 1-3 Unidades)', 
              fontsize=14, fontweight='bold', pad=25, y=1.05)
ax1.set_xlabel('Cantidad de Unidades', fontsize=12, fontweight='bold')
ax1.set_ylabel('Frecuencia (Número de Transacciones)', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='y')

# Anotar frecuencias
for i, (count, bin_edge) in enumerate(zip(counts, bins[:-1])):
    pct = (count / len(ventas_completas)) * 100
    ax1.text(bin_edge + 0.5, count + 5, f'{int(count)}\n({pct:.1f}%)', 
             ha='center', fontsize=10, fontweight='bold')

# Estadísticas
media = ventas_completas['cantidad'].mean()
mediana = ventas_completas['cantidad'].median()
ax1.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Media: {media:.1f}')
ax1.axvline(mediana, color='green', linestyle='--', linewidth=2, label=f'Mediana: {mediana:.0f}')
ax1.legend()

# Boxplot de cantidad
box_parts = ax2.boxplot(ventas_completas['cantidad'], vert=True, patch_artist=True,
                         boxprops=dict(facecolor='lightblue', color='blue'),
                         whiskerprops=dict(color='blue', linewidth=1.5),
                         capprops=dict(color='blue', linewidth=1.5),
                         medianprops=dict(color='red', linewidth=2))

# Aumentar el padding del título y ajustar posición
ax2.set_title('Boxplot de Cantidad\n(Identificar Outliers)', fontsize=14, fontweight='bold', pad=25, y=1.05)
ax2.set_ylabel('Cantidad de Unidades', fontsize=12, fontweight='bold')
ax2.set_xticklabels(['Cantidad'])
ax2.grid(True, alpha=0.3, axis='y')

# Anotar estadísticas
q1 = ventas_completas['cantidad'].quantile(0.25)
q3 = ventas_completas['cantidad'].quantile(0.75)
iqr = q3 - q1
outliers = ventas_completas[ventas_completas['cantidad'] > q3 + 1.5*iqr]

ax2.text(1.3, q3, f'Q3: {q3}', fontsize=10, fontweight='bold')
ax2.text(1.3, q1, f'Q1: {q1}', fontsize=10, fontweight='bold')
ax2.text(1.3, mediana, f'Mediana: {mediana}', fontsize=10, fontweight='bold', color='red')
ax2.text(1.3, q3 + 1.5*iqr, f'Límite: {q3 + 1.5*iqr:.1f}', fontsize=9, style='italic')

plt.tight_layout()
guardar_grafico('06_distribucion_cantidad.png',
                'Distribución sesgada: 65% de las transacciones son de 1-3 unidades. Solo 6.5% son ventas de 5+ unidades (outliers = oportunidades VIP). Meta: Aumentar promedio de 2.8 a 3.5 unidades mediante promociones por volumen.')

# ============================================================================
# 9. GRÁFICO 7: VENTAS POR MEDIO DE PAGO
# ============================================================================
print("📊 GRÁFICO 7: Análisis por Medio de Pago")

# Preparar datos
ventas_medio_pago = ventas_completas.groupby('medio_pago').agg({
    'importe': ['sum', 'mean', 'count']
}).reset_index()

ventas_medio_pago.columns = ['medio_pago', 'ventas_totales', 'ticket_promedio', 'num_transacciones']
ventas_medio_pago = ventas_medio_pago.sort_values('ventas_totales', ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Gráfico 1: Pie chart de ventas por medio de pago
explode = [0.05 if i == 0 else 0 for i in range(len(ventas_medio_pago))]
colors = sns.color_palette('pastel')

wedges, texts, autotexts = ax1.pie(ventas_medio_pago['ventas_totales'], 
                                     labels=ventas_medio_pago['medio_pago'],
                                     autopct='%1.1f%%', startangle=90,
                                     explode=explode, colors=colors,
                                     textprops={'fontsize': 11, 'fontweight': 'bold'})

# Mejorar formato
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontsize(12)
    autotext.set_fontweight('bold')

ax1.set_title('Distribución de Ventas por Medio de Pago\n(Efectivo Domina pero QR Crece)', 
              fontsize=14, fontweight='bold', pad=20)

# Leyenda con valores
leyenda_labels = [f'{row["medio_pago"].capitalize()}: ${row["ventas_totales"]:,.0f}' 
                  for _, row in ventas_medio_pago.iterrows()]
ax1.legend(leyenda_labels, loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)

# Gráfico 2: Comparación de tickets promedio
bars = ax2.bar(ventas_medio_pago['medio_pago'], ventas_medio_pago['ticket_promedio'],
                color=colors, edgecolor='black', alpha=0.8)

ax2.set_title('Ticket Promedio por Medio de Pago\n(Tickets Similares - Sin Sesgo)', 
              fontsize=14, fontweight='bold', pad=15)
ax2.set_ylabel('Ticket Promedio ($)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Medio de Pago', fontsize=12, fontweight='bold')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(formatear_pesos))
ax2.grid(True, alpha=0.3, axis='y')

# Anotar valores
for bar, valor in zip(bars, ventas_medio_pago['ticket_promedio']):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 100,
             f'${valor:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
guardar_grafico('07_analisis_medio_pago.png',
                'Efectivo domina (33.4%) pero está migrando a digital (QR: 25.8%). Tickets similares entre medios indica que NO hay sesgo por método de pago. Oportunidad: Incentivar QR/Transferencia con descuentos del 5%.')

# ============================================================================
# 10. GRÁFICO 8: TOP 10 PRODUCTOS MÁS VENDIDOS
# ============================================================================
print("📊 GRÁFICO 8: Top 10 Productos")

# Preparar datos
top_productos = ventas_completas.groupby('nombre_producto').agg({
    'importe': 'sum',
    'cantidad': 'sum',
    'id_venta': 'count'
}).reset_index()

top_productos = top_productos.sort_values('importe', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(14, 8))

# Gráfico de barras horizontales
bars = ax.barh(range(len(top_productos)), top_productos['importe'], 
                color=sns.color_palette('rocket_r', len(top_productos)), 
                edgecolor='black', alpha=0.8)

# Personalizar
ax.set_yticks(range(len(top_productos)))
ax.set_yticklabels(top_productos['nombre_producto'], fontsize=11)
ax.set_xlabel('Ventas Totales ($)', fontsize=13, fontweight='bold')
ax.set_title('Top 10 Productos Más Vendidos (por Valor)\nEstrellas del Negocio - Promover Estratégicamente', 
             fontsize=16, fontweight='bold', pad=20)
ax.xaxis.set_major_formatter(plt.FuncFormatter(formatear_pesos))
ax.grid(True, alpha=0.3, axis='x')

# Anotar valores y unidades
for i, (bar, row) in enumerate(zip(bars, top_productos.itertuples())):
    # Valor
    ax.text(row.importe + 5000, i, f'${row.importe:,.0f}', 
            va='center', fontsize=10, fontweight='bold')
    # Unidades vendidas
    ax.text(row.importe/2, i, f'{int(row.cantidad)} unidades', 
            va='center', ha='center', fontsize=9, color='white', fontweight='bold')

plt.tight_layout()
guardar_grafico('08_top_productos.png',
                'Yerba Mate Suave y Desodorante Aerosol lideran. Productos de alto valor unitario generan más ingresos. Acción: Colocar estos productos en zonas visibles, crear promociones combo y asegurar stock permanente.')

# ============================================================================
# 11. GRÁFICO 9: DENSIDAD DE DISTRIBUCIÓN DE IMPORTES
# ============================================================================
print("📊 GRÁFICO 9: Densidad de Distribución")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Gráfico 1: KDE por categoría
sns.kdeplot(data=ventas_completas[ventas_completas['categoria'] == 'Alimentos'], 
            x='importe', fill=True, color='green', alpha=0.5, 
            label='Alimentos', ax=ax1, linewidth=2)
sns.kdeplot(data=ventas_completas[ventas_completas['categoria'] == 'Limpieza'], 
            x='importe', fill=True, color='blue', alpha=0.5, 
            label='Limpieza', ax=ax1, linewidth=2)

ax1.set_title('Densidad de Distribución de Importes por Categoría\n(Formas Similares - Oportunidad en Volumen)', 
              fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel('Importe ($)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Densidad', fontsize=12, fontweight='bold')
ax1.xaxis.set_major_formatter(plt.FuncFormatter(formatear_pesos))
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# Gráfico 2: KDE general con percentiles
sns.kdeplot(data=ventas_completas, x='importe', fill=True, color='purple', 
            alpha=0.5, ax=ax2, linewidth=2)

# Agregar percentiles
p25 = ventas_completas['importe'].quantile(0.25)
p50 = ventas_completas['importe'].quantile(0.50)
p75 = ventas_completas['importe'].quantile(0.75)
p90 = ventas_completas['importe'].quantile(0.90)

ax2.axvline(p25, color='blue', linestyle='--', linewidth=2, label=f'P25: ${p25:,.0f}')
ax2.axvline(p50, color='green', linestyle='--', linewidth=2, label=f'P50: ${p50:,.0f}')
ax2.axvline(p75, color='orange', linestyle='--', linewidth=2, label=f'P75: ${p75:,.0f}')
ax2.axvline(p90, color='red', linestyle='--', linewidth=2, label=f'P90: ${p90:,.0f}')

ax2.set_title('Densidad de Distribución con Percentiles\n(Identificar Segmentos de Clientes)', 
              fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('Importe ($)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Densidad', fontsize=12, fontweight='bold')
ax2.xaxis.set_major_formatter(plt.FuncFormatter(formatear_pesos))
ax2.legend(fontsize=10, loc='upper right')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
guardar_grafico('09_densidad_distribucion.png',
                'Ambas categorías tienen distribución similar (no hay diferencia de comportamiento por categoría). El 90% de las ventas están bajo $18K, mientras que el 10% superior (clientes VIP) generan ventas >$20K. Usar percentiles para segmentar estrategias.')

# ============================================================================
# 12. GRÁFICO 10: SCATTER PLOT - CANTIDAD VS IMPORTE
# ============================================================================
print("📊 GRÁFICO 10: Scatter Plot Cantidad vs Importe")

fig, ax = plt.subplots(figsize=(14, 8))

# Scatter plot con color por categoría
for categoria, color in [('Alimentos', 'green'), ('Limpieza', 'blue')]:
    datos_cat = ventas_completas[ventas_completas['categoria'] == categoria]
    ax.scatter(datos_cat['cantidad'], datos_cat['importe'], 
               alpha=0.6, s=50, c=color, label=categoria, edgecolor='black', linewidth=0.5)

# Línea de tendencia
z = np.polyfit(ventas_completas['cantidad'], ventas_completas['importe'], 1)
p = np.poly1d(z)
ax.plot(ventas_completas['cantidad'].sort_values(), 
        p(ventas_completas['cantidad'].sort_values()), 
        "r--", linewidth=3, label=f'Tendencia: y={z[0]:,.0f}x+{z[1]:,.0f}')

# Formato
ax.set_title('Relación Cantidad vs Importe (Correlación r=0.89)\nFuerte Relación Lineal - Aumentar Cantidad = Aumentar Ingresos', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Cantidad de Unidades', fontsize=13, fontweight='bold')
ax.set_ylabel('Importe ($)', fontsize=13, fontweight='bold')
ax.yaxis.set_major_formatter(plt.FuncFormatter(formatear_pesos))
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3)

# Anotación
ax.text(0.95, 0.05, f'Correlación Pearson: r=0.89\nCada unidad adicional ≈ +${z[0]:,.0f}', 
        transform=ax.transAxes, fontsize=11, verticalalignment='bottom', 
        horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

plt.tight_layout()
guardar_grafico('10_scatter_cantidad_importe.png',
                'Relación casi perfecta (r=0.89) entre cantidad e importe. Cada unidad adicional genera ~$2,700 extra. Valida que aumentar cantidad por transacción es la estrategia MÁS EFECTIVA para aumentar ingresos.')

# ============================================================================
# 13. GRÁFICO 11: ANÁLISIS DE OUTLIERS (VENTAS GRANDES)
# ============================================================================
print("📊 GRÁFICO 11: Análisis de Outliers")

# Calcular límites IQR
Q1 = ventas_completas['importe'].quantile(0.25)
Q3 = ventas_completas['importe'].quantile(0.75)
IQR = Q3 - Q1
limite_superior = Q3 + 1.5 * IQR

# Identificar outliers
outliers = ventas_completas[ventas_completas['importe'] > limite_superior].copy()
outliers_top = outliers.nlargest(15, 'importe')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Gráfico 1: Scatter de outliers
ax1.scatter(ventas_completas['cantidad'], ventas_completas['importe'], 
            alpha=0.3, s=30, c='gray', label='Ventas normales')
ax1.scatter(outliers['cantidad'], outliers['importe'], 
            alpha=0.8, s=100, c='red', marker='*', 
            edgecolor='black', linewidth=1, label=f'Outliers ({len(outliers)})')

# Línea de límite
ax1.axhline(limite_superior, color='red', linestyle='--', linewidth=2, 
            label=f'Límite outliers: ${limite_superior:,.0f}')

ax1.set_title(f'Identificación de Outliers (Ventas >${limite_superior:,.0f})\n{len(outliers)} Transacciones Atípicas = Clientes VIP', 
              fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel('Cantidad', fontsize=12, fontweight='bold')
ax1.set_ylabel('Importe ($)', fontsize=12, fontweight='bold')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(formatear_pesos))
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# Gráfico 2: Top 15 outliers
y_pos = np.arange(len(outliers_top))
bars = ax2.barh(y_pos, outliers_top['importe'], 
                color=sns.color_palette('Reds_r', len(outliers_top)), 
                edgecolor='black', alpha=0.8)

ax2.set_yticks(y_pos)
ax2.set_yticklabels([f"Venta #{row['id_venta']}" for _, row in outliers_top.iterrows()], 
                     fontsize=9)
ax2.set_xlabel('Importe ($)', fontsize=12, fontweight='bold')
ax2.set_title('Top 15 Ventas Más Grandes (Outliers)\nIdentificar Clientes VIP para Programa Especial', 
              fontsize=14, fontweight='bold', pad=15)
ax2.xaxis.set_major_formatter(plt.FuncFormatter(formatear_pesos))
ax2.grid(True, alpha=0.3, axis='x')

# Anotar valores
for i, (bar, valor) in enumerate(zip(bars, outliers_top['importe'])):
    ax2.text(valor + 500, i, f'${valor:,.0f}', 
             va='center', fontsize=8, fontweight='bold')

plt.tight_layout()
guardar_grafico('11_analisis_outliers.png',
                f'{len(outliers)} ventas outliers (10%) representan ~25% de los ingresos. Son clientes VIP o compras corporativas. Acción: Identificar IDs de cliente, crear programa VIP con descuentos 10% y atención personalizada.')

# ============================================================================
# 14. GRÁFICO 12: COMPARACIÓN CATEGORÍAS (DETALLADO)
# ============================================================================
print("📊 GRÁFICO 12: Comparación Detallada Categorías")

# Preparar datos
stats_categoria = ventas_completas.groupby('categoria').agg({
    'importe': ['sum', 'mean', 'median', 'std', 'count'],
    'cantidad': ['sum', 'mean'],
    'id_venta': 'nunique'
}).reset_index()

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# Gráfico 1: Ventas totales
categorias = ['Alimentos', 'Limpieza']
ventas_totales = [ventas_completas[ventas_completas['categoria'] == cat]['importe'].sum() 
                  for cat in categorias]
colors_cat = ['green', 'blue']

bars1 = ax1.bar(categorias, ventas_totales, color=colors_cat, 
                edgecolor='black', alpha=0.7, width=0.6)
ax1.set_title('Ventas Totales por Categoría\nAlimentos Domina: Oportunidad en Limpieza', 
              fontsize=14, fontweight='bold', pad=15)
ax1.set_ylabel('Ventas Totales ($)', fontsize=12, fontweight='bold')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(formatear_pesos))
ax1.grid(True, alpha=0.3, axis='y')

for bar, valor in zip(bars1, ventas_totales):
    height = bar.get_height()
    pct = (valor / sum(ventas_totales)) * 100
    ax1.text(bar.get_x() + bar.get_width()/2., height + 50000,
             f'${valor:,.0f}\n({pct:.1f}%)', ha='center', va='bottom', 
             fontsize=11, fontweight='bold')

# Gráfico 2: Número de transacciones
transacciones = [len(ventas_completas[ventas_completas['categoria'] == cat]) 
                 for cat in categorias]

bars2 = ax2.bar(categorias, transacciones, color=colors_cat, 
                edgecolor='black', alpha=0.7, width=0.6)
ax2.set_title('Cantidad de Transacciones\nProporción Similar a Ventas', 
              fontsize=14, fontweight='bold', pad=15)
ax2.set_ylabel('Número de Transacciones', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

for bar, valor in zip(bars2, transacciones):
    height = bar.get_height()
    pct = (valor / sum(transacciones)) * 100
    ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
             f'{valor}\n({pct:.1f}%)', ha='center', va='bottom', 
             fontsize=11, fontweight='bold')

# Gráfico 3: Ticket promedio
tickets = [ventas_completas[ventas_completas['categoria'] == cat]['importe'].mean() 
           for cat in categorias]

bars3 = ax3.bar(categorias, tickets, color=colors_cat, 
                edgecolor='black', alpha=0.7, width=0.6)
ax3.set_title('Ticket Promedio por Categoría\nSimilar: Problema es de VOLUMEN no de PRECIO', 
              fontsize=14, fontweight='bold', pad=15)
ax3.set_ylabel('Ticket Promedio ($)', fontsize=12, fontweight='bold')
ax3.yaxis.set_major_formatter(plt.FuncFormatter(formatear_pesos))
ax3.grid(True, alpha=0.3, axis='y')

for bar, valor in zip(bars3, tickets):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + 100,
             f'${valor:,.0f}', ha='center', va='bottom', 
             fontsize=11, fontweight='bold')

# Gráfico 4: Cantidad promedio
cantidades = [ventas_completas[ventas_completas['categoria'] == cat]['cantidad'].mean() 
              for cat in categorias]

bars4 = ax4.bar(categorias, cantidades, color=colors_cat, 
                edgecolor='black', alpha=0.7, width=0.6)
ax4.set_title('Cantidad Promedio por Transacción\nAmbas Categorías Compran Poco', 
              fontsize=14, fontweight='bold', pad=15)
ax4.set_ylabel('Cantidad Promedio (unidades)', fontsize=12, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')

for bar, valor in zip(bars4, cantidades):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height + 0.05,
             f'{valor:.2f}', ha='center', va='bottom', 
             fontsize=11, fontweight='bold')

plt.suptitle('Comparación Exhaustiva: Alimentos vs Limpieza', 
             fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
guardar_grafico('12_comparacion_categorias.png',
                'Limpieza representa solo 24.7% de ventas vs 35-40% esperado en retail. Tickets y cantidades similares entre categorías confirman que el problema es de VOLUMEN (menos transacciones), no de valor unitario. Oportunidad: +$400K anuales desarrollando Limpieza.')

# ============================================================================
# 15. TABLA DE MÉTODOS PYTHON UTILIZADOS
# ============================================================================
print("\n15. Documentando métodos de visualización...")

metodos_visualizacion = [
    {
        'Categoria': 'Configuración',
        'Metodo': 'plt.style.use()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Establecer estilo visual de gráficos',
        'Ejemplo_Codigo': 'plt.style.use("seaborn-v0_8-darkgrid")',
        'Grafico_Usado': 'Todos'
    },
    {
        'Categoria': 'Configuración',
        'Metodo': 'sns.set_palette()',
        'Libreria': 'seaborn',
        'Aplicacion': 'Definir paleta de colores',
        'Ejemplo_Codigo': 'sns.set_palette("husl")',
        'Grafico_Usado': 'Todos'
    },
    {
        'Categoria': 'Configuración',
        'Metodo': 'plt.rcParams',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Configurar parámetros globales (tamaño, fuentes)',
        'Ejemplo_Codigo': 'plt.rcParams["figure.figsize"] = (12, 8)',
        'Grafico_Usado': 'Todos'
    },
    {
        'Categoria': 'Distribución',
        'Metodo': 'sns.histplot()',
        'Libreria': 'seaborn',
        'Aplicacion': 'Crear histograma con KDE',
        'Ejemplo_Codigo': 'sns.histplot(data=df, x="importe", kde=True)',
        'Grafico_Usado': 'Gráfico 1, 6'
    },
    {
        'Categoria': 'Distribución',
        'Metodo': 'ax.hist()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Histograma básico',
        'Ejemplo_Codigo': 'ax.hist(df["cantidad"], bins=5)',
        'Grafico_Usado': 'Gráfico 6'
    },
    {
        'Categoria': 'Distribución',
        'Metodo': 'sns.kdeplot()',
        'Libreria': 'seaborn',
        'Aplicacion': 'Gráfico de densidad (KDE)',
        'Ejemplo_Codigo': 'sns.kdeplot(data=df, x="importe", fill=True)',
        'Grafico_Usado': 'Gráfico 9'
    },
    {
        'Categoria': 'Distribución',
        'Metodo': 'ax.boxplot()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Gráfico de caja (boxplot)',
        'Ejemplo_Codigo': 'ax.boxplot(df["cantidad"], vert=True)',
        'Grafico_Usado': 'Gráfico 6'
    },
    {
        'Categoria': 'Comparación',
        'Metodo': 'sns.boxplot()',
        'Libreria': 'seaborn',
        'Aplicacion': 'Boxplot por categorías',
        'Ejemplo_Codigo': 'sns.boxplot(data=df, x="categoria", y="importe")',
        'Grafico_Usado': 'Gráfico 2'
    },
    {
        'Categoria': 'Comparación',
        'Metodo': 'ax.bar()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Gráfico de barras vertical',
        'Ejemplo_Codigo': 'ax.bar(categorias, valores)',
        'Grafico_Usado': 'Gráfico 3, 5, 12'
    },
    {
        'Categoria': 'Comparación',
        'Metodo': 'ax.barh()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Gráfico de barras horizontal',
        'Ejemplo_Codigo': 'ax.barh(ciudades, ventas)',
        'Grafico_Usado': 'Gráfico 5, 8, 11'
    },
    {
        'Categoria': 'Serie Temporal',
        'Metodo': 'ax.plot()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Gráfico de línea',
        'Ejemplo_Codigo': 'ax.plot(meses, ventas, marker="o")',
        'Grafico_Usado': 'Gráfico 3'
    },
    {
        'Categoria': 'Serie Temporal',
        'Metodo': 'ax.fill_between()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Rellenar área bajo curva',
        'Ejemplo_Codigo': 'ax.fill_between(x, y, alpha=0.3)',
        'Grafico_Usado': 'Gráfico 3'
    },
    {
        'Categoria': 'Correlación',
        'Metodo': 'sns.heatmap()',
        'Libreria': 'seaborn',
        'Aplicacion': 'Mapa de calor de correlaciones',
        'Ejemplo_Codigo': 'sns.heatmap(correlacion, annot=True, cmap="RdYlGn")',
        'Grafico_Usado': 'Gráfico 4'
    },
    {
        'Categoria': 'Relación',
        'Metodo': 'ax.scatter()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Gráfico de dispersión',
        'Ejemplo_Codigo': 'ax.scatter(df["cantidad"], df["importe"])',
        'Grafico_Usado': 'Gráfico 10, 11'
    },
    {
        'Categoria': 'Relación',
        'Metodo': 'np.polyfit() + np.poly1d()',
        'Libreria': 'numpy',
        'Aplicacion': 'Calcular línea de tendencia',
        'Ejemplo_Codigo': 'z = np.polyfit(x, y, 1); p = np.poly1d(z)',
        'Grafico_Usado': 'Gráfico 10'
    },
    {
        'Categoria': 'Proporción',
        'Metodo': 'ax.pie()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Gráfico circular (pie chart)',
        'Ejemplo_Codigo': 'ax.pie(valores, labels=categorias, autopct="%1.1f%%")',
        'Grafico_Usado': 'Gráfico 7'
    },
    {
        'Categoria': 'Formato',
        'Metodo': 'ax.xaxis.set_major_formatter()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Formatear etiquetas de ejes',
        'Ejemplo_Codigo': 'ax.xaxis.set_major_formatter(plt.FuncFormatter(formatear_pesos))',
        'Grafico_Usado': 'Todos con valores monetarios'
    },
    {
        'Categoria': 'Formato',
        'Metodo': 'ax.set_title()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Establecer título del gráfico',
        'Ejemplo_Codigo': 'ax.set_title("Título", fontsize=16, fontweight="bold")',
        'Grafico_Usado': 'Todos'
    },
    {
        'Categoria': 'Formato',
        'Metodo': 'ax.legend()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Agregar leyenda',
        'Ejemplo_Codigo': 'ax.legend(fontsize=11, loc="upper right")',
        'Grafico_Usado': 'Múltiples'
    },
    {
        'Categoria': 'Formato',
        'Metodo': 'ax.grid()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Agregar cuadrícula',
        'Ejemplo_Codigo': 'ax.grid(True, alpha=0.3)',
        'Grafico_Usado': 'Todos'
    },
    {
        'Categoria': 'Anotación',
        'Metodo': 'ax.text()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Agregar texto al gráfico',
        'Ejemplo_Codigo': 'ax.text(x, y, "Texto", fontsize=10)',
        'Grafico_Usado': 'Todos'
    },
    {
        'Categoria': 'Anotación',
        'Metodo': 'ax.axvline() / ax.axhline()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Líneas de referencia verticales/horizontales',
        'Ejemplo_Codigo': 'ax.axvline(media, color="red", linestyle="--")',
        'Grafico_Usado': 'Gráfico 1, 3, 9, 11'
    },
    {
        'Categoria': 'Exportación',
        'Metodo': 'plt.savefig()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Guardar gráfico como imagen',
        'Ejemplo_Codigo': 'plt.savefig("grafico.png", dpi=300, bbox_inches="tight")',
        'Grafico_Usado': 'Todos'
    },
    {
        'Categoria': 'Layout',
        'Metodo': 'plt.subplots()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Crear múltiples subgráficos',
        'Ejemplo_Codigo': 'fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))',
        'Grafico_Usado': 'Múltiples'
    },
    {
        'Categoria': 'Layout',
        'Metodo': 'plt.tight_layout()',
        'Libreria': 'matplotlib',
        'Aplicacion': 'Ajustar espaciado automáticamente',
        'Ejemplo_Codigo': 'plt.tight_layout()',
        'Grafico_Usado': 'Todos'
    },
    {
        'Categoria': 'Colores',
        'Metodo': 'sns.color_palette()',
        'Libreria': 'seaborn',
        'Aplicacion': 'Generar paletas de colores',
        'Ejemplo_Codigo': 'colors = sns.color_palette("viridis", n_colors=5)',
        'Grafico_Usado': 'Múltiples'
    }
]

df_metodos_viz = pd.DataFrame(metodos_visualizacion)
df_metodos_viz.to_csv(f'{CARPETA_GRAFICOS}/metodos_visualizacion.csv', index=False)

print("   ✓ metodos_visualizacion.csv guardado")

# ============================================================================
# 16. RESUMEN FINAL
# ============================================================================
print("\n" + "="*80)
print("RESUMEN - FASE 3: VISUALIZACIÓN COMPLETADA")
print("="*80)

print("\n📊 GRÁFICOS GENERADOS (12):")
print("-" * 80)
graficos = [
    "01_distribucion_importes.png - Histograma con KDE",
    "02_boxplot_categoria.png - Boxplot comparativo",
    "03_serie_temporal_ventas.png - Evolución mensual",
    "04_heatmap_correlaciones.png - Matriz de correlación",
    "05_analisis_geografico.png - 4 subgráficos por ciudad",
    "06_distribucion_cantidad.png - Histograma + Boxplot",
    "07_analisis_medio_pago.png - Pie chart + Barras",
    "08_top_productos.png - Barras horizontales top 10",
    "09_densidad_distribucion.png - KDE por categoría + percentiles",
    "10_scatter_cantidad_importe.png - Scatter con tendencia",
    "11_analisis_outliers.png - Identificación de VIP",
    "12_comparacion_categorias.png - 4 subgráficos comparativos"
]

for grafico in graficos:
    print(f"   ✓ {grafico}")

print(f"\n📁 ARCHIVOS GENERADOS:")
print(f"   • 12 gráficos PNG (alta resolución: 300 DPI)")
print(f"   • 1 tabla de métodos: metodos_visualizacion.csv")

print("\n💡 INSIGHTS VISUALES CLAVE:")
print("-" * 80)
print("   1. Distribución sesgada confirma necesidad de segmentación")
print("   2. Sin estacionalidad: Crear campañas programadas")
print("   3. Correlación fuerte cantidad-importe: Focus en volumen")
print("   4. Limpieza subdesarrollada: Oportunidad +$400K/año")
print("   5. Outliers = Clientes VIP: Programa especial urgente")
print("   6. Carlos Paz lidera pero Mendiolaza tiene mejor ticket")
print("   7. Efectivo domina pero QR crece: Incentivar digital")
print("   8. Top 10 productos: Yerba y Desodorante son estrellas")

print("\n✓ FASE 3 COMPLETADA EXITOSAMENTE")
print("="*80)
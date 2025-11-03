"""
PROYECTO TIENDA AURELION - FASE 3 (VERSIÓN INTERACTIVA)
Visualización de Datos: Gráficos Interactivos con Plotly
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
CARPETA_LIMPIOS = 'datos_limpios'
CARPETA_ESTADISTICAS = 'estadisticas'
CARPETA_GRAFICOS = 'graficos_interactivos'

import os
os.makedirs(CARPETA_GRAFICOS, exist_ok=True)

print("="*80)
print("FASE 3: VISUALIZACIÓN INTERACTIVA - TIENDA AURELION")
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
# 2. GRÁFICO 1: DISTRIBUCIÓN DE IMPORTES (HISTOGRAMA INTERACTIVO)
# ============================================================================
print("\n2. Generando gráficos interactivos...")
print("\n📊 GRÁFICO 1: Distribución de Importes (Interactivo)")

fig1 = go.Figure()

# Histograma
fig1.add_trace(go.Histogram(
    x=ventas_completas['importe'],
    nbinsx=30,
    name='Distribución',
    marker_color='steelblue',
    opacity=0.7,
    hovertemplate='Rango: $%{x:,.0f}<br>Frecuencia: %{y}<extra></extra>'
))

# Líneas de referencia
media = ventas_completas['importe'].mean()
mediana = ventas_completas['importe'].median()

fig1.add_vline(x=media, line_dash="dash", line_color="red", 
               annotation_text=f"Media: ${media:,.0f}", 
               annotation_position="top right")
fig1.add_vline(x=mediana, line_dash="dash", line_color="green",
               annotation_text=f"Mediana: ${mediana:,.0f}",
               annotation_position="top left")

fig1.update_layout(
    title={
        'text': 'Distribución de Importes por Línea de Venta<br><sub>Sesgo a la Derecha - Mayoría de Ventas Pequeñas</sub>',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Importe ($)',
    yaxis_title='Frecuencia (Cantidad de Ventas)',
    hovermode='x unified',
    template='plotly_white',
    height=600
)

fig1.write_html(f'{CARPETA_GRAFICOS}/01_distribucion_importes_interactivo.html')
print("   ✓ 01_distribucion_importes_interactivo.html")

# ============================================================================
# 3. GRÁFICO 2: BOXPLOT INTERACTIVO POR CATEGORÍA
# ============================================================================
print("📊 GRÁFICO 2: Boxplot Importes por Categoría")

fig2 = go.Figure()

for categoria in ['Alimentos', 'Limpieza']:
    datos_cat = ventas_completas[ventas_completas['categoria'] == categoria]['importe']
    
    fig2.add_trace(go.Box(
        y=datos_cat,
        name=categoria,
        boxmean='sd',
        hovertemplate='<b>%{fullData.name}</b><br>Valor: $%{y:,.0f}<extra></extra>'
    ))

fig2.update_layout(
    title={
        'text': 'Comparación de Importes: Alimentos vs Limpieza<br><sub>Distribución Similar - Oportunidad en Limpieza</sub>',
        'x': 0.5,
        'xanchor': 'center'
    },
    yaxis_title='Importe ($)',
    xaxis_title='Categoría',
    template='plotly_white',
    height=600,
    showlegend=False
)

fig2.write_html(f'{CARPETA_GRAFICOS}/02_boxplot_categoria_interactivo.html')
print("   ✓ 02_boxplot_categoria_interactivo.html")

# ============================================================================
# 4. GRÁFICO 3: SERIE TEMPORAL INTERACTIVA
# ============================================================================
print("📊 GRÁFICO 3: Serie Temporal de Ventas")

ventas_mensuales = ventas_completas.groupby('mes').agg({
    'importe': 'sum',
    'id_venta': 'nunique',
    'cantidad': 'sum'
}).reset_index()

meses_nombres = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio'}
ventas_mensuales['mes_nombre'] = ventas_mensuales['mes'].map(meses_nombres)

fig3 = make_subplots(
    rows=2, cols=1,
    subplot_titles=('Evolución de Ventas Mensuales 2024', 'Cantidad de Transacciones por Mes'),
    vertical_spacing=0.12
)

# Gráfico superior: Ventas totales
fig3.add_trace(go.Scatter(
    x=ventas_mensuales['mes_nombre'],
    y=ventas_mensuales['importe'],
    mode='lines+markers',
    name='Ventas Mensuales',
    line=dict(color='steelblue', width=3),
    marker=dict(size=12),
    fill='tozeroy',
    hovertemplate='<b>%{x}</b><br>Ventas: $%{y:,.0f}<extra></extra>'
), row=1, col=1)

# Línea de promedio
promedio = ventas_mensuales['importe'].mean()
fig3.add_hline(y=promedio, line_dash="dash", line_color="red",
               annotation_text=f"Promedio: ${promedio:,.0f}",
               row=1, col=1)

# Gráfico inferior: Número de transacciones
fig3.add_trace(go.Bar(
    x=ventas_mensuales['mes_nombre'],
    y=ventas_mensuales['id_venta'],
    name='Transacciones',
    marker_color='coral',
    text=ventas_mensuales['id_venta'],
    textposition='outside',
    hovertemplate='<b>%{x}</b><br>Transacciones: %{y}<extra></extra>'
), row=2, col=1)

fig3.update_xaxes(title_text="Mes", row=2, col=1)
fig3.update_yaxes(title_text="Ventas Totales ($)", row=1, col=1)
fig3.update_yaxes(title_text="Número de Ventas", row=2, col=1)

fig3.update_layout(
    template='plotly_white',
    height=900,
    showlegend=False,
    hovermode='x unified'
)

fig3.write_html(f'{CARPETA_GRAFICOS}/03_serie_temporal_interactiva.html')
print("   ✓ 03_serie_temporal_interactiva.html")

# ============================================================================
# 5. GRÁFICO 4: HEATMAP INTERACTIVO DE CORRELACIONES
# ============================================================================
print("📊 GRÁFICO 4: Heatmap de Correlaciones")

datos_correlacion = ventas_completas[['cantidad', 'precio_unitario', 'importe', 'mes', 'dia_semana']].copy()
correlacion = datos_correlacion.corr()

fig4 = go.Figure(data=go.Heatmap(
    z=correlacion.values,
    x=correlacion.columns,
    y=correlacion.columns,
    colorscale='RdYlGn',
    zmid=0,
    text=correlacion.values,
    texttemplate='%{text:.3f}',
    textfont={"size": 12},
    hovertemplate='%{y} vs %{x}<br>Correlación: %{z:.3f}<extra></extra>',
    colorbar=dict(title="Correlación")
))

fig4.update_layout(
    title={
        'text': 'Matriz de Correlación de Variables Principales<br><sub>Pearson r - Identificar Relaciones Clave</sub>',
        'x': 0.5,
        'xanchor': 'center'
    },
    template='plotly_white',
    height=600,
    width=700
)

fig4.write_html(f'{CARPETA_GRAFICOS}/04_heatmap_correlaciones_interactivo.html')
print("   ✓ 04_heatmap_correlaciones_interactivo.html")

# ============================================================================
# 6. GRÁFICO 5: ANÁLISIS GEOGRÁFICO INTERACTIVO
# ============================================================================
print("📊 GRÁFICO 5: Análisis por Ciudad")

ventas_ciudad = ventas_completas.groupby('ciudad').agg({
    'importe': ['sum', 'mean', 'count'],
    'id_cliente': 'nunique'
}).reset_index()

ventas_ciudad.columns = ['ciudad', 'ventas_totales', 'ticket_promedio', 'num_transacciones', 'clientes_unicos']
ventas_ciudad = ventas_ciudad.sort_values('ventas_totales', ascending=True)

fig5 = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Ventas Totales por Ciudad', 'Ticket Promedio por Ciudad',
                    'Cantidad de Transacciones', 'Clientes Únicos'),
    specs=[[{"type": "bar"}, {"type": "bar"}],
           [{"type": "bar"}, {"type": "bar"}]]
)

# Ventas totales
fig5.add_trace(go.Bar(
    y=ventas_ciudad['ciudad'],
    x=ventas_ciudad['ventas_totales'],
    orientation='h',
    marker_color='lightblue',
    text=[f'${v:,.0f}' for v in ventas_ciudad['ventas_totales']],
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>Ventas: $%{x:,.0f}<extra></extra>'
), row=1, col=1)

# Ticket promedio
fig5.add_trace(go.Bar(
    y=ventas_ciudad['ciudad'],
    x=ventas_ciudad['ticket_promedio'],
    orientation='h',
    marker_color='coral',
    text=[f'${v:,.0f}' for v in ventas_ciudad['ticket_promedio']],
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>Ticket: $%{x:,.0f}<extra></extra>'
), row=1, col=2)

# Transacciones
fig5.add_trace(go.Bar(
    x=ventas_ciudad['ciudad'],
    y=ventas_ciudad['num_transacciones'],
    marker_color='lightgreen',
    text=ventas_ciudad['num_transacciones'],
    textposition='outside',
    hovertemplate='<b>%{x}</b><br>Transacciones: %{y}<extra></extra>'
), row=2, col=1)

# Clientes únicos
fig5.add_trace(go.Bar(
    x=ventas_ciudad['ciudad'],
    y=ventas_ciudad['clientes_unicos'],
    marker_color='gold',
    text=ventas_ciudad['clientes_unicos'],
    textposition='outside',
    hovertemplate='<b>%{x}</b><br>Clientes: %{y}<extra></extra>'
), row=2, col=2)

fig5.update_layout(
    title_text='Análisis Geográfico de Ventas - Identificar Oportunidades por Ciudad',
    template='plotly_white',
    height=900,
    showlegend=False
)

fig5.write_html(f'{CARPETA_GRAFICOS}/05_analisis_geografico_interactivo.html')
print("   ✓ 05_analisis_geografico_interactivo.html")

# ============================================================================
# 7. GRÁFICO 6: SCATTER PLOT INTERACTIVO - CANTIDAD VS IMPORTE
# ============================================================================
print("📊 GRÁFICO 6: Scatter Plot Cantidad vs Importe")

fig6 = px.scatter(
    ventas_completas,
    x='cantidad',
    y='importe',
    color='categoria',
    trendline='ols',
    title='Relación Cantidad vs Importe (Correlación r=0.89)<br><sub>Fuerte Relación Lineal - Aumentar Cantidad = Aumentar Ingresos</sub>',
    labels={'cantidad': 'Cantidad de Unidades', 'importe': 'Importe ($)', 'categoria': 'Categoría'},
    color_discrete_map={'Alimentos': 'green', 'Limpieza': 'blue'},
    hover_data={
        'cantidad': True,
        'importe': ':$,.0f',
        'nombre_producto': True,
        'categoria': True
    }
)

fig6.update_layout(
    template='plotly_white',
    height=700,
    hovermode='closest'
)

fig6.write_html(f'{CARPETA_GRAFICOS}/06_scatter_cantidad_importe_interactivo.html')
print("   ✓ 06_scatter_cantidad_importe_interactivo.html")

# ============================================================================
# 8. GRÁFICO 7: SUNBURST CHART - VENTAS POR CATEGORÍA Y PRODUCTO
# ============================================================================
print("📊 GRÁFICO 7: Sunburst Chart - Jerarquía de Ventas")

# Top 10 productos por categoría
top_productos_cat = ventas_completas.groupby(['categoria', 'nombre_producto']).agg({
    'importe': 'sum'
}).reset_index()

# Tomar top 10 de cada categoría
alimentos_top = top_productos_cat[top_productos_cat['categoria'] == 'Alimentos'].nlargest(10, 'importe')
limpieza_top = top_productos_cat[top_productos_cat['categoria'] == 'Limpieza'].nlargest(10, 'importe')
top_productos_final = pd.concat([alimentos_top, limpieza_top])

fig7 = px.sunburst(
    top_productos_final,
    path=['categoria', 'nombre_producto'],
    values='importe',
    title='Distribución de Ventas: Categorías y Top Productos<br><sub>Haz clic para explorar</sub>',
    color='importe',
    color_continuous_scale='Viridis',
    hover_data={'importe': ':$,.0f'}
)

fig7.update_layout(
    template='plotly_white',
    height=700
)

fig7.write_html(f'{CARPETA_GRAFICOS}/07_sunburst_ventas_interactivo.html')
print("   ✓ 07_sunburst_ventas_interactivo.html")

# ============================================================================
# 9. GRÁFICO 8: TREEMAP INTERACTIVO - MEDIO DE PAGO
# ============================================================================
print("📊 GRÁFICO 8: Treemap - Distribución por Medio de Pago")

ventas_medio_pago = ventas_completas.groupby('medio_pago').agg({
    'importe': 'sum'
}).reset_index()

fig8 = px.treemap(
    ventas_medio_pago,
    path=['medio_pago'],
    values='importe',
    title='Distribución de Ventas por Medio de Pago<br><sub>Tamaño representa volumen de ventas</sub>',
    color='importe',
    color_continuous_scale='Blues',
    hover_data={'importe': ':$,.0f'}
)

fig8.update_traces(
    texttemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percentParent}',
    textposition='middle center'
)

fig8.update_layout(
    template='plotly_white',
    height=600
)

fig8.write_html(f'{CARPETA_GRAFICOS}/08_treemap_medio_pago_interactivo.html')
print("   ✓ 08_treemap_medio_pago_interactivo.html")

# ============================================================================
# 10. GRÁFICO 9: VIOLIN PLOT - DISTRIBUCIÓN POR CATEGORÍA
# ============================================================================
print("📊 GRÁFICO 9: Violin Plot - Distribución Detallada")

fig9 = go.Figure()

for categoria in ['Alimentos', 'Limpieza']:
    datos_cat = ventas_completas[ventas_completas['categoria'] == categoria]['importe']
    
    fig9.add_trace(go.Violin(
        y=datos_cat,
        name=categoria,
        box_visible=True,
        meanline_visible=True,
        hovertemplate='<b>%{fullData.name}</b><br>Importe: $%{y:,.0f}<extra></extra>'
    ))

fig9.update_layout(
    title={
        'text': 'Distribución de Importes por Categoría (Violin Plot)<br><sub>Muestra densidad y dispersión completa</sub>',
        'x': 0.5,
        'xanchor': 'center'
    },
    yaxis_title='Importe ($)',
    xaxis_title='Categoría',
    template='plotly_white',
    height=600
)

fig9.write_html(f'{CARPETA_GRAFICOS}/09_violin_plot_categoria_interactivo.html')
print("   ✓ 09_violin_plot_categoria_interactivo.html")

# ============================================================================
# 11. GRÁFICO 10: DASHBOARD COMPARATIVO CATEGORÍAS
# ============================================================================
print("📊 GRÁFICO 10: Dashboard Comparativo Alimentos vs Limpieza")

categorias = ['Alimentos', 'Limpieza']
ventas_totales = [ventas_completas[ventas_completas['categoria'] == cat]['importe'].sum() for cat in categorias]
transacciones = [len(ventas_completas[ventas_completas['categoria'] == cat]) for cat in categorias]
tickets = [ventas_completas[ventas_completas['categoria'] == cat]['importe'].mean() for cat in categorias]
cantidades = [ventas_completas[ventas_completas['categoria'] == cat]['cantidad'].mean() for cat in categorias]

fig10 = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Ventas Totales', 'Cantidad de Transacciones',
                    'Ticket Promedio', 'Cantidad Promedio'),
    specs=[[{"type": "bar"}, {"type": "bar"}],
           [{"type": "bar"}, {"type": "bar"}]]
)

colors = ['green', 'blue']

# Ventas totales
fig10.add_trace(go.Bar(
    x=categorias,
    y=ventas_totales,
    marker_color=colors,
    text=[f'${v:,.0f}<br>({v/sum(ventas_totales)*100:.1f}%)' for v in ventas_totales],
    textposition='outside',
    hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>'
), row=1, col=1)

# Transacciones
fig10.add_trace(go.Bar(
    x=categorias,
    y=transacciones,
    marker_color=colors,
    text=[f'{v}<br>({v/sum(transacciones)*100:.1f}%)' for v in transacciones],
    textposition='outside',
    hovertemplate='<b>%{x}</b><br>%{y} transacciones<extra></extra>'
), row=1, col=2)

# Ticket promedio
fig10.add_trace(go.Bar(
    x=categorias,
    y=tickets,
    marker_color=colors,
    text=[f'${v:,.0f}' for v in tickets],
    textposition='outside',
    hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>'
), row=2, col=1)

# Cantidad promedio
fig10.add_trace(go.Bar(
    x=categorias,
    y=cantidades,
    marker_color=colors,
    text=[f'{v:.2f}' for v in cantidades],
    textposition='outside',
    hovertemplate='<b>%{x}</b><br>%{y:.2f} unidades<extra></extra>'
), row=2, col=2)

fig10.update_layout(
    title_text='Comparación Exhaustiva: Alimentos vs Limpieza',
    template='plotly_white',
    height=900,
    showlegend=False
)

fig10.write_html(f'{CARPETA_GRAFICOS}/10_dashboard_comparativo_interactivo.html')
print("   ✓ 10_dashboard_comparativo_interactivo.html")

# ============================================================================
# 12. RESUMEN FINAL
# ============================================================================
print("\n" + "="*80)
print("RESUMEN - FASE 3: VISUALIZACIÓN INTERACTIVA COMPLETADA")
print("="*80)

print("\n📊 GRÁFICOS INTERACTIVOS GENERADOS (10):")
print("-" * 80)
graficos = [
    "01_distribucion_importes_interactivo.html - Histograma con zoom",
    "02_boxplot_categoria_interactivo.html - Boxplot comparativo con detalles",
    "03_serie_temporal_interactiva.html - Evolución mensual con hover",
    "04_heatmap_correlaciones_interactivo.html - Matriz interactiva",
    "05_analisis_geografico_interactivo.html - Dashboard 4 subgráficos",
    "06_scatter_cantidad_importe_interactivo.html - Scatter con tendencia",
    "07_sunburst_ventas_interactivo.html - Jerarquía explorable",
    "08_treemap_medio_pago_interactivo.html - Distribución proporcional",
    "09_violin_plot_categoria_interactivo.html - Densidad detallada",
    "10_dashboard_comparativo_interactivo.html - Comparación exhaustiva"
]

for grafico in graficos:
    print(f"   ✓ {grafico}")

print("\n💡 VENTAJAS DE GRÁFICOS INTERACTIVOS:")
print("-" * 80)
print("   • Zoom y pan para explorar detalles")
print("   • Hover tooltips con información precisa")
print("   • Filtrado dinámico por categorías")
print("   • Exportación a PNG desde el navegador")
print("   • Gráficos responsivos (adaptables)")
print("   • Jerarquías explorables (Sunburst, Treemap)")

print("\n🔧 BIBLIOTECAS UTILIZADAS:")
print("   • Plotly Express: Gráficos rápidos de alto nivel")
print("   • Plotly Graph Objects: Control granular y layouts complejos")
print("   • Subplots: Dashboards con múltiples visualizaciones")

print("\n✓ FASE 3 INTERACTIVA COMPLETADA EXITOSAMENTE")
print("="*80)

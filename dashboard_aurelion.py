"""
DASHBOARD EJECUTIVO INTERACTIVO - TIENDA AURELION
Análisis Comercial con Streamlit

Instalación requerida:
pip install streamlit plotly pandas numpy

Ejecución:
streamlit run dashboard_aurelion.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import json

# ============================================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Dashboard Ejecutivo - Tienda Aurelion",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
    }
    .info-box {
        text-align: center;
        padding: 1.5rem;
        background-color: #ffffff;
        border-radius: 8px;
        border: 2px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .info-box p {
        font-size: 1.1rem;
        margin: 0.5rem 0;
        color: #2c3e50;
        font-weight: 600;
        line-height: 1.8;
    }
    .info-label {
        color: #1f77b4;
        font-weight: 700;
    }
    @media (max-width: 768px) {
        .info-box p {
            font-size: 0.95rem;
        }
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #2c3e50;
    }
    .metric-card h4 {
        color: #1f77b4;
        margin-top: 0;
        font-size: 1.2rem;
    }
    .metric-card ul {
        color: #2c3e50;
        line-height: 1.8;
    }
    @media (max-width: 768px) {
        .metric-card {
            padding: 1rem;
        }
        .metric-card h4 {
            font-size: 1rem;
        }
    }
    .problem-card {
        background-color: #fff8dc;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #ff8c00;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #2c3e50;
    }
    .problem-card h4 {
        color: #d35400;
        margin-top: 0;
        font-size: 1.2rem;
    }
    .problem-card ul {
        color: #2c3e50;
        line-height: 1.8;
        font-weight: 500;
    }
    @media (max-width: 768px) {
        .problem-card {
            padding: 1rem;
        }
    }
    .solution-card {
        background-color: #e8f8f5;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #27ae60;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #2c3e50;
    }
    .solution-card h4, .solution-card h5 {
        color: #27ae60;
        margin-top: 0;
        font-size: 1.2rem;
    }
    .solution-card ul {
        color: #2c3e50;
        line-height: 1.8;
        font-weight: 500;
    }
    .solution-card p {
        color: #2c3e50;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    @media (max-width: 768px) {
        .solution-card {
            padding: 1rem;
        }
        .solution-card h4 {
            font-size: 1rem;
        }
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        font-weight: bold;
    }
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 8px 12px;
            font-size: 0.85rem;
        }
    }
    .download-section {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 8px;
        border: 2px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNCIONES DE EXPORTACIÓN
# ============================================================================
def generar_resumen_texto(datos):
    """Genera un resumen ejecutivo en texto plano"""
    resumen = f"""
RESUMEN EJECUTIVO - TIENDA AURELION
Período: Enero - Junio 2024
Fecha de Generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*80}
MÉTRICAS PRINCIPALES
{'='*80}
Total Ventas:          ${datos['importe'].sum():,.0f}
Transacciones:         {datos['id_venta'].nunique():,}
Ticket Promedio:       ${datos['importe'].mean():,.0f}
Cantidad Promedio:     {datos['cantidad'].mean():.2f} unidades
Clientes Activos:      {datos['id_cliente'].nunique():,}

{'='*80}
PROBLEMAS CRÍTICOS
{'='*80}
1. Baja Frecuencia de Compra: 0.67 ventas/día
   - Pérdida estimada: $1,200,000 en 6 meses

2. Productos Sin Rotación: 5 productos con 0 ventas
   - Capital inmovilizado: ~$80,000

3. Categoría Limpieza Subdesarrollada: 24.7% vs 35-40% esperado
   - Oportunidad perdida: $400,000 en 6 meses

4. Tasa de Conversión Baja: 32% (objetivo 60%)
   - Ingresos adicionales potenciales: +$600,000

5. Alta Volatilidad: Caída de -37.5% en Abril
   - Dificulta planificación

6. 33% Clientes Inactivos
   - Potencial: $898,227

{'='*80}
SOLUCIONES PROPUESTAS
{'='*80}
1. Programa Fidelización:     Inversión $185K | ROI 1,157%
2. Optimización Surtido:      Inversión $390K | ROI 272%
3. Desarrollo Limpieza:       Inversión $155K | ROI 792%
4. Marketing Automation:      Inversión $150K | ROI 10,343%
5. Pricing & Promos:          Inversión $150K | ROI 1,340%
6. Expansión Geográfica:      Inversión $180K | ROI 756%

INVERSIÓN TOTAL:              $1,210,000
RETORNO PROYECTADO (70%):     $16,320,311
ROI TOTAL:                    1,349%

{'='*80}
QUICK WINS (IMPLEMENTAR YA)
{'='*80}
Día 1-7:    Campaña Reactivación VIP      → +$300K (ROI 2,000%)
Día 7-14:   Liquidación Productos         → +$120K (ROI 300%)
Día 14-30:  Lanzar Programa Fidelización  → +$450K (ROI 375%)
"""
    return resumen

def generar_datos_csv(datos):
    """Genera CSV con datos filtrados actuales"""
    return datos.to_csv(index=False).encode('utf-8')

def generar_metricas_json(datos):
    """Genera JSON con métricas principales"""
    metricas = {
        'fecha_generacion': datetime.now().isoformat(),
        'periodo': 'Enero-Junio 2024',
        'metricas_principales': {
            'total_ventas': float(datos['importe'].sum()),
            'transacciones': int(datos['id_venta'].nunique()),
            'ticket_promedio': float(datos['importe'].mean()),
            'cantidad_promedio': float(datos['cantidad'].mean()),
            'clientes_activos': int(datos['id_cliente'].nunique())
        },
        'por_categoria': {
            'alimentos': {
                'ventas': float(datos[datos['categoria']=='Alimentos']['importe'].sum()) if len(datos[datos['categoria']=='Alimentos']) > 0 else 0,
                'porcentaje': float(datos[datos['categoria']=='Alimentos']['importe'].sum() / datos['importe'].sum() * 100) if datos['importe'].sum() > 0 else 0
            },
            'limpieza': {
                'ventas': float(datos[datos['categoria']=='Limpieza']['importe'].sum()) if len(datos[datos['categoria']=='Limpieza']) > 0 else 0,
                'porcentaje': float(datos[datos['categoria']=='Limpieza']['importe'].sum() / datos['importe'].sum() * 100) if datos['importe'].sum() > 0 else 0
            }
        },
        'estrategias': {
            'inversion_total': 1210000,
            'retorno_proyectado': 16320311,
            'roi': 1349
        }
    }
    
    return json.dumps(metricas, indent=2, ensure_ascii=False).encode('utf-8')

def generar_reporte_html(datos):
    """Genera reporte HTML completo"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporte Tienda Aurelion</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
            .header {{ background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%); padding: 30px; border-radius: 10px; text-align: center; }}
            h1 {{ color: #1f77b4; margin: 0; }}
            .section {{ background-color: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .metric {{ display: inline-block; margin: 10px 20px; }}
            .metric-label {{ font-weight: bold; color: #1f77b4; }}
            .problem {{ background-color: #fff8dc; padding: 15px; margin: 10px 0; border-left: 5px solid #ff8c00; border-radius: 5px; }}
            .solution {{ background-color: #e8f8f5; padding: 15px; margin: 10px 0; border-left: 5px solid #27ae60; border-radius: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #1f77b4; color: white; }}
            @media (max-width: 768px) {{
                body {{ margin: 20px; }}
                .metric {{ display: block; margin: 10px 0; }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎯 REPORTE EJECUTIVO - TIENDA AURELION</h1>
            <p>Período: Enero - Junio 2024 | Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="section">
            <h2>📊 Métricas Principales</h2>
            <div class="metric">
                <span class="metric-label">Total Ventas:</span> ${datos['importe'].sum():,.0f}
            </div>
            <div class="metric">
                <span class="metric-label">Transacciones:</span> {datos['id_venta'].nunique():,}
            </div>
            <div class="metric">
                <span class="metric-label">Ticket Promedio:</span> ${datos['importe'].mean():,.0f}
            </div>
            <div class="metric">
                <span class="metric-label">Cantidad Promedio:</span> {datos['cantidad'].mean():.2f} unidades
            </div>
        </div>
        
        <div class="section">
            <h2>🔴 Problemas Críticos</h2>
            <div class="problem">
                <h3>1. Baja Frecuencia de Compra</h3>
                <p>Solo 0.67 ventas/día | Pérdida estimada: $1,200,000 en 6 meses</p>
            </div>
            <div class="problem">
                <h3>2. Productos Sin Rotación</h3>
                <p>5 productos con 0 ventas | Capital inmovilizado: ~$80,000</p>
            </div>
            <div class="problem">
                <h3>3. Categoría Limpieza Subdesarrollada</h3>
                <p>24.7% vs 35-40% esperado | Oportunidad: $400,000 en 6 meses</p>
            </div>
        </div>
        
        <div class="section">
            <h2>💡 Soluciones Propuestas</h2>
            <table>
                <tr>
                    <th>Estrategia</th>
                    <th>Inversión</th>
                    <th>Retorno 6M</th>
                    <th>ROI</th>
                </tr>
                <tr>
                    <td>Programa Fidelización</td>
                    <td>$185,000</td>
                    <td>$2,140,950</td>
                    <td>1,157%</td>
                </tr>
                <tr>
                    <td>Marketing Automation</td>
                    <td>$150,000</td>
                    <td>$15,514,830</td>
                    <td>10,343%</td>
                </tr>
                <tr>
                    <td>Pricing & Promos</td>
                    <td>$150,000</td>
                    <td>$2,010,000</td>
                    <td>1,340%</td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <h2>🎯 Quick Wins</h2>
            <div class="solution">
                <h3>Día 1-7: Campaña Reactivación VIP</h3>
                <p>Inversión: $15K | Retorno: +$300K | ROI: 2,000%</p>
            </div>
            <div class="solution">
                <h3>Día 7-14: Liquidación Productos</h3>
                <p>Inversión: $40K | Retorno: +$120K | ROI: 300%</p>
            </div>
            <div class="solution">
                <h3>Día 14-30: Lanzar Fidelización</h3>
                <p>Inversión: $120K | Retorno: +$450K | ROI: 375%</p>
            </div>
        </div>
        
        <div class="section" style="text-align: center; background-color: #1f77b4; color: white;">
            <h3>PROYECCIÓN TOTAL (70% cumplimiento)</h3>
            <p style="font-size: 1.2rem; margin: 10px 0;">
                <strong>Inversión:</strong> $1,210,000 | 
                <strong>Retorno:</strong> $16,320,311 | 
                <strong>ROI:</strong> 1,349%
            </p>
        </div>
    </body>
    </html>
    """
    return html.encode('utf-8')

# ============================================================================
# CARGA DE DATOS
# ============================================================================
@st.cache_data
def cargar_datos():
    """Carga y prepara todos los datos necesarios"""
    try:
        # Leer archivos
        clientes = pd.read_csv('datos_limpios/clientes_limpios.csv')
        productos = pd.read_csv('datos_limpios/productos_limpios.csv')
        ventas = pd.read_csv('datos_limpios/ventas_limpias.csv')
        detalle_ventas = pd.read_csv('datos_limpios/detalle_ventas_limpios.csv')
        calendario = pd.read_csv('datos_limpios/calendario.csv')
        
        # Convertir fechas
        ventas['fecha'] = pd.to_datetime(ventas['fecha'])
        calendario['fecha'] = pd.to_datetime(calendario['fecha'])
        clientes['fecha_alta'] = pd.to_datetime(clientes['fecha_alta'])
        
        # Dataset consolidado
        ventas_completas = detalle_ventas.merge(ventas, on='id_venta', how='left')
        productos_sin_precio = productos.drop('precio_unitario', axis=1)
        ventas_completas = ventas_completas.merge(productos_sin_precio, on='id_producto', how='left')
        ventas_completas = ventas_completas.merge(clientes[['id_cliente', 'ciudad']], on='id_cliente', how='left')
        ventas_completas = ventas_completas.merge(
            calendario[['fecha', 'anio', 'mes', 'dia_semana', 'nombre_dia', 'nombre_mes']], 
            on='fecha', how='left'
        )
        
        return clientes, productos, ventas, detalle_ventas, calendario, ventas_completas
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return None, None, None, None, None, None

clientes, productos, ventas, detalle_ventas, calendario, ventas_completas = cargar_datos()

if ventas_completas is None:
    st.error("⚠️ No se pudieron cargar los datos. Verifica que los archivos estén en la carpeta 'datos_limpios/'")
    st.stop()

# ============================================================================
# HEADER
# ============================================================================
st.markdown('<div class="main-header">🎯 DASHBOARD EJECUTIVO - TIENDA AURELION</div>', unsafe_allow_html=True)

# Caja de información con diseño responsive
st.markdown("""
<div class="info-box">
    <p>
        <span class="info-label">Período:</span> Enero - Junio 2024<br>
        <span class="info-label">Análisis:</span> 120 ventas, 431 líneas, 67 clientes activos
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SECCIÓN DE DESCARGA DE INFORMES
# ============================================================================
st.markdown("---")
st.markdown("""
<div class="download-section">
    <h3 style='color: #1f77b4; margin-top: 0;'>📥 DESCARGAR INFORMES</h3>
    <p style='color: #2c3e50; margin-bottom: 1rem;'>
        Exporta los datos y análisis en diferentes formatos según tus necesidades
    </p>
</div>
""", unsafe_allow_html=True)

col_d1, col_d2, col_d3, col_d4 = st.columns(4)

with col_d1:
    resumen_txt = generar_resumen_texto(datos_filtrados)
    st.download_button(
        label="📄 Resumen TXT",
        data=resumen_txt,
        file_name=f"resumen_aurelion_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        help="Descarga resumen ejecutivo en texto plano",
        use_container_width=True
    )

with col_d2:
    datos_csv = generar_datos_csv(datos_filtrados)
    st.download_button(
        label="📊 Datos CSV",
        data=datos_csv,
        file_name=f"datos_aurelion_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        help="Descarga datos filtrados en formato CSV",
        use_container_width=True
    )

with col_d3:
    metricas_json = generar_metricas_json(datos_filtrados)
    st.download_button(
        label="📋 Métricas JSON",
        data=metricas_json,
        file_name=f"metricas_aurelion_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json",
        help="Descarga métricas en formato JSON",
        use_container_width=True
    )

with col_d4:
    html_reporte = generar_reporte_html(datos_filtrados)
    st.download_button(
        label="📑 Reporte HTML",
        data=html_reporte,
        file_name=f"reporte_aurelion_{datetime.now().strftime('%Y%m%d')}.html",
        mime="text/html",
        help="Descarga reporte completo en HTML",
        use_container_width=True
    )

st.markdown("---")

# ============================================================================
# SIDEBAR - FILTROS
# ============================================================================
st.sidebar.header("🔍 FILTROS")

# Filtro por fecha
fecha_min = ventas_completas['fecha'].min()
fecha_max = ventas_completas['fecha'].max()
fecha_range = st.sidebar.date_input(
    "Rango de Fechas",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)

# Filtro por categoría
categorias_disponibles = ['Todas'] + list(ventas_completas['categoria'].unique())
categoria_filtro = st.sidebar.selectbox("Categoría", categorias_disponibles)

# Filtro por ciudad
ciudades_disponibles = ['Todas'] + list(ventas_completas['ciudad'].unique())
ciudad_filtro = st.sidebar.selectbox("Ciudad", ciudades_disponibles)

# Filtro por medio de pago
medios_pago = ['Todos'] + list(ventas_completas['medio_pago'].unique())
medio_pago_filtro = st.sidebar.selectbox("Medio de Pago", medios_pago)

# Aplicar filtros
datos_filtrados = ventas_completas.copy()

if len(fecha_range) == 2:
    datos_filtrados = datos_filtrados[
        (datos_filtrados['fecha'] >= pd.Timestamp(fecha_range[0])) &
        (datos_filtrados['fecha'] <= pd.Timestamp(fecha_range[1]))
    ]

if categoria_filtro != 'Todas':
    datos_filtrados = datos_filtrados[datos_filtrados['categoria'] == categoria_filtro]

if ciudad_filtro != 'Todas':
    datos_filtrados = datos_filtrados[datos_filtrados['ciudad'] == ciudad_filtro]

if medio_pago_filtro != 'Todos':
    datos_filtrados = datos_filtrados[datos_filtrados['medio_pago'] == medio_pago_filtro]

# Información de filtros aplicados
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Registros filtrados:** {len(datos_filtrados):,}")
st.sidebar.markdown(f"**Ventas totales:** ${datos_filtrados['importe'].sum():,.0f}")

# Botón de descarga rápida en sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Descarga Rápida")
resumen_sidebar = generar_resumen_texto(datos_filtrados)
st.sidebar.download_button(
    label="📄 Descargar Resumen",
    data=resumen_sidebar,
    file_name=f"resumen_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
    mime="text/plain",
    use_container_width=True
)

# ============================================================================
# TABS PRINCIPALES
# ============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 RESUMEN EJECUTIVO", 
    "🔴 PROBLEMAS CRÍTICOS", 
    "💡 SOLUCIONES", 
    "📈 ANÁLISIS DETALLADO",
    "🎯 PROYECCIÓN"
])

# ============================================================================
# TAB 1: RESUMEN EJECUTIVO
# ============================================================================
with tab1:
    st.header("📊 RESUMEN EJECUTIVO")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    total_ventas = datos_filtrados['importe'].sum()
    num_transacciones = datos_filtrados['id_venta'].nunique()
    ticket_promedio = datos_filtrados['importe'].mean()
    cantidad_promedio = datos_filtrados['cantidad'].mean()
    
    with col1:
        st.metric(
            label="💰 Ventas Totales",
            value=f"${total_ventas:,.0f}",
            delta=f"{(total_ventas/3266246 - 1)*100:.1f}% vs total"
        )
    
    with col2:
        st.metric(
            label="🛒 Transacciones",
            value=f"{num_transacciones:,}",
            delta=f"{num_transacciones - 120} vs total"
        )
    
    with col3:
        st.metric(
            label="🎫 Ticket Promedio",
            value=f"${ticket_promedio:,.0f}",
            delta=f"{(ticket_promedio/27219 - 1)*100:.1f}% vs media"
        )
    
    with col4:
        st.metric(
            label="📦 Cantidad Promedio",
            value=f"{cantidad_promedio:.1f} unidades",
            delta=f"{cantidad_promedio - 2.8:.1f} vs media"
        )
    
    st.markdown("---")
    
    # Gráficos principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Evolución Mensual de Ventas")
        
        ventas_mes = datos_filtrados.groupby('mes').agg({
            'importe': 'sum',
            'id_venta': 'nunique'
        }).reset_index()
        
        meses_nombres = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 
                        4: 'Abril', 5: 'Mayo', 6: 'Junio'}
        ventas_mes['mes_nombre'] = ventas_mes['mes'].map(meses_nombres)
        
        fig_serie = go.Figure()
        fig_serie.add_trace(go.Scatter(
            x=ventas_mes['mes_nombre'],
            y=ventas_mes['importe'],
            mode='lines+markers',
            name='Ventas',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=12),
            fill='tozeroy',
            hovertemplate='<b>%{x}</b><br>Ventas: $%{y:,.0f}<extra></extra>'
        ))
        
        promedio = ventas_mes['importe'].mean()
        fig_serie.add_hline(
            y=promedio, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"Promedio: ${promedio:,.0f}"
        )
        
        fig_serie.update_layout(
            height=400,
            template='plotly_white',
            hovermode='x unified',
            showlegend=False
        )
        
        st.plotly_chart(fig_serie, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Distribución por Categoría")
        
        ventas_categoria = datos_filtrados.groupby('categoria')['importe'].sum().reset_index()
        
        fig_pie = px.pie(
            ventas_categoria,
            values='importe',
            names='categoria',
            hole=0.4,
            color_discrete_map={'Alimentos': '#2ecc71', 'Limpieza': '#3498db'}
        )
        
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>'
        )
        
        fig_pie.update_layout(
            height=400,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1)
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Insights clave
    st.markdown("---")
    st.subheader("💡 INSIGHTS CLAVE")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>✅ Fortalezas</h4>
            <ul>
                <li><strong>Base de 100 clientes registrados</strong></li>
                <li><strong>Productos estrella identificados</strong></li>
                <li><strong>7 ciudades con presencia</strong></li>
                <li><strong>Mix de precios saludable</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="problem-card">
            <h4>⚠️ Problemas Críticos</h4>
            <ul>
                <li><strong>Frecuencia: 0.67 ventas/día</strong></li>
                <li><strong>33% clientes inactivos</strong></li>
                <li><strong>5 productos sin ventas</strong></li>
                <li><strong>Limpieza: 24.7% (vs 35-40%)</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="solution-card">
            <h4>🎯 Oportunidades</h4>
            <ul>
                <li><strong>Aumentar cantidad: 2.8 → 3.5</strong></li>
                <li><strong>Programa VIP para top 10%</strong></li>
                <li><strong>Desarrollar Limpieza +$400K</strong></li>
                <li><strong>Reactivar 33 clientes</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 2: PROBLEMAS CRÍTICOS
# ============================================================================
with tab2:
    st.header("🔴 PROBLEMAS CRÍTICOS DETECTADOS")
    
    # Selector de problema
    problema_seleccionado = st.selectbox(
        "Selecciona un problema para ver detalles:",
        [
            "1. Baja Frecuencia de Compra",
            "2. Productos Sin Rotación",
            "3. Categoría Limpieza Subdesarrollada",
            "4. Tasa de Conversión Baja",
            "5. Volatilidad en Ventas",
            "6. Clientes Inactivos"
        ]
    )
    
    if "Baja Frecuencia" in problema_seleccionado:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            ### 📉 PROBLEMA: Baja Frecuencia de Compra
            
            <div style='background-color: #fff8dc; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #ff8c00; color: #2c3e50;'>
            
            <h4 style='color: #d35400; margin-top: 0;'>Situación Actual:</h4>
            <ul style='color: #2c3e50; line-height: 1.8; font-weight: 500;'>
                <li>Solo <strong>0.67 ventas/día</strong> (120 ventas en 178 días)</li>
                <li><strong>58 días SIN VENTAS</strong> en 6 meses</li>
                <li>33% de clientes registrados <strong>NUNCA compraron</strong></li>
            </ul>
            
            <h4 style='color: #d35400;'>Impacto Financiero:</h4>
            <ul style='color: #2c3e50; line-height: 1.8; font-weight: 500;'>
                <li>Pérdida estimada: <strong>$1,200,000</strong> en 6 meses</li>
                <li>Si frecuencia fuera 2 ventas/día: <strong>+$2,400,000</strong></li>
            </ul>
            
            <h4 style='color: #d35400;'>Causas Probables:</h4>
            <ol style='color: #2c3e50; line-height: 1.8; font-weight: 500;'>
                <li>Sin programas de fidelización</li>
                <li>Falta de marketing recurrente</li>
                <li>Experiencia no memorable</li>
                <li>No hay incentivos para regresar</li>
            </ol>
            
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Gráfico de frecuencia
            ventas_diarias = datos_filtrados.groupby('fecha')['id_venta'].nunique().reset_index()
            ventas_diarias.columns = ['fecha', 'num_ventas']
            
            fig_freq = go.Figure()
            fig_freq.add_trace(go.Scatter(
                x=ventas_diarias['fecha'],
                y=ventas_diarias['num_ventas'],
                mode='lines+markers',
                name='Ventas Diarias',
                line=dict(color='#e74c3c', width=2),
                fill='tozeroy'
            ))
            
            fig_freq.add_hline(
                y=ventas_diarias['num_ventas'].mean(),
                line_dash="dash",
                line_color="green",
                annotation_text=f"Media: {ventas_diarias['num_ventas'].mean():.2f}"
            )
            
            fig_freq.update_layout(
                title="Frecuencia de Ventas Diarias",
                height=400,
                template='plotly_white'
            )
            
            st.plotly_chart(fig_freq, use_container_width=True)
    
    elif "Sin Rotación" in problema_seleccionado:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            ### 📦 PROBLEMA: Productos Sin Rotación
            
            <div style='background-color: #fff8dc; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #ff8c00; color: #2c3e50;'>
            
            <h4 style='color: #d35400; margin-top: 0;'>Situación Actual:</h4>
            <ul style='color: #2c3e50; line-height: 1.8; font-weight: 500;'>
                <li><strong>5 productos con 0 ventas</strong> en 6 meses</li>
                <li><strong>15 productos con &lt;5 ventas</strong> (rotación crítica)</li>
                <li>20% del inventario con bajo/nulo desempeño</li>
            </ul>
            
            <h4 style='color: #d35400;'>Impacto Financiero:</h4>
            <ul style='color: #2c3e50; line-height: 1.8; font-weight: 500;'>
                <li>Capital inmovilizado: <strong>~$80,000</strong></li>
                <li>Costo de oportunidad: <strong>$150,000</strong></li>
                <li>Riesgo de vencimiento: <strong>$30,000</strong></li>
            </ul>
            
            <h4 style='color: #d35400;'>Productos Críticos:</h4>
            <ul style='color: #2c3e50; line-height: 1.8; font-weight: 500;'>
                <li>❌ <strong>Suavizante 1L</strong> (0 ventas)</li>
                <li>❌ <strong>Esponjas x3</strong> (0 ventas)</li>
                <li>❌ <strong>Chupetín</strong> (0 ventas)</li>
                <li>❌ <strong>Sidra 750ml</strong> (0 ventas)</li>
                <li>❌ <strong>Licor de Café</strong> (0 ventas)</li>
            </ul>
            
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Gráfico productos sin rotación
            productos_ventas = datos_filtrados.groupby('nombre_producto')['cantidad'].sum().reset_index()
            productos_ventas = productos_ventas.sort_values('cantidad', ascending=True).head(15)
            
            fig_rot = px.bar(
                productos_ventas,
                x='cantidad',
                y='nombre_producto',
                orientation='h',
                title="15 Productos con Menor Rotación",
                color='cantidad',
                color_continuous_scale='Reds_r'
            )
            
            fig_rot.update_layout(
                height=500,
                template='plotly_white',
                showlegend=False
            )
            
            st.plotly_chart(fig_rot, use_container_width=True)
    
    elif "Limpieza" in problema_seleccionado:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            ### 🧹 PROBLEMA: Categoría Limpieza Subdesarrollada
            
            <div style='background-color: #fff8dc; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #ff8c00; color: #2c3e50;'>
            
            <h4 style='color: #d35400; margin-top: 0;'>Situación Actual:</h4>
            <ul style='color: #2c3e50; line-height: 1.8; font-weight: 500;'>
                <li>Solo <strong>24.7%</strong> de las ventas totales</li>
                <li>Benchmark de mercado: <strong>35-40%</strong> para retail</li>
                <li>Gap de performance: <strong>-10 puntos porcentuales</strong></li>
            </ul>
            
            <h4 style='color: #d35400;'>Impacto Financiero:</h4>
            <ul style='color: #2c3e50; line-height: 1.8; font-weight: 500;'>
                <li>Pérdida estimada: <strong>$400,000</strong> en 6 meses</li>
                <li>Proyección anual: <strong>$800,000</strong> de oportunidad</li>
            </ul>
            
            <h4 style='color: #d35400;'>Análisis:</h4>
            <ul style='color: #2c3e50; line-height: 1.8; font-weight: 500;'>
                <li>Tickets similares: <strong>$7,589</strong> (Alimentos) vs <strong>$7,544</strong> (Limpieza)</li>
                <li>Problema es de <strong>VOLUMEN</strong>, no de precio</li>
                <li><strong>324 transacciones</strong> (Alimentos) vs <strong>107</strong> (Limpieza)</li>
                <li>Ratio 3:1 cuando debería ser 2:1</li>
            </ul>
            
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Comparación categorías
            stats_cat = datos_filtrados.groupby('categoria').agg({
                'importe': ['sum', 'mean', 'count']
            }).reset_index()
            stats_cat.columns = ['categoria', 'total', 'promedio', 'transacciones']
            
            fig_cat = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Ventas Totales', 'Número de Transacciones'),
                specs=[[{"type": "bar"}, {"type": "bar"}]]
            )
            
            colors = ['#2ecc71', '#3498db']
            
            fig_cat.add_trace(
                go.Bar(x=stats_cat['categoria'], y=stats_cat['total'], 
                       marker_color=colors, name='Ventas'),
                row=1, col=1
            )
            
            fig_cat.add_trace(
                go.Bar(x=stats_cat['categoria'], y=stats_cat['transacciones'],
                       marker_color=colors, name='Transacciones'),
                row=1, col=2
            )
            
            fig_cat.update_layout(height=400, showlegend=False, template='plotly_white')
            st.plotly_chart(fig_cat, use_container_width=True)

# ============================================================================
# TAB 3: SOLUCIONES
# ============================================================================
with tab3:
    st.header("💡 SOLUCIONES Y ESTRATEGIAS ACCIONABLES")
    
    # Tabla resumen de estrategias
    estrategias = pd.DataFrame({
        'Estrategia': [
            '🎯 Programa Fidelización',
            '📦 Optimización Surtido',
            '🧹 Desarrollo Limpieza',
            '📱 Marketing Automation',
            '💰 Pricing & Promos',
            '🌍 Expansión Geográfica'
        ],
        'Inversión': [185000, 390000, 155000, 150000, 150000, 180000],
        'Retorno 6M': [2140950, 1060000, 1228000, 15514830, 2010000, 1360950],
        'ROI': ['1,157%', '272%', '792%', '10,343%', '1,340%', '756%'],
        'Prioridad': ['⭐⭐⭐', '⭐⭐⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐', '⭐']
    })
    
    st.dataframe(
        estrategias.style.background_gradient(subset=['Inversión', 'Retorno 6M'], cmap='RdYlGn'),
        use_container_width=True,
        height=300
    )
    
    st.markdown("---")
    
    # Selector de estrategia
    estrategia_seleccionada = st.selectbox(
        "Selecciona una estrategia para ver detalles:",
        estrategias['Estrategia'].tolist()
    )
    
    if "Fidelización" in estrategia_seleccionada:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div style='background-color: #e8f8f5; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #27ae60; color: #2c3e50;'>
            
            <h3 style='color: #27ae60; margin-top: 0;'>🎯 ESTRATEGIA 1: Programa de Fidelización</h3>
            
            <h4 style='color: #27ae60;'>Objetivo:</h4>
            <p style='color: #2c3e50; font-weight: 500;'>Aumentar frecuencia de 0.67 a 1.5 ventas/día (+124%)</p>
            
            <h4 style='color: #27ae60;'>Acciones:</h4>
            
            <h5 style='color: #27ae60;'>1. Club de Puntos "Aurelion Plus"</h5>
            <ul style='color: #2c3e50; line-height: 1.8; font-weight: 500;'>
                <li>$100 de compra = 1 punto</li>
                <li>100 puntos = $500 de descuento</li>
                <li>Puntos dobles en productos seleccionados</li>
                <li>Triple puntos día de cumpleaños</li>
            </ul>
            
            <h5 style='color: #27ae60;'>2. Campaña de Reactivación VIP</h5>
            <ul style='color: #2c3e50; line-height: 1.8; font-weight: 500;'>
                <li>WhatsApp personalizado con cupón 20% off</li>
                <li>Email con productos basados en historial</li>
                <li>Llamada telefónica (top 10)</li>
            </ul>
            
            <h5 style='color: #27ae60;'>3. Programa de Referidos</h5>
            <ul style='color: #2c3e50; line-height: 1.8; font-weight: 500;'>
                <li>Cliente referidor: $500 de descuento</li>
                <li>Cliente nuevo: $300 en 1ra compra</li>
                <li>Mínimo de compra: $2,000</li>
            </ul>
            
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background-color: #e8f8f5; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #27ae60; color: #2c3e50;'>
            
            <h3 style='color: #27ae60; margin-top: 0;'>📊 Proyección de Impacto</h3>
            
            </div>
            """, unsafe_allow_html=True)
            
            impacto_df = pd.DataFrame({
                'Métrica': ['Inversión', 'Retorno 6M', 'ROI', 'Nuevos Clientes', 'Frecuencia'],
                'Actual': ['$0', '$0', '0%', '0', '0.67/día'],
                'Proyectado': ['$185K', '$2.14M', '1,157%', '50+', '1.5/día']
            })
            
            st.dataframe(impacto_df, use_container_width=True)
            
            # Gráfico de proyección
            meses = ['Mes 1', 'Mes 2', 'Mes 3', 'Mes 4', 'Mes 5', 'Mes 6']
            ventas_actual = [544374] * 6
            ventas_proyectado = [650000, 750000, 900000, 1100000, 1400000, 1600000]
            
            fig_proj = go.Figure()
            fig_proj.add_trace(go.Scatter(
                x=meses, y=ventas_actual, name='Sin Estrategia',
                line=dict(color='red', dash='dash')
            ))
            fig_proj.add_trace(go.Scatter(
                x=meses, y=ventas_proyectado, name='Con Fidelización',
                line=dict(color='green'), fill='tonexty'
            ))
            
            fig_proj.update_layout(
                title="Proyección de Ventas",
                height=300,
                template='plotly_white'
            )
            
            st.plotly_chart(fig_proj, use_container_width=True)
    
    elif "Marketing" in estrategia_seleccionada:
        st.markdown("""
        <div style='background-color: #e8f8f5; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #27ae60; color: #2c3e50;'>
        
        <h3 style='color: #27ae60; margin-top: 0;'>📱 ESTRATEGIA 4: Marketing Automation</h3>
        
        <h4 style='color: #27ae60;'>Objetivo:</h4>
        <p style='color: #2c3e50; font-weight: 500;'>Aumentar frecuencia de contacto y conversión</p>
        
        </div>
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='background-color: #e8f8f5; padding: 1.2rem; border-radius: 8px; border-left: 5px solid #27ae60; color: #2c3e50;'>
            
            <h4 style='color: #27ae60; margin-top: 0;'>📲 WhatsApp Business</h4>
            
            <h5 style='color: #27ae60; font-size: 1rem;'>Campaña Bienvenida:</h5>
            <ul style='color: #2c3e50; line-height: 1.6; font-size: 0.95rem;'>
                <li>Día 0: Mensaje + cupón $300</li>
                <li>Día 3: Recordatorio</li>
                <li>Día 7: Recomendaciones</li>
            </ul>
            
            <h5 style='color: #27ae60; font-size: 1rem;'>Campaña Cumpleaños:</h5>
            <ul style='color: #2c3e50; line-height: 1.6; font-size: 0.95rem;'>
                <li>-7 días: Aviso</li>
                <li>Día 0: Cupón 25% off</li>
                <li>+7 días: Recordatorio</li>
            </ul>
            
            <p style='color: #2c3e50; font-weight: 600; margin: 0.8rem 0 0.3rem 0;'><strong>Inversión:</strong> $80K</p>
            <p style='color: #2c3e50; font-weight: 600; margin: 0.3rem 0;'><strong>Conversión:</strong> 25%</p>
            <p style='color: #2c3e50; font-weight: 600; margin: 0.3rem 0;'><strong>Retorno:</strong> $8.16M</p>
            
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background-color: #e8f8f5; padding: 1.2rem; border-radius: 8px; border-left: 5px solid #27ae60; color: #2c3e50;'>
            
            <h4 style='color: #27ae60; margin-top: 0;'>📧 Email Marketing</h4>
            
            <h5 style='color: #27ae60; font-size: 1rem;'>Segmentos:</h5>
            <ul style='color: #2c3e50; line-height: 1.6; font-size: 0.95rem;'>
                <li>VIP: Ofertas exclusivas</li>
                <li>Activos: Ofertas generales</li>
                <li>Inactivos: Reactivación</li>
                <li>Nuevos: Educación</li>
            </ul>
            
            <p style='color: #2c3e50; font-weight: 500; margin: 0.5rem 0;'><strong>Frecuencia:</strong> 2/semana</p>
            
            <p style='color: #2c3e50; font-weight: 600; margin: 0.8rem 0 0.3rem 0;'><strong>Inversión:</strong> $40K</p>
            <p style='color: #2c3e50; font-weight: 600; margin: 0.3rem 0;'><strong>Conversión:</strong> 8%</p>
            <p style='color: #2c3e50; font-weight: 600; margin: 0.3rem 0;'><strong>Retorno:</strong> $2.45M</p>
            
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background-color: #e8f8f5; padding: 1.2rem; border-radius: 8px; border-left: 5px solid #27ae60; color: #2c3e50;'>
            
            <h4 style='color: #27ae60; margin-top: 0;'>📍 Push Geográficas</h4>
            
            <h5 style='color: #27ae60; font-size: 1rem;'>Tácticas:</h5>
            <ul style='color: #2c3e50; line-height: 1.6; font-size: 0.95rem;'>
                <li>Cliente cerca: 10% off 1h</li>
                <li>21 días sin compra: Notif.</li>
                <li>Viernes 18-20h: "Prepara finde"</li>
            </ul>
            
            <p style='color: #2c3e50; font-weight: 600; margin: 0.8rem 0 0.3rem 0;'><strong>Inversión:</strong> $30K</p>
            <p style='color: #2c3e50; font-weight: 600; margin: 0.3rem 0;'><strong>Conversión:</strong> 15%</p>
            <p style='color: #2c3e50; font-weight: 600; margin: 0.3rem 0;'><strong>Retorno:</strong> $4.90M</p>
            
            <hr style='border: none; border-top: 2px solid #27ae60; margin: 1rem 0;'>
            
            <p style='color: #27ae60; font-weight: 700; font-size: 1.1rem; text-align: center; margin: 0.5rem 0;'>
            ROI TOTAL: 10,343%
            </p>
            
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# TAB 4: ANÁLISIS DETALLADO
# ============================================================================
with tab4:
    st.header("📈 ANÁLISIS DETALLADO")
    
    # Subtabs para diferentes análisis
    subtab1, subtab2, subtab3, subtab4 = st.tabs([
        "🎯 Por Categoría", 
        "🌍 Por Ciudad", 
        "💳 Medios de Pago",
        "⭐ Top Productos"
    ])
    
    with subtab1:
        st.subheader("Análisis por Categoría")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Boxplot por categoría
            fig_box = px.box(
                datos_filtrados,
                x='categoria',
                y='importe',
                color='categoria',
                title="Distribución de Importes por Categoría",
                color_discrete_map={'Alimentos': '#2ecc71', 'Limpieza': '#3498db'}
            )
            fig_box.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)
        
        with col2:
            # Estadísticas por categoría
            stats = datos_filtrados.groupby('categoria').agg({
                'importe': ['sum', 'mean', 'median', 'count'],
                'cantidad': 'mean'
            }).round(0)
            
            st.markdown("**Estadísticas Detalladas**")
            st.dataframe(stats, use_container_width=True)
    
    with subtab2:
        st.subheader("Análisis Geográfico")
        
        ventas_ciudad = datos_filtrados.groupby('ciudad').agg({
            'importe': ['sum', 'mean', 'count'],
            'id_cliente': 'nunique'
        }).reset_index()
        ventas_ciudad.columns = ['ciudad', 'total', 'ticket_prom', 'transacciones', 'clientes']
        ventas_ciudad = ventas_ciudad.sort_values('total', ascending=False)
        
        # Mapa de burbujas
        fig_geo = px.scatter(
            ventas_ciudad,
            x='transacciones',
            y='ticket_prom',
            size='total',
            color='ciudad',
            hover_data={'total': ':$,.0f', 'clientes': True},
            title="Análisis Comparativo por Ciudad (tamaño = ventas totales)"
        )
        fig_geo.update_layout(height=500, template='plotly_white')
        st.plotly_chart(fig_geo, use_container_width=True)
        
        # Tabla detallada
        st.markdown("**Detalle por Ciudad**")
        ventas_ciudad['total'] = ventas_ciudad['total'].apply(lambda x: f"${x:,.0f}")
        ventas_ciudad['ticket_prom'] = ventas_ciudad['ticket_prom'].apply(lambda x: f"${x:,.0f}")
        st.dataframe(ventas_ciudad, use_container_width=True)
    
    with subtab3:
        st.subheader("Análisis de Medios de Pago")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribución por medio de pago
            medio_pago_stats = datos_filtrados.groupby('medio_pago').agg({
                'importe': 'sum',
                'id_venta': 'count'
            }).reset_index()
            
            fig_medio = px.pie(
                medio_pago_stats,
                values='importe',
                names='medio_pago',
                title="Distribución de Ventas por Medio de Pago",
                hole=0.4
            )
            fig_medio.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_medio, use_container_width=True)
        
        with col2:
            # Evolución temporal por medio de pago
            evol_medio = datos_filtrados.groupby(['mes', 'medio_pago'])['importe'].sum().reset_index()
            meses_map = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun'}
            evol_medio['mes_nombre'] = evol_medio['mes'].map(meses_map)
            
            fig_evol = px.line(
                evol_medio,
                x='mes_nombre',
                y='importe',
                color='medio_pago',
                title="Evolución Mensual por Medio de Pago",
                markers=True
            )
            fig_evol.update_layout(height=400)
            st.plotly_chart(fig_evol, use_container_width=True)
    
    with subtab4:
        st.subheader("⭐ Top Productos")
        
        # Selector de métrica
        metrica_top = st.radio(
            "Ordenar por:",
            ["Ventas Totales ($)", "Unidades Vendidas", "Número de Transacciones"],
            horizontal=True
        )
        
        top_n = st.slider("Mostrar top:", 5, 20, 10)
        
        if metrica_top == "Ventas Totales ($)":
            top_productos = datos_filtrados.groupby('nombre_producto')['importe'].sum().nlargest(top_n).reset_index()
            y_col = 'importe'
            formato = '$:,.0f'
        elif metrica_top == "Unidades Vendidas":
            top_productos = datos_filtrados.groupby('nombre_producto')['cantidad'].sum().nlargest(top_n).reset_index()
            y_col = 'cantidad'
            formato = None
        else:
            top_productos = datos_filtrados.groupby('nombre_producto')['id_venta'].count().nlargest(top_n).reset_index()
            y_col = 'id_venta'
            formato = None
        
        top_productos = top_productos.sort_values(y_col, ascending=True)
        
        fig_top = px.bar(
            top_productos,
            x=y_col,
            y='nombre_producto',
            orientation='h',
            title=f"Top {top_n} Productos por {metrica_top}",
            color=y_col,
            color_continuous_scale='Viridis'
        )
        
        if formato:
            fig_top.update_traces(hovertemplate='<b>%{y}</b><br>Ventas: %{x' + formato + '}<extra></extra>')
        
        fig_top.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_top, use_container_width=True)

# ============================================================================
# TAB 5: PROYECCIÓN
# ============================================================================
with tab5:
    st.header("🎯 PROYECCIÓN DE IMPACTO")
    
    st.markdown("""
    ### 📊 Escenarios de Implementación
    
    Proyección de resultados según el nivel de cumplimiento de las estrategias propuestas:
    """)
    
    # Selector de escenario
    escenario = st.select_slider(
        "Selecciona el escenario de implementación:",
        options=['Conservador (50%)', 'Realista (70%)', 'Optimista (90%)'],
        value='Realista (70%)'
    )
    
    # Datos de proyección
    inversion_total = 1210000
    
    if 'Conservador' in escenario:
        factor = 0.5
        retorno = 11657365
        roi = 963
        crecimiento = 357
    elif 'Realista' in escenario:
        factor = 0.7
        retorno = 16320311
        roi = 1349
        crecimiento = 500
    else:
        factor = 0.9
        retorno = 20986400
        roi = 1734
        crecimiento = 643
    
    # Métricas del escenario
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Inversión Total", f"${inversion_total:,.0f}")
    
    with col2:
        st.metric("📈 Retorno 6 Meses", f"${retorno:,.0f}", delta=f"+${retorno-inversion_total:,.0f}")
    
    with col3:
        st.metric("🎯 ROI", f"{roi}%", delta="Excelente")
    
    with col4:
        st.metric("📊 Crecimiento", f"+{crecimiento}%", delta=f"vs actual")
    
    st.markdown("---")
    
    # Gráfico de proyección mensual
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Proyección de Ventas Mensuales")
        
        meses = ['Mes 1', 'Mes 2', 'Mes 3', 'Mes 4', 'Mes 5', 'Mes 6']
        ventas_actual = [544374] * 6
        ventas_proyectado = [
            544374 * (1 + 0.2*factor),
            544374 * (1 + 0.4*factor),
            544374 * (1 + 0.6*factor),
            544374 * (1 + 0.8*factor),
            544374 * (1 + 1.0*factor),
            544374 * (1 + 1.2*factor)
        ]
        
        fig_proj = go.Figure()
        
        fig_proj.add_trace(go.Scatter(
            x=meses,
            y=ventas_actual,
            name='Sin Estrategias',
            line=dict(color='red', dash='dash', width=2),
            mode='lines+markers'
        ))
        
        fig_proj.add_trace(go.Scatter(
            x=meses,
            y=ventas_proyectado,
            name=f'Con Estrategias ({escenario})',
            line=dict(color='green', width=3),
            mode='lines+markers',
            fill='tonexty',
            fillcolor='rgba(0, 255, 0, 0.1)'
        ))
        
        fig_proj.update_layout(
            height=400,
            template='plotly_white',
            hovermode='x unified',
            yaxis_title='Ventas ($)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        
        st.plotly_chart(fig_proj, use_container_width=True)
    
    with col2:
        st.subheader("Desglose de Inversión")
        
        inversiones = pd.DataFrame({
            'Estrategia': ['Fidelización', 'Surtido', 'Limpieza', 'Marketing', 'Pricing', 'Expansión'],
            'Inversión': [185000, 390000, 155000, 150000, 150000, 180000]
        })
        
        fig_inv = px.pie(
            inversiones,
            values='Inversión',
            names='Estrategia',
            hole=0.5
        )
        fig_inv.update_traces(textposition='inside', textinfo='percent')
        fig_inv.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig_inv, use_container_width=True)
    
    st.markdown("---")
    
    # Timeline de implementación
    st.subheader("📅 Timeline de Implementación (180 días)")
    
    timeline_data = {
        'Fase': ['Fase 1: Quick Wins', 'Fase 2: Consolidación', 'Fase 3: Expansión'],
        'Días': ['1-30', '31-90', '91-180'],
        'Inversión': ['$200K', '$580K', '$430K'],
        'Retorno Esperado': ['+$450K', '+$3.3M', '+$8.3M'],
        'Acciones Clave': [
            'Programa VIP, Liquidación, Capacitación',
            'Optimización Surtido, Bundles, Email Marketing',
            'Expansión Geográfica, Refinamiento, Escala'
        ]
    }
    
    timeline_df = pd.DataFrame(timeline_data)
    
    st.dataframe(
        timeline_df.style.set_properties(**{
            'background-color': '#f0f2f6',
            'color': 'black',
            'border-color': 'white'
        }),
        use_container_width=True,
        hide_index=True
    )
    
    # Quick Wins
    st.markdown("---")
    st.subheader("⚡ QUICK WINS (Implementar YA)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="solution-card">
            <h4 style='color: #27ae60; margin-top: 0; font-size: 1.3rem;'>📅 Día 1-7</h4>
            <h5 style='color: #27ae60; margin-top: 0.5rem; font-size: 1.1rem;'>Campaña Reactivación VIP</h5>
            <ul style='color: #2c3e50; line-height: 1.8; font-weight: 500;'>
                <li><strong>Contactar Top 20 clientes</strong></li>
                <li><strong>Cupón 20% off personalizado</strong></li>
                <li><strong>Seguimiento telefónico</strong></li>
            </ul>
            <p style='color: #2c3e50; font-weight: 700; font-size: 1rem; margin: 0.5rem 0;'><strong>Inversión:</strong> $15K</p>
            <p style='color: #2c3e50; font-weight: 700; font-size: 1rem; margin: 0.5rem 0;'><strong>Retorno:</strong> +$300K</p>
            <p style='color: #27ae60; font-weight: 700; font-size: 1.1rem; margin: 0.5rem 0;'><strong>ROI:</strong> 2,000%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="solution-card">
            <h4 style='color: #27ae60; margin-top: 0; font-size: 1.3rem;'>📅 Día 7-14</h4>
            <h5 style='color: #27ae60; margin-top: 0.5rem; font-size: 1.1rem;'>Liquidación Productos</h5>
            <ul style='color: #2c3e50; line-height: 1.8; font-weight: 500;'>
                <li><strong>Descuento 50% sin movimiento</strong></li>
                <li><strong>2x1 rotación lenta</strong></li>
                <li><strong>Degustaciones gratis</strong></li>
            </ul>
            <p style='color: #2c3e50; font-weight: 700; font-size: 1rem; margin: 0.5rem 0;'><strong>Inversión:</strong> $40K</p>
            <p style='color: #2c3e50; font-weight: 700; font-size: 1rem; margin: 0.5rem 0;'><strong>Retorno:</strong> +$120K</p>
            <p style='color: #27ae60; font-weight: 700; font-size: 1.1rem; margin: 0.5rem 0;'><strong>ROI:</strong> 300%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="solution-card">
            <h4 style='color: #27ae60; margin-top: 0; font-size: 1.3rem;'>📅 Día 14-30</h4>
            <h5 style='color: #27ae60; margin-top: 0.5rem; font-size: 1.1rem;'>Lanzar Fidelización</h5>
            <ul style='color: #2c3e50; line-height: 1.8; font-weight: 500;'>
                <li><strong>Club Aurelion Plus</strong></li>
                <li><strong>Sistema de puntos</strong></li>
                <li><strong>Beneficios inmediatos</strong></li>
            </ul>
            <p style='color: #2c3e50; font-weight: 700; font-size: 1rem; margin: 0.5rem 0;'><strong>Inversión:</strong> $120K</p>
            <p style='color: #2c3e50; font-weight: 700; font-size: 1rem; margin: 0.5rem 0;'><strong>Retorno:</strong> +$450K</p>
            <p style='color: #27ae60; font-weight: 700; font-size: 1.1rem; margin: 0.5rem 0;'><strong>ROI:</strong> 375%</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background-color: #ffffff; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #3498db; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
        <h3 style='color: #3498db; margin-top: 0; font-size: 1.3rem;'>📊 Sobre este Dashboard</h3>
        
        <p style='color: #2c3e50; line-height: 1.8; font-weight: 500; margin: 0.5rem 0;'>
        Dashboard ejecutivo interactivo para análisis comercial de Tienda Aurelion.
        </p>
        
        <p style='color: #2c3e50; line-height: 1.8; font-weight: 600; margin: 0.8rem 0 0.3rem 0;'>
        <strong>Período:</strong> Enero-Junio 2024
        </p>
        <p style='color: #2c3e50; line-height: 1.8; font-weight: 600; margin: 0.3rem 0;'>
        <strong>Datos:</strong> 431 líneas de venta
        </p>
        <p style='color: #2c3e50; line-height: 1.8; font-weight: 600; margin: 0.3rem 0;'>
        <strong>Clientes:</strong> 67 activos
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background-color: #ffffff; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #27ae60; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
        <h3 style='color: #27ae60; margin-top: 0; font-size: 1.3rem;'>🎯 Características</h3>
        
        <ul style='color: #2c3e50; line-height: 1.8; font-weight: 500; margin: 0.5rem 0;'>
            <li><strong>✅ Filtros dinámicos múltiples</strong></li>
            <li><strong>✅ Visualizaciones interactivas</strong></li>
            <li><strong>✅ Análisis en tiempo real</strong></li>
            <li><strong>✅ Proyecciones personalizadas</strong></li>
            <li><strong>✅ Insights accionables</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background-color: #ffffff; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #e74c3c; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
        <h3 style='color: #e74c3c; margin-top: 0; font-size: 1.3rem;'>📈 Próximos Pasos</h3>
        
        <ol style='color: #2c3e50; line-height: 1.8; font-weight: 500; margin: 0.5rem 0;'>
            <li><strong>Revisar problemas críticos</strong></li>
            <li><strong>Aprobar presupuesto ($1.21M)</strong></li>
            <li><strong>Implementar Quick Wins</strong></li>
            <li><strong>Seguimiento semanal de KPIs</strong></li>
            <li><strong>Ajustar según resultados</strong></li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1rem; background-color: #1f77b4; color: white; border-radius: 8px;'>
    <p style='margin: 0; font-size: 1.1rem;'>
        <strong>Dashboard creado con Streamlit y Plotly</strong><br>
        Análisis Comercial Tienda Aurelion | Octubre 2025
    </p>
</div>
""", unsafe_allow_html=True)
"""
DASHBOARD EJECUTIVO INTERACTIVO - TIENDA AURELION
Análisis Comercial con Streamlit

Instalación requerida:
pip install streamlit plotly pandas numpy

Ejecución:
streamlit run dashboard_completo.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import json
from scipy import stats

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
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        line-height: 1.3;
    }
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.8rem;
        }
    }
    .info-box {
        text-align: center;
        padding: 0.8rem 1rem;
        background-color: #ffffff;
        border-radius: 8px;
        border: 2px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0 auto 1rem auto;
        max-width: 600px;
    }
    .info-box p {
        font-size: 1.4rem;
        margin: 0.3rem 0;
        color: #2c3e50;
        font-weight: 600;
        line-height: 1.6;
    }
    .info-label {
        color: #1f77b4;
        font-weight: 700;
        font-size: 1.5rem;
    }
    @media (max-width: 768px) {
        .info-box p {
            font-size: 1.1rem;
        }
        .info-label {
            font-size: 1.2rem;
        }
    }
    .footer-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 100%;
    }
    .footer-card h3 {
        margin-top: 0;
        font-size: 1.4rem;
        margin-bottom: 1rem;
    }
    .footer-card p, .footer-card li {
        color: #2c3e50;
        line-height: 1.8;
        font-weight: 500;
        margin: 0.5rem 0;
        font-size: 1.05rem;
    }
    .footer-card strong {
        color: #1f77b4;
    }
    .card-azul {
        border-left: 5px solid #3498db;
    }
    .card-azul h3 {
        color: #3498db;
    }
    .card-verde {
        border-left: 5px solid #27ae60;
    }
    .card-verde h3 {
        color: #27ae60;
    }
    .card-rojo {
        border-left: 5px solid #e74c3c;
    }
    .card-rojo h3 {
        color: #e74c3c;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #2c3e50;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .metric-card h4 {
        color: #1f77b4;
        margin-top: 0;
        font-size: 1.2rem;
    }
    .metric-card ul {
        color: #2c3e50;
        line-height: 1.8;
        flex-grow: 1;
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
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        overflow-x: auto;
        white-space: nowrap;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 14px;
        font-weight: bold;
        font-size: 0.9rem;
        white-space: nowrap;
        flex-shrink: 0;
    }
    @media (max-width: 1024px) {
        .stTabs [data-baseweb="tab"] {
            padding: 8px 10px;
            font-size: 0.75rem;
        }
    }
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            padding: 6px 8px;
            font-size: 0.7rem;
        }
    }
    .download-section {
        background-color: #f0f8ff;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: 2px solid #1f77b4;
        margin: 1rem 0;
    }
    /* Responsive improvements */
    @media (max-width: 768px) {
        .stMetric {
            font-size: 0.9rem;
        }
        .stMetric label {
            font-size: 0.85rem;
        }
        .stMetric [data-testid="stMetricValue"] {
            font-size: 1.2rem;
        }
    }
    /* Ensure charts are responsive */
    .js-plotly-plot {
        width: 100% !important;
    }
    /* Column responsiveness */
    @media (max-width: 768px) {
        [data-testid="column"] {
            min-width: 100% !important;
            flex: 100% !important;
        }
    }
    /* Mobile optimizations */
    @media (max-width: 480px) {
        .main-header {
            font-size: 1.5rem;
            padding: 0.5rem;
        }
        .info-box {
            padding: 0.5rem;
            margin: 0.5rem auto;
        }
        .info-box p {
            font-size: 1rem;
        }
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
2. Productos Sin Rotación: 5 productos con 0 ventas
3. Categoría Limpieza Subdesarrollada: 24.7% vs 35-40%
4. Tasa de Conversión Baja: 32%
5. Alta Volatilidad: Caída de -37.5% en Abril
6. 33% Clientes Inactivos

{'='*80}
SOLUCIONES PROPUESTAS
{'='*80}
1. Programa Fidelización:     Inversión $185K | ROI 1,157%
2. Marketing Automation:      Inversión $150K | ROI 10,343%
3. Pricing & Promos:          Inversión $150K | ROI 1,340%

INVERSIÓN TOTAL:              $1,210,000
RETORNO PROYECTADO (70%):     $16,320,311
ROI TOTAL:                    1,349%
"""
    return resumen

def generar_datos_csv(datos):
    return datos.to_csv(index=False).encode('utf-8')

def generar_metricas_json(datos):
    metricas = {
        'fecha_generacion': datetime.now().isoformat(),
        'periodo': 'Enero-Junio 2024',
        'metricas_principales': {
            'total_ventas': float(datos['importe'].sum()),
            'transacciones': int(datos['id_venta'].nunique()),
            'ticket_promedio': float(datos['importe'].mean()),
            'cantidad_promedio': float(datos['cantidad'].mean()),
            'clientes_activos': int(datos['id_cliente'].nunique())
        }
    }
    return json.dumps(metricas, indent=2, ensure_ascii=False).encode('utf-8')

def generar_reporte_html(datos):
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>Reporte Aurelion</title></head>
    <body><h1>Reporte Tienda Aurelion</h1><p>Ventas: ${datos['importe'].sum():,.0f}</p></body></html>"""
    return html.encode('utf-8')

# ============================================================================
# CARGA DE DATOS
# ============================================================================
@st.cache_data
def cargar_datos():
    try:
        clientes = pd.read_csv('datos_limpios/clientes_limpios.csv')
        productos = pd.read_csv('datos_limpios/productos_limpios.csv')
        ventas = pd.read_csv('datos_limpios/ventas_limpias.csv')
        detalle_ventas = pd.read_csv('datos_limpios/detalle_ventas_limpios.csv')
        calendario = pd.read_csv('datos_limpios/calendario.csv')
        
        ventas['fecha'] = pd.to_datetime(ventas['fecha'])
        calendario['fecha'] = pd.to_datetime(calendario['fecha'])
        clientes['fecha_alta'] = pd.to_datetime(clientes['fecha_alta'])
        
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
    st.error("⚠️ No se pudieron cargar los datos")
    st.stop()

# ============================================================================
# HEADER
# ============================================================================
st.markdown('<div class="main-header">🎯 DASHBOARD EJECUTIVO<br>TIENDA AURELION</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <p>
        <span class="info-label">Período:</span> Enero - Junio 2024<br>
        <span class="info-label">Análisis:</span> 120 ventas, 431 líneas, 67 clientes activos
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# SIDEBAR - FILTROS
# ============================================================================

st.sidebar.header("🔍 FILTROS")

fecha_min = ventas_completas['fecha'].min()
fecha_max = ventas_completas['fecha'].max()

# Manejo de reset ANTES de instanciar widgets
if st.session_state.get('do_reset', False):
    st.session_state['fecha_range'] = (fecha_min, fecha_max)
    st.session_state['categoria_sel'] = 'Todas'
    st.session_state['ciudad_sel'] = 'Todas'
    st.session_state['medio_pago_sel'] = 'Todos'
    st.session_state['cmp_prev'] = True
    st.session_state['do_reset'] = False

fecha_range = st.sidebar.date_input(
    "Rango de Fechas",
    value=st.session_state.get('fecha_range', (fecha_min, fecha_max)),
    min_value=fecha_min,
    max_value=fecha_max,
    key='fecha_range'
)

categorias_disponibles = ['Todas'] + list(ventas_completas['categoria'].unique())
categoria_filtro = st.sidebar.selectbox("Categoría", categorias_disponibles, index=0, key='categoria_sel')

ciudades_disponibles = ['Todas'] + list(ventas_completas['ciudad'].unique())
ciudad_filtro = st.sidebar.selectbox("Ciudad", ciudades_disponibles, index=0, key='ciudad_sel')

medios_pago = ['Todos'] + list(ventas_completas['medio_pago'].unique())
medio_pago_filtro = st.sidebar.selectbox("Medio de Pago", medios_pago, index=0, key='medio_pago_sel')

# Comparación con período anterior y reset de filtros
comparar_prev = st.sidebar.checkbox("Comparar con período anterior", value=True, key='cmp_prev')
if st.sidebar.button("↩️ Reset filtros", use_container_width=True):
    st.session_state['do_reset'] = True
    st.rerun()

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

# Construir dataset del período anterior si corresponde
datos_prev = None
if 'cmp_prev' in st.session_state and st.session_state['cmp_prev'] and len(st.session_state.get('fecha_range', [])) == 2:
    _start = pd.Timestamp(st.session_state['fecha_range'][0])
    _end = pd.Timestamp(st.session_state['fecha_range'][1])
    if pd.notnull(_start) and pd.notnull(_end):
        _dur = (_end - _start).days + 1
        _prev_end = _start - pd.Timedelta(days=1)
        _prev_start = _prev_end - pd.Timedelta(days=_dur - 1)
        datos_prev = ventas_completas.copy()
        datos_prev = datos_prev[(datos_prev['fecha'] >= _prev_start) & (datos_prev['fecha'] <= _prev_end)]
        if categoria_filtro != 'Todas':
            datos_prev = datos_prev[datos_prev['categoria'] == categoria_filtro]
        if ciudad_filtro != 'Todas':
            datos_prev = datos_prev[datos_prev['ciudad'] == ciudad_filtro]
        if medio_pago_filtro != 'Todos':
            datos_prev = datos_prev[datos_prev['medio_pago'] == medio_pago_filtro]
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Registros filtrados:** {len(datos_filtrados):,}")
st.sidebar.markdown(f"**Ventas totales:** ${datos_filtrados['importe'].sum():,.0f}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 DESCARGA RÁPIDA")

resumen_sidebar = generar_resumen_texto(datos_filtrados)
st.sidebar.download_button(
    label="📄 Resumen TXT",
    data=resumen_sidebar,
    file_name=f"resumen_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
    mime="text/plain",
    use_container_width=True,
    key="download_resumen_sidebar"
)

st.sidebar.download_button(
    label="📊 Datos CSV",
    data=generar_datos_csv(datos_filtrados),
    file_name=f"datos_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
    use_container_width=True,
    key="download_csv_sidebar"
)

st.sidebar.download_button(
    label="📋 Métricas JSON",
    data=generar_metricas_json(datos_filtrados),
    file_name=f"metricas_{datetime.now().strftime('%Y%m%d')}.json",
    mime="application/json",
    use_container_width=True,
    key="download_json_sidebar"
)

st.sidebar.download_button(
    label="🔒 Reporte HTML",
    data=generar_reporte_html(datos_filtrados),
    file_name=f"reporte_{datetime.now().strftime('%Y%m%d')}.html",
    mime="text/html",
    use_container_width=True,
    key="download_html_sidebar"
)

# ============================================================================
# TABS PRINCIPALES
# ============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 RESUMEN",
    "🔴 PROBLEMAS", 
    "💡 SOLUCIONES",
    "📈 ANÁLISIS",
    "🎯 PROYECCIÓN"
])

# TAB 1: RESUMEN EJECUTIVO
with tab1:
    st.header("📊 RESUMEN EJECUTIVO")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_ventas = datos_filtrados['importe'].sum()
    num_transacciones = datos_filtrados['id_venta'].nunique()
    ticket_promedio = datos_filtrados['importe'].mean()
    cantidad_promedio = datos_filtrados['cantidad'].mean()

    prev_ventas = prev_trans = prev_ticket = prev_cantidad = None
    if datos_prev is not None and len(datos_prev) > 0:
        prev_ventas = datos_prev['importe'].sum()
        prev_trans = datos_prev['id_venta'].nunique()
        prev_ticket = datos_prev['importe'].mean()
        prev_cantidad = datos_prev['cantidad'].mean()

    def fmt_delta_pct(cur, prev):
        if prev is None or prev == 0 or pd.isna(prev):
            return "—"
        change = (cur - prev) / prev * 100
        return f"{change:+.1f}% vs período anterior"

    with col1:
        st.metric("💰 Ventas Totales", f"${total_ventas:,.0f}", 
                 delta=fmt_delta_pct(total_ventas, prev_ventas))
    
    with col2:
        st.metric("🛒 Transacciones", f"{num_transacciones:,}",
                 delta=fmt_delta_pct(num_transacciones, prev_trans))
    
    with col3:
        st.metric("🎫 Ticket Promedio", f"${ticket_promedio:,.0f}",
                 delta=fmt_delta_pct(ticket_promedio, prev_ticket))
    
    with col4:
        st.metric("📦 Cantidad Promedio", f"{cantidad_promedio:.1f} unidades",
                 delta=fmt_delta_pct(cantidad_promedio, prev_cantidad))

    st.markdown("---")
    col_alert1, col_alert2 = st.columns([2, 1])
    with col_alert1:
        st.subheader("🔔 Alertas Ejecutivas")
    with col_alert2:
        if datos_prev is None or len(datos_prev) == 0:
            st.info("💡 Activa 'Comparar con período anterior' en la barra lateral para ver alertas.")

    if datos_prev is not None and len(datos_prev) > 0:
        # Ventas
        if prev_ventas and total_ventas < prev_ventas:
            st.warning(f"📉 Ventas ↓ {((total_ventas - prev_ventas)/prev_ventas)*100:+.1f}% vs período anterior")
        elif prev_ventas:
            st.success(f"📈 Ventas ↑ {((total_ventas - prev_ventas)/prev_ventas)*100:+.1f}% vs período anterior")

        # Transacciones
        if prev_trans and num_transacciones < prev_trans:
            st.warning(f"🛒 Transacciones ↓ {((num_transacciones - prev_trans)/prev_trans)*100:+.1f}% vs período anterior")
        elif prev_trans:
            st.success(f"🛒 Transacciones ↑ {((num_transacciones - prev_trans)/prev_trans)*100:+.1f}% vs período anterior")

        # Ticket
        if prev_ticket and ticket_promedio < prev_ticket:
            st.info("🎫 Ticket promedio por debajo del período anterior")
        elif prev_ticket:
            st.success("🎫 Ticket promedio por encima del período anterior")

        # Cantidad por transacción
        if prev_cantidad and cantidad_promedio > prev_cantidad:
            st.success("📦 Mejora en unidades por transacción")
        elif prev_cantidad:
            st.info("📦 Unidades por transacción sin mejora significativa")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Evolución Mensual")
        
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
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=12),
            fill='tozeroy'
        ))
        
        promedio = ventas_mes['importe'].mean()
        fig_serie.add_hline(y=promedio, line_dash="dash", line_color="red",
                          annotation_text=f"Promedio: ${promedio:,.0f}")
        
        fig_serie.update_layout(height=400, template='plotly_white', showlegend=False)
        st.plotly_chart(fig_serie, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Distribución por Categoría")
        
        ventas_categoria = datos_filtrados.groupby('categoria')['importe'].sum().reset_index()
        
        # GRÁFICO CIRCULAR 3D
        fig_pie = px.pie(
            ventas_categoria,
            values='importe',
            names='categoria',
            hole=0.4,
            color_discrete_map={'Alimentos': '#2ecc71', 'Limpieza': '#3498db'}
        )
        
        # EFECTO 3D MEJORADO
        fig_pie.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            pull=[0.02, 0.02],
            marker=dict(
                line=dict(color='#ffffff', width=2),
                colors=['#2ecc71', '#3498db']
            )
        )
        
        fig_pie.update_layout(
            height=400,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            title="Distribución por Categoría - Vista 3D"
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")
    st.subheader("💡 INSIGHTS CLAVE")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: white; border-radius: 15px; padding: 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden; height: 100%;'>
            <div style='background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); padding: 1.2rem; text-align: center;'>
                <h3 style='color: white; margin: 0; font-size: 1.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>
                    ✅ FORTALEZAS
                </h3>
            </div>
            <div style='padding: 1.5rem;'>
                <p style='color: #2c3e50; font-size: 1.05rem; line-height: 2; margin: 0.5rem 0;'>
                    💪 <strong>Base de 100 clientes</strong>
                </p>
                <p style='color: #2c3e50; font-size: 1.05rem; line-height: 2; margin: 0.5rem 0;'>
                    ⭐ <strong>Productos estrella</strong>
                </p>
                <p style='color: #2c3e50; font-size: 1.05rem; line-height: 2; margin: 0.5rem 0;'>
                    🌏 <strong>7 ciudades</strong>
                </p>
                <p style='color: #2c3e50; font-size: 1.05rem; line-height: 2; margin: 0.5rem 0;'>
                    💰 <strong>Mix de precios saludable</strong>
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: white; border-radius: 15px; padding: 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden; height: 100%;'>
            <div style='background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); padding: 1.2rem; text-align: center;'>
                <h3 style='color: white; margin: 0; font-size: 1.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>
                    ⚠️ PROBLEMAS
                </h3>
            </div>
            <div style='padding: 1.5rem;'>
                <p style='color: #2c3e50; font-size: 1.05rem; line-height: 2; margin: 0.5rem 0;'>
                    📉 <strong>0.67 ventas/día</strong>
                </p>
                <p style='color: #2c3e50; font-size: 1.05rem; line-height: 2; margin: 0.5rem 0;'>
                    😴 <strong>33% inactivos</strong>
                </p>
                <p style='color: #2c3e50; font-size: 1.05rem; line-height: 2; margin: 0.5rem 0;'>
                    📦 <strong>5 sin ventas</strong>
                </p>
                <p style='color: #2c3e50; font-size: 1.05rem; line-height: 2; margin: 0.5rem 0;'>
                    🧹 <strong>Limpieza: 24.7%</strong>
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: white; border-radius: 15px; padding: 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden; height: 100%;'>
            <div style='background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); padding: 1.2rem; text-align: center;'>
                <h3 style='color: white; margin: 0; font-size: 1.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>
                    🎯 OPORTUNIDADES
                </h3>
            </div>
            <div style='padding: 1.5rem;'>
                <p style='color: #2c3e50; font-size: 1.05rem; line-height: 2; margin: 0.5rem 0;'>
                    📊 <strong>Cantidad: 2.8 → 3.5</strong>
                </p>
                <p style='color: #2c3e50; font-size: 1.05rem; line-height: 2; margin: 0.5rem 0;'>
                    💎 <strong>Programa VIP</strong>
                </p>
                <p style='color: #2c3e50; font-size: 1.05rem; line-height: 2; margin: 0.5rem 0;'>
                    💵 <strong>Limpieza +$400K</strong>
                </p>
                <p style='color: #2c3e50; font-size: 1.05rem; line-height: 2; margin: 0.5rem 0;'>
                    🔄 <strong>Reactivar 33</strong>
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# TAB 2: PROBLEMAS CRÍTICOS (EXPANDIDO)
with tab2:
    st.header("🔴 6 PROBLEMAS CRÍTICOS DETECTADOS")
    
    # Problema 1
    st.markdown("### 1️⃣ 📉 Baja Frecuencia de Compra")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Situación:** Solo 0.67 ventas/día (120 ventas en 178 días)
        
        **Impacto:** Pérdida de $1,200,000 en 6 meses
        
        **Causas:**
        - Sin programas de fidelización
        - Falta marketing recurrente
        - No hay incentivos para regresar
        
        **Acción:** Implementar programa de puntos y campaña de reactivación VIP
        """)
    with col2:
        fig_freq = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=0.67,
            delta={'reference': 2.0, 'increasing': {'color': "green"}},
            gauge={'axis': {'range': [None, 3]},
                   'bar': {'color': "red"},
                   'steps': [
                       {'range': [0, 1], 'color': "lightgray"},
                       {'range': [1, 2], 'color': "gray"}],
                   'threshold': {'line': {'color': "green", 'width': 4}, 'thickness': 0.75, 'value': 2}},
            title={'text': "Ventas/Día"}))
        fig_freq.update_layout(height=250)
        st.plotly_chart(fig_freq, use_container_width=True)
    
    st.markdown("---")
    
    # Problema 2
    st.markdown("### 2️⃣ 📦 Productos Sin Rotación")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Situación:** 5 productos con 0 ventas en 6 meses
        
        **Impacto:** Capital inmovilizado ~$80,000
        
        **Productos críticos:**
        - Suavizante 1L
        - Esponjas x3  
        - Chupetín
        - Sidra 750ml
        - Licor de Café
        
        **Acción:** Liquidación inmediata con descuentos 50%
        """)
    with col2:
        # Mostrar los 5 productos con menor rotación
        productos_rotacion = datos_filtrados.groupby('nombre_producto')['cantidad'].sum().reset_index()
        productos_rotacion = productos_rotacion.sort_values('cantidad', ascending=True).head(5)
        
        if len(productos_rotacion) > 0:
            fig_prod = go.Figure()
            
            # Agregar barras horizontales
            fig_prod.add_trace(go.Bar(
                y=productos_rotacion['nombre_producto'],
                x=productos_rotacion['cantidad'],
                orientation='h',
                marker=dict(
                    color=productos_rotacion['cantidad'],
                    colorscale='Reds',
                    showscale=False
                ),
                text=productos_rotacion['cantidad'],
                textposition='outside'
            ))
            
            fig_prod.update_layout(
                title='Top 5 Productos con Menor Rotación',
                xaxis_title='Unidades Vendidas',
                yaxis_title='',
                height=250,
                showlegend=False,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            
            st.plotly_chart(fig_prod, use_container_width=True)
        else:
            st.info("No hay datos de productos disponibles")
    
    st.markdown("---")
    
    # Problema 3
    st.markdown("### 3️⃣ 🧹 Categoría Limpieza Subdesarrollada")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Situación:** Solo 24.7% vs 35-40% esperado
        
        **Impacto:** Oportunidad perdida de $400,000 en 6 meses
        
        **Análisis:** Tickets similares ($7,589 vs $7,544) = problema de VOLUMEN
        
        **Acción:** Bundles, promoción cruzada, sampling
        """)
    with col2:
        fig_limpieza = go.Figure(go.Indicator(
            mode="gauge+number",
            value=24.7,
            gauge={'axis': {'range': [None, 50]},
                   'bar': {'color': "orange"},
                   'steps': [
                       {'range': [0, 30], 'color': "lightgray"},
                       {'range': [30, 40], 'color': "lightgreen"}],
                   'threshold': {'line': {'color': "green", 'width': 4}, 'thickness': 0.75, 'value': 35}},
            title={'text': "% Limpieza"}))
        fig_limpieza.update_layout(height=250)
        st.plotly_chart(fig_limpieza, use_container_width=True)
    
    st.markdown("---")
    
    # Problema 4
    st.markdown("### 4️⃣ 💳 Tasa de Conversión Baja")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Situación:** Solo 32% de conversión
        
        **Impacto:** Pérdida de 68 clientes potenciales cada 100 visitas
        
        **Causas:**
        - Falta de incentivos en primera compra
        - Proceso de compra complejo
        - Sin seguimiento post-visita
        
        **Acción:** Optimizar funnel de conversión y ofrecer descuento bienvenida
        """)
    with col2:
        fig_conv = go.Figure(go.Indicator(
            mode="gauge+number",
            value=32,
            gauge={'axis': {'range': [None, 100]},
                   'bar': {'color': "orange"},
                   'steps': [
                       {'range': [0, 50], 'color': "lightcoral"},
                       {'range': [50, 75], 'color': "lightyellow"},
                       {'range': [75, 100], 'color': "lightgreen"}],
                   'threshold': {'line': {'color': "green", 'width': 4}, 'thickness': 0.75, 'value': 60}},
            title={'text': "% Conversión"}))
        fig_conv.update_layout(height=250)
        st.plotly_chart(fig_conv, use_container_width=True)
    
    st.markdown("---")
    
    # Problema 5
    st.markdown("### 5️⃣ 📊 Alta Volatilidad en Ventas")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Situación:** Caída de -37.5% en Abril
        
        **Impacto:** Inestabilidad en flujo de caja y planificación
        
        **Causas:**
        - Dependencia de pocos clientes grandes
        - Sin estrategia de estabilización
        - Falta de promociones regulares
        
        **Acción:** Diversificar base de clientes y crear calendario promocional
        """)
    with col2:
        meses_vol = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
        variacion = [0, 15, -10, -37.5, 20, 8]
        fig_vol = go.Figure(data=[
            go.Bar(x=meses_vol, y=variacion, 
                   marker_color=['red' if v < 0 else 'green' for v in variacion])
        ])
        fig_vol.update_layout(height=250, title='Variación % Mensual', showlegend=False)
        st.plotly_chart(fig_vol, use_container_width=True)
    
    st.markdown("---")
    
    # Problema 6
    st.markdown("### 6️⃣ 😴 33% Clientes Inactivos")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Situación:** 33 de 100 clientes sin compras recientes
        
        **Impacto:** Pérdida potencial de $500,000 anuales
        
        **Causas:**
        - Sin programa de reactivación
        - Falta de comunicación post-compra
        - No hay incentivos de regreso
        
        **Acción:** Campaña de reactivación con ofertas personalizadas
        """)
    with col2:
        # GRÁFICO CIRCULAR 3D PARA CLIENTES INACTIVOS
        fig_inactivos = go.Figure(data=[
            go.Pie(
                labels=['Inactivos', 'Activos'], 
                values=[33, 67],
                hole=0.4,
                marker_colors=['#e74c3c', '#2ecc71'],
                pull=[0.05, 0],
                textinfo='percent+label',
                marker=dict(line=dict(color='#ffffff', width=2))
            )
        ])
        fig_inactivos.update_layout(
            height=250, 
            showlegend=True,
            title="Distribución de Clientes - Vista 3D"
        )
        st.plotly_chart(fig_inactivos, use_container_width=True)

# TAB 3: SOLUCIONES (EXPANDIDO)
with tab3:
    st.header("💡 SOLUCIONES Y ESTRATEGIAS")
    
    estrategias = pd.DataFrame({
        'Estrategia': ['🎯 Fidelización', '📦 Surtido', '🧹 Limpieza', 
                      '📱 Marketing', '💰 Pricing', '🌍 Expansión'],
        'Inversión': [185000, 390000, 155000, 150000, 150000, 180000],
        'Retorno': [2140950, 1060000, 1228000, 15514830, 2010000, 1360950],
        'ROI_num': [1157, 272, 792, 10343, 1340, 756],
        'ROI': ['1,157%', '272%', '792%', '10,343%', '1,340%', '756%'],
        'Prioridad': ['⭐⭐⭐', '⭐⭐⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐', '⭐']
    })
    
    st.dataframe(estrategias[['Estrategia', 'Inversión', 'Retorno', 'ROI', 'Prioridad']], 
                 use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Gráfico comparativo de ROI
    col1, col2 = st.columns(2)
    
    with col1:
        fig_roi = px.bar(estrategias, x='Estrategia', y='ROI_num',
                        title='Comparación de ROI por Estrategia',
                        labels={'ROI_num': 'ROI (%)', 'Estrategia': ''},
                        color='ROI_num',
                        color_continuous_scale='Viridis')
        fig_roi.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_roi, use_container_width=True)
    
    with col2:
        fig_inv = px.scatter(estrategias, x='Inversión', y='Retorno',
                            size='ROI_num', color='Estrategia',
                            title='Inversión vs Retorno',
                            labels={'Inversión': 'Inversión ($)', 'Retorno': 'Retorno ($)'},
                            hover_data=['ROI'])
        fig_inv.update_layout(height=400)
        st.plotly_chart(fig_inv, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📋 DETALLE DE ESTRATEGIAS")
    
    # Estrategia 1: Fidelización
    with st.expander("🎯 Programa de Fidelización - ROI: 1,157%", expanded=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            **Objetivo:** Aumentar frecuencia de 0.67 a 1.5 ventas/día
            
            **Acciones:**
            1. Club Aurelion Plus (sistema de puntos)
            2. Campaña reactivación VIP
            3. Programa de referidos
            
            **Inversión:** $185K | **Retorno:** $2.14M | **ROI:** 1,157%
            """)
        with col2:
            st.metric("Inversión", "$185K")
            st.metric("Retorno", "$2.14M", delta="+$1.96M")
            st.metric("ROI", "1,157%", delta="Excelente")
    
    # Estrategia 2: Marketing Automation
    with st.expander("📱 Marketing Automation - ROI: 10,343%", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **📲 WhatsApp**
            - Bienvenida automática
            - Felicitaciones cumpleaños
            - Reactivación 30 días
            
            **Inv:** $80K | **ROI:** 10,000%
            """)
        
        with col2:
            st.markdown("""
            **📧 Email Marketing**
            - Segmentado por perfil
            - 2 envíos/semana
            - 4 grupos objetivo
            
            **Inv:** $40K | **ROI:** 6,000%
            """)
        
        with col3:
            st.markdown("""
            **📍 Push Geolocalizado**
            - Cliente cerca tienda
            - Sin compra 21 días
            - Fines de semana
            
            **Inv:** $30K | **ROI:** 16,000%
            """)
    
    # Estrategia 3: Optimización Surtido
    with st.expander("📦 Optimización de Surtido - ROI: 272%"):
        st.markdown("""
        **Objetivo:** Eliminar productos sin rotación y agregar nuevos
        
        **Acciones:**
        1. Liquidar 5 productos sin ventas (descuento 50%)
        2. Incorporar 8 productos de alta demanda
        3. Ampliar categoría limpieza (+15 SKUs)
        
        **Inversión:** $390K | **Retorno:** $1.06M | **ROI:** 272%
        """)
    
    # Estrategia 4: Desarrollo Limpieza
    with st.expander("🧹 Desarrollo Categoría Limpieza - ROI: 792%"):
        st.markdown("""
        **Objetivo:** Aumentar participación de 24.7% a 35%
        
        **Acciones:**
        1. Bundles Alimentos + Limpieza (descuento 15%)
        2. Sampling gratuito productos nuevos
        3. Promoción cruzada en punto de venta
        
        **Inversión:** $155K | **Retorno:** $1.23M | **ROI:** 792%
        """)
    
    # Estrategia 5: Pricing Dinámico
    with st.expander("💰 Pricing y Promociones - ROI: 1,340%"):
        st.markdown("""
        **Objetivo:** Aumentar ticket promedio y frecuencia
        
        **Acciones:**
        1. Descuentos por volumen (3x2, 2x1)
        2. Happy hours (martes y jueves 15-18h)
        3. Precios dinámicos según stock
        
        **Inversión:** $150K | **Retorno:** $2.01M | **ROI:** 1,340%
        """)
    
    # Estrategia 6: Expansión Geográfica
    with st.expander("🌍 Expansión Geográfica - ROI: 756%"):
        st.markdown("""
        **Objetivo:** Captar nuevos clientes en ciudades sin presencia
        
        **Acciones:**
        1. Delivery en 3 ciudades nuevas
        2. Alianzas con comercios locales
        3. Campaña de lanzamiento digital
        
        **Inversión:** $180K | **Retorno:** $1.36M | **ROI:** 756%
        """)

# TAB 4: ANÁLISIS DETALLADO (EXPANDIDO)
with tab4:
    st.header("📈 ANÁLISIS DETALLADO")
    
    subtab1, subtab2, subtab3, subtab4, subtab5 = st.tabs(["🎯 Categoría", "🌏 Ciudad", "⭐ Productos", "👤 Cliente", "📅 Temporal"])
    
    with subtab1:
        st.subheader("Análisis por Categoría")
        
        # TABLA SOLA EN PRIMERA LÍNEA
        stats_cat = datos_filtrados.groupby('categoria').agg({
            'importe': ['sum', 'mean', 'count'],
            'cantidad': 'mean'
        }).round(0)
        st.dataframe(stats_cat, use_container_width=True)
        
        st.markdown("---")
        
        # SEGUNDA LÍNEA: DOS GRÁFICOS HORIZONTALES
        col1, col2 = st.columns(2)
        
        with col1:
            ventas_cat = datos_filtrados.groupby('categoria')['importe'].sum().reset_index()
            fig_cat_bar = px.bar(ventas_cat, x='categoria', y='importe',
                                title='Ventas Totales por Categoría',
                                color='categoria',
                                color_discrete_map={'Alimentos': '#2ecc71', 'Limpieza': '#3498db'})
            fig_cat_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_cat_bar, use_container_width=True)
        
        with col2:
            # Ticket promedio por categoría
            ticket_cat = datos_filtrados.groupby('categoria')['importe'].mean().reset_index()
            fig_ticket = px.bar(ticket_cat, x='categoria', y='importe',
                               title='Ticket Promedio por Categoría',
                               labels={'importe': 'Ticket Promedio ($)', 'categoria': 'Categoría'},
                               color='categoria',
                               color_discrete_map={'Alimentos': '#2ecc71', 'Limpieza': '#3498db'})
            st.plotly_chart(fig_ticket, use_container_width=True)
        
        # Análisis de ticket promedio por categoría
        st.markdown("---")
        
        # BoxPlot comparación de importes
        st.subheader("Comparación de Distribución de Importes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_boxplot = px.box(datos_filtrados, 
                                x='categoria', 
                                y='importe',
                                title='BoxPlot: Distribución de Importes por Categoría',
                                labels={'categoria': 'Categoría', 'importe': 'Importe ($)'},
                                color='categoria',
                                color_discrete_map={'Alimentos': '#2ecc71', 'Limpieza': '#3498db'})
            fig_boxplot.update_layout(showlegend=False)
            st.plotly_chart(fig_boxplot, use_container_width=True)
            
            # Mostrar estadísticas descriptivas
            st.markdown("**Estadísticas por Categoría:**")
            stats_box = datos_filtrados.groupby('categoria')['importe'].describe()[['mean', '50%', 'std', 'min', 'max']].round(2)
            stats_box.columns = ['Media', 'Mediana', 'Desv. Est.', 'Mínimo', 'Máximo']
            st.dataframe(stats_box, use_container_width=True)
        
        with col2:
            # Histograma con media y mediana MEJORADO
            fig_hist = go.Figure()

            # Histograma con bordes suaves
            fig_hist.add_trace(go.Histogram(
                x=datos_filtrados['importe'],
                nbinsx=30,
                name='Distribución',
                marker_color='#3498db',
                opacity=0.7,
                marker_line=dict(
                    color='#2c3e50',
                    width=1.5
                ),
                hovertemplate='<b>Rango:</b> %{x}<br><b>Frecuencia:</b> %{y}<extra></extra>'
            ))

            # Calcular estadísticas
            media = datos_filtrados['importe'].mean()
            mediana = datos_filtrados['importe'].median()

            # Línea de media
            fig_hist.add_vline(
                x=media, 
                line_dash="dash", 
                line_color="red", 
                annotation_text=f"Media: ${media:,.0f}",
                annotation_position="top right"
            )

            # Línea de mediana
            fig_hist.add_vline(
                x=mediana, 
                line_dash="dot", 
                line_color="green",
                annotation_text=f"Mediana: ${mediana:,.0f}",
                annotation_position="top left"
            )

            fig_hist.update_layout(
                title='Distribución de Importes por Línea de Venta',
                xaxis_title='Importe ($)',
                yaxis_title='Frecuencia',
                showlegend=False,
                height=400,
                bargap=0.05  # Espacio entre barras para mejor distinción
            )
            
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Calcular sesgo
            from scipy import stats
            sesgo = stats.skew(datos_filtrados['importe'])
            
            st.markdown("**Métricas de Distribución:**")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Media", f"${media:,.0f}")
            with col_b:
                st.metric("Mediana", f"${mediana:,.0f}")
            with col_c:
                interpretacion = "Sesgada derecha" if sesgo > 0.5 else "Sesgada izquierda" if sesgo < -0.5 else "Simétrica"
                st.metric("Sesgo", f"{sesgo:.2f}", delta=interpretacion)

    with subtab2:
        st.subheader("Análisis por Ciudad")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ventas_ciudad = datos_filtrados.groupby('ciudad').agg({
                'importe': ['sum', 'mean', 'count']
            }).round(0).sort_values(('importe', 'sum'), ascending=False)
            st.dataframe(ventas_ciudad, use_container_width=True)
        
        with col2:
            ciudad_ventas = datos_filtrados.groupby('ciudad')['importe'].sum().reset_index().sort_values('importe', ascending=True)
            fig_ciudad = px.bar(ciudad_ventas, x='importe', y='ciudad',
                               title='Ventas por Ciudad',
                               orientation='h',
                               color='importe',
                               color_continuous_scale='Blues')
            fig_ciudad.update_layout(showlegend=False)
            st.plotly_chart(fig_ciudad, use_container_width=True)
        
        # Mapa de calor: Ciudad vs Categoría
        st.markdown("---")
        st.subheader("Ventas por Ciudad y Categoría")
        heatmap_data = datos_filtrados.pivot_table(
            values='importe', 
            index='ciudad', 
            columns='categoria', 
            aggfunc='sum', 
            fill_value=0
        )
        fig_heat = px.imshow(heatmap_data,
                            labels=dict(x="Categoría", y="Ciudad", color="Ventas ($)"),
                            title="Mapa de Calor: Ventas por Ciudad y Categoría",
                            color_continuous_scale='YlOrRd')
        st.plotly_chart(fig_heat, use_container_width=True)
    
    with subtab3:
        st.subheader("Análisis de Productos")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Top 10 Productos por Ventas")
            top_prod = datos_filtrados.groupby('nombre_producto')['importe'].sum().nlargest(10).reset_index()
            fig_top = px.bar(top_prod, x='importe', y='nombre_producto',
                            orientation='h',
                            title='Top 10 Productos',
                            labels={'importe': 'Ventas ($)', 'nombre_producto': 'Producto'},
                            color='importe',
                            color_continuous_scale='Greens')
            fig_top.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_top, use_container_width=True)
        
        with col2:
            st.markdown("#### Top 10 Productos por Cantidad")
            top_cant = datos_filtrados.groupby('nombre_producto')['cantidad'].sum().nlargest(10).reset_index()
            fig_cant = px.bar(top_cant, x='cantidad', y='nombre_producto',
                             orientation='h',
                             title='Top 10 por Unidades',
                             labels={'cantidad': 'Unidades Vendidas', 'nombre_producto': 'Producto'},
                             color='cantidad',
                             color_continuous_scale='Oranges')
            fig_cant.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_cant, use_container_width=True)
        
        # Análisis de precio vs cantidad
        st.markdown("---")
        st.subheader("Relación Precio vs Cantidad Vendida")
        prod_analysis = datos_filtrados.groupby('nombre_producto').agg({
            'precio_unitario': 'mean',
            'cantidad': 'sum',
            'importe': 'sum'
        }).reset_index()
        
        fig_scatter = px.scatter(prod_analysis, x='precio_unitario', y='cantidad',
                                size='importe', color='importe',
                                hover_data=['nombre_producto'],
                                title='Análisis: Precio vs Cantidad (tamaño = ventas totales)',
                                labels={'precio_unitario': 'Precio Unitario ($)', 
                                       'cantidad': 'Cantidad Total Vendida'},
                                color_continuous_scale='Viridis')
        st.plotly_chart(fig_scatter, use_container_width=True)

    with subtab4:
        st.subheader("Análisis por Cliente")
        
        # Detectar columnas disponibles en clientes
        columnas_cliente = clientes.columns.tolist()
        
        # Intentar identificar columna de nombre
        if 'nombre_cliente' in columnas_cliente:
            nombre_col = 'nombre_cliente'
        elif 'nombre' in columnas_cliente:
            nombre_col = 'nombre'
        elif 'cliente' in columnas_cliente:
            nombre_col = 'cliente'
        else:
            nombre_col = None
        
        # Crear dataset con nombres de clientes si existe la columna
        if nombre_col:
            datos_con_nombres = datos_filtrados.merge(
                clientes[['id_cliente', nombre_col]], 
                on='id_cliente', 
                how='left'
            )
            datos_con_nombres['nombre_completo'] = datos_con_nombres[nombre_col]
        else:
            # Si no hay columna de nombre, usar ID como fallback
            datos_con_nombres = datos_filtrados.copy()
            datos_con_nombres['nombre_completo'] = 'Cliente ' + datos_con_nombres['id_cliente'].astype(str)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top 10 Clientes por Ventas")
            ventas_cliente = datos_con_nombres.groupby('nombre_completo').agg({
                'importe': 'sum',
                'id_venta': 'nunique',
                'cantidad': 'sum'
            }).reset_index()
            ventas_cliente.columns = ['Cliente', 'Total Ventas', 'Num Compras', 'Unidades']
            ventas_cliente = ventas_cliente.sort_values('Total Ventas', ascending=False).head(10)
            
            fig_cliente = px.bar(ventas_cliente, x='Total Ventas', y='Cliente',
                                orientation='h',
                                title='Top 10 Clientes',
                                labels={'Total Ventas': 'Ventas ($)', 'Cliente': 'Cliente'},
                                color='Total Ventas',
                                color_continuous_scale='Purples')
            fig_cliente.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_cliente, use_container_width=True)
        
        with col2:
            st.markdown("#### Top 10 Clientes por Frecuencia")
            ventas_freq = datos_con_nombres.groupby('nombre_completo').agg({
                'id_venta': 'nunique',
                'importe': 'sum'
            }).reset_index()
            ventas_freq.columns = ['Cliente', 'Num Compras', 'Total Ventas']
            ventas_freq = ventas_freq.sort_values('Num Compras', ascending=False).head(10)
            
            fig_freq_cliente = px.bar(ventas_freq, x='Num Compras', y='Cliente',
                                     orientation='h',
                                     title='Top 10 por Frecuencia',
                                     labels={'Num Compras': 'Número de Compras', 'Cliente': 'Cliente'},
                                     color='Num Compras',
                                     color_continuous_scale='Blues')
            fig_freq_cliente.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_freq_cliente, use_container_width=True)
        
        # Tabla resumen de clientes
        st.markdown("---")
        st.subheader("Resumen Estadístico por Cliente")
        
        stats_clientes = datos_con_nombres.groupby('nombre_completo').agg({
            'importe': ['sum', 'mean', 'count'],
            'cantidad': 'sum',
            'id_venta': 'nunique'
        }).round(0)
        stats_clientes.columns = ['Total Ventas', 'Ticket Promedio', 'Transacciones', 'Unidades', 'Compras']
        stats_clientes = stats_clientes.sort_values('Total Ventas', ascending=False).head(20)
        
        st.dataframe(stats_clientes, use_container_width=True)
        
        # Análisis de segmentación RFM simplificado
        st.markdown("---")
        st.subheader("Distribución de Clientes por Valor")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de dispersión: Frecuencia vs Valor
            cliente_analisis = datos_con_nombres.groupby('nombre_completo').agg({
                'importe': 'sum',
                'id_venta': 'nunique'
            }).reset_index()
            cliente_analisis.columns = ['Cliente', 'Total Ventas', 'Frecuencia']
            
            fig_scatter_cliente = px.scatter(cliente_analisis, 
                                            x='Frecuencia', 
                                            y='Total Ventas',
                                            size='Total Ventas',
                                            hover_data=['Cliente'],
                                            title='Frecuencia vs Valor del Cliente',
                                            labels={'Frecuencia': 'Número de Compras', 
                                                   'Total Ventas': 'Ventas Totales ($)'},
                                            color='Total Ventas',
                                            color_continuous_scale='Viridis')
            st.plotly_chart(fig_scatter_cliente, use_container_width=True)
        
        with col2:
            # Distribución por ciudad - GRÁFICO CIRCULAR 3D
            if 'ciudad' in datos_con_nombres.columns:
                ventas_ciudad_cliente = datos_con_nombres.groupby('ciudad').agg({
                    'nombre_completo': 'nunique',
                    'importe': 'sum'
                }).reset_index()
                ventas_ciudad_cliente.columns = ['Ciudad', 'Num Clientes', 'Total Ventas']
                
                fig_ciudad_pie = px.pie(
                    ventas_ciudad_cliente, 
                    values='Num Clientes', 
                    names='Ciudad',
                    title='Distribución de Clientes por Ciudad - Vista 3D',
                    hole=0.4
                )
                
                # EFECTO 3D
                fig_ciudad_pie.update_traces(
                    pull=[0.02] * len(ventas_ciudad_cliente),
                    marker=dict(line=dict(color='#ffffff', width=2))
                )
                
                st.plotly_chart(fig_ciudad_pie, use_container_width=True)

    with subtab5:
        st.subheader("Análisis Temporal")
        
        # Verificar que hay datos
        if len(datos_filtrados) == 0:
            st.warning("No hay datos disponibles para el análisis temporal con los filtros actuales.")
        else:
            # Ventas por día de la semana
            col1, col2 = st.columns(2)
            
            with col1:
                if 'nombre_dia' in datos_filtrados.columns:
                    ventas_dia = datos_filtrados.dropna(subset=['nombre_dia']).groupby('nombre_dia')['importe'].sum().reset_index()
                    
                    if len(ventas_dia) > 0:
                        # Traducir días de inglés a español
                        dias_traduccion = {
                            'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
                            'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
                        }
                        ventas_dia['dia_es'] = ventas_dia['nombre_dia'].map(dias_traduccion)
                        
                        # Ordenar días
                        dias_orden = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
                        ventas_dia['dia_es'] = pd.Categorical(ventas_dia['dia_es'], categories=dias_orden, ordered=True)
                        ventas_dia = ventas_dia.sort_values('dia_es').dropna(subset=['dia_es'])
                        
                        fig_dia = px.bar(ventas_dia, x='dia_es', y='importe',
                                        title='Ventas por Día de la Semana',
                                        labels={'dia_es': 'Día', 'importe': 'Ventas ($)'},
                                        color='importe',
                                        color_continuous_scale='Blues')
                        fig_dia.update_layout(showlegend=False)
                        st.plotly_chart(fig_dia, use_container_width=True)
                    else:
                        st.info("No hay datos de días de la semana disponibles.")
                else:
                    st.warning("Columna 'nombre_dia' no disponible en los datos.")
            
            with col2:
                if 'nombre_mes' in datos_filtrados.columns:
                    ventas_mes_nombre = datos_filtrados.dropna(subset=['nombre_mes']).groupby('nombre_mes')['importe'].sum().reset_index()
                    
                    if len(ventas_mes_nombre) > 0:
                        # Traducir meses de inglés a español
                        meses_traduccion = {
                            'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo',
                            'April': 'Abril', 'May': 'Mayo', 'June': 'Junio',
                            'July': 'Julio', 'August': 'Agosto', 'September': 'Septiembre',
                            'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
                        }
                        ventas_mes_nombre['mes_es'] = ventas_mes_nombre['nombre_mes'].map(meses_traduccion)
                        
                        # Ordenar meses
                        meses_orden = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                                      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
                        ventas_mes_nombre['mes_es'] = pd.Categorical(ventas_mes_nombre['mes_es'], 
                                                                     categories=meses_orden, ordered=True)
                        ventas_mes_nombre = ventas_mes_nombre.sort_values('mes_es').dropna(subset=['mes_es'])
                        
                        fig_mes = px.line(ventas_mes_nombre, x='mes_es', y='importe',
                                         title='Tendencia Mensual',
                                         labels={'mes_es': 'Mes', 'importe': 'Ventas ($)'},
                                         markers=True)
                        fig_mes.update_traces(line_color='#e74c3c', line_width=3, marker_size=10)
                        st.plotly_chart(fig_mes, use_container_width=True)
                    else:
                        st.info("No hay datos mensuales disponibles.")
                else:
                    st.warning("Columna 'nombre_mes' no disponible en los datos.")
            
            # Análisis de medios de pago
            st.markdown("---")
            st.subheader("Análisis de Medios de Pago")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if 'medio_pago' in datos_filtrados.columns:
                    medio_pago_ventas = datos_filtrados.dropna(subset=['medio_pago']).groupby('medio_pago')['importe'].sum().reset_index()
                    
                    if len(medio_pago_ventas) > 0:
                        # GRÁFICO CIRCULAR 3D PARA MEDIOS DE PAGO
                        fig_pago = px.pie(
                            medio_pago_ventas, 
                            values='importe', 
                            names='medio_pago',
                            title='Distribución por Medio de Pago - Vista 3D',
                            hole=0.4
                        )
                        
                        # EFECTO 3D
                        fig_pago.update_traces(
                            pull=[0.02] * len(medio_pago_ventas),
                            marker=dict(line=dict(color='#ffffff', width=2))
                        )
                        
                        st.plotly_chart(fig_pago, use_container_width=True)
                    else:
                        st.info("No hay datos de medios de pago disponibles.")
                else:
                    st.warning("Columna 'medio_pago' no disponible en los datos.")
            
            with col2:
                if 'medio_pago' in datos_filtrados.columns:
                    medio_pago_stats = datos_filtrados.dropna(subset=['medio_pago']).groupby('medio_pago').agg({
                        'importe': ['sum', 'mean', 'count']
                    }).round(0)
                    
                    if len(medio_pago_stats) > 0:
                        st.dataframe(medio_pago_stats, use_container_width=True)
                    else:
                        st.info("No hay estadísticas de medios de pago disponibles.")
                else:
                    st.warning("Columna 'medio_pago' no disponible en los datos.")

# TAB 5: PROYECCIÓN (EXPANDIDO)
with tab5:
    st.header("🎯 PROYECCIÓN DE IMPACTO")
    
    escenario = st.select_slider(
        "Selecciona el Escenario de Implementación:",
        options=['Conservador (50%)', 'Realista (70%)', 'Optimista (90%)'],
        value='Realista (70%)'
    )
    
    if 'Conservador' in escenario:
        factor, retorno, roi = 0.5, 11657365, 963
    elif 'Realista' in escenario:
        factor, retorno, roi = 0.7, 16320311, 1349
    else:
        factor, retorno, roi = 0.9, 20986400, 1734
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Inversión Total", "$1,210,000")
    
    with col2:
        st.metric("📈 Retorno 6M", f"${retorno:,.0f}", 
                 delta=f"+${retorno-1210000:,.0f}")
    
    with col3:
        st.metric("🎯 ROI", f"{roi}%", delta="Excelente")
    
    with col4:
        st.metric("📊 Crecimiento", f"+{int(factor*500)}%")
    
    st.markdown("---")
    
    # Comparación de escenarios
    st.subheader("📊 Comparación de Escenarios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de proyección
        meses = ['Mes 1', 'Mes 2', 'Mes 3', 'Mes 4', 'Mes 5', 'Mes 6']
        base = 544374
        ventas_actual = [base] * 6
        ventas_conservador = [base * (1 + 0.2*i*0.5) for i in range(1, 7)]
        ventas_realista = [base * (1 + 0.2*i*0.7) for i in range(1, 7)]
        ventas_optimista = [base * (1 + 0.2*i*0.9) for i in range(1, 7)]
        
        fig_proj = go.Figure()
        
        fig_proj.add_trace(go.Scatter(
            x=meses, y=ventas_actual,
            name='Sin Estrategias',
            line=dict(color='red', dash='dash', width=2)
        ))
        
        fig_proj.add_trace(go.Scatter(
            x=meses, y=ventas_conservador,
            name='Conservador (50%)',
            line=dict(color='orange', width=2)
        ))
        
        fig_proj.add_trace(go.Scatter(
            x=meses, y=ventas_realista,
            name='Realista (70%)',
            line=dict(color='green', width=3)
        ))
        
        fig_proj.add_trace(go.Scatter(
            x=meses, y=ventas_optimista,
            name='Optimista (90%)',
            line=dict(color='blue', width=2)
        ))
        
        fig_proj.update_layout(
            height=400,
            template='plotly_white',
            hovermode='x unified',
            yaxis_title='Ventas ($)',
            title='Proyección de Ventas por Escenario',
            legend=dict(orientation="h", yanchor="bottom", y=-0.3)
        )
        
        st.plotly_chart(fig_proj, use_container_width=True)
    
    with col2:
        # Comparación ROI
        escenarios_df = pd.DataFrame({
            'Escenario': ['Conservador', 'Realista', 'Optimista'],
            'Inversión': [1210000, 1210000, 1210000],
            'Retorno': [11657365, 16320311, 20986400],
            'ROI': [963, 1349, 1734]
        })
        
        fig_roi_comp = go.Figure()
        
        fig_roi_comp.add_trace(go.Bar(
            name='Inversión',
            x=escenarios_df['Escenario'],
            y=escenarios_df['Inversión'],
            marker_color='lightcoral'
        ))
        
        fig_roi_comp.add_trace(go.Bar(
            name='Retorno',
            x=escenarios_df['Escenario'],
            y=escenarios_df['Retorno'],
            marker_color='lightgreen'
        ))
        
        fig_roi_comp.update_layout(
            height=400,
            barmode='group',
            title='Inversión vs Retorno por Escenario',
            yaxis_title='Monto ($)',
            legend=dict(orientation="h", yanchor="bottom", y=-0.3)
        )
        
        st.plotly_chart(fig_roi_comp, use_container_width=True)
    
    st.markdown("---")
    
    # Timeline de implementación
    st.subheader("📅 TIMELINE DE IMPLEMENTACIÓN")
    
    timeline_data = pd.DataFrame({
        'Fase': ['Fase 1', 'Fase 2', 'Fase 3', 'Fase 4'],
        'Inicio': ['Día 1', 'Día 8', 'Día 15', 'Día 30'],
        'Fin': ['Día 7', 'Día 14', 'Día 30', 'Día 90'],
        'Actividades': [
            'Reactivación VIP + Análisis inicial',
            'Liquidación productos + Setup fidelización',
            'Lanzamiento Club Aurelion + Marketing',
            'Optimización continua + Expansión'
        ],
        'Inversión': ['$15K', '$40K', '$120K', '$1,035K'],
        'Retorno Esperado': ['$300K', '$120K', '$450K', '$15.5M']
    })
    
    st.dataframe(timeline_data, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("⚡ QUICK WINS (Implementar YA)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📅 Día 1-7")
        st.markdown("**Reactivación VIP**")
        st.write("✅ Top 20 clientes")
        st.write("✅ Cupón 20% off")
        st.write("✅ Seguimiento telefónico")
        st.metric("Inversión", "$15K")
        st.metric("Retorno", "+$300K", delta="ROI: 2,000%")
    
    with col2:
        st.markdown("#### 📅 Día 7-14")
        st.markdown("**Liquidación Productos**")
        st.write("✅ Descuento 50%")
        st.write("✅ 2x1 rotación lenta")
        st.write("✅ Degustaciones gratis")
        st.metric("Inversión", "$40K")
        st.metric("Retorno", "+$120K", delta="ROI: 300%")
    
    with col3:
        st.markdown("#### 📅 Día 14-30")
        st.markdown("**Lanzar Fidelización**")
        st.write("✅ Club Aurelion Plus")
        st.write("✅ Sistema de puntos")
        st.write("✅ Beneficios inmediatos")
        st.metric("Inversión", "$120K")
        st.metric("Retorno", "+$450K", delta="ROI: 375%")
    
    st.markdown("---")
    
    # KPIs a monitorear
    st.subheader("📊 KPIs CLAVE A MONITOREAR")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**📈 Ventas**")
        st.write("• Ventas diarias")
        st.write("• Ticket promedio")
        st.write("• Unidades/transacción")
    
    with col2:
        st.markdown("**👥 Clientes**")
        st.write("• Frecuencia compra")
        st.write("• Tasa retención")
        st.write("• Clientes nuevos")
    
    with col3:
        st.markdown("**📦 Productos**")
        st.write("• Rotación inventario")
        st.write("• Mix categorías")
        st.write("• Productos top")
    
    with col4:
        st.markdown("**💰 Rentabilidad**")
        st.write("• Margen bruto")
        st.write("• ROI campañas")
        st.write("• Costo adquisición")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background-color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 100%;'>
        <h3 style='color: #1f77b4; margin-top: 0;'>📊 Sobre este Dashboard</h3>
        <p style='color: #2c3e50; line-height: 1.8;'>Dashboard ejecutivo interactivo para análisis comercial de Tienda Aurelion.</p>
        <p style='color: #2c3e50;'><strong>Período:</strong> Enero-Junio 2024</p>
        <p style='color: #2c3e50;'><strong>Datos:</strong> 431 líneas de venta</p>
        <p style='color: #2c3e50;'><strong>Clientes:</strong> 67 activos</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background-color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 100%;'>
        <h3 style='color: #27ae60; margin-top: 0;'>🎯 Características</h3>
        <p style='color: #2c3e50; line-height: 1.8;'>✅ Filtros dinámicos múltiples</p>
        <p style='color: #2c3e50; line-height: 1.8;'>✅ Visualizaciones interactivas</p>
        <p style='color: #2c3e50; line-height: 1.8;'>✅ Análisis en tiempo real</p>
        <p style='color: #2c3e50; line-height: 1.8;'>✅ Proyecciones personalizadas</p>
        <p style='color: #2c3e50; line-height: 1.8;'>✅ Insights accionables</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background-color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 100%;'>
        <h3 style='color: #e74c3c; margin-top: 0;'>📈 Próximos Pasos</h3>
        <p style='color: #2c3e50; line-height: 1.8;'>1. Revisar problemas críticos</p>
        <p style='color: #2c3e50; line-height: 1.8;'>2. Aprobar presupuesto ($1.21M)</p>
        <p style='color: #2c3e50; line-height: 1.8;'>3. Implementar Quick Wins</p>
        <p style='color: #2c3e50; line-height: 1.8;'>4. Seguimiento semanal de KPIs</p>
        <p style='color: #2c3e50; line-height: 1.8;'>5. Ajustar según resultados</p>
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
"""
DASHBOARD EJECUTIVO INTERACTIVO - TIENDA AURELION
Análisis Comercial con Streamlit

Instalación requerida:
pip install streamlit plotly pandas numpy

Ejecución:
streamlit run dashboard_aurelion-E.py
"""
"""
DASHBOARD EJECUTIVO FINAL - TIENDA AURELION
100% RESPONSIVE | TODOS LOS GRÁFICOS | 6 PROBLEMAS VISIBLES | +CONTENIDO
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# ============================================================================
# CONFIGURACIÓN RESPONSIVE
# ============================================================================
st.set_page_config(
    page_title="Aurelion Dashboard",
    page_icon="target",
    layout="wide",
    initial_sidebar_state="auto"
)

# ============================================================================
# CSS RESPONSIVE + CONTRASTE ALTO
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .main-header { 
        font-size: clamp(1.8rem, 5vw, 2.8rem); font-weight: 700; color: white; 
        text-align: center; padding: 1.2rem; margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        border-radius: 16px; box-shadow: 0 8px 20px rgba(102,126,234,0.3); 
    }
    .info-box { 
        background: #f0f4f8; border-left: 6px solid #667eea; padding: 1rem; border-radius: 10px; 
        font-size: clamp(0.9rem, 2.5vw, 1.1rem); color: #1a1a1a; font-weight: 600; 
    }
    .kpi-card { 
        background: white; padding: clamp(1rem, 3vw, 1.8rem); border-radius: 14px; 
        box-shadow: 0 6px 16px rgba(0,0,0,0.1); text-align: center; height: 100%; 
    }
    .kpi-value { font-size: clamp(1.6rem, 4vw, 2.3rem); font-weight: 700; color: #1a1a1a; }
    .kpi-label { color: #2c3e50; font-size: clamp(0.8rem, 2vw, 0.95rem); text-transform: uppercase; letter-spacing: 1.2px; font-weight: 600; }
    .problem-card { 
        background: #fff5f5; border-left: 7px solid #e74c3c; padding: 1.4rem; border-radius: 12px; 
        box-shadow: 0 4px 14px rgba(231,76,60,0.15); margin: 1rem 0; 
        font-size: clamp(0.9rem, 2.5vw, 1rem); color: #1a1a1a; font-weight: 600;
    }
    .solution-card { 
        background: #f0fff4; border-left: 7px solid #27ae60; padding: 1.4rem; border-radius: 12px; 
        box-shadow: 0 4px 14px rgba(39,174,96,0.15); margin: 1rem 0; 
        font-size: clamp(0.9rem, 2.5vw, 1rem); color: #1a1a1a; font-weight: 600;
    }
    .roi-badge { 
        background: #27ae60; color: white; padding: 0.4rem 1rem; border-radius: 50px; 
        font-weight: 700; font-size: clamp(0.9rem, 2.5vw, 1.1rem); display: inline-block; 
    }
    .footer { 
        text-align: center; padding: 2rem; background: #1a1a1a; color: white; 
        border-radius: 12px; margin-top: 3rem; font-size: clamp(0.8rem, 2vw, 1rem); font-weight: 500; 
    }
    .stTabs [data-baseweb="tab"] { 
        font-weight: 700; font-size: clamp(0.9rem, 2.5vw, 1.05rem); padding: 12px 20px; 
    }
    @media (max-width: 600px) {
        .stTabs [data-baseweb="tab-list"] { flex-direction: column; }
        .stPlotlyChart { width: 100% !important; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CARGA DE DATOS
# ============================================================================
@st.cache_data
def cargar_datos():
    try:
        clientes = pd.read_csv('datos_limpios/clientes_limpios.csv')
        productos = pd.read_csv('datos_limpios/productos_limpios.csv')
        ventas = pd.read_csv('datos_limpios/ventas_limpias.csv')
        detalle = pd.read_csv('datos_limpios/detalle_ventas_limpios.csv')
        calendario = pd.read_csv('datos_limpios/calendario.csv')

        ventas['fecha'] = pd.to_datetime(ventas['fecha'])
        calendario['fecha'] = pd.to_datetime(calendario['fecha'])

        df = detalle.merge(ventas, on='id_venta').merge(productos, on='id_producto')
        df = df.merge(clientes[['id_cliente', 'ciudad', 'nombre_cliente']], on='id_cliente', how='left')
        df = df.merge(calendario, on='fecha', how='left')
        df['ciudad'] = df['ciudad'].fillna('Desconocida')
        df['nombre_cliente'] = df['nombre_cliente'].fillna('Cliente Desconocido')
        return df, clientes
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame(), pd.DataFrame()

df_full, clientes_df = cargar_datos()
if df_full.empty:
    st.stop()

# ============================================================================
# KPIs GLOBALES (FIJOS)
# ============================================================================
total_ventas_global = df_full['importe'].sum()
total_transacciones_global = df_full['id_venta'].nunique()
ticket_promedio_global = total_ventas_global / total_transacciones_global
cantidad_promedio_global = df_full['cantidad'].mean()

# ============================================================================
# HEADER
# ============================================================================
st.markdown('<div class="main-header">DASHBOARD EJECUTIVO<br><small style="font-weight:400;">Tienda Aurelion | Enero - Junio 2024</small></div>', unsafe_allow_html=True)
st.markdown("""
<div class="info-box">
    <strong>120 transacciones</strong> · <strong>431 líneas</strong> · <strong>67 clientes activos</strong> · <strong>7 ciudades</strong> · <strong>100 productos</strong>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - FILTROS
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1rem; background:linear-gradient(135deg, #667eea, #764ba2); color:white; border-radius:12px; font-weight:700;">
        AURELION
    </div>
    """, unsafe_allow_html=True)
    try:
        st.image("assets/logo_aurelion.png", use_container_width=True)
    except: pass

    st.markdown("### FILTROS")
    fecha_range = st.date_input("Período", [df_full['fecha'].min().date(), df_full['fecha'].max().date()])
    categoria = st.multiselect("Categoría", df_full['categoria'].unique(), default=df_full['categoria'].unique())
    ciudad = st.multiselect("Ciudad", df_full['ciudad'].unique(), default=df_full['ciudad'].unique())
    clientes_list = clientes_df[['id_cliente', 'nombre_cliente']].drop_duplicates()
    clientes_list['label'] = clientes_list['id_cliente'].astype(str) + " - " + clientes_list['nombre_cliente']
    cliente_sel = st.multiselect("Cliente", clientes_list['label'].tolist(), default=[])

# ============================================================================
# APLICAR FILTROS
# ============================================================================
data = df_full.copy()
mask = (data['fecha'].dt.date >= fecha_range[0]) & (data['fecha'].dt.date <= fecha_range[1])
data = data[mask]
if categoria: data = data[data['categoria'].isin(categoria)]
if ciudad: data = data[data['ciudad'].isin(ciudad)]
if cliente_sel:
    ids = [int(x.split(" - ")[0]) for x in cliente_sel]
    data = data[data['id_cliente'].isin(ids)]

# ============================================================================
# TABS
# ============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["RESUMEN", "PROBLEMAS", "SOLUCIONES", "ANÁLISIS", "PROYECCIÓN"])

# ====================== RESUMEN ======================
with tab1:
    st.subheader("KPIs GLOBALES")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(f'<div class="kpi-card"><div class="kpi-value">${total_ventas_global:,.0f}</div><div class="kpi-label">Ventas Totales</div></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_transacciones_global:,}</div><div class="kpi-label">Transacciones</div></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="kpi-card"><div class="kpi-value">${ticket_promedio_global:,.0f}</div><div class="kpi-label">Ticket Promedio</div></div>', unsafe_allow_html=True)
    with col4: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{cantidad_promedio_global:.1f}</div><div class="kpi-label">Cant. Promedio</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("KPIs FILTRADOS")
    total_f = data['importe'].sum()
    trans_f = data['id_venta'].nunique()
    ticket_f = total_f / trans_f if trans_f > 0 else 0
    cant_f = data['cantidad'].mean() if len(data) > 0 else 0
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(f'<div class="kpi-card"><div class="kpi-value">${total_f:,.0f}</div><div class="kpi-label">Ventas</div></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{trans_f:,}</div><div class="kpi-label">Transacciones</div></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="kpi-card"><div class="kpi-value">${ticket_f:,.0f}</div><div class="kpi-label">Ticket</div></div>', unsafe_allow_html=True)
    with col4: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{cant_f:.1f}</div><div class="kpi-label">Cantidad</div></div>', unsafe_allow_html=True)

# ====================== PROBLEMAS - 6 TARJETAS + GRÁFICOS ======================
with tab2:
    st.subheader("6 PROBLEMAS CRÍTICOS DETECTADOS")

    # GRÁFICO 1: Ventas diarias
    ventas_dia = data.groupby('fecha')['id_venta'].nunique().reset_index()
    fig1 = px.area(ventas_dia, x='fecha', y='id_venta', title="Ventas Diarias (0.67 promedio)")
    fig1.add_hline(y=1, line_dash="dash", line_color="red", annotation_text="Meta: 1/día")
    st.plotly_chart(fig1, use_container_width=True)

    # 6 TARJETAS COMPLETAS
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="problem-card">
            <h4>Warning 1. Baja Frecuencia</h4>
            <p><strong>0.67 ventas/día</strong> → 120 en 178 días</p>
            <p>Caída del <strong>-37.5% en abril</strong></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="problem-card">
            <h4>Warning 2. 33% Clientes Inactivos</h4>
            <p>33 de 100 no compraron en 3+ meses</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="problem-card">
            <h4>Warning 3. Limpieza Subdesarrollada</h4>
            <p>Solo <strong>24.7% de ventas</strong> vs meta 35-40%</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="problem-card">
            <h4>Warning 4. 5 Productos Sin Rotación</h4>
            <p>ID: <strong>53, 55, 57, 91, 97</strong> → 0 ventas</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="problem-card">
            <h4>Warning 5. Ticket Bajo</h4>
            <p>$8,500 promedio → oportunidad de upselling</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="problem-card">
            <h4>Warning 6. Concentración Geográfica</h4>
            <p>70% de ventas en 2 ciudades</p>
        </div>
        """, unsafe_allow_html=True)

    # GRÁFICO 2: Clientes activos
    clientes_activos = data['id_cliente'].nunique()
    fig_pie = px.pie(values=[clientes_activos, 100 - clientes_activos], names=['Activos', 'Inactivos'],
                     color_discrete_sequence=['#27ae60', '#e74c3c'], title="Clientes Activos vs Inactivos")
    st.plotly_chart(fig_pie, use_container_width=True)

# ====================== SOLUCIONES + GRÁFICO ROI ======================
with tab3:
    st.subheader("3 ESTRATEGIAS CON ROI >1,000%")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="solution-card">
            <h4>Target Programa Fidelización</h4>
            <p>Club VIP + Puntos</p>
            <p><strong>Inversión:</strong> $185K</p>
            <p><strong>Retorno:</strong> +$2.1M</p>
            <div class="roi-badge">ROI: 1,157%</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="solution-card">
            <h4>Target Marketing Automation</h4>
            <p>Email + SMS segmentado</p>
            <p><strong>Inversión:</strong> $150K</p>
            <p><strong>Retorno:</strong> +$15.5M</p>
            <div class="roi-badge">ROI: 10,343%</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="solution-card">
            <h4>Target Pricing & Promos</h4>
            <p>2x1 + descuentos</p>
            <p><strong>Inversión:</strong> $150K</p>
            <p><strong>Retorno:</strong> +$2.0M</p>
            <div class="roi-badge">ROI: 1,340%</div>
        </div>
        """, unsafe_allow_html=True)

    # GRÁFICO ROI
    estrategias = ["Fidelización", "Marketing", "Promociones"]
    roi = [1157, 10343, 1340]
    fig_roi = px.bar(x=estrategias, y=roi, title="ROI por Estrategia (%)", color=roi, color_continuous_scale='Greens')
    st.plotly_chart(fig_roi, use_container_width=True)

# ====================== ANÁLISIS - 5 SUBPESTAÑAS + GRÁFICOS ======================
with tab4:
    sub1, sub2, sub3, sub4, sub5 = st.tabs(["Categoría", "Ciudad", "Clientes", "Temporal", "Productos"])

    with sub1:
        cat = data.groupby('categoria')['importe'].sum().reset_index()
        fig = px.bar(cat, x='categoria', y='importe', title="Ventas por Categoría", color='categoria')
        st.plotly_chart(fig, use_container_width=True)

    with sub2:
        ciudad = data.groupby('ciudad')['importe'].sum().reset_index()
        fig = px.bar(ciudad, x='ciudad', y='importe', title="Ventas por Ciudad", color='ciudad')
        st.plotly_chart(fig, use_container_width=True)

    with sub3:
        top = data.groupby(['id_cliente', 'nombre_cliente'])['importe'].sum().nlargest(10).reset_index()
        top['label'] = top['id_cliente'].astype(str) + " - " + top['nombre_cliente']
        fig = px.bar(top, x='importe', y='label', orientation='h', title="Top 10 Clientes")
        st.plotly_chart(fig, use_container_width=True)

    with sub4:
        ventas_mes = data.groupby(data['fecha'].dt.to_period('M'))['importe'].sum().reset_index()
        ventas_mes['fecha'] = ventas_mes['fecha'].dt.to_timestamp()
        fig = px.line(ventas_mes, x='fecha', y='importe', title="Evolución Mensual", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    with sub5:
        top_prod = data.groupby(['id_producto', 'nombre_producto'])['cantidad'].sum().nlargest(10).reset_index()
        fig = px.bar(top_prod, x='cantidad', y='nombre_producto', orientation='h', title="Top 10 Productos por Cantidad")
        st.plotly_chart(fig, use_container_width=True)

# ====================== PROYECCIÓN + 2 GRÁFICOS ======================
with tab5:
    st.subheader("PROYECCIÓN 12 MESES")
    meses = pd.date_range(start='2024-07-01', periods=12, freq='M')
    base = total_ventas_global / 6
    proy = [base * (1.08 ** i) for i in range(12)]
    df_proy = pd.DataFrame({'Mes': meses, 'Ventas': proy})
    fig = px.line(df_proy, x='Mes', y='Ventas', title="Proyección de Ventas", markers=True)
    fig.add_hline(y=base * 12, line_dash="dash", line_color="green")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1: st.metric("Inversión Total", "$1,210,000")
    with col2: st.metric("Retorno Proyectado", "$16,320,311", delta="ROI: 1,349%")

    # GRÁFICO ESCENARIOS
    escenarios = pd.DataFrame({
        'Escenario': ['Conservador', 'Realista', 'Agresivo'],
        'Crecimiento': [15, 70, 200],
        'Ventas': [total_ventas_global * 1.15, total_ventas_global * 1.7, total_ventas_global * 3]
    })
    fig_esc = px.bar(escenarios, x='Escenario', y='Ventas', text='Crecimiento', title="Escenarios de Crecimiento")
    fig_esc.update_traces(texttemplate='%{text}%', textposition='outside')
    st.plotly_chart(fig_esc, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
<div class="footer">
    <p><strong>Dashboard Ejecutivo Tienda Aurelion</strong> | 100% Responsive | +Contenido | 2025</p>
</div>
""", unsafe_allow_html=True)
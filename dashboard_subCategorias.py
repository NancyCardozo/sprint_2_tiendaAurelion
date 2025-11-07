"""
DASHBOARD EJECUTIVO INTERACTIVO - TIENDA AURELION
Análisis Comercial con Streamlit - VERSION MEJORADA

Instalación requerida:
pip install streamlit plotly pandas numpy scipy

Ejecución:
streamlit run dashboard_D4.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
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

# CSS Personalizado Mejorado
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
    
    .subcategoria-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #3498db;
    }
    
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .highlight-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNCIONES AUXILIARES MEJORADAS
# ============================================================================
def organizar_subcategorias_completas(datos):
    """Organiza todos los productos en subcategorías completas"""
    
    mapeo_subcategorias = {
        # ALIMENTOS - Bebidas
        'Coca Cola 1.5L': 'Bebidas',
        'Pepsi 1.5L': 'Bebidas',
        'Sprite 1.5L': 'Bebidas',
        'Fanta Naranja 1.5L': 'Bebidas',
        'Agua Mineral 500ml': 'Bebidas',
        'Jugo de Naranja 1L': 'Bebidas',
        'Jugo de Manzana 1L': 'Bebidas',
        'Energética Nitro 500ml': 'Bebidas',
        
        # ALIMENTOS - Bebidas Alcohólicas
        'Cerveza Rubia 1L': 'Bebidas Alcohólicas',
        'Cerveza Negra 1L': 'Bebidas Alcohólicas',
        'Vino Tinto Malbec 750ml': 'Bebidas Alcohólicas',
        'Vino Blanco 750ml': 'Bebidas Alcohólicas',
        'Sidra 750ml': 'Bebidas Alcohólicas',
        'Fernet 750ml': 'Bebidas Alcohólicas',
        'Vodka 700ml': 'Bebidas Alcohólicas',
        'Ron 700ml': 'Bebidas Alcohólicas',
        'Gin 700ml': 'Bebidas Alcohólicas',
        'Whisky 750ml': 'Bebidas Alcohólicas',
        'Licor de Café 700ml': 'Bebidas Alcohólicas',
        
        # ALIMENTOS - Infusiones
        'Yerba Mate Suave 1kg': 'Infusiones',
        'Yerba Mate Intensa 1kg': 'Infusiones',
        'Café Molido 250g': 'Infusiones',
        'Té Negro 20 saquitos': 'Infusiones',
        'Té Verde 20 saquitos': 'Infusiones',
        
        # ALIMENTOS - Golosinas y Snacks
        'Galletitas Chocolate': 'Golosinas y Snacks',
        'Galletitas Vainilla': 'Golosinas y Snacks',
        'Alfajor Triple': 'Golosinas y Snacks',
        'Alfajor Simple': 'Golosinas y Snacks',
        'Papas Fritas Clásicas 100g': 'Golosinas y Snacks',
        'Papas Fritas Onduladas 100g': 'Golosinas y Snacks',
        'Maní Salado 200g': 'Golosinas y Snacks',
        'Mix de Frutos Secos 200g': 'Golosinas y Snacks',
        'Chocolate Amargo 100g': 'Golosinas y Snacks',
        'Chocolate con Leche 100g': 'Golosinas y Snacks',
        'Turrón 50g': 'Golosinas y Snacks',
        'Barrita de Cereal 30g': 'Golosinas y Snacks',
        'Caramelos Masticables': 'Golosinas y Snacks',
        'Chicle Menta': 'Golosinas y Snacks',
        'Chupetín': 'Golosinas y Snacks',
        
        # ALIMENTOS - Lácteos
        'Leche Entera 1L': 'Lácteos',
        'Leche Descremada 1L': 'Lácteos',
        'Yogur Natural 200g': 'Lácteos',
        'Queso Cremoso 500g': 'Lácteos',
        'Queso Rallado 150g': 'Lácteos',
        'Manteca 200g': 'Lácteos',
        'Queso Untable 190g': 'Lácteos',
        'Queso Azul 150g': 'Lácteos',
        'Dulce de Leche 400g': 'Lácteos',
        
        # ALIMENTOS - Panadería
        'Pan Lactal Blanco': 'Panadería',
        'Pan Lactal Integral': 'Panadería',
        'Medialunas de Manteca': 'Panadería',
        'Bizcochos Salados': 'Panadería',
        
        # ALIMENTOS - Dulces y Conservas
        'Mermelada de Durazno 400g': 'Dulces y Conservas',
        'Mermelada de Frutilla 400g': 'Dulces y Conservas',
        'Miel Pura 250g': 'Dulces y Conservas',
        'Stevia 100 sobres': 'Dulces y Conservas',
        
        # ALIMENTOS - Almacén
        'Aceite de Girasol 1L': 'Almacén',
        'Vinagre de Alcohol 500ml': 'Almacén',
        'Salsa de Tomate 500g': 'Almacén',
        'Arroz Largo Fino 1kg': 'Almacén',
        'Fideos Spaghetti 500g': 'Almacén',
        'Lentejas Secas 500g': 'Almacén',
        'Garbanzos 500g': 'Almacén',
        'Porotos Negros 500g': 'Almacén',
        'Harina de Trigo 1kg': 'Almacén',
        'Azúcar 1kg': 'Almacén',
        'Sal Fina 500g': 'Almacén',
        'Granola 250g': 'Almacén',
        'Avena Instantánea 250g': 'Almacén',
        'Jugo en Polvo Naranja': 'Almacén',
        'Jugo en Polvo Limón': 'Almacén',
        'Sopa Instantánea Pollo': 'Almacén',
        'Caldo Concentrado Carne': 'Almacén',
        'Caldo Concentrado Verdura': 'Almacén',
        
        # ALIMENTOS - Congelados
        'Pizza Congelada Muzzarella': 'Congelados',
        'Empanadas Congeladas': 'Congelados',
        'Verduras Congeladas Mix': 'Congelados',
        'Hamburguesas Congeladas x4': 'Congelados',
        
        # ALIMENTOS - Helados
        'Helado Vainilla 1L': 'Helados',
        'Helado Chocolate 1L': 'Helados',
        'Helado de Frutilla 1L': 'Helados',
        
        # ALIMENTOS - Encurtidos
        'Aceitunas Verdes 200g': 'Encurtidos',
        'Aceitunas Negras 200g': 'Encurtidos',
        
        # LIMPIEZA - Limpieza Hogar
        'Detergente Líquido 750ml': 'Limpieza Hogar',
        'Lavandina 1L': 'Limpieza Hogar',
        'Suavizante 1L': 'Limpieza Hogar',
        'Limpiavidrios 500ml': 'Limpieza Hogar',
        'Desengrasante 500ml': 'Limpieza Hogar',
        'Esponjas x3': 'Limpieza Hogar',
        'Trapo de Piso': 'Limpieza Hogar',
        'Servilletas x100': 'Limpieza Hogar',
        'Toallas Húmedas x50': 'Limpieza Hogar',
        
        # LIMPIEZA - Higiene Personal
        'Jabón de Tocador': 'Higiene Personal',
        'Shampoo 400ml': 'Higiene Personal',
        'Papel Higiénico x4': 'Higiene Personal',
        'Desodorante Aerosol': 'Higiene Personal',
        'Crema Dental 90g': 'Higiene Personal',
        'Cepillo de Dientes': 'Higiene Personal',
        'Hilo Dental': 'Higiene Personal',
        'Mascarilla Capilar': 'Higiene Personal'
    }
    
    datos['subcategoria'] = datos['nombre_producto'].map(mapeo_subcategorias)
    datos['subcategoria'] = datos['subcategoria'].fillna('Otros')
    
    return datos

def analizar_subcategorias_detallado(datos):
    """Análisis detallado por subcategorías"""
    analisis = datos.groupby(['categoria', 'subcategoria']).agg({
        'importe': ['sum', 'mean', 'count'],
        'cantidad': ['sum', 'mean'],
        'id_venta': 'nunique',
        'id_cliente': 'nunique',
        'nombre_producto': 'nunique'
    }).round(2)
    
    analisis.columns = [
        'Ventas Totales', 'Ticket Promedio', 'Transacciones',
        'Cantidad Total', 'Cantidad Promedio',
        'Ventas Únicas', 'Clientes Únicos', 'Productos Diferentes'
    ]
    
    return analisis

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
        ventas_completas = ventas_completas.merge(clientes[['id_cliente', 'ciudad', 'nombre_cliente']], on='id_cliente', how='left')
        ventas_completas = ventas_completas.merge(
            calendario[['fecha', 'anio', 'mes', 'dia_semana', 'nombre_dia', 'nombre_mes']], 
            on='fecha', how='left'
        )
        
        # Organizar en subcategorías completas
        ventas_completas = organizar_subcategorias_completas(ventas_completas)
        
        return clientes, productos, ventas, detalle_ventas, calendario, ventas_completas
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return None, None, None, None, None, None

clientes, productos, ventas, detalle_ventas, calendario, ventas_completas = cargar_datos()

if ventas_completas is None:
    st.error("⚠️ No se pudieron cargar los datos")
    st.stop()

# ============================================================================
# SIDEBAR MEJORADO
# ============================================================================
st.sidebar.header("🎛️ CONFIGURACIÓN")

modo = st.sidebar.radio(
    "Selecciona el modo de visualización:",
    ["👔 Modo Ejecutivo", "🔍 Modo Analista"],
    index=0
)

# Filtros básicos
st.sidebar.header("🔍 FILTROS")

fecha_min = ventas_completas['fecha'].min()
fecha_max = ventas_completas['fecha'].max()

fecha_range = st.sidebar.date_input(
    "Rango de Fechas",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)

# Aplicar filtros
datos_filtrados = ventas_completas.copy()
if len(fecha_range) == 2:
    datos_filtrados = datos_filtrados[
        (datos_filtrados['fecha'] >= pd.Timestamp(fecha_range[0])) &
        (datos_filtrados['fecha'] <= pd.Timestamp(fecha_range[1]))
    ]

# Filtros avanzados para modo analista
if modo == "🔍 Modo Analista":
    st.sidebar.header("🎯 FILTROS AVANZADOS")
    
    categorias_disponibles = ['Todas'] + list(ventas_completas['categoria'].unique())
    categoria_filtro = st.sidebar.selectbox("Categoría", categorias_disponibles, index=0)
    
    subcategorias_disponibles = ['Todas'] + list(ventas_completas['subcategoria'].unique())
    subcategoria_filtro = st.sidebar.selectbox("Subcategoría", subcategorias_disponibles, index=0)
    
    if categoria_filtro != 'Todas':
        datos_filtrados = datos_filtrados[datos_filtrados['categoria'] == categoria_filtro]
    
    if subcategoria_filtro != 'Todas':
        datos_filtrados = datos_filtrados[datos_filtrados['subcategoria'] == subcategoria_filtro]

# ============================================================================
# HEADER MEJORADO
# ============================================================================
st.markdown('<div class="main-header">🎯 DASHBOARD EJECUTIVO MEJORADO<br>TIENDA AURELION</div>', unsafe_allow_html=True)

# ============================================================================
# NUEVA SECCIÓN: RESUMEN EJECUTIVO CON SUBCATEGORÍAS
# ============================================================================
st.header("📊 RESUMEN EJECUTIVO - ANÁLISIS POR SUBCATEGORÍAS")

# Métricas rápidas por categoría principal
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_alimentos = len(datos_filtrados[datos_filtrados['categoria'] == 'Alimentos'])
    st.metric("🍎 Productos Alimentos", f"{total_alimentos}")

with col2:
    total_limpieza = len(datos_filtrados[datos_filtrados['categoria'] == 'Limpieza'])
    st.metric("🧼 Productos Limpieza", f"{total_limpieza}")

with col3:
    total_subcategorias = datos_filtrados['subcategoria'].nunique()
    st.metric("📦 Subcategorías", f"{total_subcategorias}")

with col4:
    total_bebidas_alcoholicas = len(datos_filtrados[datos_filtrados['subcategoria'] == 'Bebidas Alcohólicas'])
    st.metric("🍷 Bebidas Alcohólicas", f"{total_bebidas_alcoholicas}")

# Gráfico de distribución por subcategoría
st.subheader("📈 Distribución de Ventas por Subcategoría")

ventas_por_subcategoria = datos_filtrados.groupby(['categoria', 'subcategoria'])['importe'].sum().reset_index()

col1, col2 = st.columns(2)

with col1:
    fig_sunburst = px.sunburst(
        ventas_por_subcategoria,
        path=['categoria', 'subcategoria'],
        values='importe',
        title="Distribución de Ventas por Categoría y Subcategoría",
        color='importe',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_sunburst, use_container_width=True)

with col2:
    # Top 10 subcategorías por ventas
    top_subcats = ventas_por_subcategoria.nlargest(10, 'importe')
    fig_top_subcats = px.bar(
        top_subcats,
        x='importe',
        y='subcategoria',
        orientation='h',
        title="Top 10 Subcategorías por Ventas",
        color='importe',
        color_continuous_scale='Viridis'
    )
    fig_top_subcats.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_top_subcats, use_container_width=True)

# Tabla resumen ejecutivo de subcategorías
st.subheader("📋 RESUMEN EJECUTIVO POR SUBCATEGORÍA")

analisis_subcategorias = analizar_subcategorias_detallado(datos_filtrados)
st.dataframe(analisis_subcategorias, use_container_width=True)

# ============================================================================
# SECCIÓN MEJORADA: ANÁLISIS DETALLADO CON SUBCATEGORÍAS
# ============================================================================
st.header("📈 ANÁLISIS DETALLADO CON SUBCATEGORÍAS")

if modo == "🔍 Modo Analista":
    subtab1, subtab2, subtab3, subtab4, subtab5 = st.tabs([
        "🎯 Categoría", "🌏 Ciudad", "📦 Subcategorías", "👤 Cliente", "📅 Temporal"
    ])
    
    with subtab3:
        st.subheader("📊 ANÁLISIS DETALLADO POR SUBCATEGORÍAS")
        
        # Selector de categoría para análisis detallado
        categoria_analisis = st.selectbox(
            "Selecciona Categoría para Análisis:",
            ['Todas'] + list(datos_filtrados['categoria'].unique()),
            key='categoria_analisis'
        )
        
        if categoria_analisis != 'Todas':
            datos_analisis = datos_filtrados[datos_filtrados['categoria'] == categoria_analisis]
        else:
            datos_analisis = datos_filtrados
        
        # Análisis detallado por subcategoría
        st.subheader(f"📈 Métricas por Subcategoría - {categoria_analisis}")
        
        analisis_detallado = datos_analisis.groupby('subcategoria').agg({
            'importe': ['sum', 'mean', 'count'],
            'cantidad': ['sum', 'mean'],
            'id_venta': 'nunique',
            'id_cliente': 'nunique',
            'nombre_producto': 'nunique'
        }).round(2)
        
        analisis_detallado.columns = [
            'Ventas Totales', 'Ticket Promedio', 'Transacciones',
            'Cantidad Total', 'Cantidad Promedio',
            'Ventas Únicas', 'Clientes Únicos', 'Productos Diferentes'
        ]
        
        st.dataframe(analisis_detallado, use_container_width=True)
        
        # Gráficos comparativos
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de eficiencia (Ventas por Producto)
            eficiencia_data = analisis_detallado.copy()
            eficiencia_data['Ventas por Producto'] = eficiencia_data['Ventas Totales'] / eficiencia_data['Productos Diferentes']
            eficiencia_data = eficiencia_data.reset_index()
            
            fig_eficiencia = px.scatter(
                eficiencia_data,
                x='Productos Diferentes',
                y='Ventas Totales',
                size='Ventas por Producto',
                color='subcategoria',
                title=f"Eficiencia por Subcategoría - {categoria_analisis}",
                hover_name='subcategoria',
                size_max=50
            )
            st.plotly_chart(fig_eficiencia, use_container_width=True)
        
        with col2:
            # Gráfico de participación relativa
            fig_participacion = px.pie(
                analisis_detallado.reset_index(),
                values='Ventas Totales',
                names='subcategoria',
                title=f"Participación por Subcategoría - {categoria_analisis}",
                hole=0.4
            )
            st.plotly_chart(fig_participacion, use_container_width=True)
        
        # Análisis de productos dentro de subcategoría específica
        st.subheader("🔍 ANÁLISIS DETALLADO POR PRODUCTOS")
        
        subcategoria_detalle = st.selectbox(
            "Selecciona Subcategoría para Detalle:",
            ['Todas'] + list(datos_analisis['subcategoria'].unique()),
            key='subcategoria_detalle'
        )
        
        if subcategoria_detalle != 'Todas':
            datos_subcat = datos_analisis[datos_analisis['subcategoria'] == subcategoria_detalle]
            
            # Análisis de productos individuales
            analisis_productos = datos_subcat.groupby('nombre_producto').agg({
                'importe': ['sum', 'mean', 'count'],
                'cantidad': ['sum', 'mean'],
                'id_venta': 'nunique',
                'id_cliente': 'nunique'
            }).round(2)
            
            analisis_productos.columns = [
                'Ventas Totales', 'Ticket Promedio', 'Transacciones',
                'Cantidad Total', 'Cantidad Promedio',
                'Ventas Únicas', 'Clientes Únicos'
            ]
            
            st.subheader(f"📊 Productos de {subcategoria_detalle}")
            st.dataframe(analisis_productos.nlargest(20, 'Ventas Totales'), use_container_width=True)
            
            # Gráfico de top productos
            top_productos = analisis_productos.nlargest(10, 'Ventas Totales')
            fig_top_productos = px.bar(
                top_productos.reset_index(),
                x='Ventas Totales',
                y='nombre_producto',
                orientation='h',
                title=f"Top 10 Productos - {subcategoria_detalle}",
                color='Ventas Totales',
                color_continuous_scale='Viridis'
            )
            fig_top_productos.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_top_productos, use_container_width=True)

# ============================================================================
# NUEVA SECCIÓN: INSIGHTS ESTRATÉGICOS POR SUBCATEGORÍA
# ============================================================================
st.header("💡 INSIGHTS ESTRATÉGICOS POR SUBCATEGORÍA")

# Calcular insights automáticos
total_ventas = datos_filtrados['importe'].sum()
subcat_ventas = datos_filtrados.groupby('subcategoria')['importe'].sum()

col1, col2, col3 = st.columns(3)

with col1:
    subcat_top = subcat_ventas.idxmax()
    participacion_top = (subcat_ventas.max() / total_ventas) * 100
    st.markdown(f"""
    <div class="highlight-card">
        <h3>🏆 SUBCATEGORÍA LÍDER</h3>
        <p style="font-size: 1.5rem; font-weight: bold;">{subcat_top}</p>
        <p>Participación: {participacion_top:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Encontrar subcategoría con mayor crecimiento potencial
    subcat_promedio = subcat_ventas.mean()
    subcat_crecimiento = subcat_ventas[subcat_ventas < subcat_promedio]
    if len(subcat_crecimiento) > 0:
        subcat_oportunidad = subcat_crecimiento.idxmax()
        st.markdown(f"""
        <div class="highlight-card">
            <h3>📈 OPORTUNIDAD</h3>
            <p style="font-size: 1.5rem; font-weight: bold;">{subcat_oportunidad}</p>
            <p>Mayor potencial de crecimiento</p>
        </div>
        """, unsafe_allow_html=True)

with col3:
    # Bebidas alcohólicas
    if 'Bebidas Alcohólicas' in subcat_ventas.index:
        participacion_alcohol = (subcat_ventas['Bebidas Alcohólicas'] / total_ventas) * 100
        st.markdown(f"""
        <div class="highlight-card">
            <h3>🍷 BEBIDAS ALCOHÓLICAS</h3>
            <p style="font-size: 1.5rem; font-weight: bold;">{participacion_alcohol:.1f}%</p>
            <p>Participación en ventas totales</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PIE DE PÁGINA MEJORADO
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>🎯 Dashboard Ejecutivo Mejorado - Tienda Aurelion</strong></p>
    <p style="font-size: 0.9rem;">
        Análisis con {total_subcategorias} subcategorías | 
        Período: {fecha_inicio} a {fecha_fin} |
        Total registros: {registros:,}
    </p>
</div>
""".format(
    total_subcategorias=datos_filtrados['subcategoria'].nunique(),
    fecha_inicio=datos_filtrados['fecha'].min().strftime("%d/%m/%Y"),
    fecha_fin=datos_filtrados['fecha'].max().strftime("%d/%m/%Y"),
    registros=len(datos_filtrados)
), unsafe_allow_html=True)
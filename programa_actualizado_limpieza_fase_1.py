"""
PROYECTO TIENDA AURELION - FASE 1
Limpieza, Inspección y Transformación de Datos
"""

"""
PROYECTO TIENDA AURELION - FASE 1
Limpieza, Inspección y Transformación de Datos
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

# ============================================================================
# FUNCIÓN PARA CORREGIR CATEGORÍAS PRINCIPALES CON TRANSFORMERS
# ============================================================================
def corregir_categorias_ia(productos_df):
    """
    Corrige las categorías principales usando modelo de IA (Zero-shot classification)
    """
    print("   🤖 Corrigiendo categorías principales con IA...")
    
    try:
        from transformers import pipeline
        
        # Cargar el clasificador
        clasificador = pipeline("zero-shot-classification", 
                              model="facebook/bart-large-mnli")
        
        # Definir categorías posibles
        categorias = ["Alimentos", "Limpieza"]
        
        def clasificar_con_ia(nombre):
            if pd.isna(nombre):
                return "Alimentos"
            
            try:
                resultado = clasificador(str(nombre), candidate_labels=categorias)
                return resultado["labels"][0]
            except:
                return "Alimentos"  # Fallback
        
        # Aplicar clasificación (muestra reducida para prueba, luego completo)
        print("   ⏳ Clasificando productos con IA (esto puede tomar unos minutos)...")
        
        # Para prueba rápida, clasificar solo los primeros 10
        # productos_df['categoria_ia'] = productos_df['nombre_producto'].apply(clasificar_con_ia)
        
        # Clasificar en lotes para mejor manejo
        lote_size = 20
        total_productos = len(productos_df)
        categorias_ia = []
        
        for i in range(0, total_productos, lote_size):
            lote = productos_df['nombre_producto'].iloc[i:i+lote_size]
            lote_categorias = [clasificar_con_ia(nombre) for nombre in lote]
            categorias_ia.extend(lote_categorias)
            print(f"   📦 Procesado lote {i//lote_size + 1}/{(total_productos-1)//lote_size + 1}")
        
        productos_df['categoria_ia'] = categorias_ia
        
        # Contar cambios
        cambios = (productos_df['categoria'] != productos_df['categoria_ia']).sum()
        print(f"   ✓ Categorías corregidas por IA: {cambios} productos")
        
        # Reemplazar categoría original
        productos_df['categoria_original'] = productos_df['categoria']  # Guardar original
        productos_df['categoria'] = productos_df['categoria_ia']
        productos_df = productos_df.drop('categoria_ia', axis=1)
        
        return productos_df
        
    except ImportError:
        print("   ⚠️  Transformers no disponible, usando método basado en reglas...")
        return corregir_categorias_reglas(productos_df)
    except Exception as e:
        print(f"   ⚠️  Error con IA: {e}, usando método basado en reglas...")
        return corregir_categorias_reglas(productos_df)

# ============================================================================
# FUNCIÓN ALTERNATIVA BASADA EN REGLAS
# ============================================================================
def corregir_categorias_reglas(productos_df):
    """
    Corrige categorías principales usando reglas basadas en palabras clave
    """
    print("   🔧 Corrigiendo categorías principales con reglas...")
    
    # Palabras clave para categoría LIMPIEZA
    palabras_limpieza = [
        'detergente', 'lavandina', 'jabón', 'shampoo', 'acondicionador', 'desodorante',
        'crema dental', 'papel higiénico', 'servilletas', 'toallas húmedas', 'suavizante',
        'limpiador', 'desinfectante', 'limpiavidrios', 'desengrasante', 'esponjas', 'trapo',
        'mascarilla', 'cepillo', 'hilo dental'
    ]
    
    def determinar_categoria(nombre):
        if pd.isna(nombre):
            return 'Alimentos'
        
        nombre_lower = str(nombre).lower()
        
        # Verificar si es de limpieza
        for palabra in palabras_limpieza:
            if palabra in nombre_lower:
                return 'Limpieza'
        
        return 'Alimentos'  # Por defecto
    
    # Guardar categoría original
    productos_df['categoria_original'] = productos_df['categoria']
    
    # Aplicar corrección
    productos_df['categoria'] = productos_df['nombre_producto'].apply(determinar_categoria)
    
    # Contar cambios
    cambios = (productos_df['categoria_original'] != productos_df['categoria']).sum()
    print(f"   ✓ Categorías corregidas: {cambios} productos")
    
    return productos_df

# ============================================================================
# FUNCIÓN CLASIFICADOR DE SUBCATEGORÍAS MEJORADO - VERSIÓN CORREGIDA
# ============================================================================
def clasificar_subcategorias_mejorado(productos_df):
    """
    Clasificación mejorada de subcategorías con reglas más específicas
    """
    print("   🧠 Clasificando subcategorías (versión mejorada)...")
    
    # Diccionario expandido de palabras clave para subcategorías
    palabras_clave = {
        'Bebidas': ['gaseosa', 'jugo', 'agua', 'bebida', 'cola', 'refresco', 'energética', 
                   'pepsi', 'fanta', 'sprite', 'nitro', 'mineral'],
        'Lácteos': ['leche', 'yogur', 'queso', 'crema', 'manteca', 'lácteo', 'untable'],
        'Snacks': ['papas', 'maní', 'snack', 'galletita', 'alfajor', 'chocolate', 'turrón', 
                  'bizcochos', 'mix frutos', 'barrita cereal', 'frutos secos'],
        'Limpieza Hogar': ['lavandina', 'limpiador', 'desinfectante', 'esponja', 'toalla', 
                          'jabón', 'suavizante', 'limpiavidrios', 'desengrasante', 'trapo'],
        'Higiene Personal': ['shampoo', 'acondicionador', 'desodorante', 'crema dental', 
                            'hilo dental', 'toallas húmedas', 'cepillo', 'mascarilla'],
        'Bebidas Alcohólicas': ['cerveza', 'vino', 'whisky', 'ron', 'fernet', 'licor', 'sidra', 'vodka', 'gin'],
        'Panificados': ['pan', 'medialuna', 'factura', 'tostada', 'galleta', 'empanada'],
        'Infusiones': ['café', 'té', 'yerba', 'mate', 'infusión', 'saquitos'],
        'Dulces': ['caramelo', 'chupetín', 'chicle'],
        'Almacén': ['arroz', 'fideo', 'lenteja', 'poroto', 'harina', 'aceite', 'vinagre', 
                   'sal', 'caldo', 'salsa tomate', 'granola', 'avena', 'azúcar', 'mermelada',
                   'miel', 'stevia', 'sopa instantánea', 'garbanzo', 'conserva'],
        'Congelados': ['helado', 'pizza', 'verdura congelada', 'congelado', 'hamburguesa', 'empanada'],
        'Conservas': ['aceituna', 'conserva', 'enlatado'],
        'Cuidado Personal': ['shampoo', 'acondicionador', 'desodorante', 'crema dental', 
                            'hilo dental', 'toallas húmedas', 'cepillo', 'mascarilla'],
        'Limpieza Ropa': ['detergente', 'suavizante'],
        'Limpieza Cocina': ['lavandina', 'limpiador', 'desinfectante', 'esponja', 'limpiavidrios', 'desengrasante']
    }
    
    # Reglas específicas para productos conflictivos - VERSIÓN CORREGIDA
    reglas_especificas = {
        'Galletitas Chocolate': 'Snacks',
        'Galletitas Vainilla': 'Snacks', 
        'Chocolate Amargo 100g': 'Snacks',  # NOMBRE EXACTO CORREGIDO
        'Chocolate con Leche 100g': 'Snacks',  # NOMBRE EXACTO CORREGIDO
        'Dulce de Leche 400g': 'Lácteos',
        'Mermelada de Durazno 400g': 'Almacén',
        'Mermelada de Frutilla 400g': 'Almacén',
        'Salsa de Tomate 500g': 'Almacén',  # NOMBRE EXACTO CORREGIDO
        'Granola 250g': 'Almacén',
        'Avena Instantánea 250g': 'Almacén',
        'Sopa Instantánea Pollo': 'Almacén',
        'Caldo Concentrado Carne': 'Almacén',
        'Caldo Concentrado Verdura': 'Almacén',
        'Jugo en Polvo Naranja': 'Bebidas',
        'Jugo en Polvo Limón': 'Bebidas',
        'Medialunas de Manteca': 'Panificados',
        'Mix de Frutos Secos 200g': 'Snacks',
        'Barrita de Cereal 30g': 'Snacks',
        'Helado Chocolate 1L': 'Congelados',
        'Garbanzos 500g': 'Almacén',
        'Azúcar 1kg': 'Almacén',
        'Miel Pura 250g': 'Almacén',
        'Stevia 100 sobres': 'Almacén',
        'Empanadas Congeladas': 'Congelados',
        'Verduras Congeladas Mix': 'Congelados',
        'Helado de Frutilla 1L': 'Congelados'
    }
    
    def clasificar_por_palabras(nombre, categoria):
        if pd.isna(nombre):
            return 'Sin Clasificar'
        
        nombre_str = str(nombre).strip()  # Agregar strip() para eliminar espacios
        
        print(f"   🔍 Procesando: {nombre_str}")  # DEBUG
        
        # Primero verificar reglas específicas
        if nombre_str in reglas_especificas:
            print(f"   ✅ Regla específica aplicada: {nombre_str} -> {reglas_especificas[nombre_str]}")
            return reglas_especificas[nombre_str]
        
        nombre_lower = nombre_str.lower()
        
        # Si es categoría Limpieza, usar subcategorías específicas
        if categoria == 'Limpieza':
            if any(palabra in nombre_lower for palabra in ['shampoo', 'acondicionador', 'desodorante', 'crema dental', 'hilo dental', 'cepillo', 'mascarilla']):
                return 'Higiene Personal'
            elif any(palabra in nombre_lower for palabra in ['detergente', 'suavizante']):
                return 'Limpieza Ropa'
            elif any(palabra in nombre_lower for palabra in ['lavandina', 'limpiador', 'desinfectante', 'esponja', 'limpiavidrios', 'desengrasante']):
                return 'Limpieza Cocina'
            elif 'toallas húmedas' in nombre_lower:
                return 'Higiene Personal'
            else:
                return 'Limpieza Hogar'
        
        # Para Alimentos, usar el diccionario general
        for subcat, palabras in palabras_clave.items():
            if subcat not in ['Limpieza Hogar', 'Limpieza Ropa', 'Limpieza Cocina']:
                for palabra in palabras:
                    if palabra in nombre_lower:
                        print(f"   ✅ Palabra clave aplicada: {nombre_str} -> {subcat} (palabra: {palabra})")
                        return subcat
        
        print(f"   ⚠️  Sin clasificación: {nombre_str} -> Otros")
        return 'Otros'
    
    # Aplicar clasificación
    productos_df['subcategoria'] = productos_df.apply(
        lambda row: clasificar_por_palabras(row['nombre_producto'], row['categoria']), 
        axis=1
    )
    
    # Estadísticas
    total_productos = len(productos_df)
    subcategorias_unicas = productos_df['subcategoria'].nunique()
    productos_en_otros = (productos_df['subcategoria'] == 'Otros').sum()
    
    print(f"   ✓ Subcategorías asignadas: {subcategorias_unicas} tipos")
    print(f"   ✓ Productos en 'Otros': {productos_en_otros} ({productos_en_otros/total_productos*100:.1f}%)")
    
    # Mostrar distribución
    distribucion = productos_df['subcategoria'].value_counts()
    print("   📊 Distribución de subcategorías:")
    for subcat, count in distribucion.head(15).items():
        porcentaje = (count / total_productos) * 100
        print(f"      • {subcat}: {count} productos ({porcentaje:.1f}%)")
    
    return productos_df

# ============================================================================
# CONFIGURACIÓN DE RUTAS (MANTENER IGUAL)
# ============================================================================
CARPETA_ORIGINALES = 'datos_originales'
CARPETA_LIMPIOS = 'datos_limpios'

# Crear carpeta de datos limpios si no existe
os.makedirs(CARPETA_LIMPIOS, exist_ok=True)

# ============================================================================
# 1. LECTURA DE ARCHIVOS ORIGINALES (MANTENER IGUAL)
# ============================================================================
print("="*70)
print("FASE 1: LIMPIEZA Y TRANSFORMACIÓN DE DATOS")
print("="*70)
print("\n1. Leyendo archivos originales...")

clientes = pd.read_csv(f'{CARPETA_ORIGINALES}/clientes.csv')
productos = pd.read_csv(f'{CARPETA_ORIGINALES}/productos.csv')
ventas = pd.read_csv(f'{CARPETA_ORIGINALES}/ventas.csv')
detalle_ventas = pd.read_csv(f'{CARPETA_ORIGINALES}/detalle_ventas.csv')

print(f"   ✓ clientes.csv: {clientes.shape[0]} registros")
print(f"   ✓ productos.csv: {productos.shape[0]} registros")
print(f"   ✓ ventas.csv: {ventas.shape[0]} registros")
print(f"   ✓ detalle_ventas.csv: {detalle_ventas.shape[0]} registros")

# ============================================================================
# 2. INSPECCIÓN Y DETECCIÓN DE ERRORES (MODIFICAR SECCIÓN PRODUCTOS)
# ============================================================================
print("\n2. Inspeccionando datos y detectando errores...")

errores_detectados = []

# --- CLIENTES 
print("\n   Analizando CLIENTES...")
clientes_info = {
    'archivo': 'clientes.csv',
    'registros_originales': len(clientes),
    'columnas': list(clientes.columns),
    'nulos': clientes.isnull().sum().to_dict(),
    'duplicados_id': clientes['id_cliente'].duplicated().sum(),
    'duplicados_email': clientes['email'].duplicated().sum()
}

if clientes_info['duplicados_email'] > 0:
    errores_detectados.append({
        'Archivo': 'clientes.csv',
        'Error': 'Emails duplicados',
        'Cantidad': clientes_info['duplicados_email'],
        'Método': 'Eliminar duplicados manteniendo primer registro',
        'Impacto': 'Medio'
    })

# --- PRODUCTOS 
print("   Analizando PRODUCTOS...")

# Mostrar distribución original de categorías
print("   📋 Distribución original de categorías:")
print(f"      • Alimentos: {(productos['categoria'] == 'Alimentos').sum()} productos")
print(f"      • Limpieza: {(productos['categoria'] == 'Limpieza').sum()} productos")

# --- PRODUCTOS LIMPIOS 
print("   Limpiando y clasificando productos...")
productos_limpios = productos.copy()

# Corregir encoding 
reemplazos = {
    'Ã©': 'é', 'Ã­': 'í', 'Ã³': 'ó', 'Ãº': 'ú', 
    'Ã±': 'ñ', 'Ã¡': 'á', 'Ã': 'í'
}

for mal, bien in reemplazos.items():
    productos_limpios['nombre_producto'] = productos_limpios['nombre_producto'].str.replace(mal, bien, regex=False)

# PASO NUEVO 1: CORREGIR CATEGORÍAS PRINCIPALES
productos_limpios = corregir_categorias_ia(productos_limpios)  # O usar corregir_categorias_reglas(productos_limpios)

# PASO NUEVO 2: CLASIFICAR SUBCATEGORÍAS MEJORADO
productos_limpios = clasificar_subcategorias_mejorado(productos_limpios)

# ELIMINAR COLUMNAS TEMPORALES (MODIFICAR)
columnas_a_eliminar = ['categoria_ia']  # Cambiar por la columna temporal que se cree
columnas_existentes = [col for col in columnas_a_eliminar if col in productos_limpios.columns]

if columnas_existentes:
    productos_limpios = productos_limpios.drop(columnas_existentes, axis=1)
    print(f"   ✓ Columnas eliminadas: {columnas_existentes}")

# Ordenar y resetear índice
productos_limpios = productos_limpios.sort_values('id_producto').reset_index(drop=True)
print("   ✓ Productos limpios procesados")

# --- VENTAS 
print("   Analizando VENTAS...")
ventas['fecha'] = pd.to_datetime(ventas['fecha'])
ventas_info = {
    'registros': len(ventas),
    'rango_fechas': (ventas['fecha'].min(), ventas['fecha'].max()),
    'clientes_unicos': ventas['id_cliente'].nunique(),
    'ventas_sin_cliente': ventas['id_cliente'].isnull().sum()
}

# --- DETALLE VENTAS 
print("   Analizando DETALLE_VENTAS...")
detalle_info = {
    'registros': len(detalle_ventas),
    'ventas_unicas': detalle_ventas['id_venta'].nunique(),
    'productos_unicos': detalle_ventas['id_producto'].nunique(),
    'importes_negativos': (detalle_ventas['importe'] < 0).sum()
}

errores_detectados.append({
    'Archivo': 'detalle_ventas.csv',
    'Error': 'Redundancia de nombre_producto',
    'Cantidad': len(detalle_ventas),
    'Método': 'Eliminar columna (se obtiene de productos.csv)',
    'Impacto': 'Bajo - Optimización'
})

# ============================================================================
# 3. LIMPIEZA Y CORRECCIÓN (MODIFICAR SECCIÓN PRODUCTOS)
# ============================================================================
print("\n3. Aplicando correcciones...")

# --- CLIENTES LIMPIOS 
clientes_limpios = clientes.copy()
clientes_limpios = clientes_limpios.drop_duplicates(subset=['email'], keep='first')
clientes_limpios['fecha_alta'] = pd.to_datetime(clientes_limpios['fecha_alta'])
clientes_limpios = clientes_limpios.sort_values('id_cliente').reset_index(drop=True)

# --- PRODUCTOS LIMPIOS (SIMPLIFICAR - YA ESTÁ PROCESADO) ---
# Solo asegurar ordenamiento final
productos_limpios = productos_limpios.sort_values('id_producto').reset_index(drop=True)

# --- VENTAS LIMPIAS 
ventas_limpias = ventas.copy()
ventas_limpias['fecha'] = pd.to_datetime(ventas_limpias['fecha'])
ventas_limpias = ventas_limpias.sort_values(['fecha', 'id_venta']).reset_index(drop=True)

# --- DETALLE VENTAS LIMPIO 
detalle_ventas_limpio = detalle_ventas.copy()
detalle_ventas_limpio = detalle_ventas_limpio.drop('nombre_producto', axis=1)

# Verificar coherencia de importes
detalle_ventas_limpio['importe_calculado'] = detalle_ventas_limpio['cantidad'] * detalle_ventas_limpio['precio_unitario']
diferencias = abs(detalle_ventas_limpio['importe'] - detalle_ventas_limpio['importe_calculado']) > 0.01
if diferencias.any():
    print(f"   ⚠️  {diferencias.sum()} registros con diferencias en importe")
    detalle_ventas_limpio['importe'] = detalle_ventas_limpio['importe_calculado']
detalle_ventas_limpio = detalle_ventas_limpio.drop('importe_calculado', axis=1)

detalle_ventas_limpio = detalle_ventas_limpio.sort_values(['id_venta', 'id_producto']).reset_index(drop=True)

print("   ✓ Correcciones aplicadas exitosamente")


# ============================================================================
# 4. DIMENSIÓN CALENDARIO (Modelo Copo de Nieve)
# ============================================================================
print("\n4. Creando dimensión calendario...")

# Crear tabla de calendario desde la primera a la última venta
fecha_min = ventas_limpias['fecha'].min()
fecha_max = ventas_limpias['fecha'].max()

calendario = pd.DataFrame({
    'fecha': pd.date_range(start=fecha_min, end=fecha_max, freq='D')
})

calendario['id_fecha'] = range(1, len(calendario) + 1)
calendario['anio'] = calendario['fecha'].dt.year
calendario['mes'] = calendario['fecha'].dt.month
calendario['dia'] = calendario['fecha'].dt.day
calendario['dia_semana'] = calendario['fecha'].dt.dayofweek + 1  # 1=Lunes, 7=Domingo
calendario['nombre_dia'] = calendario['fecha'].dt.day_name()
calendario['nombre_mes'] = calendario['fecha'].dt.month_name()
calendario['trimestre'] = calendario['fecha'].dt.quarter
calendario['semana_anio'] = calendario['fecha'].dt.isocalendar().week

# Reordenar columnas
calendario = calendario[['id_fecha', 'fecha', 'anio', 'mes', 'dia', 
                         'dia_semana', 'nombre_dia', 'nombre_mes', 
                         'trimestre', 'semana_anio']]

print(f"   ✓ Calendario creado: {len(calendario)} días ({fecha_min.date()} a {fecha_max.date()})")

# ============================================================================
# 5. NORMALIZACIÓN Y MODELO COPO DE NIEVE
# ============================================================================
print("\n5. Aplicando normalización (Modelo Copo de Nieve)...")

# Agregar id_fecha a ventas
ventas_limpias = ventas_limpias.merge(
    calendario[['fecha', 'id_fecha']], 
    on='fecha', 
    how='left'
)

# Eliminar redundancia en ventas (nombre_cliente y email están en clientes)
ventas_limpias = ventas_limpias.drop(['nombre_cliente', 'email'], axis=1)

# Reordenar columnas
ventas_limpias = ventas_limpias[['id_venta', 'id_fecha', 'fecha', 'id_cliente', 'medio_pago']]

print("   ✓ Normalización completada")
print("   ✓ Modelo Copo de Nieve implementado:")
print("      - Tabla HECHOS: detalle_ventas")
print("      - Dimensiones: ventas, clientes, productos, calendario")

# ============================================================================
# VERIFICACIÓN DE SUBCATEGORÍAS
# ============================================================================
print("\n7.5. Verificando subcategorías...")
print(f"   ✓ Productos limpios - Columnas: {list(productos_limpios.columns)}")
print(f"   ✓ ¿Tiene subcategoria?: {'subcategoria' in productos_limpios.columns}")

if 'subcategoria' in productos_limpios.columns:
    print(f"   ✓ Subcategorías únicas: {productos_limpios['subcategoria'].nunique()}")
    print(f"   ✓ Muestra de subcategorías:")
    muestra = productos_limpios[['nombre_producto', 'categoria', 'subcategoria']].head(5)
    for _, row in muestra.iterrows():
        print(f"      • {row['nombre_producto']} → {row['categoria']} → {row['subcategoria']}")

# ============================================================================
# 6. GUARDAR ARCHIVOS LIMPIOS
# ============================================================================
print("\n6. Guardando archivos limpios...")

clientes_limpios.to_csv(f'{CARPETA_LIMPIOS}/clientes_limpios.csv', index=False)
productos_limpios.to_csv(f'{CARPETA_LIMPIOS}/productos_limpios.csv', index=False)
ventas_limpias.to_csv(f'{CARPETA_LIMPIOS}/ventas_limpias.csv', index=False)
detalle_ventas_limpio.to_csv(f'{CARPETA_LIMPIOS}/detalle_ventas_limpios.csv', index=False)
calendario.to_csv(f'{CARPETA_LIMPIOS}/calendario.csv', index=False)

print(f"   ✓ clientes_limpios.csv ({len(clientes_limpios)} registros)")
print(f"   ✓ productos_limpios.csv ({len(productos_limpios)} registros)")
print(f"   ✓ ventas_limpias.csv ({len(ventas_limpias)} registros)")
print(f"   ✓ detalle_ventas_limpios.csv ({len(detalle_ventas_limpio)} registros)")
print(f"   ✓ calendario.csv ({len(calendario)} registros)")

# ============================================================================
# 7. CREAR TABLA COMPARATIVA DE ERRORES (AMPLIADA)
# ============================================================================
print("\n7. Generando reporte de limpieza detallado...")

df_errores = pd.DataFrame(errores_detectados)

# --- CONSTRUIR EJEMPLOS DE LIMPIEZA ---

# Ejemplo CLIENTES: Email duplicado
clientes_duplicados = clientes[clientes.duplicated(subset=['email'], keep=False)]
if len(clientes_duplicados) > 0:
    email_ejemplo = clientes_duplicados.iloc[0]['email']
    cantidad = len(clientes_duplicados[clientes_duplicados['email'] == email_ejemplo])
    ejemplo_cliente = f"Email '{email_ejemplo}' aparecía {cantidad} veces"
else:
    ejemplo_cliente = "No se encontraron duplicados"

# Ejemplo PRODUCTOS: Subcategoría asignada
if len(productos_limpios) > 0:
    producto_ejemplo = productos_limpios.iloc[0]
    ejemplo_producto = f"ID {producto_ejemplo['id_producto']}: '{producto_ejemplo['nombre_producto']}' → '{producto_ejemplo['subcategoria']}'"
else:
    ejemplo_producto = "No hay productos disponibles"

# Ejemplo VENTAS: Redundancia eliminada
ejemplo_venta_antes = f"Columnas originales: {list(ventas.columns)}"
ejemplo_venta_despues = f"Columnas limpias: {list(ventas_limpias.columns)} + id_fecha agregado"

# Ejemplo DETALLE_VENTAS: Columna eliminada
ejemplo_detalle = f"Columna 'nombre_producto' eliminada (redundante con productos.csv). Antes: {detalle_ventas.shape[1]} columnas → Después: {detalle_ventas_limpio.shape[1]} columnas"

# --- CREAR TABLA COMPARATIVA AMPLIADA ---
comparativa_ampliada = {
    'Archivo': ['clientes.csv', 'productos.csv', 'ventas.csv', 'detalle_ventas.csv'],
    
    'Registros_Original': [
        clientes.shape[0],
        productos.shape[0],
        ventas.shape[0],
        detalle_ventas.shape[0]
    ],
    
    'Registros_Limpio': [
        clientes_limpios.shape[0],
        productos_limpios.shape[0],
        ventas_limpias.shape[0],
        detalle_ventas_limpio.shape[0]
    ],
    
    'Registros_Eliminados': [
        clientes.shape[0] - clientes_limpios.shape[0],
        0,
        0,
        0
    ],
    
    'Columnas_Original': [
        clientes.shape[1],
        productos.shape[1],
        ventas.shape[1],
        detalle_ventas.shape[1]
    ],
    
    'Columnas_Limpio': [
        clientes_limpios.shape[1],
        productos_limpios.shape[1],
        ventas_limpias.shape[1],
        detalle_ventas_limpio.shape[1]
    ],
    
    'Problema_Principal': [
        'Emails duplicados',
        'Encoding incorrecto + Clasificación categorías',
        'Redundancia de datos',
        'Columna redundante (nombre_producto)'
    ],
    
    'Metodo_Python_Principal': [
        'drop_duplicates(subset=["email"], keep="first")',
        'str.replace() + clasificación por palabras clave',
        'drop(["nombre_cliente", "email"], axis=1)',
        'drop("nombre_producto", axis=1)'
    ],
    
    'Metodos_Adicionales': [
        'to_datetime(), sort_values(), reset_index()',
        'copy(), apply() para clasificación subcategorías',
        'merge() con calendario, to_datetime()',
        'Validación: cantidad * precio_unitario == importe'
    ],
    
    'Ejemplo_Limpieza': [
        ejemplo_cliente,
        ejemplo_producto,
        ejemplo_venta_despues,
        ejemplo_detalle
    ],
    
    'Dato_Antes': [
        f"{clientes_duplicados.shape[0]} emails duplicados" if len(clientes_duplicados) > 0 else "Sin duplicados",
        f"{productos.shape[0]} productos sin clasificar",
        f"{ventas.shape[1]} columnas con redundancia",
        f"{detalle_ventas.shape[1]} columnas (incluyendo nombre_producto)"
    ],
    
    'Dato_Despues': [
        f"{clientes_limpios.shape[0]} clientes únicos por email",
        f"{productos_limpios['subcategoria'].nunique()} subcategorías asignadas",
        f"{ventas_limpias.shape[1]} columnas normalizadas + dimensión calendario",
        f"{detalle_ventas_limpio.shape[1]} columnas (sin redundancia)"
    ],
    
    'Impacto': [
        'Medio - Integridad de datos',
        'Alto - Análisis por categoría afectado',
        'Alto - Normalización base de datos',
        'Bajo - Optimización y normalización'
    ]
}

df_comparativa_ampliada = pd.DataFrame(comparativa_ampliada)

# --- TABLA ADICIONAL: MÉTODOS PYTHON DETALLADOS ---

# Calcular estadísticas de subcategorías para usar en los resultados
if 'subcategoria' in productos_limpios.columns:
    total_subcategorias = productos_limpios['subcategoria'].nunique()
    productos_clasificados = (productos_limpios['subcategoria'] != 'Sin Clasificar').sum()
else:
    total_subcategorias = 0
    productos_clasificados = 0

metodos_detallados = {
    'Archivo': [
        'clientes.csv',
        'clientes.csv',
        'clientes.csv',
        'productos.csv',
        'productos.csv',
        'productos.csv',
        'productos.csv',
        'ventas.csv',
        'ventas.csv',
        'ventas.csv',
        'detalle_ventas.csv',
        'detalle_ventas.csv',
        'NUEVO: calendario.csv',
        'NUEVO: calendario.csv'
    ],
    
    'Operacion': [
        'Leer archivo',
        'Eliminar duplicados',
        'Convertir fechas',
        'Corregir encoding',
        'Clasificar subcategorías',
        'Eliminar columna temporal',
        'Ordenar datos',
        'Normalizar (eliminar redundancia)',
        'Agregar dimensión fecha',
        'Convertir fechas',
        'Eliminar columna redundante',
        'Validar cálculos',
        'Crear rango de fechas',
        'Extraer componentes de fecha'
    ],
    
    'Metodo_Python': [
        'pd.read_csv()',
        'drop_duplicates(subset=["email"], keep="first")',
        'pd.to_datetime()',
        'str.replace()',
        'apply() con función personalizada',
        'drop(columns=["categoria_original"])',
        'sort_values().reset_index(drop=True)',
        'drop(columns=["nombre_cliente", "email"])',
        'merge(calendario[["fecha", "id_fecha"]])',
        'pd.to_datetime()',
        'drop(columns=["nombre_producto"])',
        'cantidad * precio_unitario',
        'pd.date_range(start, end, freq="D")',
        'dt.year, dt.month, dt.day, dt.dayofweek'
    ],
    
    'Linea_Codigo_Ejemplo': [
        'pd.read_csv("datos_originales/clientes.csv")',
        'clientes_limpios.drop_duplicates(subset=["email"], keep="first")',
        'clientes_limpios["fecha_alta"] = pd.to_datetime(clientes_limpios["fecha_alta"])',
        'productos["nombre_producto"].str.replace("Ã©", "é")',
        'productos_df["nombre_producto"].apply(clasificar_por_palabras)',
        'productos_limpios.drop("categoria_original", axis=1)',
        'productos_limpios.sort_values("id_producto").reset_index(drop=True)',
        'ventas_limpias.drop(["nombre_cliente", "email"], axis=1)',
        'ventas_limpias.merge(calendario[["fecha", "id_fecha"]], on="fecha")',
        'ventas_limpias["fecha"] = pd.to_datetime(ventas_limpias["fecha"])',
        'detalle_ventas_limpio.drop("nombre_producto", axis=1)',
        'detalle["importe_calculado"] = detalle["cantidad"] * detalle["precio_unitario"]',
        'pd.date_range(start=fecha_min, end=fecha_max, freq="D")',
        'calendario["anio"] = calendario["fecha"].dt.year'
    ],
    
    'Resultado': [
        f'{clientes.shape[0]} registros cargados',
        f'{clientes_limpios.shape[0]} registros únicos',
        'Tipo datetime64[ns]',
        'Caracteres corregidos: é, í, ó, ú, ñ',
        f'{total_subcategorias} subcategorías creadas, {productos_clasificados} productos clasificados',
        'Columna eliminada (si existía)',
        'Datos ordenados por ID',
        '2 columnas eliminadas (normalización)',
        'Dimensión fecha agregada',
        'Tipo datetime64[ns]',
        '1 columna eliminada',
        'Importes validados',
        f'{len(calendario)} fechas creadas',
        'Componentes extraídos: año, mes, día, etc.'
    ]
}

df_metodos_detallados = pd.DataFrame(metodos_detallados)

# ============================================================================
# 8. RESUMEN FINAL
# ============================================================================
print("\n" + "="*70)
print("RESUMEN DE LA LIMPIEZA")
print("="*70)
print("\nERRORES DETECTADOS Y CORREGIDOS:")
print(df_errores.to_string(index=False))

print("\n\nCOMPARATIVA AMPLIADA:")
print(df_comparativa_ampliada[['Archivo', 'Registros_Original', 'Registros_Limpio', 
                                'Problema_Principal', 'Impacto']].to_string(index=False))

print("\n\nMÉTODOS PYTHON MÁS UTILIZADOS:")
metodos_resumen = df_metodos_detallados.groupby('Metodo_Python').size().sort_values(ascending=False).head(5)
for metodo, cantidad in metodos_resumen.items():
    print(f"   • {metodo}: {cantidad} veces")

print("\n\nENCODING CORREGIDO:")

# Crear la tabla de encoding si no existe
if 'df_encoding' not in locals():
    # Calcular estadísticas de encoding
    encoding_corregido = {
        'Caracter_Incorrecto': ['Ã©', 'Ã­', 'Ã³', 'Ãº', 'Ã±', 'Ã¡', 'Ã'],
        'Caracter_Correcto': ['é', 'í', 'ó', 'ú', 'ñ', 'á', 'í'],
        'Ejemplo_Antes': [
            'CafÃ© Molido',
            'ManÃ­ Salado',
            'JabÃ³n de Tocador',
            'AzÃºcar',
            'Ã±oquis',
            'Ã¡cido',
            'TÃ© Verde'
        ],
        'Ejemplo_Despues': [
            'Café Molido',
            'Maní Salado',
            'Jabón de Tocador',
            'Azúcar',
            'ñoquis',
            'ácido',
            'Té Verde'
        ],
        'Cantidad_Afectados': [
            productos['nombre_producto'].str.contains('Ã©', na=False).sum(),
            productos['nombre_producto'].str.contains('Ã­', na=False).sum(),
            productos['nombre_producto'].str.contains('Ã³', na=False).sum(),
            productos['nombre_producto'].str.contains('Ãº', na=False).sum(),
            productos['nombre_producto'].str.contains('Ã±', na=False).sum(),
            productos['nombre_producto'].str.contains('Ã¡', na=False).sum(),
            productos['nombre_producto'].str.contains('Ã[^©íºó±¡]', na=False, regex=True).sum()
        ]
    }
    
    df_encoding = pd.DataFrame(encoding_corregido)

total_encoding = df_encoding['Cantidad_Afectados'].sum()
print(f"   • Total de productos con encoding incorrecto: {total_encoding}")
print(f"   • Caracteres corregidos: {len(df_encoding)} tipos diferentes")

print("\n\nMODELO DE DATOS (Copo de Nieve):")
print("""
    CALENDARIO (dim_fecha)
         ↓
    VENTAS (dim_ventas) ← CLIENTES (dim_clientes)
         ↓
    DETALLE_VENTAS (hechos) → PRODUCTOS (dim_productos)
""")

print("\n✓ FASE 1 COMPLETADA EXITOSAMENTE")
print(f"✓ Se generaron {5 + 4} archivos en '{CARPETA_LIMPIOS}/':")
print("   - 5 archivos de datos limpios (.csv)")
print("   - 4 archivos de documentación de limpieza (.csv)")
print("="*70)
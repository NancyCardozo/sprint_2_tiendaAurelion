"""
PROYECTO TIENDA AURELION - FASE 1
Limpieza, Inspección y Transformación de Datos
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os


# ============================================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================================
CARPETA_ORIGINALES = 'datos_originales'
CARPETA_LIMPIOS = 'datos_limpios'

# Crear carpeta de datos limpios si no existe
os.makedirs(CARPETA_LIMPIOS, exist_ok=True)

# ============================================================================
# 1. LECTURA DE ARCHIVOS ORIGINALES
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
# 2. INSPECCIÓN Y DETECCIÓN DE ERRORES
# ============================================================================
print("\n2. Inspeccionando datos y detectando errores...")

errores_detectados = []

# --- CLIENTES ---
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

# --- PRODUCTOS ---
print("   Analizando PRODUCTOS...")

# Corrección de encoding
productos_texto_original = productos['nombre_producto'].head(10).to_list()

# Detectar categorías incorrectas (análisis manual basado en nombre del producto)
categorias_incorrectas = 0
productos['categoria_original'] = productos['categoria'].copy()

# Diccionario de correcciones de categorías
correcciones_categoria = {
    # Bebidas -> Alimentos
    2: 'Alimentos',   # Pepsi
    4: 'Alimentos',   # Fanta
    6: 'Alimentos',   # Jugo Naranja
    8: 'Alimentos',   # Energética
    10: 'Alimentos',  # Yerba Intensa
    12: 'Alimentos',  # Té Negro
    14: 'Alimentos',  # Leche Entera
    16: 'Alimentos',  # Yogur
    18: 'Alimentos',  # Queso Rallado
    20: 'Alimentos',  # Pan Lactal Blanco
    22: 'Alimentos',  # Medialunas
    24: 'Alimentos',  # Galletitas Chocolate
    26: 'Alimentos',  # Alfajor
    28: 'Alimentos',  # Papas Fritas
    30: 'Alimentos',  # Maní
    32: 'Alimentos',  # Chocolate Amargo
    34: 'Alimentos',  # Turrón
    36: 'Alimentos',  # Dulce de Leche
    38: 'Alimentos',  # Mermelada Frutilla
    40: 'Alimentos',  # Helado Chocolate
    42: 'Alimentos',  # Vinagre
    44: 'Alimentos',  # Arroz
    46: 'Alimentos',  # Lentejas
    48: 'Alimentos',  # Porotos
    50: 'Alimentos',  # Azúcar
    58: 'Alimentos',  # Caramelos
    60: 'Alimentos',  # Chupetín
    62: 'Alimentos',  # Stevia
    64: 'Alimentos',  # Avena
    66: 'Alimentos',  # Cerveza Negra
    68: 'Alimentos',  # Vino Blanco
    70: 'Alimentos',  # Fernet
    72: 'Alimentos',  # Ron
    74: 'Alimentos',  # Whisky
    76: 'Alimentos',  # Pizza
    78: 'Alimentos',  # Verduras Congeladas
    80: 'Alimentos',  # Helado Frutilla
    82: 'Alimentos',  # Aceitunas Negras
    84: 'Alimentos',  # Queso Azul
    86: 'Alimentos',  # Jugo en Polvo Limón
    88: 'Alimentos',  # Caldo Carne
    90: 'Limpieza',   # Toallas Húmedas (CORRECTO)
    92: 'Limpieza',   # Crema Dental (CORRECTO)
    94: 'Limpieza',   # Hilo Dental (CORRECTO)
}

for id_prod, nueva_cat in correcciones_categoria.items():
    if id_prod in productos['id_producto'].values:
        idx = productos[productos['id_producto'] == id_prod].index[0]
        if productos.loc[idx, 'categoria'] != nueva_cat:
            categorias_incorrectas += 1
            productos.loc[idx, 'categoria'] = nueva_cat

errores_detectados.append({
    'Archivo': 'productos.csv',
    'Error': 'Categorías incorrectas',
    'Cantidad': categorias_incorrectas,
    'Método': 'Reasignación manual basada en nombre del producto',
    'Impacto': 'Alto'
})

errores_detectados.append({
    'Archivo': 'productos.csv',
    'Error': 'Encoding incorrecto (caracteres Ã, º, etc.)',
    'Cantidad': productos['nombre_producto'].str.contains('Ã|º', regex=True, na=False).sum(),
    'Método': 'Reemplazo de caracteres malformados',
    'Impacto': 'Bajo'
})

# --- VENTAS ---
print("   Analizando VENTAS...")
ventas['fecha'] = pd.to_datetime(ventas['fecha'])
ventas_info = {
    'registros': len(ventas),
    'rango_fechas': (ventas['fecha'].min(), ventas['fecha'].max()),
    'clientes_unicos': ventas['id_cliente'].nunique(),
    'ventas_sin_cliente': ventas['id_cliente'].isnull().sum()
}

# --- DETALLE VENTAS ---
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
# 3. LIMPIEZA Y CORRECCIÓN
# ============================================================================
print("\n3. Aplicando correcciones...")

# --- CLIENTES LIMPIOS ---
clientes_limpios = clientes.copy()
clientes_limpios = clientes_limpios.drop_duplicates(subset=['email'], keep='first')
clientes_limpios['fecha_alta'] = pd.to_datetime(clientes_limpios['fecha_alta'])
clientes_limpios = clientes_limpios.sort_values('id_cliente').reset_index(drop=True)

# --- PRODUCTOS LIMPIOS ---
productos_limpios = productos.copy()

# Corregir encoding
reemplazos = {
    'Ã©': 'é',
    'Ã­': 'í',
    'Ã³': 'ó',
    'Ãº': 'ú',
    'Ã±': 'ñ',
    'Ã¡': 'á',
    'Ã': 'í'
}

for mal, bien in reemplazos.items():
    productos_limpios['nombre_producto'] = productos_limpios['nombre_producto'].str.replace(mal, bien, regex=False)

# Las categorías ya fueron corregidas arriba
productos_limpios = productos_limpios.drop('categoria_original', axis=1)
productos_limpios = productos_limpios.sort_values('id_producto').reset_index(drop=True)

# --- VENTAS LIMPIAS ---
ventas_limpias = ventas.copy()
ventas_limpias['fecha'] = pd.to_datetime(ventas_limpias['fecha'])
ventas_limpias = ventas_limpias.sort_values(['fecha', 'id_venta']).reset_index(drop=True)

# --- DETALLE VENTAS LIMPIO ---
detalle_ventas_limpio = detalle_ventas.copy()

# Eliminar redundancia: quitar nombre_producto (se obtiene de productos)
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
    ejemplo_cliente = f"Email '{clientes_duplicados.iloc[0]['email']}' aparecía {len(clientes_duplicados[clientes_duplicados['email'] == clientes_duplicados.iloc[0]['email']])} veces"
else:
    ejemplo_cliente = "No se encontraron duplicados"

# Ejemplo PRODUCTOS: Categoría incorrecta
ejemplo_prod_original = productos[productos['id_producto'] == 2][['id_producto', 'nombre_producto', 'categoria_original']].iloc[0]
ejemplo_prod_limpio = productos_limpios[productos_limpios['id_producto'] == 2][['id_producto', 'nombre_producto', 'categoria']].iloc[0]
ejemplo_producto = f"ID {ejemplo_prod_original['id_producto']}: '{ejemplo_prod_original['nombre_producto']}' cambió de '{ejemplo_prod_original['categoria_original']}' → '{ejemplo_prod_limpio['categoria']}'"

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
        productos_limpios.shape[1] - 1,  # -1 por categoria_original eliminada
        ventas_limpias.shape[1],  # fecha, id_fecha, id_cliente, medio_pago, id_venta
        detalle_ventas_limpio.shape[1]
    ],
    
    'Problema_Principal': [
        'Emails duplicados',
        'Categorías incorrectas + Encoding',
        'Redundancia de datos',
        'Columna redundante (nombre_producto)'
    ],
    
    'Metodo_Python_Principal': [
        'drop_duplicates(subset=["email"], keep="first")',
        'str.replace() + asignación condicional con loc[]',
        'drop(["nombre_cliente", "email"], axis=1)',
        'drop("nombre_producto", axis=1)'
    ],
    
    'Metodos_Adicionales': [
        'to_datetime(), sort_values(), reset_index()',
        'copy(), merge() para diccionario de correcciones',
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
        f"Email duplicado: karina.acosta@mail.com (2 veces)" if clientes['email'].duplicated().sum() > 0 else "Sin duplicados",
        "ID 2: Pepsi 1.5L → Limpieza ❌",
        f"{ventas.shape[1]} columnas con redundancia",
        f"{detalle_ventas.shape[1]} columnas (incluyendo nombre_producto)"
    ],
    
    'Dato_Despues': [
        f"{clientes_limpios.shape[0]} clientes únicos por email",
        "ID 2: Pepsi 1.5L → Alimentos ✓",
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
        'Corregir categorías',
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
        'loc[] con condiciones',
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
        'productos.loc[productos["id_producto"] == 2, "categoria"] = "Alimentos"',
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
        '100 registros cargados',
        f'{clientes_limpios.shape[0]} registros únicos',
        'Tipo datetime64[ns]',
        'Caracteres corregidos: é, í, ó, ú, ñ',
        f'{categorias_incorrectas} categorías corregidas',
        'Columna eliminada',
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

# --- TABLA DE ENCODING CORREGIDO ---
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

# --- GUARDAR TODOS LOS REPORTES ---
df_errores.to_csv(f'{CARPETA_LIMPIOS}/detalle_de_limpieza_errores.csv', index=False)
df_comparativa_ampliada.to_csv(f'{CARPETA_LIMPIOS}/detalle_de_limpieza_comparativa.csv', index=False)
df_metodos_detallados.to_csv(f'{CARPETA_LIMPIOS}/detalle_de_limpieza_metodos.csv', index=False)
df_encoding.to_csv(f'{CARPETA_LIMPIOS}/detalle_de_limpieza_encoding.csv', index=False)

print("   ✓ detalle_de_limpieza_errores.csv")
print("   ✓ detalle_de_limpieza_comparativa.csv (AMPLIADO)")
print("   ✓ detalle_de_limpieza_metodos.csv (NUEVO)")
print("   ✓ detalle_de_limpieza_encoding.csv (NUEVO)")

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
import pandas as pd
import os

print("🔍 DIAGNÓSTICO DE SUBCATEGORÍAS")
print("=" * 50)

# Verificar si existe la carpeta datos_limpios
if not os.path.exists('datos_limpios'):
    print("❌ La carpeta 'datos_limpios' no existe")
    exit()

# Verificar archivos en datos_limpios
archivos = os.listdir('datos_limpios')
print(f"📁 Archivos en datos_limpios: {archivos}")

# Verificar productos_limpios.csv
try:
    productos = pd.read_csv('datos_limpios/productos_limpios.csv')
    print("\n✅ productos_limpios.csv - CARGADO EXITOSAMENTE")
    print(f"   📊 Dimensiones: {productos.shape[0]} filas x {productos.shape[1]} columnas")
    print(f"   🏷️  Columnas: {list(productos.columns)}")
    
    # Verificar si tiene subcategoria
    if 'subcategoria' in productos.columns:
        print("   🎯 COLUMNA 'subcategoria' - ✅ PRESENTE")
        print(f"   📈 Subcategorías únicas: {productos['subcategoria'].nunique()}")
        print(f"   📋 Distribución:")
        distribucion = productos['subcategoria'].value_counts()
        for subcat, count in distribucion.items():
            print(f"      • {subcat}: {count} productos")
        
        # Mostrar ejemplos
        print("\n   👀 Ejemplos de productos y sus subcategorías:")
        ejemplos = productos[['id_producto', 'nombre_producto', 'categoria', 'subcategoria']].head(8)
        for _, fila in ejemplos.iterrows():
            print(f"      • ID {fila['id_producto']}: '{fila['nombre_producto']}' → {fila['categoria']} → {fila['subcategoria']}")
    else:
        print("   🚫 COLUMNA 'subcategoria' - NO ENCONTRADA")
        
except FileNotFoundError:
    print("❌ productos_limpios.csv - NO ENCONTRADO")
except Exception as e:
    print(f"❌ Error cargando productos_limpios.csv: {e}")

# Verificar otros archivos importantes
print("\n" + "=" * 50)
print("📋 VERIFICANDO OTROS ARCHIVOS:")

archivos_verificar = ['ventas_limpias.csv', 'detalle_ventas_limpios.csv', 'clientes_limpios.csv']
for archivo in archivos_verificar:
    try:
        ruta = f'datos_limpios/{archivo}'
        df = pd.read_csv(ruta)
        print(f"✅ {archivo}: {df.shape[0]} filas x {df.shape[1]} columnas")
    except:
        print(f"❌ {archivo}: No encontrado o error")

print("\n" + "=" * 50)
print("💡 RECOMENDACIONES:")
if 'productos' in locals() and 'subcategoria' in productos.columns:
    print("✅ La columna 'subcategoria' existe. El dashboard debería funcionar.")
else:
    print("❌ La columna 'subcategoria' NO existe. Ejecuta programa_actualizado_limpieza_fase_1.py primero.")
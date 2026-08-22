# procesar.py
import pandas as pd

def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Limpieza básica: eliminar nulos, convertir fechas, etc."""
    df = df.copy()
    # Intentar convertir columna de fecha si existe
    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    # Eliminar filas con nulos en columnas clave
    columnas_clave = ['fecha', 'producto', 'venta']  # ajustar según dataset
    df = df.dropna(subset=[col for col in columnas_clave if col in df.columns])
    return df

def obtener_resumen(df: pd.DataFrame) -> dict:
    """
    Calcula métricas básicas y devuelve un diccionario.
    """
    resumen = {}
    
    # Ventas totales (suma de 'venta')
    if 'venta' in df.columns:
        resumen['total_ventas'] = df['venta'].sum()
    else:
        resumen['total_ventas'] = None
    
    # Productos más y menos vendidos (por cantidad o monto)
    if 'producto' in df.columns and 'venta' in df.columns:
        ventas_por_producto = df.groupby('producto')['venta'].sum().sort_values(ascending=False)
        resumen['top_productos'] = ventas_por_producto.head(5).to_dict()
        resumen['bottom_productos'] = ventas_por_producto.tail(5).to_dict()
    elif 'producto' in df.columns and 'cantidad' in df.columns:
        cant_por_producto = df.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
        resumen['top_productos'] = cant_por_producto.head(5).to_dict()
        resumen['bottom_productos'] = cant_por_producto.tail(5).to_dict()
    else:
        resumen['top_productos'] = {}
        resumen['bottom_productos'] = {}
    
    # Ventas por mes (si hay fecha)
    if 'fecha' in df.columns and 'venta' in df.columns:
        df['mes'] = df['fecha'].dt.to_period('M').astype(str)
        ventas_por_mes = df.groupby('mes')['venta'].sum()
        resumen['ventas_por_mes'] = ventas_por_mes.to_dict()
    else:
        resumen['ventas_por_mes'] = {}
    
    # Ventas por categoría
    if 'categoria' in df.columns and 'venta' in df.columns:
        ventas_por_categoria = df.groupby('categoria')['venta'].sum().sort_values(ascending=False)
        resumen['ventas_por_categoria'] = ventas_por_categoria.to_dict()
    else:
        resumen['ventas_por_categoria'] = {}
    
    # Ventas por sede
    if 'sede' in df.columns and 'venta' in df.columns:
        ventas_por_sede = df.groupby('sede')['venta'].sum().sort_values(ascending=False)
        resumen['ventas_por_sede'] = ventas_por_sede.to_dict()
    else:
        resumen['ventas_por_sede'] = {}
    
    return resumen
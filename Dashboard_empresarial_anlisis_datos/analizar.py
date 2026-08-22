"""Cálculo de indicadores y respuestas empresariales."""

import pandas as pd


def datos_grafico(df: pd.DataFrame, eje_x: str, eje_y: str) -> list[dict]:
    """Agrega los datos para cualquier combinación válida de ejes."""
    datos = df.copy()
    if eje_x == "fecha":
        datos["fecha"] = pd.to_datetime(datos["fecha"], dayfirst=True, errors="coerce").dt.strftime("%Y-%m-%d")
    elif eje_x == "mes":
        datos["mes"] = pd.to_datetime(datos["fecha"], dayfirst=True, errors="coerce").dt.to_period("M").astype(str)
    if eje_x not in datos.columns or eje_y not in datos.columns:
        return []
    agrupado = datos.dropna(subset=[eje_x, eje_y]).groupby(eje_x, as_index=False)[eje_y].sum()
    return [{eje_x: str(fila[eje_x]), eje_y: float(fila[eje_y])} for _, fila in agrupado.iterrows()]


def _agrupado(df: pd.DataFrame, columna: str, medida: str) -> pd.Series:
    if columna not in df.columns or medida not in df.columns:
        return pd.Series(dtype=float)
    return df.groupby(columna)[medida].sum().sort_values(ascending=False)


def analizar_datos(df: pd.DataFrame) -> dict:
    """Genera KPIs, rankings y conclusiones a partir de los datos normalizados."""
    venta = pd.to_numeric(df.get("venta", pd.Series(dtype=float)), errors="coerce").fillna(0)
    cantidad = pd.to_numeric(df.get("cantidad", pd.Series(dtype=float)), errors="coerce").fillna(0)
    medida_producto = "cantidad" if "cantidad" in df.columns else "venta"
    producto = _agrupado(df, "producto", medida_producto)
    por_categoria = _agrupado(df, "categoria", "venta")
    por_sede = _agrupado(df, "sede", "venta")

    por_mes = pd.Series(dtype=float)
    if "fecha" in df.columns:
        temporal = df.assign(mes=df["fecha"].dt.to_period("M").astype(str))
        por_mes = _agrupado(temporal, "mes", "venta")

    producto_top = str(producto.index[0]) if not producto.empty else "Sin datos"
    producto_bajo = str(producto.index[-1]) if not producto.empty else "Sin datos"
    categoria_top = str(por_categoria.index[0]) if not por_categoria.empty else "Sin datos"
    mes_top = str(por_mes.index[0]) if not por_mes.empty else "Sin datos"
    sede_top = str(por_sede.index[0]) if not por_sede.empty else "Sin datos"

    return {
        "total_ventas": float(venta.sum()),
        "transacciones": int(len(df)),
        "productos_vendidos": int(cantidad.sum()) if "cantidad" in df.columns else int(len(df)),
        "promedio_venta": float(venta.mean()) if len(venta) else 0.0,
        "producto_mas_vendido": producto_top,
        "producto_menos_vendido": producto_bajo,
        "categoria_mayor_venta": categoria_top,
        "mes_mayor_venta": mes_top,
        "sede_mayor_venta": sede_top,
        "ventas_por_mes": por_mes.to_dict(),
        "ventas_por_categoria": por_categoria.to_dict(),
        "ventas_por_sede": por_sede.to_dict(),
        "ventas_por_producto": producto.to_dict(),
        "cantidad_por_categoria": _agrupado(df, "categoria", "cantidad").to_dict(),
        "filas": int(len(df)),
        "columnas": int(len(df.columns)),
    }


def generar_interpretacion(resumen: dict) -> dict[str, str]:
    """Convierte los indicadores principales en decisiones empresariales."""
    return {
        "stock": f"{resumen['producto_mas_vendido']} concentra la mayor demanda registrada.",
        "stock_decision": f"Priorizar el stock de {resumen['producto_mas_vendido']} y revisar su nivel de reposición.",
        "categoria": f"{resumen['categoria_mayor_venta']} es la categoría con mayor facturación.",
        "categoria_decision": f"Evaluar mayor inversión comercial en {resumen['categoria_mayor_venta']}.",
        "sede": f"{resumen['sede_mayor_venta']} lidera las ventas entre las sedes disponibles.",
        "sede_decision": f"Comparar las prácticas de {resumen['sede_mayor_venta']} con las sedes de menor rendimiento.",
    }
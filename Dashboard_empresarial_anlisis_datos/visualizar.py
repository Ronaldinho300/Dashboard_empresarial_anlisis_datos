# visualizar.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Paleta alineada con el tema oscuro tipo terminal de trading de la interfaz.
BG_PANEL = "#0F1620"
GRID = "#1C2836"
TEXT_MUTED = "#8A97AA"
ACCENT = "#22D3B8"
ACCENT_AMBER = "#F0B429"
ACCENT_VIOLET = "#8B7CF6"
ACCENT_BLUE = "#4F8CFF"
POSITIVE = "#2ED47A"
NEGATIVE = "#F4574F"
PALETA_DISCRETA = [ACCENT, ACCENT_AMBER, ACCENT_VIOLET, ACCENT_BLUE, POSITIVE, "#E879F9", "#FB923C"]


def _aplicar_tema(fig: go.Figure) -> go.Figure:
    """Aplica la paleta oscura del dashboard a cualquier figura Plotly."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=BG_PANEL,
        plot_bgcolor=BG_PANEL,
        font={"color": TEXT_MUTED, "family": "'JetBrains Mono', monospace", "size": 12},
        title_font={"color": "#E7ECF3", "family": "'Space Grotesk', sans-serif", "size": 15},
        colorway=PALETA_DISCRETA,
        margin=dict(t=60, l=20, r=20, b=40),
        legend={"bgcolor": "rgba(0,0,0,0)"},
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID)
    return fig


def plotly_to_html(fig) -> str:
    """Convierte una figura Plotly a un fragmento HTML autosuficiente (para reportes)."""
    return pio.to_html(fig, full_html=False, config={"displayModeBar": False})


def _agrupar(datos: pd.DataFrame, eje_x: str, eje_y: str) -> pd.DataFrame:
    """Agrupa los datos y decide el orden más útil según el tipo de eje X."""
    agrupado = datos.groupby(eje_x, as_index=False)[eje_y].sum()
    if eje_x in ("fecha", "fecha_str", "mes"):
        # Series temporales: orden cronológico.
        agrupado = agrupado.sort_values(eje_x)
    else:
        # producto / categoria / sede: de mayor a menor venta, así el
        # "más vendido" / "menos vendido" se lee directo del gráfico.
        agrupado = agrupado.sort_values(eje_y, ascending=False)
    return agrupado


def _figura_vacia(mensaje: str) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        title="",
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[{
            "text": mensaje, "xref": "paper", "yref": "paper",
            "showarrow": False, "font": {"size": 15, "color": TEXT_MUTED},
        }],
    )
    return _aplicar_tema(fig)


def _preparar_eje(datos: pd.DataFrame, eje_x: str) -> tuple[pd.DataFrame, str]:
    """Convierte fechas a mes/fecha para que el eje de gráfico siempre tenga valores válidos."""
    datos = datos.copy()
    if "fecha" in datos.columns:
        datos["fecha"] = pd.to_datetime(datos["fecha"], dayfirst=True, errors="coerce")
    if eje_x == "fecha" and "fecha" in datos.columns:
        datos["fecha_str"] = datos["fecha"].dt.strftime("%Y-%m-%d")
        return datos, "fecha_str"
    if eje_x == "mes" and "fecha" in datos.columns:
        datos["mes"] = datos["fecha"].dt.to_period("M").astype(str)
        return datos, "mes"
    return datos, eje_x


def resumen_estadistico_grafico(df: pd.DataFrame, eje_x: str, eje_y: str) -> list[dict]:
    """Devuelve el resumen estadístico del eje Y para la combinación seleccionada."""
    datos, eje_x_real = _preparar_eje(df, eje_x)
    if eje_x_real not in datos.columns or eje_y not in datos.columns:
        return [
            {"titulo": "Máximo", "valor": "N/A"},
            {"titulo": "Mínimo", "valor": "N/A"},
            {"titulo": "Media", "valor": "N/A"},
            {"titulo": "Moda", "valor": "N/A"},
        ]

    agregado = _agrupar(datos, eje_x_real, eje_y)
    if agregado.empty:
        return [
            {"titulo": "Máximo", "valor": "N/A"},
            {"titulo": "Mínimo", "valor": "N/A"},
            {"titulo": "Media", "valor": "N/A"},
            {"titulo": "Moda", "valor": "N/A"},
        ]

    serie = pd.to_numeric(agregado[eje_y], errors="coerce").dropna()
    if serie.empty:
        return [
            {"titulo": "Máximo", "valor": "N/A"},
            {"titulo": "Mínimo", "valor": "N/A"},
            {"titulo": "Media", "valor": "N/A"},
            {"titulo": "Moda", "valor": "N/A"},
        ]

    moda = serie.mode()
    return [
        {"titulo": "Máximo", "valor": f"{serie.max():,.2f}"},
        {"titulo": "Mínimo", "valor": f"{serie.min():,.2f}"},
        {"titulo": "Media", "valor": f"{serie.mean():,.2f}"},
        {"titulo": "Moda", "valor": f"{moda.iloc[0]:,.2f}" if not moda.empty else "N/A"},
    ]


def crear_figura_interactiva(df: pd.DataFrame, tipo: str, eje_x: str, eje_y: str) -> go.Figure:
    """Crea y devuelve una figura Plotly (objeto go.Figure) según el tipo y los ejes elegidos.

    Se devuelve el objeto de figura (no HTML) para poder renderizarlo con
    rx.plotly, que sí ejecuta correctamente los gráficos interactivos en Reflex.
    """
    datos = df.copy()
    if datos.empty:
        return _figura_vacia("No hay datos para la combinación seleccionada")

    if "fecha" in datos.columns:
        datos["fecha"] = pd.to_datetime(datos["fecha"], dayfirst=True, errors="coerce")

    if eje_x == "fecha" and "fecha" in datos.columns:
        datos["fecha_str"] = datos["fecha"].dt.strftime("%Y-%m-%d")
        eje_x = "fecha_str"

    if eje_x == "mes" and "fecha" in datos.columns:
        datos["mes"] = datos["fecha"].dt.to_period("M").astype(str)

    if eje_x not in datos.columns or eje_y not in datos.columns:
        return _figura_vacia("No hay datos para la combinación seleccionada")

    if tipo == "velas":
        if "precio" not in datos.columns:
            return _figura_vacia("Se requiere la columna 'precio' para velas japonesas")
        datos["fecha"] = pd.to_datetime(datos["fecha"], dayfirst=True, errors="coerce")
        datos["precio"] = pd.to_numeric(datos["precio"], errors="coerce")
        datos = datos.dropna(subset=["fecha", "precio"])
        if datos.empty:
            return _figura_vacia("No hay datos suficientes para velas japonesas")
        ohlc = datos.groupby(datos["fecha"].dt.date)["precio"].agg(
            apertura="first", maximo="max", minimo="min", cierre="last"
        ).reset_index(names="fecha")
        fig = go.Figure(go.Candlestick(
            x=ohlc["fecha"], open=ohlc["apertura"], high=ohlc["maximo"],
            low=ohlc["minimo"], close=ohlc["cierre"], name="Precio",
            increasing_line_color=POSITIVE, decreasing_line_color=NEGATIVE,
        ))
        fig.update_layout(title="Velas japonesas", xaxis_rangeslider_visible=False)
        return _aplicar_tema(fig)

    if tipo == "cascada":
        if "fecha" not in datos.columns:
            return _figura_vacia("La cascada requiere la columna 'fecha'")
        datos["fecha"] = pd.to_datetime(datos["fecha"], dayfirst=True, errors="coerce")
        datos["mes"] = datos["fecha"].dt.to_period("M").astype(str)
        serie = datos.groupby("mes")[eje_y].sum().sort_index()
        if serie.empty:
            return _figura_vacia("No hay datos suficientes para la cascada")
        variaciones = serie.diff().fillna(serie.iloc[0])
        medidas = ["relative"] * len(variaciones)
        medidas[0] = "absolute"
        fig = go.Figure(go.Waterfall(
            x=variaciones.index.tolist(), y=variaciones.tolist(), measure=medidas,
            text=[f"{v:,.2f}" for v in variaciones], textposition="outside",
            connector={"line": {"color": GRID}},
            increasing={"marker": {"color": POSITIVE}},
            decreasing={"marker": {"color": NEGATIVE}},
            totals={"marker": {"color": ACCENT_AMBER}},
        ))
        fig.update_layout(title=f"Variación de {eje_y} por mes", showlegend=False)
        return _aplicar_tema(fig)

    # Para líneas, barras y cualquier otra combinación de ejes.
    agrupado = _agrupar(datos, eje_x, eje_y)
    if agrupado.empty:
        return _figura_vacia("No hay datos para la combinación seleccionada")

    if tipo == "lineas":
        fig = px.line(
            agrupado, x=eje_x, y=eje_y, title=f"Evolución de {eje_y} por {eje_x}", markers=True,
            color_discrete_sequence=[ACCENT],
        )
        fig.update_traces(line_color=ACCENT, marker={"color": ACCENT_AMBER, "size": 7})
    else:  # "barras" (y cualquier valor no reconocido, por defecto)
        fig = px.bar(
            agrupado, x=eje_x, y=eje_y, title=f"{eje_y} por {eje_x}", text_auto=True, color=eje_x,
            color_discrete_sequence=PALETA_DISCRETA,
        )
    return _aplicar_tema(fig)

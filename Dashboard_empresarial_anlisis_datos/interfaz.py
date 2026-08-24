"""Componentes visuales — estilo terminal de trading, navegación por iconos."""
import reflex as rx
from Dashboard_empresarial_anlisis_datos.estado import State
from Dashboard_empresarial_anlisis_datos.estilos import (
    ACCENT, ACCENT_AMBER, ACCENT_BLUE, ACCENT_VIOLET, BG_DEEP, BG_PANEL, BG_RAISED,
    BORDER, FONT_DISPLAY, FONT_MONO, LABEL_STYLE, MONO_NUM_STYLE, NEGATIVE, PANEL_STYLE,
    POSITIVE, TEXT_MUTED, TEXT_PRIMARY,
)

SECCIONES = [
    ("carga", "cloud_upload", "Cargar datos"),
    ("resumen", "gauge", "Resumen ejecutivo"),
    ("graficos", "chart_candlestick", "Gráficos"),
    ("analisis", "brain_circuit", "Análisis"),
    ("datos", "table_2", "Datos"),
    ("reportes", "receipt_text", "Reportes"),
]


# ---------------------------------------------------------------- utilidades

def panel_header(icon: str, titulo: str) -> rx.Component:
    return rx.hstack(
        rx.icon(tag=icon, size=18, color=ACCENT),
        rx.heading(titulo, style={"font_family": FONT_DISPLAY, "font_size": "1.15rem", "color": TEXT_PRIMARY}),
        spacing="2", align="center", margin_bottom="0.3em",
    )


def estado_vacio(mensaje: str, icon: str = "inbox") -> rx.Component:
    return rx.vstack(
        rx.icon(tag=icon, size=30, color=TEXT_MUTED),
        rx.text(mensaje, style={"color": TEXT_MUTED, "font_size": "0.9rem"}),
        align="center", justify="center", spacing="3",
        style={"height": "45vh", "width": "100%"},
    )


def kpi(icon: str, titulo: str, valor, accent: str = ACCENT, on_click=None) -> rx.Component:
    contenido = rx.box(
        rx.hstack(
            rx.icon(tag=icon, size=14, color=accent),
            rx.text(titulo, style=LABEL_STYLE),
            spacing="2", align="center",
        ),
        rx.text(valor, style=MONO_NUM_STYLE, margin_top="0.35em"),
        style={
            **PANEL_STYLE,
            "padding": "0.9em 1.1em",
            "border_left": f"2px solid {accent}",
            "min_width": "185px",
            "flex": "1",
            "cursor": "pointer" if on_click else "default",
        },
    )
    if on_click is None:
        return contenido
    return rx.box(contenido, on_click=on_click, style={"width": "100%"})


# --------------------------------------------------------------- navegación

def nav_icon(vista: str, icon: str, tooltip: str) -> rx.Component:
    activo = State.vista_activa == vista
    return rx.tooltip(
        rx.box(
            rx.icon(tag=icon, size=19, color=rx.cond(activo, ACCENT, TEXT_MUTED)),
            on_click=lambda: State.set_vista_activa(vista),
            style={
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
                "width": "42px",
                "height": "42px",
                "border_radius": "10px",
                "background": rx.cond(activo, "rgba(34, 211, 184, 0.12)", "transparent"),
                "border_left": rx.cond(activo, f"2px solid {ACCENT}", "2px solid transparent"),
                "cursor": "pointer",
                "transition": "background 0.15s ease",
                "_hover": {"background": BG_RAISED},
            },
        ),
        content=tooltip,
        side="right",
    )


def barra_lateral() -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.icon(tag="zap", size=20, color=ACCENT),
            style={"padding": "1em 0 0.6em 0", "display": "flex", "justify_content": "center"},
        ),
        rx.divider(style={"border_color": BORDER, "width": "60%"}),
        rx.vstack(
            *[nav_icon(vista, icono, texto) for vista, icono, texto in SECCIONES],
            spacing="2", padding_top="0.8em",
        ),
        rx.spacer(),
        rx.tooltip(
            rx.box(rx.color_mode.button(), style={"opacity": "0.55"}),
            content="Modo de color",
            side="right",
        ),
        align="center",
        spacing="2",
        style={
            "width": "64px",
            "min_width": "64px",
            "height": "100vh",
            "position": "sticky",
            "top": "0",
            "background": BG_PANEL,
            "border_right": f"1px solid {BORDER}",
            "padding_bottom": "1em",
        },
    )


def barra_superior() -> rx.Component:
    return rx.hstack(
        rx.icon(tag=rx.match(
            State.vista_activa,
            *[(vista, icono) for vista, icono, _ in SECCIONES],
            "layout_dashboard",
        ), size=16, color=TEXT_MUTED),
        rx.heading(
            "DASHBOARD EMPRESARIAL",
            style={
                "font_family": FONT_DISPLAY, "font_size": "0.95rem",
                "letter_spacing": "0.05em", "color": TEXT_PRIMARY,
            },
        ),
        rx.spacer(),
        rx.cond(
            State.archivo_seleccionado != "",
            rx.hstack(
                rx.icon(tag="database", size=13, color=TEXT_MUTED),
                rx.text(State.archivo_seleccionado, style={
                    "font_family": FONT_MONO, "font_size": "0.76rem", "color": TEXT_MUTED,
                }),
                spacing="1", align="center",
                style={
                    "background": BG_RAISED, "border": f"1px solid {BORDER}",
                    "border_radius": "999px", "padding": "0.3em 0.9em",
                },
            ),
        ),
        align="center", spacing="3",
        style={
            "width": "100%", "padding": "0.95em 1.6em",
            "border_bottom": f"1px solid {BORDER}", "background": BG_DEEP,
            "position": "sticky", "top": "0", "z_index": "10",
        },
    )


# ------------------------------------------------------------------ paneles

def ventana_carga() -> rx.Component:
    return rx.vstack(
        panel_header("cloud_upload", "Cargar y validar"),
        rx.text("Selecciona un archivo CSV o Excel para iniciar el análisis.", style={"color": TEXT_MUTED, "font_size": "0.85rem"}),
        rx.upload(
            rx.vstack(
                rx.icon(tag="hard_drive_upload", size=32, color=ACCENT),
                rx.text("Arrastra o selecciona un archivo", style={"color": TEXT_PRIMARY, "font_size": "0.85rem"}),
                rx.text(".csv · .xlsx · .xls", style={"color": TEXT_MUTED, "font_size": "0.72rem"}),
                spacing="2", align="center",
            ),
            style={
                "border": f"1.5px dashed {BORDER}", "border_radius": "12px",
                "padding": "2.4em", "width": "100%", "background": BG_PANEL,
                "_hover": {"border_color": ACCENT},
            },
            accept={
                "text/csv": [".csv"],
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
                "application/vnd.ms-excel": [".xls"],
            },
            multiple=False, on_drop=State.handle_upload,
        ),
        rx.cond(
            State.archivos.length() > 0,
            rx.vstack(
                rx.text("Archivos guardados", style=LABEL_STYLE),
                rx.select(
                    State.archivos,
                    value=State.archivo_seleccionado,
                    placeholder="Selecciona un archivo para analizar",
                    on_change=State.seleccionar_archivo,
                    width="100%",
                ),
                width="100%", spacing="2", margin_top="0.6em",
            ),
        ),
        rx.cond(State.message, rx.hstack(
            rx.icon(tag="circle_dot", size=13, color=ACCENT),
            rx.text(State.message, style={"color": TEXT_MUTED, "font_size": "0.82rem"}),
            align="center", spacing="2",
        )),
        width="100%", spacing="4", style=PANEL_STYLE,
    )


def ventana_resumen() -> rx.Component:
    return rx.vstack(
        panel_header("gauge", "Resumen ejecutivo"),
        rx.hstack(
            kpi("dollar_sign", "Total de ventas", State.total_ventas_fmt, ACCENT),
            kpi("receipt_text", "Transacciones", State.transacciones, ACCENT_BLUE),
            kpi("package", "Productos vendidos", State.productos_vendidos, ACCENT_AMBER),
            kpi("gauge", "Promedio de venta", State.promedio_venta_fmt, ACCENT_VIOLET),
            wrap="wrap", spacing="3", width="100%",
        ),
        rx.hstack(
            kpi("trending_up", "Producto más vendido", State.producto_mas_vendido, POSITIVE, on_click=lambda: State.ir_a_grafico("producto")),
            kpi("trending_down", "Producto menos vendido", State.producto_menos_vendido, NEGATIVE, on_click=lambda: State.ir_a_grafico("producto")),
            kpi("map_pin", "Sede más productiva", State.sede_mayor_venta, ACCENT, on_click=lambda: State.ir_a_grafico("sede")),
            wrap="wrap", spacing="3", width="100%",
        ),
        rx.text(f"Columnas: {State.columnas}  ·  Registros: {State.filas}", style={
            "color": TEXT_MUTED, "font_family": FONT_MONO, "font_size": "0.78rem",
        }),
        width="100%", spacing="4", style=PANEL_STYLE,
    )


def tarjeta_estadistica(titulo: str, valor: str, accent: str) -> rx.Component:
    return rx.vstack(
        rx.text(titulo, style={"color": TEXT_MUTED, "font_size": "0.7rem", "letter_spacing": "0.08em", "text_transform": "uppercase"}),
        rx.text(valor, style={"color": TEXT_PRIMARY, "font_family": FONT_MONO, "font_size": "1rem", "font_weight": "600"}),
        spacing="1",
        style={
            **PANEL_STYLE,
            "padding": "0.8em 1em",
            "border_left": f"2px solid {accent}",
            "min_width": "130px",
            "flex": "1",
            "background": BG_PANEL,
        },
    )


def ventana_graficos() -> rx.Component:
    return rx.vstack(
        panel_header("chart_candlestick", "Gráficos estadísticos"),
        rx.hstack(
            rx.vstack(rx.text("Tipo", style=LABEL_STYLE), rx.select(["barras", "lineas", "cascada", "velas"], value=State.tipo_grafico, on_change=State.set_tipo_grafico)),
            rx.vstack(rx.text("Eje X", style=LABEL_STYLE), rx.select(["fecha", "mes", "producto", "sede", "categoria"], value=State.eje_x, on_change=State.set_eje_x)),
            rx.vstack(rx.text("Eje Y", style=LABEL_STYLE), rx.select(["venta", "cantidad", "precio"], value=State.eje_y, on_change=State.set_eje_y)),
            rx.cond(
                State.eje_x != "producto",
                rx.vstack(rx.text("Producto", style=LABEL_STYLE), rx.select(State.productos_disponibles, value=State.filtro_producto, on_change=State.set_filtro_producto)),
            ),
            rx.cond(
                State.eje_x != "sede",
                rx.vstack(rx.text("Ciudad", style=LABEL_STYLE), rx.select(State.ciudades_disponibles, value=State.filtro_ciudad, on_change=State.set_filtro_ciudad)),
            ),
            rx.cond(
                (State.eje_x != "fecha") & (State.eje_x != "mes"),
                rx.vstack(rx.text("Desde", style=LABEL_STYLE), rx.input(type="date", value=State.fecha_inicio, on_change=State.set_fecha_inicio)),
            ),
            rx.cond(
                (State.eje_x != "fecha") & (State.eje_x != "mes"),
                rx.vstack(rx.text("Hasta", style=LABEL_STYLE), rx.input(type="date", value=State.fecha_fin, on_change=State.set_fecha_fin)),
            ),
            rx.button(rx.icon(tag="filter", size=15), "Aplicar", on_click=State.aplicar_filtros),
            align="end", wrap="wrap", spacing="4", width="100%",
        ),
        rx.box(
            rx.plotly(data=State.datos_grafico, width="100%", height="480px"),
            style={"width": "100%", "background": BG_RAISED, "border_radius": "10px", "padding": "0.5em"},
        ),
        rx.hstack(
            rx.foreach(
                State.resumen_estadistico,
                lambda item: rx.cond(
                    item["titulo"] == "Máximo",
                    tarjeta_estadistica(item["titulo"], item["valor"], ACCENT),
                    rx.cond(
                        item["titulo"] == "Mínimo",
                        tarjeta_estadistica(item["titulo"], item["valor"], ACCENT_BLUE),
                        rx.cond(
                            item["titulo"] == "Media",
                            tarjeta_estadistica(item["titulo"], item["valor"], ACCENT_AMBER),
                            tarjeta_estadistica(item["titulo"], item["valor"], ACCENT_VIOLET),
                        ),
                    ),
                ),
            ),
            spacing="3",
            wrap="wrap",
            width="100%",
        ),
        rx.text(State.resumen_grafico, style={"color": TEXT_MUTED, "font_family": FONT_MONO, "font_size": "0.78rem"}),
        width="100%", spacing="4", style=PANEL_STYLE,
    )


def bloque_analisis(icon: str, pregunta: str, interpretacion, decision, accent: str, on_click=None) -> rx.Component:
    contenido = rx.vstack(
        rx.hstack(rx.icon(tag=icon, size=15, color=accent), rx.text(pregunta, weight="bold", style={"color": TEXT_PRIMARY, "font_size": "0.88rem"}), spacing="2", align="center"),
        rx.text(interpretacion, style={"color": TEXT_MUTED, "font_size": "0.85rem"}),
        rx.hstack(rx.icon(tag="arrow_up_right", size=13, color=accent), rx.text(decision, style={"color": accent, "font_size": "0.85rem"}), spacing="2", align="center"),
        style={**PANEL_STYLE, "background": BG_RAISED, "border_left": f"2px solid {accent}", "cursor": "pointer" if on_click else "default"},
        align="start", spacing="2", width="100%",
    )
    if on_click is None:
        return contenido
    return rx.box(contenido, on_click=on_click, style={"width": "100%"})


def ventana_analisis() -> rx.Component:
    return rx.vstack(
        panel_header("brain_circuit", "Análisis e interpretación"),
        bloque_analisis("package", "¿Qué producto debería recibir mayor stock?", State.interpretacion_stock, State.decision_stock, ACCENT_AMBER, on_click=lambda: State.ir_a_grafico("producto")),
        bloque_analisis("tag", "¿Qué categoría debería recibir mayor inversión?", State.interpretacion_categoria, State.decision_categoria, ACCENT_VIOLET, on_click=lambda: State.ir_a_grafico("categoria")),
        bloque_analisis("map_pin", "¿Qué sede tiene mejor rendimiento?", State.interpretacion_sede, State.decision_sede, POSITIVE, on_click=lambda: State.ir_a_grafico("sede")),
        width="100%", spacing="3", style=PANEL_STYLE,
    )


def ventana_datos() -> rx.Component:
    return rx.vstack(
        panel_header("table_2", "Datos procesados"),
        rx.text("Vista previa de los primeros 10 registros", style={"color": TEXT_MUTED, "font_size": "0.82rem"}),
        rx.box(rx.html(State.vista_datos_html), style={"width": "100%", "overflow_x": "auto", "border_radius": "8px", "border": f"1px solid {BORDER}"}),
        width="100%", spacing="3", style=PANEL_STYLE,
    )


def ventana_reportes() -> rx.Component:
    return rx.vstack(
        panel_header("receipt_text", "Reportes de análisis"),
        rx.hstack(
            rx.button(rx.icon(tag="database", size=15), "Reporte global", on_click=State.generar_reporte_global),
            rx.button(rx.icon(tag="filter", size=15), "Reporte filtrado", on_click=State.generar_reporte_filtrado, variant="surface"),
            spacing="3",
        ),
        rx.text("Reportes guardados", style=LABEL_STYLE, margin_top="0.4em"),
        rx.vstack(
            rx.foreach(
                State.reportes,
                lambda reporte: rx.hstack(
                    rx.icon(tag="file_text", size=15, color=ACCENT),
                    rx.text(reporte["nombre"], style={"color": TEXT_PRIMARY, "font_family": FONT_MONO, "font_size": "0.82rem"}),
                    rx.spacer(),
                    rx.icon_button(rx.icon(tag="download", size=14), on_click=lambda nombre=reporte["nombre"]: State.descargar_reporte(nombre), variant="ghost", size="1"),
                    rx.icon_button(rx.icon(tag="trash_2", size=14), on_click=lambda nombre=reporte["nombre"]: State.eliminar_reporte(nombre), variant="ghost", color_scheme="red", size="1"),
                    align="center", width="100%",
                    style={"background": BG_RAISED, "border": f"1px solid {BORDER}", "border_radius": "8px", "padding": "0.6em 1em"},
                ),
            ),
            spacing="2", width="100%",
        ),
        width="100%", spacing="3", style=PANEL_STYLE,
    )


# --------------------------------------------------------------------- root

def contenido_principal() -> rx.Component:
    return rx.box(
        rx.match(
            State.vista_activa,
            ("carga", ventana_carga()),
            ("resumen", rx.cond(State.data_loaded, ventana_resumen(), estado_vacio("Carga un archivo para ver el resumen.", "gauge"))),
            ("graficos", rx.cond(State.data_loaded, ventana_graficos(), estado_vacio("Carga un archivo para ver los gráficos.", "chart_candlestick"))),
            ("analisis", rx.cond(State.data_loaded, ventana_analisis(), estado_vacio("Carga un archivo para ver el análisis.", "brain_circuit"))),
            ("datos", rx.cond(State.data_loaded, ventana_datos(), estado_vacio("Carga un archivo para ver los datos.", "table_2"))),
            ("reportes", rx.cond(State.data_loaded, ventana_reportes(), estado_vacio("Carga un archivo para gestionar reportes.", "receipt_text"))),
            ventana_carga(),
        ),
        style={"width": "100%", "padding": "1.6em", "max_width": "1400px"},
    )


def index() -> rx.Component:
    return rx.hstack(
        barra_lateral(),
        rx.vstack(
            barra_superior(),
            contenido_principal(),
            spacing="0", width="100%", align="center",
        ),
        spacing="0", width="100%", align="stretch",
        style={"background": BG_DEEP, "min_height": "100vh"},
    )

"""Estado reactivo y coordinación del flujo de datos."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import reflex as rx
from Dashboard_empresarial_anlisis_datos.analizar import analizar_datos, generar_interpretacion
from Dashboard_empresarial_anlisis_datos.cargar import (
    guardar_archivo, leer_archivo, leer_archivo_guardado, listar_archivos, validar_datos,
)
from Dashboard_empresarial_anlisis_datos.normalizar import normalizar_datos
from Dashboard_empresarial_anlisis_datos.visualizar import (
    crear_figura_interactiva, plotly_to_html, resumen_estadistico_grafico,
)

class State(rx.State):
    """Valores serializables que la interfaz puede mostrar."""

    _df: pd.DataFrame = pd.DataFrame()
    _df_base: pd.DataFrame = pd.DataFrame()
    archivos: list[str] = listar_archivos()
    archivo_seleccionado: str = ""
    productos_disponibles: list[str] = []
    ciudades_disponibles: list[str] = []
    filtro_producto: str = "Todos"
    filtro_ciudad: str = "Todas"
    fecha_inicio: str = ""
    fecha_fin: str = ""
    file_name: str = ""
    message: str = ""
    data_loaded: bool = False
    total_ventas: float = 0.0
    transacciones: int = 0
    productos_vendidos: int = 0
    promedio_venta: float = 0.0
    producto_mas_vendido: str = "Sin datos"
    producto_menos_vendido: str = "Sin datos"
    categoria_mayor_venta: str = "Sin datos"
    mes_mayor_venta: str = "Sin datos"
    sede_mayor_venta: str = "Sin datos"
    filas: int = 0
    columnas: int = 0
    interpretacion_stock: str = ""
    decision_stock: str = ""
    interpretacion_categoria: str = ""
    decision_categoria: str = ""
    interpretacion_sede: str = ""
    decision_sede: str = ""
    vista_datos_html: str = ""
    vista_activa: str = "carga"
    tipo_grafico: str = "barras"
    eje_x: str = "mes"
    eje_y: str = "venta"
    datos_grafico: go.Figure = go.Figure()  # objeto de figura, renderizado con rx.plotly
    resumen_grafico: str = ""
    resumen_estadistico: list[dict] = []

    # --- Reportes ---
    reportes: list[dict] = []  # cada reporte: {nombre, fecha, contenido_html, global}
    reporte_actual: str = ""

    @rx.var
    def total_ventas_fmt(self) -> str:
        return f"{self.total_ventas:,.2f}"

    @rx.var
    def promedio_venta_fmt(self) -> str:
        return f"{self.promedio_venta:,.2f}"

    def set_vista_activa(self, valor: str):
        self.vista_activa = valor

    def ir_a_grafico(self, tipo: str):
        """Cambia a la vista de gráficos y prepara la visualización del dato del resumen."""
        self.vista_activa = "graficos"
        if tipo == "producto":
            self.tipo_grafico = "barras"
            self.eje_x = "producto"
            self.eje_y = "venta"
        elif tipo == "categoria":
            self.tipo_grafico = "barras"
            self.eje_x = "categoria"
            self.eje_y = "venta"
        elif tipo == "sede":
            self.tipo_grafico = "barras"
            self.eje_x = "sede"
            self.eje_y = "venta"
        elif tipo == "mes":
            self.tipo_grafico = "lineas"
            self.eje_x = "mes"
            self.eje_y = "venta"
        else:
            return
        datos = self._df if not self._df.empty else self._df_base
        if not datos.empty:
            self._actualizar_grafico_principal(datos)

    def set_filtro_producto(self, valor: str):
        self.filtro_producto = valor

    def set_filtro_ciudad(self, valor: str):
        self.filtro_ciudad = valor

    def set_fecha_inicio(self, valor: str):
        self.fecha_inicio = valor

    def set_fecha_fin(self, valor: str):
        self.fecha_fin = valor

    def set_tipo_grafico(self, valor: str):
        self.tipo_grafico = valor
        self._actualizar_grafico_principal(self._df)

    def set_eje_x(self, valor: str):
        self.eje_x = valor
        self._actualizar_grafico_principal(self._df)

    def set_eje_y(self, valor: str):
        self.eje_y = valor
        self._actualizar_grafico_principal(self._df)

    def _actualizar_grafico_principal(self, datos: pd.DataFrame):
        if datos.empty:
            return
        self.datos_grafico = crear_figura_interactiva(datos, self.tipo_grafico, self.eje_x, self.eje_y)
        self.resumen_estadistico = resumen_estadistico_grafico(datos, self.eje_x, self.eje_y)
        self.resumen_grafico = f"Gráfico de {self.eje_y} por {self.eje_x}. Registros filtrados: {len(datos)}."

    def _analizar_archivo(self, datos: pd.DataFrame, nombre: str):
        datos = normalizar_datos(datos)
        problemas = validar_datos(datos)
        if problemas:
            self.message = " ".join(problemas)
            self.data_loaded = False
            return

        self._df = datos
        self.archivo_seleccionado = nombre
        resumen = analizar_datos(datos)
        interpretacion = generar_interpretacion(resumen)
        for clave, valor in resumen.items():
            if clave not in {"ventas_por_mes", "ventas_por_categoria", "ventas_por_sede", "ventas_por_producto", "cantidad_por_categoria"}:
                setattr(self, clave, valor)
        self.interpretacion_stock = interpretacion["stock"]
        self.decision_stock = interpretacion["stock_decision"]
        self.interpretacion_categoria = interpretacion["categoria"]
        self.decision_categoria = interpretacion["categoria_decision"]
        self.interpretacion_sede = interpretacion["sede"]
        self.decision_sede = interpretacion["sede_decision"]
        self.vista_datos_html = datos.head(10).to_html(index=False, border=0, classes="tabla-datos")
        self._actualizar_grafico_principal(datos)
        self.data_loaded = True
        self.message = f"Datos procesados correctamente: {self.filas} registros y {self.columnas} columnas."

    def _actualizar_filtros_disponibles(self, datos: pd.DataFrame):
        productos = sorted(datos["producto"].dropna().astype(str).unique().tolist()) if "producto" in datos.columns else []
        ciudades = sorted(datos["sede"].dropna().astype(str).unique().tolist()) if "sede" in datos.columns else []
        self.productos_disponibles = ["Todos"] + productos
        self.ciudades_disponibles = ["Todas"] + ciudades
        if "fecha" in datos.columns and not datos["fecha"].dropna().empty:
            self.fecha_inicio = datos["fecha"].min().strftime("%Y-%m-%d")
            self.fecha_fin = datos["fecha"].max().strftime("%Y-%m-%d")
        self.filtro_producto = "Todos"
        self.filtro_ciudad = "Todas"

    async def handle_upload(self, files: list[rx.UploadFile]):
        if not files:
            return
        self.file_name = files[0].filename
        try:
            contenido = await files[0].read()
            nombre_guardado = guardar_archivo(contenido, self.file_name)
            self.archivos = listar_archivos()
            self._analizar_archivo(leer_archivo(contenido, nombre_guardado), nombre_guardado)
            self._df_base = self._df.copy()
            self._actualizar_filtros_disponibles(self._df)
        except (OSError, ValueError, TypeError, ImportError) as error:
            self.message = f"No se pudo procesar el archivo: {error}"
            self.data_loaded = False

    def seleccionar_archivo(self, nombre: str):
        if not nombre:
            return
        try:
            self._analizar_archivo(leer_archivo_guardado(nombre), nombre)
            self._df_base = self._df.copy()
            self._actualizar_filtros_disponibles(self._df)
        except (OSError, ValueError, TypeError, ImportError) as error:
            self.message = f"No se pudo abrir el archivo seleccionado: {error}"
            self.data_loaded = False

    def aplicar_filtros(self):
        if self._df_base.empty:
            return
        datos = self._df_base.copy()
        if self.filtro_producto != "Todos" and "producto" in datos.columns:
            datos = datos[datos["producto"].astype(str) == self.filtro_producto]
        if self.filtro_ciudad != "Todas" and "sede" in datos.columns:
            datos = datos[datos["sede"].astype(str) == self.filtro_ciudad]
        if "fecha" in datos.columns:
            if self.fecha_inicio:
                datos = datos[datos["fecha"] >= pd.Timestamp(self.fecha_inicio)]
            if self.fecha_fin:
                datos = datos[datos["fecha"] <= pd.Timestamp(self.fecha_fin)]
        if datos.empty:
            self.data_loaded = False
            self.message = "No hay registros para los filtros seleccionados."
            return
        self._analizar_archivo(datos, self.archivo_seleccionado)

    # --- Reportes ---
    def _generar_reporte(self, datos: pd.DataFrame, global_reporte: bool) -> str:
        """Genera un HTML con KPIs, resumen, gráficos, datos y análisis."""
        resumen = analizar_datos(datos)
        interpretacion = generar_interpretacion(resumen)

        graficos_html = ""
        if "fecha" in datos.columns and "venta" in datos.columns:
            graficos_html += plotly_to_html(crear_figura_interactiva(datos, "barras", "mes", "venta"))
        if "producto" in datos.columns and "venta" in datos.columns:
            top = (
                datos.groupby("producto", as_index=False)["venta"].sum()
                .sort_values("venta", ascending=False).head(5)
            )
            fig = px.bar(top, x="producto", y="venta", title="Top 5 productos más vendidos", text_auto=True)
            graficos_html += plotly_to_html(fig)
        if "categoria" in datos.columns and "venta" in datos.columns:
            cat = (
                datos.groupby("categoria", as_index=False)["venta"].sum()
                .sort_values("venta", ascending=False)
            )
            fig = px.pie(cat, values="venta", names="categoria", title="Ventas por categoría")
            graficos_html += plotly_to_html(fig)
        if "sede" in datos.columns and "venta" in datos.columns:
            sede = (
                datos.groupby("sede", as_index=False)["venta"].sum()
                .sort_values("venta", ascending=False)
            )
            fig = px.bar(sede, x="sede", y="venta", title="Comparación de ventas entre sedes", text_auto=True)
            graficos_html += plotly_to_html(fig)

        if not graficos_html:
            graficos_html = "<p>No hay columnas suficientes para generar gráficos.</p>"

        tabla_datos = datos.head(20).to_html(index=False, border=0)
        tipo_reporte = "Global" if global_reporte else "Filtrado"

        html = f"""
        <html>
        <head><meta charset="utf-8"><title>Reporte de Análisis - {tipo_reporte}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 2em; color: #1e293b; }}
            table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
            th, td {{ border: 1px solid #cbd5e1; padding: 6px 10px; text-align: left; }}
            th {{ background: #f1f5f9; }}
            .kpis {{ display: flex; flex-wrap: wrap; gap: 1em; margin: 1em 0; }}
            .kpi {{ border: 1px solid #cbd5e1; border-radius: 8px; padding: 0.8em 1.2em; min-width: 170px; }}
            .kpi strong {{ display: block; font-size: 1.4em; margin-top: 4px; }}
        </style>
        </head>
        <body>
            <h1>Reporte de Análisis ({tipo_reporte})</h1>
            <p>Generado a partir de {resumen['transacciones']} transacciones.</p>

            <h3>A. Resumen general (KPIs)</h3>
            <div class="kpis">
                <div class="kpi">Total de ventas<strong>{resumen['total_ventas']:,.2f}</strong></div>
                <div class="kpi">Productos vendidos<strong>{resumen['productos_vendidos']}</strong></div>
                <div class="kpi">Transacciones<strong>{resumen['transacciones']}</strong></div>
                <div class="kpi">Promedio de venta<strong>{resumen['promedio_venta']:,.2f}</strong></div>
            </div>

            <h3>B. Principales resultados</h3>
            <ul>
                <li>Producto más vendido: {resumen['producto_mas_vendido']}</li>
                <li>Producto menos vendido: {resumen['producto_menos_vendido']}</li>
                <li>Categoría con mayor venta: {resumen['categoria_mayor_venta']}</li>
                <li>Mes con mayor venta: {resumen['mes_mayor_venta']}</li>
                <li>Sede con mayor venta: {resumen['sede_mayor_venta']}</li>
            </ul>

            <h3>C. Gráficos</h3>
            {graficos_html}

            <h3>D. Análisis</h3>
            <p>{interpretacion['stock']} {interpretacion['stock_decision']}</p>
            <p>{interpretacion['categoria']} {interpretacion['categoria_decision']}</p>
            <p>{interpretacion['sede']} {interpretacion['sede_decision']}</p>

            <h3>E. Datos (primeras 20 filas)</h3>
            {tabla_datos}
        </body>
        </html>
        """
        return html

    def generar_reporte_global(self):
        if self._df_base.empty:
            self.message = "No hay datos para generar el reporte global."
            return
        nombre = f"reporte_global_{len(self.reportes)+1}"
        contenido = self._generar_reporte(self._df_base, True)
        self.reportes.append({"nombre": nombre, "contenido": contenido})
        self.message = f"Reporte global '{nombre}' generado."

    def generar_reporte_filtrado(self):
        if self._df.empty:
            self.message = "No hay datos filtrados para generar el reporte."
            return
        nombre = f"reporte_filtrado_{len(self.reportes)+1}"
        contenido = self._generar_reporte(self._df, False)
        self.reportes.append({"nombre": nombre, "contenido": contenido})
        self.message = f"Reporte filtrado '{nombre}' generado."

    def eliminar_reporte(self, nombre: str):
        self.reportes = [r for r in self.reportes if r["nombre"] != nombre]
        self.message = f"Reporte '{nombre}' eliminado."

    def descargar_reporte(self, nombre: str):
        for r in self.reportes:
            if r["nombre"] == nombre:
                return rx.download(data=r["contenido"], filename=f"{nombre}.html")
        return rx.console.log("Reporte no encontrado.")

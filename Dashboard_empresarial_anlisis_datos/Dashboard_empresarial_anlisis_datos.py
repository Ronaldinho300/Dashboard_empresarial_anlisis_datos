"""Punto de entrada de la aplicación Reflex."""

import reflex as rx

from Dashboard_empresarial_anlisis_datos.interfaz import index
from Dashboard_empresarial_anlisis_datos.estilos import FONT_IMPORTS, GLOBAL_STYLE


app = rx.App(
    theme=rx.theme(appearance="dark", accent_color="teal", gray_color="slate", radius="medium"),
    stylesheets=[FONT_IMPORTS],
    style=GLOBAL_STYLE,
    html_lang="es",
)
app.add_page(index, title="Dashboard Empresarial")
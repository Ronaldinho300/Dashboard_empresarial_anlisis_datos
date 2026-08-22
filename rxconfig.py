import reflex as rx

config = rx.Config(
    app_name="Dashboard_empresarial_anlisis_datos",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)
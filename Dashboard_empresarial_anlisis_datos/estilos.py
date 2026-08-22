"""Sistema de diseño: tokens de color, tipografía y estilos globales.

Inspirado en terminales de trading: fondo casi negro, cifras en monoespaciada,
un solo acento (teal) para el estado activo y colores semánticos (verde/rojo)
para lectura rápida de indicadores.
"""

# --- Color ---
BG_DEEP = "#070B12"        # fondo general de la app
BG_PANEL = "#0F1620"       # tarjetas, sidebar, paneles
BG_RAISED = "#141C29"      # hover / filas alternas / inputs
BORDER = "#1C2836"         # líneas divisorias

TEXT_PRIMARY = "#E7ECF3"
TEXT_MUTED = "#66768C"
TEXT_FAINT = "#3C495A"

ACCENT = "#22D3B8"         # teal — acento principal / estado activo
ACCENT_AMBER = "#F0B429"   # cifras destacadas secundarias
ACCENT_VIOLET = "#8B7CF6"  # cifras destacadas terciarias
ACCENT_BLUE = "#4F8CFF"

POSITIVE = "#2ED47A"       # crecimiento / top
NEGATIVE = "#F4574F"       # caída / bottom

# --- Tipografía ---
FONT_DISPLAY = "'Space Grotesk', sans-serif"
FONT_BODY = "'Inter', sans-serif"
FONT_MONO = "'JetBrains Mono', monospace"

FONT_IMPORTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Space+Grotesk:wght@500;600;700"
    "&family=Inter:wght@400;500;600"
    "&family=JetBrains+Mono:wght@400;500;600"
    "&display=swap"
)

LABEL_STYLE = {
    "font_family": FONT_BODY,
    "font_size": "0.7rem",
    "color": TEXT_MUTED,
    "text_transform": "uppercase",
    "letter_spacing": "0.06em",
}

MONO_NUM_STYLE = {
    "font_family": FONT_MONO,
    "font_size": "1.35rem",
    "font_weight": "600",
    "color": TEXT_PRIMARY,
}

PANEL_STYLE = {
    "background": BG_PANEL,
    "border": f"1px solid {BORDER}",
    "border_radius": "12px",
    "padding": "1.4em 1.6em",
}

# --- Estilo global de la app (fuentes + tabla de datos inyectada como HTML) ---
GLOBAL_STYLE = {
    "font_family": FONT_BODY,
    "background_color": BG_DEEP,
    "color": TEXT_PRIMARY,
    ".tabla-datos": {
        "width": "100%",
        "border_collapse": "collapse",
        "font_family": FONT_MONO,
        "font_size": "0.8rem",
    },
    ".tabla-datos th": {
        "background": BG_RAISED,
        "color": TEXT_MUTED,
        "text_align": "left",
        "padding": "0.55em 0.9em",
        "border_bottom": f"1px solid {BORDER}",
        "text_transform": "uppercase",
        "font_size": "0.66rem",
        "letter_spacing": "0.05em",
        "position": "sticky",
        "top": "0",
    },
    ".tabla-datos td": {
        "padding": "0.5em 0.9em",
        "border_bottom": f"1px solid {BORDER}",
        "color": TEXT_PRIMARY,
        "white_space": "nowrap",
    },
    ".tabla-datos tr:hover td": {
        "background": BG_RAISED,
    },
}

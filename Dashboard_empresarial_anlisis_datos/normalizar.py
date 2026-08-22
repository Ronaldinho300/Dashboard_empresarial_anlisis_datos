"""Normalización de nombres, tipos y valores del conjunto de datos."""

import re
import unicodedata

import pandas as pd


ALIASES = {
    "date": "fecha",
    "fecha venta": "fecha",
    "product": "producto",
    "product name": "producto",
    "category": "categoria",
    "categoría": "categoria",
    "city": "sede",
    "ciudad": "sede",
    "branch": "sede",
    "sales": "venta",
    "ventas": "venta",
    "amount": "venta",
    "quantity": "cantidad",
    "cant": "cantidad",
    "price": "precio",
    "unit price": "precio",
}


def _normalizar_nombre(nombre: object) -> str:
    texto = unicodedata.normalize("NFKD", str(nombre))
    texto = "".join(char for char in texto if not unicodedata.combining(char))
    texto = re.sub(r"[^a-zA-Z0-9]+", " ", texto).strip().lower()
    return ALIASES.get(texto, texto.replace(" ", "_"))


def normalizar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia nombres, tipos y filas incompletas para el análisis."""
    datos = df.copy()
    datos.columns = [_normalizar_nombre(col) for col in datos.columns]

    if "fecha" in datos.columns:
        datos["fecha"] = pd.to_datetime(datos["fecha"], dayfirst=True, errors="coerce")
    for columna in ("venta", "cantidad", "precio"):
        if columna in datos.columns:
            datos[columna] = pd.to_numeric(datos[columna], errors="coerce")

    if "venta" not in datos.columns and {"cantidad", "precio"}.issubset(datos.columns):
        datos["venta"] = datos["cantidad"] * datos["precio"]

    columnas_clave = [col for col in ("fecha", "producto", "venta") if col in datos.columns]
    if columnas_clave:
        datos = datos.dropna(subset=columnas_clave)
    return datos.reset_index(drop=True)
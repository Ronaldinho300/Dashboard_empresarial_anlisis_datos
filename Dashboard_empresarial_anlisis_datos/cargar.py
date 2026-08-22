"""Lectura y validación inicial de archivos de datos."""

import io
from pathlib import Path

import pandas as pd


EXTENSIONES_PERMITIDAS = (".csv", ".xlsx", ".xls")
CARPETA_DATOS = Path(__file__).resolve().parent.parent / "datos"


def guardar_archivo(content: bytes, file_name: str) -> str:
    """Guarda el archivo original y devuelve el nombre almacenado."""
    nombre = Path(file_name).name
    extension = Path(nombre).suffix.lower()
    if extension not in EXTENSIONES_PERMITIDAS:
        raise ValueError("Formato no soportado. Use .csv, .xlsx o .xls")
    CARPETA_DATOS.mkdir(exist_ok=True)
    destino = CARPETA_DATOS / nombre
    contador = 1
    while destino.exists():
        destino = CARPETA_DATOS / f"{Path(nombre).stem}_{contador}{extension}"
        contador += 1
    destino.write_bytes(content)
    return destino.name


def listar_archivos() -> list[str]:
    """Lista los archivos de datos guardados localmente."""
    CARPETA_DATOS.mkdir(exist_ok=True)
    return sorted(
        archivo.name
        for archivo in CARPETA_DATOS.iterdir()
        if archivo.is_file() and archivo.suffix.lower() in EXTENSIONES_PERMITIDAS
    )


def leer_archivo_guardado(file_name: str) -> pd.DataFrame:
    """Lee un archivo previamente guardado en la carpeta local."""
    nombre = Path(file_name).name
    ruta = CARPETA_DATOS / nombre
    if not ruta.is_file() or ruta.suffix.lower() not in EXTENSIONES_PERMITIDAS:
        raise ValueError("El archivo seleccionado no existe en la carpeta de datos.")
    return leer_archivo(ruta.read_bytes(), nombre)


def leer_archivo(content: bytes, file_name: str) -> pd.DataFrame:
    """Lee un archivo CSV o Excel y devuelve sus registros."""
    nombre = file_name.lower()
    if nombre.endswith(".csv"):
        try:
            return pd.read_csv(io.BytesIO(content), encoding="utf-8")
        except UnicodeDecodeError:
            return pd.read_csv(io.BytesIO(content), encoding="latin-1")
    if nombre.endswith((".xlsx", ".xls")):
        return pd.read_excel(io.BytesIO(content))
    raise ValueError("Formato no soportado. Use .csv, .xlsx o .xls")


def validar_datos(df: pd.DataFrame) -> list[str]:
    """Devuelve los problemas que impedirían analizar el conjunto de datos."""
    if df.empty:
        return ["El archivo no contiene registros."]
    if len(df.columns) == 0:
        return ["El archivo no contiene columnas."]
    if not any(col in df.columns for col in ("venta", "cantidad")):
        return ["Debe existir una columna 'venta' o 'cantidad'."]
    return []
# Dashboard empresarial de análisis de datos

Este proyecto es una aplicación web desarrollada con Reflex para analizar archivos de ventas y mostrar un dashboard con indicadores clave, gráficos interactivos, filtros y reportes.

## 1. ¿Qué hace esta aplicación?

La aplicación permite:

- Cargar archivos CSV, XLSX o XLS
- Validar si el archivo tiene datos útiles
- Normalizar nombres de columnas y tipos de datos
- Calcular KPIs empresariales
- Filtrar por producto, ciudad, fechas y otros criterios
- Visualizar gráficos con Plotly
- Generar un análisis textual de negocio
- Exportar reportes en formato HTML

## 2. Herramientas y tecnologías utilizadas

Las principales herramientas del proyecto son:

- Python 3
- Reflex: para construir la interfaz web
- Pandas: para limpiar y analizar datos tabulares
- Plotly: para crear gráficos interactivos
- Kaleido: para renderizado de gráficos
- VS Code: entorno de desarrollo
- Git: control de versiones

Las dependencias del proyecto se encuentran en `requirements.txt`:

```txt
reflex==0.9.8.post1
kaleido>=1.0.0
pandas>=2.0.0
plotly>=5.0.0
```

## 3. Estructura del proyecto

```text
Dashboard_empresarial_anlisis_datos/
├── Dashboard_empresarial_anlisis_datos/
│   ├── __init__.py
│   ├── analisis.py
│   ├── cargar.py
│   ├── Dashboard_empresarial_anlisis_datos.py
│   ├── estado.py
│   ├── estilos.py
│   ├── interfaz.py
│   ├── main.py
│   ├── normalizar.py
│   ├── procesar.py
│   └── visualizar.py
├── datos/
│   └── ventas.csv
├── uploaded_files/
├── requirements.txt
├── rxconfig.py
├── README.md
└── venv/
```

## 4. Descripción de los archivos principales

### `Dashboard_empresarial_anlisis_datos.py`
Inicia la aplicación con Reflex y registra la página principal del dashboard.

### `interfaz.py`
Aquí está la parte visual. Define la barra lateral, los paneles, los KPI, los gráficos y la navegación entre vistas.

### `estado.py`
Es el centro del funcionamiento. Maneja todos los estados reactivos de la app:

- archivo cargado
- filtros activos
- métricas calculadas
- gráficos mostrados
- reportes generados

### `cargar.py`
Se encarga de:

- guardar archivos cargados
- leer CSV, XLSX y XLS
- validar el contenido
- listar archivos disponibles

### `normalizar.py`
Normaliza los datos para que la app pueda trabajar con ellos sin errores:

- cambia columnas a nombres estándar
- convierte fechas a formato correcto
- convierte números a formato numérico
- elimina filas incompletas

### `analizar.py`
Calcula los resultados empresariales:

- total de ventas
- transacciones
- productos vendidos
- promedio de venta
- producto más y menos vendido
- categoría y sede con mayor venta
- resumen por meses y sedes

### `visualizar.py`
Genera los gráficos interactivos con Plotly usando la información procesada en el DataFrame.

### `estilos.py`
Define los colores, fuentes y estilos visuales del dashboard para que se vea como una interfaz tipo panel empresarial.

### `rxconfig.py`
Contiene la configuración del proyecto Reflex, como el nombre de la app y plugins extra.

## 5. ¿Cómo funciona el código?

El flujo general es este:

1. El usuario carga un archivo CSV o Excel desde la interfaz.
2. `cargar.py` guarda y lee el archivo.
3. `normalizar.py` limpia y organiza los datos.
4. `estado.py` valida el archivo y actualiza el estado de la app.
5. `analizar.py` calcula los indicadores y el análisis empresarial.
6. `visualizar.py` crea los gráficos interactivos.
7. `interfaz.py` muestra toda la información en la UI del dashboard.
8. El usuario puede filtrar datos y generar reportes.

## 6. Cómo se ejecuta la aplicación

Desde la carpeta principal del proyecto:

### Opción 1: si ya existe el entorno virtual

```bash
cd d:/senati/01_semana/Dashboard_empresarial_anlisis_datos
.
venv\Scripts\activate
reflex run
```

### Opción 2: si no existe el entorno virtual

```bash
cd d:/senati/01_semana/Dashboard_empresarial_anlisis_datos
python -m venv venv
.
venv\Scripts\activate
pip install -r requirements.txt
reflex run
```

### En Linux o macOS

```bash
cd /d/senati/01_semana/Dashboard_empresarial_anlisis_datos
source venv/bin/activate
pip install -r requirements.txt
reflex run
```

Cuando se levanta correctamente, la aplicación suele estar disponible en:

```text
http://localhost:3000
```

## 7. Funciones principales que cumple el proyecto

- Gestión de carga de archivos
- Validación de datos
- Limpieza y normalización
- Resumen ejecutivo con KPIs
- Visualización por gráficos
- Análisis descriptivo de ventas
- Filtros por producto y ciudad
- Exportación de reportes HTML

## 8. Resumen técnico

El proyecto combina varias tecnologías para crear un dashboard completo:

- Reflex para la interfaz web
- Pandas para el análisis de datos
- Plotly para la visualización gráfica
- Python como lenguaje principal

Esto permite que la app sea fácil de usar y además modular, porque cada tarea está separada en archivos específicos.

## 9. Recomendaciones

- Usa archivos con columnas como `fecha`, `producto`, `categoria`, `sede`, `venta`, `cantidad` o `precio`.
- Mantén una estructura clara de datos para que la validación funcione mejor.
- Si quieres expandir la app, puedes añadir más filtros, exportación a PDF o conexión a una base de datos.

## 10. Conclusión

Este proyecto funciona como un dashboard empresarial para analizar ventas y visualizar información clave de forma rápida, ordenada y amigable. Su lógica está dividida en módulos específicos para cargar, limpiar, analizar, graficar y mostrar los resultados.

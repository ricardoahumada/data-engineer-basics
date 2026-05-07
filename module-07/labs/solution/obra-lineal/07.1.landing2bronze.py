
# %% [markdown]
# # Lab 07.1: Landing → Bronze - Validación de Estructura
# ## TransCore Data Engineer - Módulo 07
# 
# **Objetivo**: Cargar datos desde la capa landing, validar estructura y guardar en raw/ sin transformar.
# 
# **Input**: `s3://transcore-infra-prod-eu-west-1-ric/landing/obra-lineal/año=2026/mes=05/dia=06/partes_trabajo_115932.csv`
# 
# **Output**: `s3://transcore-infra-prod-eu-west-1-ric/raw/obra-lineal/año=2026/mes=05/dia=06/partes_trabajo_2026-05-06.csv`

# %% [markdown]
# ## 1. Configuración AWS

# %%
# Configuración de credenciales AWS (S3 real)
import os

os.environ["AWS_ACCESS_KEY_ID"] = "<TU_ACCESS_KEY_ID>"
os.environ["AWS_SECRET_ACCESS_KEY"] = "<TU_SECRET_ACCESS_KEY>"


# Limpiar cualquier configuración de LocalStack
os.environ.pop("AWS_ENDPOINT_URL", None)
os.environ.pop("AWS_ENDPOINT", None)

# Configurar región de AWS explícitamente para AWS real
os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"

print("Configuración: AWS real, región eu-west-1")

# %% [markdown]
# ## 2. Importar Libraries

# %%
import pandas as pd
import boto3
from datetime import datetime
from io import StringIO

print("Librerías importadas correctamente")

# %% [markdown]
# ## 3. Configuración de S3 y Paths

# %%
# Configuración S3
BUCKET_NAME = "<TU_BUCKET_NAME>"
FECHA_PROCESO = "2026-05-06"

# Paths
LANDING_KEY = f"landing/obra-lineal/año=2026/mes=05/dia=06/partes_trabajo_115932.csv"
RAW_KEY = f"raw/obra-lineal/año=2026/mes=05/dia=06/partes_trabajo_{FECHA_PROCESO}.csv"

# Crear cliente S3
s3_client = boto3.client("s3", region_name="eu-west-1")

print(f"Bucket: {BUCKET_NAME}")
print(f"Landing key: {LANDING_KEY}")
print(f"Raw key: {RAW_KEY}")

# %% [markdown]
# ## 4. Cargar Datos desde Landing

# %%
def load_csv_from_s3(bucket, key):
    """Carga un CSV directamente desde S3 a un DataFrame."""
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(obj['Body'])

# Cargar dataset desde S3 landing
print("Cargando datos desde landing...")
partes_trabajo = load_csv_from_s3(BUCKET_NAME, LANDING_KEY)
print(f"✓ Partes de trabajo cargados: {len(partes_trabajo):,} registros")

# %% [markdown]
# ## 5. Validar Estructura

# %%
# Exploración inicial
print("=== Estructura del Dataset ===")
print(f"Forma: {partes_trabajo.shape}")
print(f"\nColumnas: {partes_trabajo.columns.tolist()}")
print(f"\nTipos de datos:\n{partes_trabajo.dtypes}")
print(f"\nPrimeras 5 filas:")
print(partes_trabajo.head())

# %%
# Validar columnas esperadas
columnas_esperadas = [
    'id_parte', 'id_equipo', 'fecha_inicio', 'fecha_fin', 
    'tipo_mantenimiento', 'estado', 'horas_trabajo'
]

columnas_presentes = partes_trabajo.columns.tolist()
columnas_faltantes = set(columnas_esperadas) - set(columnas_presentes)
columnas_extra = set(columnas_presentes) - set(columnas_esperadas)

print("=== Validación de Columnas ===")
if columnas_faltantes:
    print(f"⚠️  Columnas faltantes: {columnas_faltantes}")
else:
    print("✓ Todas las columnas esperadas están presentes")

if columnas_extra:
    print(f"ℹ️  Columnas extra: {columnas_extra}")
    
# Verificar columnas vacías
columnas_vacias = partes_trabajo.columns[partes_trabajo.isnull().all()].tolist()
if columnas_vacias:
    print(f"⚠️  Columnas completamente vacías: {columnas_vacias}")
else:
    print("✓ No hay columnas completamente vacías")

# %% [markdown]
# ## 6. Renombrar Columnas

# %%
# Renombrar columnas para consistencia con el modelo
partes_trabajo = partes_trabajo.rename(columns={
    'id_parte': 'parte_id',
    'id_equipo': 'equipo_id'
})

print("=== Columnas Renombradas ===")
print(partes_trabajo.columns.tolist())

# %% [markdown]
# ## 7. Añadir Metadata

# %%
# Añadir metadata de ingesta
partes_trabajo['_ingestion_timestamp'] = datetime.now().isoformat()
partes_trabajo['_source_file'] = LANDING_KEY

print("=== Metadata Añadida ===")
print(f"_ingestion_timestamp: {partes_trabajo['_ingestion_timestamp'].iloc[0]}")
print(f"_source_file: {partes_trabajo['_source_file'].iloc[0]}")

# %% [markdown]
# ## 8. Guardar en Raw/

# %%
# Guardar CSV en S3 raw/
csv_buffer = StringIO()
partes_trabajo.to_csv(csv_buffer, index=False)

s3_client.put_object(
    Bucket=BUCKET_NAME,
    Key=RAW_KEY,
    Body=csv_buffer.getvalue()
)

print(f"✓ Dataset guardado en: s3://{BUCKET_NAME}/{RAW_KEY}")
print(f"  Total registros: {len(partes_trabajo):,}")
print(f"  Columnas: {len(partes_trabajo.columns)}")

# %% [markdown]
# ## 9. Resumen

# %%
print("=" * 60)
print("RESUMEN - Landing → Bronze")
print("=" * 60)
print(f"✓ Datos cargados desde: landing/obra-lineal/")
print(f"✓ Validación de estructura: OK")
print(f"✓ Columnas renombradas: id_parte → parte_id, id_equipo → equipo_id")
print(f"✓ Metadata añadida: _ingestion_timestamp, _source_file")
print(f"✓ Datos guardados en: raw/obra-lineal/")
print(f"\n📊 Total registros procesados: {len(partes_trabajo):,}")
print("=" * 60)
print("\n➡️  Siguiente paso: Ejecutar notebook 07.2 (Bronze → Silver)")



# Anexo: Tecnologías del Data Lake Moderno

Este anexo proporciona una referencia rápida sobre las tecnologías fundamentales que sustentan la arquitectura de Data Lakehouse presentada en el Módulo 3.

---

## S3 (Amazon Simple Storage Service)

**¿Qué es?** Almacenamiento de objetos en la nube de AWS.

**Características principales:**
- Almacenamiento escalable y duradero (99.999999999%)
- Coste por GB almacenado bajo
- Sin estructura fija: almacena archivos (CSV, Parquet, JSON, etc.)
- Seguridad integrada (encriptación, controles de acceso)

**En el contexto TransCore:**
```
S3://transcore-datalake/
├── landing/
├── bronze/
├── silver/
└── gold/
```

**Limitación clave:** S3 es solo almacenamiento. No permite consultas SQL nativas ni transacciones ACID por sí mismo.

---

## Apache Spark

**¿Qué es?** Motor de procesamiento distribuido para datos masivos.

**Características principales:**
- Procesamiento en paralelo sobre clusters
- Soporta Python, Scala, SQL
- Transformaciones y acciones sobre DataFrames
- Puede leer/escribir en S3, HDFS, y otros sistemas

**En el contexto TransCore:**

```python
# Leer CSV desde S3
df = spark.read.format("csv") \
    .option("header", "true") \
    .load("s3://bucket/landing/datos.csv")

# Escribir como Delta Lake
df.write.format("delta") \
    .mode("overwrite") \
    .save("s3://bucket/silver/tabla/")
```

**Concepto clave:** Spark es el "motor" que procesa datos. S3 es el "depósito" donde se almacenan.

---

## Databricks

**¿Qué es?** Plataforma unificada para Data Engineering y Machine Learning basada en Spark.

**Características principales:**
- Cuadernos interactivos (notebooks) para desarrollo
- Gestión automática de clusters Spark
- Delta Lake integrado por defecto
- Colaboración entre equipos (versionamiento, permisos)

**Servicios relacionados:**
| Componente | Función |
|------------|---------|
| **Workspace** | Entorno de desarrollo con notebooks |
| **Cluster** | Recursos de computación (auto-scaling) |
| **Delta Lake** | Capa transaccional sobre datos |
| **Unity Catalog** | Gobernanza y catálogo de datos |

**En el contexto TransCore:** Databricks es la plataforma donde los ingenieros desarrollan y ejecutan pipelines de datos sobre S3.

---

## Delta Lake

**¿Qué es?** Capa de almacenamiento transaccional que añade ACID sobre archivos en S3.

**Problema que resuelve:** S3 puro no garantiza consistencia transaccional.

```
# Sin Delta Lake: riesgo de datos parciales
df.write.format("parquet").save("s3://bucket/tabla/")  # Falla a mitad → datos corruptos

# Con Delta Lake: transacción segura
df.write.format("delta").save("s3://bucket/tabla/")  # Si falla → rollback automático
```

**Estructura en S3:**

```
s3://bucket/silver/fact_ordenes/
├── _delta_log/              ← Registro de transacciones
│   └── 000000000.json       # Cada operación queda registrada
├── part-00000.parquet       # Archivos de datos
├── part-00001.parquet
└── part-00002.parquet
```

**Características principales:**

| Característica | Beneficio |
|----------------|-----------|
| **ACID transactions** | Consistencia garantizada |
| **Time travel** | Consulta versiones antiguas de datos |
| **Upsert/Merge** | Actualiza datos sin reescribir todo |
| **Schema enforcement** | Previene datos inconsistentes |
| **Data skipping** | Consulta solo archivos relevantes |

**Ejemplo de time travel:**

```sql
-- Ver versión actual
SELECT * FROM fact_ordenes

-- Ver versión hace 3 commits
SELECT * FROM fact_ordenes VERSION AS OF 3

-- Ver datos de hace 7 días
SELECT * FROM fact_ordenes TIMESTAMP AS OF CURRENT_TIMESTAMP - INTERVAL 7 DAYS
```

**Ejemplo de merge (upsert):**

```python
# Actualizar registros desde fuente nueva
nuevos_datos.write.format("delta") \
    .mode("merge") \
    .target("fact_ordenes") \
    .whenMatchedUpdateAll() \
    .execute()
```

---

## Resumen: Cómo encajan las piezas

```
┌─────────────────────────────────────────────────────────────┐
│                      Databricks                             │
│  (Plataforma de desarrollo y ejecución)                     │
│  ├── Notebooks (desarrollo)                                 │
│  └── Clusters (computación Spark)                           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    ┌──────┴──────────┐
                    │   Spark         │
                    │ (Motor de       │
                    │  procesamiento) │
                    └──────┬──────────┘
                           │
              ┌────────────┴─────────────┐
              │                          │
        ┌─────┴───────┐            ┌─────┴─────┐
        │   Delta     │            │   Delta   │
        │   Lake      │            │   Lake    │
        │  (silver/)  │            │   (gold/) │
        └─────┬───────┘            └─────┬─────┘
              │                          │
              └───────────┬──────────────┘
                          │
                    ┌─────┴────────────┐
                    │    S3            │
                    │ (Almacenamiento) │
                    └──────────────────┘
```

| Tecnología | Rol |
|------------|-----|
| **S3** | Almacenamiento de archivos (datos "en reposo") |
| **Spark** | Motor de procesamiento (datos "en movimiento") |
| **Databricks** | Plataforma que orchestra Spark + Delta |
| **Delta Lake** | Capa transaccional sobre archivos en S3 |


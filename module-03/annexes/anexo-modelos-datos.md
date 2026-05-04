# Anexo: Modelos de Datos

Este anexo explica los tres niveles de modelado de datos y cómo se aplican en arquitecturas de Data Lake.

---

## Modelo Conceptual

**¿Qué es?** Representación de alto nivel de los conceptos de negocio y sus relaciones.

**Enfoque:** ¿Qué datos importan y cómo se relacionan lógicamente?

**Características:**
- Sin detalles técnicos (tablas, columnas, tipos)
- Enfocado en vocabulario común del negocio
- Elimina ambigüedades entre stakeholders
- Independiente de tecnología

**Ejemplo para TransCore:**

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   Orden     │──1:N──│    Activo   │──N:1──│  Contrato   │
│  (mantenim.)│       │ (vehículo)  │       │ (cliente)   │
└─────────────┘       └─────────────┘       └─────────────┘
```

**Preguntas que responde:**
- ¿Cuáles son las entidades principales del negocio?
- ¿Cómo se relacionan entre sí?
- ¿Quién es el "owner" de cada entidad?

---

## Modelo Lógico

**¿Qué es?** Estructura formal de datos sin adicción de sistema concreto.

**Enfoque:** ¿Qué atributos tiene cada entidad? ¿Qué claves la identifican?

**Características:**
- Define entidades, atributos y relaciones
- Especifica primary keys y foreign keys
- Normalización para evitar redundancia
- Implementación independiente (relacional, documento, etc.)

**Ejemplo para TransCore:**

```
┌──────────────────────────────────────────────────────────────┐
│  dim_activos                                                 │
├──────────────────────────────────────────────────────────────┤
│ PK │ sk_activo            │ ID único generado                │
├────┼──────────────────────┼──────────────────────────────────│
│    │ id_activo_externo     │ ID del sistema origen           │
│    │ matricula            │ Matrícula del vehículo           │
│    │ tipo_activo          │ Camión, furgoneta, etc.          │
│    │ fecha_alta           │ Fecha de incorporación           │
│    │ estado               │ Activo, baja, mantenimiento      │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  fact_ordenes                                                │
├──────────────────────────────────────────────────────────────┤
│ PK │ sk_orden              │ ID único generado               │
├────┼───────────────────────┼─────────────────────────────────│
│ FK │ sk_activo             │ Referencia al activo            │
│    │ fecha_orden           │ Fecha y hora de creación        │
│    │ fecha_ejecucion       │ Fecha de ejecución              │
│    │ tipo_orden            │ Preventiva, correctiva          │
│    │ estado                │ Pendiente, en curso, completada │
│    │ duracion_minutos      │ Tiempo de ejecución             │
└──────────────────────────────────────────────────────────────┘
```

**Tipos de esquema:**

| Esquema | Descripción | Cuándo usarlo |
|---------|-------------|---------------|
| **Estrella (Star)** | Tabla de hechos + dimensiones denormalizadas | Reporting simple, mejor rendimiento |
| **Copo de nieve (Snowflake)** | Dimensiones normalizadas con jerarquía | Ahorro de storage, datos más normalizados |
| **Galaxia (Galaxy)** | Múltiples hechos comparten dimensiones | Modelos complejos de BI |

**Preguntas que responde:**
- ¿Qué tablas (entidades) necesito?
- ¿Qué columnas (atributos) tiene cada una?
- ¿Qué relaciones hay entre tablas?
- ¿Cuál es la clave primaria de cada tabla?

---

## Modelo Físico

**¿Qué es?** Implementación concreta en una tecnología específica.

**Enfoque:** ¿Cómo almaceno los datos técnicamente?

**Decisiones técnicas:**

| Decisión | Opciones | Criterio de elección |
|----------|----------|----------------------|
| **Formato archivo** | CSV, Parquet, Delta | Uso: intercambio vs procesamiento |
| **Particionado** | Por fecha, por categoría, por ID | Patrón de consulta más frecuente |
| **Indexación** | Z-ORDER, Bloom filter | Columnas con alta selectividad en filtros |
| **Compresión** | Snappy, Zstd, None | Balance velocidad vs tamaño |
| **Surrogate keys** | Sí/No | Si naturales son inestables → usar surrogates |

**Ejemplo para TransCore en S3:**

```
S3://transcore-datalake/
└── silver/
    └── fact_ordenes/
        ├── _delta_log/
        │   └── 000000000.json
        ├── part-00000-aaa0-snappy.parquet
        ├── part-00001-bbb1-snappy.parquet
        └── part-00002-ccc2-snappy.parquet
```

**Decisiones de particionado:**

```python
# Particionado por fecha (estándar para datos temporales)
df.write.format("delta") \
    .partitionBy("fecha_orden") \
    .save("s3://bucket/silver/fact_ordenes/")

# Particionado por categoría + fecha (cardinalidad moderada)
df.write.format("delta") \
    .partitionBy("tipo_orden", "fecha_orden") \
    .save("s3://bucket/silver/fact_ordenes/")
```

**Preguntas que responde:**
- ¿Qué formato de archivo uso?
- ¿Por qué columna particiono?
- ¿Cuántos archivos simultáneos genero?
- ¿Qué tipo de compresión aplico?

---

### Modelo Conceptual vs Modelo Lógico vs Modelo Físico — Resumen

| Nivel | Pregunta | Output | Independencia tecnología |
|-------|----------|--------|-------------------------|
| **Conceptual** | ¿Qué entidades importan? | Diagrama de entidades | Total |
| **Lógico** | ¿Qué atributos y relaciones? | Esquema de tablas | Alta |
| **Físico** | ¿Cómo lo implemento? | DDL, archivos, particiones | Ninguna |

---
## Otros Modelos Relevantes

### Modelo de Dominios (Domain Model)

**¿Qué es?** Organización de datos por límites funcionales del negocio.

**Diferencia con modelo conceptual:**
- El modelo de dominios agrupa entidades relacionadas
- Cada dominio tiene un "owner" responsable
- Facilita gobernanza y equipos autonomous

**Ejemplo para TransCore:**

```
Dominio Flota
├── dim_activos
├── dim_tiempo
└── fact_ordenes

Dominio Contratos
├── dim_contratistas
└── dim_contratos

Dominio Geográfico
├── dim_ubicaciones
└── dim_rutas
```

---

### Modelo de Lakes vs Warehouse

| Aspecto | Data Lake | Data Warehouse |
|---------|----------|----------------|
| **Estructura** | Archivos en S3 | Tablas relacionales |
| **Schema** | "Schema-on-read" | "Schema-on-write" |
| **Usuarios** | Científicos de datos | Analistas de negocio |
| **Casos de uso** | ML, exploración, datos raw | Reporting, BI |
| **Costo** | Menor ($/TB) | Mayor ($/TB) |
| **Rendimiento** | Variable | Predecible |

---

## Resumen: Del Negocio al Storage

```
      Negocio real
           │
           ▼
┌───────────────────────┐
│  Modelo Conceptual    │  ← Vocabulario común, qué entidades importan
│  (alto nivel)         │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│  Modelo Lógico        │  ← Atributos, claves, relaciones
│  (estructura formal)  │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│  Modelo Físico        │  ← Formato, particionado, storage
│  (implementación)     │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│  Archivos en S3       │  ← .csv, .parquet, _delta_log/
└───────────────────────┘
```

| Modelo | Foco | Pregunta clave |
|--------|------|----------------|
| **Conceptual** | Negocio | ¿Qué datos importan? |
| **Lógico** | Estructura | ¿Cómo se relacionan? |
| **Físico** | Tecnología | ¿Cómo lo almaceno? |

## Glosario: Normalización vs Denormalización

### Normalización

**Definición:** Proceso de organizar datos en tablas para minimizar redundancia y dependencias.

**Formas normales (resumen):**

| Forma | Regla | Ejemplo |
|-------|-------|---------|
| **1NF** | Valores atómicos, sin grupos repetidos | `telefono_1`, `telefono_2` → tabla separada |
| **2NF** | Sin dependencias parciales (PK compuesta) | Atributo depende de toda la PK |
| **3NF** | Sin dependencias transitivas | `ciudad` → `pais` → `continente` (evitar) |

**Objetivo:** Eliminar duplicación de datos, evitar anomalías de inserción/actualización/eliminación.

**Cuándo usar:** Sistemas transaccionales (OLTP), donde la integridad de datos es prioritaria.

---

### Denormalización

**Definición:** Proceso de añadir redundancia controlada a cambio de mejor rendimiento de lectura.

**Diferencia práctica:**

```
-- Normalizado (3NF): datos sin redundancia
dim_activos ← dim_contratistas (FK)
-- Una consulta necesita JOIN para ver contratista

-- Denormalizado: datos duplicados para evitar JOIN
fact_ordenes ← incluye columnas de contratista (nombre, contacto)
-- Consultas más rápidas sin JOIN
```

**Objetivo:** Optimizar consultas analíticas, reducir número de joins.

**Cuándo usar:** Sistemas analíticos (OLAP), reporting, Data Lake en zona gold.


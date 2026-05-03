**Módulo 08** | **Duración: 20 minutos** | **Tipo: Ejercicio Linaje**

# Ejercicio 3: Registrar Linaje en Plantilla Estándar

## Objetivo

Documentar el linaje completo de un pipeline de obra lineal utilizando la plantilla estándar de metadatos, garantizando trazabilidad desde el origen de los datos hasta el destino final.

---

## Contexto del Pipeline

El pipeline a documentar procesa datos de **obra lineal** para calcular indicadores financieros de construcción:

```
┌─────────────┐     ┌──────────────┐      ┌─────────────┐      ┌──────────────┐
│  SAP ERP    │────▶│  Landing     │────▶│  Bronze     │────▶│  Silver      │
│  (CSV)      │     │  (Raw)       │      │  (Parquet)  │      │  (Curated)   │
└─────────────┘     └──────────────┘      └─────────────┘      └──────┬───────┘
                                                                      │
                    ┌─────────────┐      ┌─────────────┐              │
                    │  Power BI   │◀────│  Gold        │◀────────────┘
                    │  Reports    │      │  (Business) │
                    └─────────────┘      └─────────────┘
```

---

## Dataset de Trabajo

### Source: Extractos SAP (CSV)

Archivo `sap_extractos_obra.csv`:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `documento` | string | Número de documento SAP |
| `fecha_documento` | date | Fecha del documento |
| `centro` | string | Centro de coste |
| `cuenta` | string | Cuenta contable |
| `importe` | decimal | Importe en euros |
| `texto` | string | Descripción del movimiento |
| `ref_obra` | string | Referencia de obra lineal |

### Transformaciones del Pipeline

1. **Limpieza Bronze**: Normalización de fechas, eliminación de duplicados
2. **Enriquecimiento Silver**: Join con catálogo de centros de coste
3. **Agregación Gold**: Sumas por obra, mes, y tipo de gasto

---

## Plantilla de Metadatos a Completar

### 1. Información General del Pipeline

```markdown
## metadata:
  pipeline_name: "pipeline_kpis_financieros_obra_lineal"
  version: "[COMPLETAR]"
  owner: "[COMPLETAR]"
  created_date: "2026-01-15"
  last_modified: "[COMPLETAR]"
  status: "production"
  schedule: "0 6 * * *"
```

**Completar:** 
- ¿Quién es el owner actual del pipeline?
- ¿Cuál es la versión actual según el control de cambios?

---

### 2. Sources (Orígenes de Datos)

```markdown
## sources:
  - name: "sap_extractos_obra"
    type: "csv_file"
    location: "[COMPLETAR]"
    format: "csv"
    delimiter: ";"
    encoding: "ISO-8859-1"
    schema:
      - documento: string
      - fecha_documento: date
      - centro: string
      - cuenta: string
      - importe: decimal
      - texto: string
      - ref_obra: string
    refresh_frequency: "[COMPLETAR]"
    last_refresh: "[COMPLETAR]"
    owner: "[COMPLETAR]"
    quality_checks:
      - row_count_min: 1000
      - required_columns: ["documento", "fecha_documento", "importe"]
      - duplicate_check: "documento"
```

**Completar:**
- ¿Dónde se ubica físicamente el archivo CSV?
- ¿Cada cuánto se actualiza el source?

---

### 3. Targets (Destinos de Datos)

```markdown
## targets:
  - name: "kpis_financieros_gold"
    type: "parquet_table"
    location: "[COMPLETAR]"
    format: "parquet"
    partition_by: ["year", "month"]
    schema:
      - ref_obra: string
      - year: integer
      - month: integer
      - tipo_gasto: string
      - total_importe: decimal
      - num_documentos: integer
      - fecha_actualizacion: timestamp
    consumers:
      - "[COMPLETAR]"
    refresh_frequency: "daily"
    sla: "[COMPLETAR]"
```

**Completar:**
- ¿Qué dashboards o reports consumen este dataset?
- ¿Cuál es el SLA de disponibilidad?

---

### 4. Transformaciones (Linaje Lógico)

```markdown
## transformations:
  - step: 1
    name: "bronze_normalization"
    input: "sap_extractos_obra"
    output: "bronze_normalized"
    logic: |
      # Limpieza de datos
      - [COMPLETAR]
    schema_changes:
      - added_columns: ["[COMPLETAR]"]
      - modified_types: ["[COMPLETAR]"]
    quality_rules:
      - "[COMPLETAR]"

  - step: 2
    name: "silver_enrichment"
    input: "bronze_normalized"
    output: "silver_enriched"
    logic: |
      # Enriquecimiento
      - [COMPLETAR]
    joins:
      - type: "left"
        right_table: "cat_centros"
        on: "centro = codigo_centro"
    schema_changes:
      - added_columns: ["[COMPLETAR]"]

  - step: 3
    name: "gold_aggregation"
    input: "silver_enriched"
    output: "kpis_financieros_gold"
    logic: |
      # Agregación final
      - [COMPLETAR]
    schema_changes:
      - aggregated_columns: ["[COMPLETAR]"]
```

**Completar:**
- ¿Qué lógica adicional de cleansing se aplica en Bronze?
- ¿Qué columnas se agregan en el enriquecimiento Silver?
- ¿Cómo se agrupan los datos en Gold?

---

### 5. Diagrama de Linaje

Completar el diagrama con los nodos y flujos del pipeline:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           LINAGE DEL PIPELINE                                │
│                    kpis_financieros_obra_lineal v[COMPLETAR]                 │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│    ┌─────────────────┐                                                       │
│    │  SAP ERP        │  (Source)                                             │
│    │                 │  [COMPLETAR ubicación]                                │
│    └────────┬────────┘                                                       │
│             │ [COMPLETAR formato y frecuencia]                               │
│             ▼                                                                │
│    ┌─────────────────┐                                                       │
│    │  Landing/Raw    │  [COMPLETAR nombre tabla]                             │
│    │                 │  ─ [COMPLETAR lógica]                                 │
│    └────────┬────────┘  ─ Columns: [COMPLETAR]                               │
│             │                                                                │
│             ▼                                                                │
│    ┌─────────────────┐                                                       │
│    │  Silver         │  [COMPLETAR nombre tabla]                             │
│    │                 │  ─ [COMPLETAR lógica]                                 │
│    └────────┬────────┘  ─ Enrich: [COMPLETAR]                                │
│             │                                                                │
│             ▼                                                                │
│    ┌─────────────────┐                                                       │
│    │  Gold           │  [COMPLETAR nombre tabla]                             │
│    │                 │  ─ [COMPLETAR lógica]                                 │
│    └────────┬────────┘  ─ GROUP BY: [COMPLETAR]                              │
│             │                                                                │
│             ▼                                                                │
│    ┌─────────────────┐      ┌─────────────────┐                              │
│    │  Power BI       │      │  Dashboards     │                              │
│    └─────────────────┘      └─────────────────┘                              │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### 6. Tabla de Metadatos Completa

```markdown
## metadata_table:

| Nodo | Tipo | Tabla/Archivo | Schema | Propietario | SLA | 
|------|------|---------------|--------|-------------|-----|
| SAP_EXT | SOURCE | [COMPLETAR] | [COMPLETAR] campos | [COMPLETAR] | - |
| BRONZE_01 | STAGE | [COMPLETAR] | [COMPLETAR] cols | [COMPLETAR] | - |
| SILVER_01 | CURATED | [COMPLETAR] | [COMPLETAR] cols | [COMPLETAR] | - |
| GOLD_01 | BUSINESS | [COMPLETAR] | [COMPLETAR] campos | [COMPLETAR] | [COMPLETAR] |
| PBI_01 | CONSUMER | [COMPLETAR] | - | [COMPLETAR] | - |
```

---

### 7. Ownership y Responsabilidades

```markdown
## ownership:

  pipeline_owner:
    name: "[COMPLETAR]"
    email: "[COMPLETAR]"
    team: "Data Engineering"
    role: "Propietario técnico"

  data_steward:
    name: "[COMPLETAR]"
    email: "[COMPLETAR]"
    team: "Business Intelligence"
    role: "Propietario de datos"

  contacts:
    on_call: "[COMPLETAR]"
    escalation: "[COMPLETAR]"

  security:
    classification: "Confidencial"
    data_masking: true
    pii_columns: ["[COMPLETAR]"]
```

---

### 8. Historial de Cambios

```markdown
## changelog:

  - version: "[COMPLETAR]"
    date: "[COMPLETAR]"
    change: "[COMPLETAR]"
    author: "[COMPLETAR]"
    ticket: "[COMPLETAR]"

  - version: "1.2.0"
    date: "2026-04-28"
    change: "Agrega tipo_gasto classification"
    author: "maria.garcia@transcore.com"
    ticket: "JIRA-DE-1842"

  - version: "1.1.0"
    date: "2026-03-15"
    change: "Agrega columnas region y responsable"
    author: "juan.lopez@transcore.com"
    ticket: "JIRA-DE-1651"

  - version: "1.0.0"
    date: "2026-01-15"
    change: "Pipeline inicial"
    author: "anonimo@transcore.com"
    ticket: "JIRA-DE-1001"
```

---

## Ejercicios de completamiento

### Ejercicio 1: Completar información de ownership

Llenar los campos `[COMPLETAR]` en la sección `ownership`.

### Ejercicio 2: Documentar un nuevo source

Agregar un segundo source al pipeline: `cat_centros` (catálogo de centros de coste).

```yaml
## sources:
  - name: "cat_centros"
    type: "parquet_table"
    location: "s3://transcore-dwh/reference/cat_centros/"
    # COMPLETAR: schema, owner, refresh_frequency
```

### Ejercicio 3: Actualizar changelog

Agregar una entrada al changelog documentando un cambio hypothetical que tu equipo realizó recently.

---

## Entregable

```markdown
## linaje_completado:
  metadata: [ yaml completo con campos completados ]
  diagrama: [ diagrama con nodos y flujos ]
  ownership: [ información de ownership ]
  changelog: [ historial actualizado ]
```

**Archivo a entregar:** `module-08/linaje/pipeline_kpis_financieros_metadata.yaml`

---

*TransCore - Data Engineer Básico - Módulo 08*
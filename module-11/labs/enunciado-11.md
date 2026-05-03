**Módulo 11** | **Duración: 2.5 horas** | **Tipo: Proyecto integrador en grupos** | **Jornada: J3 (3/3)**

# Proyecto Capstone: Data Lakehouse TransCore

## Objetivo

Diseñar e implementar una arquitectura Data Lakehouse completa para el caso TransCore, integrando todas las zonas (landing, bronze, silver, gold), aplicando reglas de calidad, documentando linaje y preparando una presentación/defensa arquitectónica.

---

## Caso TransCore: Contexto del Proyecto

### Sobre TransCore

TransCore es una empresa ficticia de logística y transporte que gestiona infraestructuras críticas incluyendo:
- Grúas portuarias de alta capacidad
- Puentes móviles sobre vías navegables
- Sistemas SCADA de control industrial

### Situación Actual

TransCore tiene datos dispersos en múltiples sistemas:
- **ERP**: Pedidos y gestión de inventario
- **WMS**: Sistema de gestión de almacenes
- **GPS**: Tracking de vehículos en tiempo real
- **SCADA**: Datos de sensores industriales (presión, temperatura, caudal)

### Requisito de Negocio

El equipo directivo ha aprobado un proyecto de modernización de datos para:
1. Centralizar todos los datos en un Data Lakehouse
2. Mejorar la visibilidad de operaciones en tiempo real
3. Habilitar analytics avanzados para mantenimiento predictivo
4. Cumplir con normativas de seguridad industrial

---

## Arquitectura Objetivo

```
┌─────────────┐      ┌───────────┐      ┌─────────┐      ┌─────────┐
│   Fuentes   │────▶│  Landing   │────▶│ Bronze  │────▶│  Silver  │
│  (archivos, │      │   (raw)   │      │ (raw,   │      │(cleansed│
│   APIs, DBs)│      │           │      │  audit) │      │ & valid)│
└─────────────┘      └───────────┘      └─────────┘      └────┬────┘
                                                              │
                                                        ┌─────▼─────┐
                                                        │   Gold    │
                                                        │(business  │
                                                        │  ready)   │
                                                        └─────┬─────┘
                                                              │
                                                        ┌─────▼─────┐
                                                        │ Catálogo  │
                                                        │  + Linaje │
                                                        └───────────┘
```

---

## Especificación de Fuentes de Datos

| Fuente | Tipo | Formato | Frecuencia | Volumen Estimado |
|--------|------|---------|------------|-------------------|
| `orders.csv` | Transaccional | CSV | Diaria | 10,000 registros/día |
| `customers.parquet` | Dimensión | Parquet | Semanal | 50,000 registros |
| `shipments_api.json` | API REST | JSON | Tiempo real | 5,000 eventos/día |
| `inventory.db` | OLTP | SQLite | Horaria | 100,000 registros |
| `GPS_events.csv` | IoT/Streaming | CSV | Cada 5 min | 1M eventos/día |

---

## Estructura de Zonas

### Zona Landing (Raw Ingestado)

**Propósito**: Recebir datos de fuentes externas sin transformaciones

**Características**:
- Retención: 7 días
- Formato: Original de la fuente
- Sin validaciones (solo metadata de ingesta)

### Zona Bronze (Raw Auditado)

**Propósito**: Datos crudos con metadata de auditoría

**Características**:
- Retención: 30 días
- Schema: Original + columnas de auditoría (`ingestion_timestamp`, `source_file`, `row_hash`)
- Validaciones básicas de formato

### Zona Silver (Cleansed & Validated)

**Propósito**: Datos limpiados y validados con reglas de calidad

**Características**:
- Retención: 1 año
- Schema: Estandarizado y limpio
- Reglas de calidad aplicadas
- Datos listos para analytics

### Zona Gold (Business Ready)

**Propósito**: Datasets agregados y optimizados para consumo de negocio

**Características**:
- Retención: Según negocio (típicamente 2-5 años)
- Formato: Optimizado para query (Parquet, Delta)
- Documentación completa
- Linaje certificado

---

## Modelo de Datos - Tablas Silver

### silver.orders

| Columna | Tipo | Descripción | Reglas de Calidad |
|---------|------|-------------|-------------------|
| `order_id` | STRING | PK, identificador único | No nulo, único |
| `customer_id` | STRING | FK a customers | Existe en customers |
| `order_date` | DATE | Fecha del pedido | No nulo, no futuro |
| `total_amount` | DECIMAL(10,2) | Importe total | > 0 |
| `status` | STRING | Estado del pedido | En valores permitidos |
| `ingestion_timestamp` | TIMESTAMP | Timestamp de ingesta | No nulo |

### silver.customers

| Columna | Tipo | Descripción | Reglas de Calidad |
|---------|------|-------------|-------------------|
| `customer_id` | STRING | PK | No nulo, único |
| `email` | STRING | Email del cliente | Formato válido |
| `name` | STRING | Nombre | No nulo |
| `country` | STRING | País | En lista válida |
| `created_at` | TIMESTAMP | Fecha creación | No nulo |

### silver.shipments

| Columna | Tipo | Descripción | Reglas de Calidad |
|---------|------|-------------|-------------------|
| `tracking_number` | STRING | PK | No nulo, único |
| `order_id` | STRING | FK a orders | Existe en orders |
| `status` | STRING | Estado del envío | En valores permitidos |
| `estimated_delivery` | DATE | Fecha estimada | No nulo, futuro |
| `actual_delivery` | DATE | Fecha real entrega | Nullable |

### silver.inventory

| Columna | Tipo | Descripción | Reglas de Calidad |
|---------|------|-------------|-------------------|
| `product_id` | STRING | PK | No nulo |
| `warehouse_id` | STRING | FK ubicación | No nulo |
| `quantity` | INT | Stock actual | >= 0 |
| `last_updated` | TIMESTAMP | Última actualización | No nulo |

### silver.gps_events

| Columna | Tipo | Descripción | Reglas de Calidad |
|---------|------|-------------|-------------------|
| `event_id` | STRING | PK | No nulo, único |
| `vehicle_id` | STRING | ID del vehículo | No nulo |
| `latitude` | FLOAT | Latitud | -90 a 90 |
| `longitude` | FLOAT | Longitud | -180 a 180 |
| `timestamp` | TIMESTAMP | Momento del evento | No nulo |
| `speed` | FLOAT | Velocidad km/h | >= 0 |

---

## Modelo de Datos - Tablas Gold

### gold.order_summary

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `order_id` | STRING | PK |
| `customer_name` | STRING | |
| `country` | STRING | |
| `order_date` | DATE | |
| `total_amount` | DECIMAL(10,2) | |
| `days_to_delivery` | INT | |
| `kpi_flag` | BOOLEAN | |

### gold.inventory_status

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `product_id` | STRING | PK |
| `product_name` | STRING | |
| `warehouse_id` | STRING | |
| `quantity` | INT | |
| `reorder_point` | INT | |
| `low_stock_alert` | BOOLEAN | |

---

## Reglas de Calidad de Datos

### silver.orders

| Regla | Descripción | Acción en Fallo |
|-------|-------------|-----------------|
| `order_date_not_null` | order_date no puede ser nulo | Rechazar registro |
| `order_date_valid` | order_date no puede ser futura | Rechazar registro |
| `total_amount_positive` | total_amount > 0 | Rechazar registro |
| `customer_exists` | customer_id existe en silver.customers | Rechazar registro |
| `status_valid` | status en ['pending', 'processing', 'shipped', 'delivered', 'cancelled'] | Rechazar registro |

### silver.customers

| Regla | Descripción | Acción en Fallo |
|-------|-------------|-----------------|
| `email_format` | Email matching regex pattern | Rechazar registro |
| `email_unique` | Email no duplicado | Rechazar registro |
| `created_at_not_null` | created_at no puede ser nulo | Rechazar registro |
| `country_valid` | country en lista de países válidos | Rechazar registro |

### silver.shipments

| Regla | Descripción | Acción en Fallo |
|-------|-------------|-----------------|
| `tracking_unique` | tracking_number único | Rechazar registro |
| `status_valid` | status en ['pending', 'in_transit', 'delivered', 'returned'] | Rechazar registro |
| `estimated_future` | estimated_delivery debe ser futuro | Rechazar registro |

---

## Lifecycle Management

### Políticas de Retención

| Zona | Retención | Archivado | Eliminación |
|------|-----------|-----------|-------------|
| Landing | 7 días | No | Automática |
| Bronze | 30 días | No | Automática |
| Silver | 1 año | A cold storage | Manual |
| Gold | 2 años | No | Manual con aprobación |

### Políticas de Particionado

- **Por fecha**: Tablas transaccionales particionadas por `order_date`
- **Por ubicación**: GPS events particionados por `date(timestamp)`
- **Por warehouse**: Inventory particionado por `warehouse_id`

---

## Requisitos del Proyecto

### Requisito 1: Diagrama de Arquitectura (25%)

**Entregable**: Diagrama arquitectónico en formato `.svg` o draw.io que muestre:

- Todas las zonas del Data Lakehouse (landing, bronze, silver, gold)
- Flujos de datos entre zonas con flechas etiquetadas
- Componentes de ingesta (pipelines)
- Componentes de procesamiento (Spark jobs, Dataframes)
- Servicios de almacenamiento (Azure Data Lake, Blob Storage)
- Catálogo y linaje (Azure Purview)
- Tecnologías utilizadas en cada etapa

**Plantilla de entrega**:

```
proyecto-transcore/arquitectura/diagrama-arquitectura.[svg|png]
```

---

### Requisito 2: Pipeline End-to-End (35%)

**Entregable**: Implementación de al menos UN pipeline completo

**Pipeline a implementar**:

```
orders.csv → [Ingesta Landing] → [Pipeline Bronze] → [Pipeline Silver] → [Gold Aggregation]
     ↓              ↓                    ↓                    ↓                    ↓
  [Fuente]    [landing/orders]    [bronze/orders]     [silver/orders]      [gold/order_summary]
```

**Para el pipeline implementar**:

1. **Script de ingesta** a landing (Python/Spark)
   - Lectura de archivo fuente
   - Escritura a zona landing con metadata

2. **Pipeline Bronze**:
   - Lectura desde landing
   - Aplicar schema
   - Añadir columnas de auditoría
   - Escritura a bronze

3. **Pipeline Silver**:
   - Lectura desde bronze
   - Aplicar reglas de calidad
   - Logging de excepciones
   - Escritura a silver

4. **Pipeline Gold**:
   - Join con dimensiones
   - Cálculo de KPIs
   - Agregaciones
   - Escritura a gold

5. **Documentación de linaje**:
   - Tabla con: dataset origen, transformaciones, dataset destino

**Plantilla de entrega**:

```
proyecto-transcore/pipelines/
├── ingesta_ordenes.py
├── pipeline_bronze.py
├── pipeline_silver.py
└── pipeline_gold.py
```

---

### Requisito 3: Calidad de Datos (20%)

**Entregable**: Implementar validaciones de calidad

**Para al menos 2 datasets** (orders y customers):

1. **Script de validación** con:
   - Al menos 3 reglas por dataset
   - Logging de registros válidos/inválidos
   - Métricas: % registros válidos, % nulls, % duplicates

2. **Reporte de calidad**:
   - Tabla con: regla, total_registros, registros_validos, registros_invalidos, porcentaje_exito

3. **Tratamiento de excepciones**:
   - Describe qué sucede con registros que fallan validación
   - Justificación de acción (rechazar, corregir, aceptar con warning)

**Plantilla de reporte de calidad**:

| Regla | Total Registros | Registros Válidos | Registros Inválidos | % Éxito |
|-------|----------------|-------------------|---------------------|---------|
| | | | | |
| | | | | |
| | | | | |

**Plantilla de tratamiento de excepciones**:

| Regla | Acción | Justificación |
|-------|--------|---------------|
| | | |
| | | |

**Plantilla de entrega**:

```
proyecto-transcore/calidad/
├── validacion_calidad.py
└── reporte_calidad.md
```

---

### Requisito 4: Documentación de Linaje (10%)

**Entregable**: Documentación completa de linaje

**Formato**: Tabla markdown con columnas:

| Dataset Origen | Tipo Origen | Transformación | Dataset Destino | Tipo Destino |
|----------------|--------------|----------------|------------------|--------------|
| | | | | |
| | | | | |
| | | | | |

**Plantilla de entrega**:

```
proyecto-transcore/linaje/
└── documentacion_linaje.md
```

---

### Requisito 5: Presentación y Defensa (10%)

**Duración**: 5 minutos por grupo

**Contenido requerido**:

1. **Pitch ejecutivo** (1-2 min)
   - Problema de negocio
   - Solución propuesta
   - Beneficios esperados

2. **Arquitectura** (1-2 min)
   - Diagrama de arquitectura
   - Decisiones técnicas clave

3. **Demo/Live walkthrough** (1 min)
   - Mostrar ejecución de pipeline
   - Mostrar datos en cada zona
   - Mostrar calidad y linaje

**Plantilla de entrega**:

```
proyecto-transcore/presentacion/
└── presentacion-grupo.[pptx|pdf]
```

---

## Formato de Entrega Final

```
proyecto-transcore/
├── arquitectura/
│   └── diagrama-arquitectura.[svg|png]
├── pipelines/
│   ├── ingesta_ordenes.py
│   ├── pipeline_bronce.py
│   ├── pipeline_silver.py
│   └── pipeline_gold.py
├── calidad/
│   ├── validacion_calidad.py
│   └── reporte_calidad.md
├── linaje/
│   └── documentacion_linaje.md
├── notebooks/
│   └── [cualquier notebook de exploración]
└── presentacion/
    └── presentacion-grupo.[pptx|pdf]
```

---

## Roles de Equipo Sugeridos (para grupos de 3-4)

| Rol | Responsabilidad |
|-----|-----------------|
| **Arquitecto de datos** | Diseño de arquitectura y diagrama |
| **Ingeniero de pipelines** | Implementación de pipelines |
| **Especialista de calidad** | Reglas de calidad y validaciones |
| **Presentador** | Preparación y ejecución de defensa |

---

*Caso TransCore - Data Lakehouse Project*
*Data Engineer Básico - Módulo 11*
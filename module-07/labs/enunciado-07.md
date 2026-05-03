# Laboratorio 1: Cálculo de KPIs y Generación Silver/Gold

**Módulo 07** | **Duración: 45 minutos** | **Tipo: Práctica B** | **Jornada: 2**

---

## Objetivo

En este laboratorio, calcularás **KPIs de disponibilidad de activos** utilizando datos de telemetría IoT de TransCore. Aplicarás técnicas de limpieza de datos, realizarás agregaciones y generarás datasets en las capas **Silver** (datos curados) y **Gold** (datos de negocio listos para consumo).

Al finalizar, serás capaz de:
- Limpiar y preparar datos de telemetría para análisis
- Calcular KPIs de disponibilidad: Disponibilidad %, MTBF y MTTR
- Generar datasets en formato Parquet en las capas Silver y Gold
- Aplicar buenas prácticas de arquitectura medallón

---

## Requisitos Previos

- Conocimiento básico de Pandas (DataFrames, groupby, merge)
- Conocimiento de Python (dict, list, datetime)
- Entorno Python con librerías: `pandas`, `pyarrow`, `python-dateutil`

---

## Dataset de Trabajo

Trabajarás con datos de telemetría IoT de sensores en activos de obra lineal:

| Archivo | Descripción |
|---------|-------------|
| `telemetria_parque_mes.csv` | Registros de telemetría del mes (50,000+ registros) |
| `activos.parquet` | Catálogo de activos con información de ubicación y tipo |
| `ordenes_mantenimiento.csv` | Órdenes de mantenimiento correctivo y preventivo |

### Estructura de telemetria_parque_mes.csv

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `activo_id` | string | Identificador único del activo |
| `timestamp` | datetime | Fecha y hora de la lectura |
| `sensor_id` | string | Identificador del sensor |
| `temperatura` | float | Temperatura en °C |
| `vibracion` | float | Vibración en mm/s |
| `estado_operativo` | int | 1=Operativo, 0=Detenido |

---

## Métricas KPI a Calcular

### 1. Disponibilidad (%)

$$Disponibilidad\% = \frac{Tiempo\ Operativo}{Tiempo\ Total} \times 100$$

### 2. MTBF (Mean Time Between Failures) - Tiempo Medio Entre Fallos

$$MTBF = \frac{Tiempo\ Total\ Operativo}{Número\ de\ Fallos}$$

### 3. MTTR (Mean Time To Repair) - Tiempo Medio de Reparación

$$MTTR = \frac{Tiempo\ Total\ de\ Inactividad}{Número\ de\ Reparaciones}$$

---

## Pasos del Laboratorio

### Paso 1: Cargar y explorar los datos

Crea un script `kpi_calculation.py` y carga los tres datasets proporcionados:
- `telemetria_parque_mes.csv`
- `activos.parquet`
- `ordenes_mantenimiento.csv`

Realiza una exploración inicial para verificar:
- Número de registros de cada dataset
- Tipos de datos de las columnas
- Primeras filas para entender la estructura

---

### Paso 2: Limpieza de datos

Aplica las siguientes transformaciones de limpieza sobre el dataset de telemetría:

1. **Convertir timestamp a datetime**: La columna `timestamp` debe estar en formato datetime para cálculos temporales
2. **Tratar valores nulos**:
   - Valores nulos en `temperatura` y `vibracion`: usar la mediana
   - Valores nulos en `estado_operativo`: rellenar con el último valor conocido (forward fill)
3. **Eliminar duplicados**: Registros duplicados que puedan existir
4. **Filtrar outliers**: Eliminar registros de vibración que estén fuera de 3 desviaciones estándar de la media

Reporta cuántos registros quedan después de la limpieza.

---

### Paso 3: Calcular tiempo operativo por activo

Para calcular los KPIs, necesitas determinar períodos operativos y de inactividad:

1. **Ordenar datos** por `activo_id` y `timestamp`
2. **Calcular duración entre lecturas** (en minutos) usando la diferencia entre timestamps consecutivos del mismo activo
3. **Rellenar última lectura**: Para la última lectura de cada activo, asume una duración típica de 5 minutos
4. **Calcular tiempo operativo**: Multiplica la duración por el estado operativo (1 u 0)
5. **Agregar por activo**: Suma el tiempo total y tiempo operativo por cada activo

**Plantilla de entrega - Tabla resumen_tiempo:**

| activo_id | tiempo_total_min | tiempo_operativo_min |
|-----------|------------------|----------------------|
|           |                  |                      |
|           |                  |                      |

---

### Paso 4: Detectar fallos y calcular tiempos de reparación

1. **Detectar transiciones de estado**:
   - Fallo: cuando `estado_operativo` pasa de 1 a 0
   - Reparación: cuando `estado_operativo` pasa de 0 a 1
2. **Contar fallos y reparaciones por activo**
3. **Calcular tiempo de reparación**: Tiempo entre un fallo y la siguiente reparación (en minutos)
4. **Sumar tiempo total de reparación por activo**

**Plantilla de entrega - Tabla fallos:**

| activo_id | num_fallos | num_reparaciones | tiempo_reparacion_min |
|-----------|------------|------------------|-----------------------|
|           |            |                  |                       |
|           |            |                  |                       |

---

### Paso 5: Calcular KPIs finales

Combina los resultados de los pasos anteriores y calcula los tres KPIs para cada activo:

1. **Disponibilidad %** = (tiempo_operativo_min / tiempo_total_min) × 100
2. **MTBF** = tiempo_operativo_min / num_fallos (evita división por cero)
3. **MTTR** = tiempo_reparacion_min / num_reparaciones (evita división por cero)

Guarda el resultado en formato Parquet: `silver/kpis_activos.parquet`

**Plantilla de entrega - Tabla KPIs (primeros 5 activos):**

| activo_id | disponibilidad_pct | mtbf_min | mttr_min |
|-----------|-------------------|----------|----------|
|           |                   |          |          |
|           |                   |          |          |
|           |                   |          |          |
|           |                   |          |          |
|           |                   |          |          |

---

### Paso 6: Enriquecer con datos de activos y generar capa Silver

1. Combina (merge) los KPIs calculados con la información de activos para añadir:
   - `nombre`
   - `tipo`
   - `ubicacion`
   - `fecha_puesta_servicio`

2. Guarda el dataset enriquecido en: `silver/kpis_activos_silver.parquet`

**Plantilla de entrega - Columnas del dataset Silver:**

Lista las columnas finales del dataset Silver:
- 
- 
- 

---

### Paso 7: Generar capa Gold (KPIs de negocio)

Genera dos agregaciones de negocio a partir del dataset Silver:

**1. KPIs por tipo de activo:**
- Agrupa por `tipo`
- Calcula: número de activos, promedio de disponibilidad, MTBF promedio, MTTR promedio
- Guarda en: `gold/kpis_por_tipo.parquet`

**2. KPIs por ubicación:**
- Agrupa por `ubicacion`
- Calcula: número de activos, promedio de disponibilidad, MTBF promedio, MTTR promedio
- Guarda en: `gold/kpis_por_ubicacion.parquet`

**Plantilla de entrega - KPIs por tipo de activo:**

| tipo | num_activos | disp_promedio | mtbf_promedio | mttr_promedio |
|------|-------------|---------------|---------------|---------------|
|      |             |               |               |               |
|      |             |               |               |               |

**Plantilla de entrega - KPIs por ubicación:**

| ubicacion | num_activos | disp_promedio | mtbf_promedio | mttr_promedio |
|-----------|-------------|---------------|---------------|---------------|
|           |             |               |               |               |
|           |             |               |               |               |

---

## Estructura de Archivos Esperada

Al finalizar, debes tener la siguiente estructura:

```
module-07/
├── kpi_calculation.py          # Tu script principal
├── data/
│   ├── telemetria_parque_mes.csv
│   ├── activos.parquet
│   └── ordenes_mantenimiento.csv
├── silver/
│   ├── kpis_activos.parquet
│   └── kpis_activos_silver.parquet
└── gold/
    ├── kpis_por_tipo.parquet
    └── kpis_por_ubicacion.parquet
```

---

## Entregables

1. **Script `kpi_calculation.py`** con todo el código desarrollado
2. **Datasets generados**:
   - `silver/kpis_activos.parquet`
   - `silver/kpis_activos_silver.parquet`
   - `gold/kpis_por_tipo.parquet`
   - `gold/kpis_por_ubicacion.parquet`
3. **Documento con tablas completadas** según las plantillas de este enunciado

---

## Preguntas de Análisis

1. ¿Qué tipo de activo tiene mayor disponibilidad promedio?
2. ¿Qué ubicación tiene el MTTR más bajo? ¿Qué implica esto para el mantenimiento?
3. ¿Qué ventajas tiene usar Parquet vs CSV para almacenar los KPIs?
4. ¿Por qué separamos los datos en capas Silver y Gold?

---

*TransCore - Data Engineer Básico - Módulo 07*

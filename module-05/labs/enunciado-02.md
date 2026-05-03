# Ejercicio 2: Estimar Coste de Pipeline Básico

**Módulo 05** | **Duración: 20 minutos** | **Tipo: Ejercicio Práctico** | **Jornada: J1**

---

## Objetivo

Aplicar principios FinOps para calcular el coste operativo mensual de un pipeline de ingestión en AWS que procesa datos de telemetría IoT para TransCore. Aprender a desglosar los costes por componente e identificar oportunidades de optimización.

---

## Prerrequisitos

- Comprensión básica de servicios AWS (S3, Lambda, Glue)
- Familiaridad con conceptos FinOps (CapEx vs OpEx)
- Calculadora o hoja de cálculo (Excel/Google Sheets)
- Conocimientos básicos de pricing cloud

---

## Contexto del Caso

TransCore necesita procesar diariamente **500 MB** de datos de telemetría desde sensores IoT en la red ferroviaria. El pipeline propuesto incluye:

1. **AWS Lambda** para validación inicial de ficheros (ejecuta 3 veces/día)
2. **AWS S3** como almacenamiento landing y procesamiento
3. **AWS Glue** Data Catalog y crawlers para descubrimiento de schemas
4. **AWS Glue ETL** job para transformación a formato Parquet
5. **Amazon CloudWatch** para monitorización

**Precios de referencia (eu-west-1):**

| Servicio | Concepto | Precio |
|----------|---------|--------|
| S3 Standard | Almacenamiento | $0.023/GB/mes |
| S3 | PUT request | $0.005/1,000 |
| S3 | GET request | $0.0004/1,000 |
| S3 | LIST request | $0.005/1,000 |
| Lambda | Compute | $0.0000166667/GB-segundo |
| Lambda | Solicitud | $0.0000002/und |
| Glue | DPU-hora | $0.44/hora |
| CloudWatch Logs | Ingesta | $0.50/GB |
| CloudWatch Metrics | Métrica estándar | $0.10/mes |
| CloudWatch | Consulta dashboard | $0.0000055/und |

---

## Desarrollo

### Parte 1: Identificar Componentes y Sus Variables de Coste

#### Paso 1: Inventariar componentes y datos de uso

Rellena la siguiente tabla con los datos de uso del pipeline:

| Componente | Variables de Uso | Tus datos del caso |
|------------|-----------------|--------------------|
| S3 | Almacenamiento, Solicitudes, Transferencia | |
| Lambda | Número ejecuciones, Duración, Memoria | |
| Glue Crawler | Tiempo de ejecución | |
| Glue ETL | DPU, Tiempo de ejecución | |
| CloudWatch | Volumen logs, Métricas | |

---

### Parte 2: Calcular Coste de S3

Utiliza los datos del caso para calcular:

1. **Almacenamiento mensual**: Considera los 500 MB/día de entrada y una retención de 90 días. ¿Cuántos GB/mes se almacenan de media?
2. **Solicitudes mensuales**: ¿Cuántas solicitudes PUT, GET y LIST se esperan al mes?
3. **Transferencia de datos**: ¿Cuántos GB se transfieren OUT a Internet al mes?

Aplica los precios de la tabla de referencia.

**Subtotal S3 = $_______/mes**

---

### Parte 3: Calcular Coste de Lambda

Datos de configuración:
- Memoria: 256 MB
- Duración promedio: 2 segundos
- Ejecuciones: 3/día × 30 días = 90 ejecuciones/mes

Calcula:
1. **Compute**: GB-segundos consumidos al mes y coste asociado
2. **Solicitudes**: coste de las 90 solicitudes

**Subtotal Lambda = $_______/mes**

---

### Parte 4: Calcular Coste de AWS Glue

#### Crawler:
- 1 crawler que ejecuta 1 vez al día, 15 minutos por ejecución
- 30 ejecuciones/mes

**Subtotal Crawler = $_______/mes**

#### ETL Job:
- 1 job que ejecuta 1 vez al día, 10 minutos por ejecución
- 2 DPUs asignadas
- 30 ejecuciones/mes

**Subtotal ETL = $_______/mes**

**Subtotal Glue = $_______/mes**

---

### Parte 5: Calcular Coste de CloudWatch

Calcula el coste de:
1. **Logs**: ~10 KB de logs por ejecución Lambda × 90 ejecuciones = ~0.9 MB/mes
2. **Métricas y Alarmas**: 5 métricas estándar + 1 alarma
3. **Consultas dashboard**: ~100 consultas/mes

**Subtotal CloudWatch = $_______/mes**

---

### Parte 6: Consolidar Resumen de Costes

| Servicio | Componente | Coste Mensual |
|----------|------------|---------------|
| S3 | Storage | |
| S3 | Solicitudes | |
| S3 | Transferencia | |
| Lambda | Compute + Requests | |
| Glue | Crawler | |
| Glue | ETL Job | |
| CloudWatch | Logs + Metrics | |
| **TOTAL** | | |

---

### Parte 7: Proyección Anual y Optimización

#### Proyección a 12 meses

Calcula el coste anual sin descuentos.

**Coste anual = $_______**

#### Identificar oportunidades de optimización

Aplica las siguientes optimizaciones y calcula el nuevo coste mensual:

| Optimización | Impacto estimado | Ahorro mensual |
|--------------|------------------|-----------------|
| Reserved Capacity para Glue (70% descuento) | Coste Glue pasa de $0.44 a $0.132/DPU-hora | $_______ |
| Reducir Glue ETL a 1 DPU (fuera de peak) | 50% reducción en coste ETL | $_______ |
| Cambiar lifecycle S3 a Glacier a los 30 días | 60% reducción en storage | $_______ |
| Comprimir datos antes de guardar en landing | 70% reducción en transferencia | $_______ |

**Coste optimizado = $_______/mes**

---

## Entregable

Rellena la siguiente tabla con tus resultados:

```
┌─────────────────────────────────────────────────────────────┐
│           PIPELINE DE INGESTIÓN - ANÁLISIS FINOPS           │
├─────────────────────────────────────────────────────────────┤
│  Componente          │ Coste Base  │ Coste Optimizado       │
│  ────────────────────┼─────────────┼────────────────────────│
│  S3 Storage          │             │                        │
│  S3 Solicitudes      │             │                        │
│  S3 Transferencia    │             │                        │
│  Lambda              │             │                        │
│  Glue Crawler        │             │                        │
│  Glue ETL            │             │                        │
│  CloudWatch          │             │                        │
│  ────────────────────┼─────────────┼────────────────────────│
│  TOTAL MENSUAL       │             │                        │
│  TOTAL ANUAL         │             │                        │
│  AHORRO ANUAL        │             │                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Preguntas de Reflexión

1. **¿Cómo afectaría al coste duplicar el volumen de datos de 500 MB a 1 GB/día?**
2. **¿Qué pasaría si el pipeline ejecutara cada hora en vez de 3 veces al día?**
3. **¿Es más económico procesar en streaming con Kinesis o mantener el batch con Glue?**
4. **¿Qué componente representa el mayor coste? ¿Por qué?**
5. **¿Qué otras optimizaciones se podrían aplicar al pipeline?**
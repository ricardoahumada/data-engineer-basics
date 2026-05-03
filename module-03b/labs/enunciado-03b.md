# Lab 3b: Práctica - Mapa Comparativo de BBDD por Caso de Uso

**Módulo 03b** | **Duración: 15 minutos** | **Tipo: Práctica individual** | **Jornada: J1**

---

## Objetivo

Crear una matriz de decisión que compare y seleccione tipos de bases de datos para distintos casos de uso en TransCore, evaluando OLTP, OLAP y NoSQL según los requisitos de cada fuente de datos.

---

## Contexto

En TransCore, el equipo de datos trabaja con múltiples fuentes de información que tienen requisitos distintos. No todas las bases de datos son iguales ni sirven para los mismos propósitos. La selección correcta del tipo de base de datos impacta directamente en:

- Rendimiento de las aplicaciones
- Coste de infraestructura
- Facilidad de mantenimiento
- Escalabilidad futura

---

## Requisitos Previos

- Haber completado las secciones 3.1 a 3.3 del módulo 03b
- Comprender las diferencias entre OLTP y OLAP
- Conocer los tipos de bases de datos NoSQL: documentales, key-value, columnares, grafos
- Entender el teorema CAP: consistencia, disponibilidad, tolerancia a partición

---

## Escenario TransCore

### Fuentes de Datos y Requisitos

En TransCore tenemos las siguientes fuentes/sistemas:

| ID | Fuente | Descripcion | Volumen | Patron Acceso |
|----|--------|-------------|---------|---------------|
| **A** | SAP PM | Ordenes de mantenimiento | 10K registros/dia | Lectura/escritura transactiones individuales |
| **B** | Plataforma IoT | Telemetria de sensores | 1M eventos/hora | Escritura masiva, lectura ocasional |
| **C** | GMAO | Partes de trabajo | 5K registros/dia | Transacciones, consultas ad-hoc |
| **D** | Cache Sensores | Estado actual de activos | 50K claves | Key-value, latencia ultra-baja |
| **E** | Consola KPIs | Agregaciones para dashboards | TBs de datos | Solo lectura, queries complejas |
| **F** | Grafo Activos | Relaciones entre activos | 100K nodos | Relaciones complejas, traversal |

---

## Tipos de Bases de Datos a Evaluar

### OLTP (Online Transaction Processing)

| Tecnologia | Descripcion | Ejemplo Cloud |
|------------|-------------|---------------|
| PostgreSQL | Relacional open-source robusto | Azure Database for PostgreSQL |
| MySQL | Relacional popular, alta velocidad | Amazon RDS MySQL |
| Oracle | Enterprise-grade, maxima fiabilidad | Oracle Cloud ATP |

### OLAP (Online Analytical Processing)

| Tecnologia | Descripcion | Ejemplo Cloud |
|------------|-------------|---------------|
| Snowflake | Data Warehouse cloud-native | Snowflake |
| BigQuery | Serverless, ML integrado | Google BigQuery |
| Redshift |MPP, optimizado para Amazon | Amazon Redshift |
| Synapse | Integrate with Azure ecosystem | Azure Synapse Analytics |

### NoSQL - Documentales

| Tecnologia | Descripcion | Ejemplo Cloud |
|------------|-------------|---------------|
| MongoDB | Documentos JSON flexibles | MongoDB Atlas |
| DocumentDB | AWS managed MongoDB-compatible | Amazon DocumentDB |
| CouchDB | Distributed, offline-first | CouchDB Cloud |

### NoSQL - Key-Value

| Tecnologia | Descripcion | Ejemplo Cloud |
|------------|-------------|---------------|
| Redis | Ultra-fast, in-memory | Redis Enterprise Cloud |
| DynamoDB | Serverless, any scale | Amazon DynamoDB |
| Cassandra | Distribuida, alta disponibilidad | Amazon Keyspaces |

### NoSQL - Columnares

| Tecnologia | Descripcion | Ejemplo Cloud |
|------------|-------------|---------------|
| Snowflake | Tambien ofrece storage columnar | Snowflake |
| BigQuery | Almacenamiento columnar nativo | Google BigQuery |
| Redshift | Massive Parallel Processing | Amazon Redshift |

### NoSQL - Grafos

| Tecnologia | Descripcion | Ejemplo Cloud |
|------------|-------------|---------------|
| Neo4j | Graph database lider | Neo4j Aura |
| Amazon Neptune | Multi-model (graph) | Amazon Neptune |
| Azure Cosmos DB | Graph API | Azure Cosmos DB (Gremlin) |

---

## Instrucciones

### Paso 1: Crear la Matriz de Decision

Completa la siguiente matriz para cada fuente de datos:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                           MATRIZ DE DECISION - BASES DE DATOS                          │
├────────────────┬───────────────────────────────────────────────────────────────────────┤
│                │                              FUENTE                                   │
│    CRITERIO    ├─────────┬─────────┬─────────┬─────────┬─────────┬─────────────────┤
│                │  A      │  B      │  C      │  D      │  E      │  F               │
│                │  SAP PM │  IoT    │  GMAO   │  Cache  │  KPIs   │  Grafo Activos   │
├────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────────────┤
│ Tipo BBDD      │         │         │         │         │         │                 │
│ Recomendado    │         │         │         │         │         │                 │
├────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────────────┤
│ Tecnologia     │         │         │         │         │         │                 │
│ Especifica     │         │         │         │         │         │                 │
├────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────────────┤
│ Opcion 2       │         │         │         │         │         │                 │
│ Alternativa    │         │         │         │         │         │                 │
├────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────────────┤
│ Opcion 3       │         │         │         │         │         │                 │
│ Tercera opcion │         │         │         │         │         │                 │
├────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────────────┤
│ Justificacion  │         │         │         │         │         │                 │
│ breve          │         │         │         │         │         │                 │
└────────────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────────────┘
```

### Paso 2: Evaluar segun Criterios

Para cada fuente, justifica tu decisión basándote en:

| Criterio | Pregunta a Responder |
|----------|----------------------|
| **Consistencia vs Disponibilidad** | Necesitas consistencia inmediata (CP) o siempre disponible (AP)? |
| **Patron de lectura** | Queries simples por ID o análisis complejo agregado? |
| **Patron de escritura** | Transacciones individuales o batches masivas? |
| **Volumen y velocidad** | Cuantos datos por unidad de tiempo? |
| **Esquema** | Estructura fija o flexible/variable? |
| **Coste** | Budget limitado o puede invertir en enterprise? |

### Paso 3: Analizar Trade-offs CAP

Para cada fuente, indica su posición en el triángulo CAP:

```
                        
                            /\
                           /  \
                          /    \
          CONSISTENCIA   /      \
                        /        \
                       /          \  DISPONIBILIDAD
                      /            \
                     /              \
                    /                \
                   /                  \
                  ──────────────────────
                  TOLERANCIA A PARTICION
```

**Zonas del triángulo:**
- **CP** (arriba): Consistencia + Tolerancia a Partición
- **AP** (izquierda): Disponibilidad + Tolerancia a Partición
- **CA** (derecha): Consistencia + Disponibilidad (no tolerante a particiones)

### Paso 4: Resumen de Selecciones

Redacta un párrafo (100-150 palabras) justificando las decisiones principales y los trade-offs aceptados.

---

## Entregable

En 15 minutos, entrega:

1. **Matriz de decisión completa** con tipo recomendado, tecnología específica y alternativas
2. **Justificación** para cada fuente de datos
3. **Diagrama CAP** con la posición de cada fuente
4. **Resumen ejecutivo** de las decisiones
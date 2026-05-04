# Caso de Ejemplo: TransCore Ingeniería

## 1. Contexto de la Empresa

**TransCore Ingeniería** es una empresa ficticia de ingeniería de infraestructuras ferroviarias. A lo largo de todas las sesiones del curso, utilizaremos este caso como hilo conductor para ilustrar la aplicación práctica de los conceptos de Data Engineering.

La empresa opera en dos dominios integrados:

### Dominio A — Obra Lineal

Gestión de obras lineales ferroviarias que incluye:

- **Partes de trabajo diarios**: Registro de actividades realizadas en campo y oficina
- **Telemetría IoT**: Datos de sensores embebidos en infraestructuras (vibraciones, temperatura, deformaciones)
- **Volumen**: ~2.000 partes de trabajo generados al día en proyectos activos

### Dominio B — Activos Ferroviarios

Gestión del inventario y mantenimiento de activos de infraestructura:

- **Inventario de activos**: Vías, catenaria, señalización y otros elementos ferroviarios
- **Órdenes de mantenimiento**: Preventivo y correctivo sobre activos
- **Volumen**: ~150.000 activos registrados con consolidación semanal

---

## 2. Sistemas de Origen de Datos

TransCore gestiona sus datos en múltiples sistemas desconectados:

| Sistema | Descripción | Dominio | Tipo de datos |
|---------|-------------|---------|---------------|
| **SAP PM** | Gestión de mantenimiento (Partes de trabajo, órdenes) | A + B | Estructurado (batch diario) |
| **Plataforma IoT** | Telemetría de sensores en infraestructuras | A | Streaming (particionado por fecha) |
| **GMAO** | Gestión de Mantenimiento Asistida por Ordenador | B | Estructurado (batch semanal) |
| **PostgreSQL Legacy** | Inventario histórico de activos | B | Estructurado |

```
                    ┌─────────────────────────────────────────────────────────┐
                    │                    TRANS_CORE                           │
                    │            Sistemas Desconectados                       │
                    └─────────────────────────────────────────────────────────┘

         ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
         │  SAP PM  │      │   IoT    │      │  GMAO    │      │PostgreSQL│
         │          │      │Platform  │      │          │      │  Legacy  │
         └────┬─────┘      └────┬─────┘      └────┬─────┘      └────┬─────┘
              │                 │                 │                 │
              ▼                 ▼                 ▼                 ▼
         ┌─────────────────────────────────────────────────────────┐
         │              DATA LAKEHOUSE (Objetivo)                  │
         │  landing ──► bronze ──► silver ──► gold                 │
         └─────────────────────────────────────────────────────────┘
```

---

## 3. Datasets del Curso

Todos los ejercicios y laboratorios trabajan sobre cuatro datasets sintéticos simulados.

### 3.1 partes_trabajo.csv

**Origen simulado**: Export SAP PM (batch diario)  
**Descripción**: Partes de trabajo diarios generados en campo y oficina

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_parte` | VARCHAR | Identificador único del parte (PT-XXXX) |
| `id_equipo` | VARCHAR | Equipo al que se asigna (EQ-XXX) |
| `fecha_inicio` | TIMESTAMP | Fecha y hora de inicio |
| `fecha_fin` | TIMESTAMP | Fecha y hora de fin (puede estar vacía) |
| `horas_trabajo` | DECIMAL | Horas invertidas |
| `tipo_mantenimiento` | VARCHAR | PREVENTIVO, CORRECTIVO, EMERGENCIA, INSPECCION |
| `estado` | VARCHAR | PENDIENTE, COMPLETADO, EN_PROCESO |
| `descripcion` | TEXT | Descripción de la tarea realizada |

**Ejemplo de registro:**
```
PT-0001,EQ-002,2026-03-23T00:00:00,2026-03-23T02:00:00,2.0,PREVENTIVO,PENDIENTE,Mantenimiento preventivo en equipo EQ-038
```

**Problemas de calidad observados:**
- Valores nulos en `fecha_fin` (partes sin cerrar)
- Valores nulos en `horas_trabajo`
- Inconsistencias en estados

### 3.2 inventario_activos.csv

**Origen simulado**: PostgreSQL Legacy  
**Descripción**: Catálogo de activos ferroviarios

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `activo_id` | VARCHAR | Identificador único (ACT-XXXX) |
| `tipo_activo` | VARCHAR | Tipo: VIA, CATENARIA, SENALIZACION, etc. |
| `linea` | VARCHAR | Línea ferroviaria |
| `kilometro` | DECIMAL | Punto kilométrico |
| `estado` | VARCHAR | ACTIVO, INACTIVO, MANTENIMIENTO |
| `fecha_instalacion` | DATE | Fecha de puesta en servicio |

### 3.3 ordenes_mantenimiento.csv

**Origen simulado**: GMAO (batch semanal)  
**Descripción**: Órdenes de mantenimiento preventivo y correctivo

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `orden_id` | VARCHAR | Identificador (OM-XXXXX) |
| `activo_id` | VARCHAR | Activo relacionado (ACT-XXXX) |
| `tipo_orden` | VARCHAR | PREVENTIVO, CORRECTIVO, PREDICTIVO |
| `fecha_creacion` | TIMESTAMP | Fecha de creación |
| `fecha_ejecucion` | TIMESTAMP | Fecha de ejecución real |
| `estado` | VARCHAR | ABIERTA, EN_PROCESO, COMPLETADA, CANCELADA |
| `prioridad` | VARCHAR | ALTA, MEDIA, BAJA |
| `descripcion` | TEXT | Descripción de la orden |

**Ejemplo de registro:**
```
OM-00001,ACT-0023,CORRECTIVO,,2026-03-17T00:00:00,COMPLETADA,ALTA,Orden de predictivo para activo ACT-0029
```

### 3.4 telemetria_parque_mes.csv

**Origen simulado**: Plataforma IoT (particionado por fecha)  
**Descripción**: Lecturas de sensores IoT embebidos en infraestructuras

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `activo_id` | VARCHAR | Equipo monitorizado (EQ-XXX) |
| `timestamp` | TIMESTAMP | Momento de la lectura |
| `sensor_id` | VARCHAR | Identificador del sensor (TEMP-001, VIB-001, PRES-001) |
| `temperatura` | DECIMAL | Temperatura en °C (solo para sensores TEMP) |
| `vibracion` | DECIMAL | Vibración en mm/s (solo para sensores VIB) |
| `estado_operativo` | INTEGER | 0 = apagado, 1 = operativo |

**Ejemplo de registro:**
```
EQ-037,2026-04-01T00:00:00,TEMP-001,82.97,,1
EQ-037,2026-04-01T00:00:00,VIB-001,,31.78,1
EQ-037,2026-04-01T00:00:00,PRES-001,,,1
```

---

## 4. Problemática y Reto

TransCore necesita consolidar todos sus datos en una arquitectura **Data Lakehouse** con las siguientes zonas:

| Zona | Propósito | Contenido |
|------|-----------|-----------|
| **Landing** | Recepción raw | Datos exactamente como llegan de las fuentes |
| **Bronze** | Raw mejorado | Datos depurados sin cambios de esquema |
| **Silver** | Datos business-ready | Datos curados, con transformación de negocio |
| **Gold** | datasets de consumo | Agregaciones y métricas para análisis |

### Objetivos del Data Lakehouse

1. **Alertas de calidad automáticas** sobre partes de trabajo diarios
2. **Cálculo de KPIs** de disponibilidad y mantenimiento de activos
3. **Publicación de datasets gold** para equipos de operaciones e ingeniería


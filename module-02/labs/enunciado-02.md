# Mini-Reto: Elegir Enfoque para Reporting Operativo

**Módulo 02** | **Duración: 10 minutos** | **Tipo: Mini-reto individual**

---

## Objetivo

Seleccionar y justificar entre arquitecturas **pull** (consulta periódica) y **push** (envío proactivo) para un caso de reporting operativo en TransCore.

---

## Contexto

En TransCore, el equipo de operaciones ferroviarias necesita recibir reportes de disponibilidad de activos en tiempo casi real. El Data Engineer debe decidir si implementar un enfoque donde los consumidores preguntan por los datos (pull) o donde el sistema envía notificaciones cuando hay cambios relevantes (push).

Esta decisión tiene implicaciones directas en:
- Latencia de la información
- Coste de infraestructura
- Complejidad de mantenimiento
- Escalabilidad del sistema

---

## Escenario TransCore

### Situación Actual

TransCore tiene un Data Lakehouse funcionando con las siguientes características:

- Datos de sensores IoT fluyendo cada 5 minutos a la zona landing
- Proceso ETL programado cada hora para actualizar silver
- Dashboards operativos en Power BI con actualización cada 2 horas
- 50 analistas de operaciones consultando dashboards

### Nuevo Requisito

El director de operaciones ha solicitado que los ingenieros de mantenimiento reciban **alertas instantáneas** cuando:

1. Un activo crítico (señales, agujas, francos) cambia su estado a no disponible
2. La disponibilidad de un tramo cae por debajo del 90%
3. Se detecta una anomalía en los datos de telemetría

---

## Opciones a Evaluar

### Opción A: Enfoque Pull (Query Periódica)

```
┌─────────────┐     ┌───────────────┐      ┌─────────────┐
│ Dashboard   │────▶│ Power BI      │────▶│ Consulta    │
│ Operador    │     │ Service       │      │ periódica   │
└─────────────┘     └───────────────┘      │ cada 5 min  │
                                           └─────────────┘
```

- Refresh automático cada 5 minutos en Power BI
- No requiere infraestructura adicional
- Latencia mínima: 5 minutos

### Opción B: Enfoque Push (Streaming + Alertas)

```
┌─────────────┐     ┌──────────────┐      ┌─────────────┐
│ Sensor IoT  │────▶│ Kafka        │────▶│ Spark       │
│ datos       │     │              │      │ Streaming   │
└─────────────┘     └──────────────┘      └──────┬──────┘
                                                 │
                                                 ▼
                                         ┌─────────────┐
                                         │ Alertas     │
                                         │ Email/SMS   │
                                         └─────────────┘
```

- Procesamiento en tiempo real con Spark Streaming
- Envío de alertas instantáneas
- Requiere infraestructura Kafka + Spark
- Latencia: segundos

### Opción C: Enfoque Híbrido

```
┌─────────────┐     ┌──────────────┐      ┌─────────────┐
│ Sensor IoT  │────▶│ Bronze       │────▶│ Power BI    │
│ datos       │     │ (landing)    │      │ Refresh     │
└─────────────┘     └──────────────┘      │ cada 5 min  │
                                          └─────────────┘
                                                │
                                         ┌──────┴──────┐
                                         │             │
                                         ▼             ▼
                                  ┌───────────┐ ┌───────────┐
                                  │ Alertas   │ │ Dashboards│
                                  │ críticas  │ │ operativos│
                                  └───────────┘ └───────────┘
```

- Uso de Power BI push datasets para alertas críticas
- Dashboard operativo con refresh periódico
- Balance entre coste y funcionalidad

---

## Instrucciones

### Paso 1: Evaluar los Criterios

Evalúa cada opción según los siguientes criterios (1-5, donde 5 es mejor):

| Criterio | Peso | Opción A | Opción B | Opción C |
|----------|------|----------|----------|----------|
| Latencia (menor es mejor) | 25% | | | |
| Coste de implementación | 20% | | | |
| Complejidad operacional | 20% | | | |
| Escalabilidad | 15% | | | |
| Mantenimiento sencillo | 10% | | | |
| Tolerancia a fallos | 10% | | | |

**Puntuación Total Ponderada** = Σ(Criterio × Peso)

### Paso 2: Documentar Trade-offs

Para cada opción, identifica al menos:

- **2 ventajas** de la aproximación
- **2 desventajas** o riesgos
- **1 caso de uso ideal** donde la opción es la mejor elección

### Paso 3: Tomar la Decisión

Redacta un párrafo de justificación (100-150 palabras) donde:

1. Indiques qué opción seleccionas
2. Expliques los 3 factores decisive que te llevan a esa elección
3. Menciones qué sacrificas al tomar esa decisión (trade-off aceptado)

### Paso 4: Preparar Elevator Pitch

```
"Para el caso de alertas críticas de mantenimiento en TransCore, 
 recomiendo [OPCIÓN] porque [RAZÓN 1], [RAZÓN 2] y [RAZÓN 3]. 
 Esto implica aceptar [TRADE-OFF]."
```

---

## Entregable

Entrega en 10 minutos:

1. Tabla de evaluación con puntuaciones
2. Trade-offs documentados para cada opción
3. Decisión justificada (100-150 palabras)
4. Elevator pitch final

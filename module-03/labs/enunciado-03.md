# Lab 3: Práctica A - Diagrama de Entidades y Flujos entre Zonas

**Módulo 03** | **Duración: 30 minutos** | **Tipo: Práctica en parejas**

---

## Objetivo

Crear un diagrama completo que muestre las entidades principales de TransCore y los flujos de datos entre las zonas landing/bronze/silver/gold del Data Lakehouse.

---

## Contexto

En TransCore, empresa de gestión de activos ferroviarios, necesitamos modelar el flujo de datos desde las fuentes operacionales hasta los datasets de consumo final. El dominio de mantenimiento de activos genera datos de:

- **SAP PM**: Sistema de gestión de mantenimiento preventivo y correctivo
- **Plataforma IoT**: Sensores que monitorizan estado de activos en tiempo real
- **GMAO**: Sistema de gestión de órdenes de trabajo y partes diarios

Tu objetivo es representar cómo estos datos fluyen a través de las zonas del Data Lakehouse y cómo se estructuran en entidades de hechos y dimensiones.

---

## Prerequisites

- Haber completado las secciones 3.1 a 3.4 del módulo 03
- Comprender el concepto de tablas de hechos vs dimensiones
- Conocer los esquemas star/snowflake para modelado analítico
- Entender las zonas de datos: landing, bronze, silver, gold

---

## Escenario TransCore

### Fuentes de Datos

| Fuente | Tipo | Frecuencia | Datos Principales |
|--------|------|------------|-------------------|
| **SAP PM** | ERP | Diaria | Órdenes de mantenimiento, estados, prioridades |
| **IoT Platform** | Streaming | Cada 5 min | Telemetría: vibraciones, temperatura, posición |
| **GMAO** | Sistema Operacional | Diaria | Partes de trabajo, horas, materiales consumidos |

### Dominio de Mantenimiento

El dominio de mantenimiento de TransCore abarca:

1. **Activos Ferroviarios**: Vías, señales, agujas, puentes, estaciones
2. **Órdenes de Mantenimiento**: Preventivo, correctivo, predictivo
3. **Partes de Trabajo**: Registro diario de actividades
4. **Historial de Estados**: Cambios de estado de cada activo

---

## Instrucciones

### Paso 1: Identificar Entidades de Hechos

Revisa las fuentes de datos e identifica los eventos/transacciones que generan métricas.

**Tu respuesta:**

| Nombre Tabla | Descripción | Tipo Flujo |
|-------------|-------------|------------|
|              |             |            |
|              |             |            |
|              |             |            |

### Paso 2: Identificar Dimensiones

Para cada hecho, identifica las entidades que los describen.

**Tu respuesta:**

| Nombre Tabla | Descripción | Atributos Principales |
|-------------|-------------|----------------------|
|              |             |                      |
|              |             |                      |
|              |             |                      |
|              |             |                      |
|              |             |                      |

### Paso 3: Dibujar el Diagrama de Flujo

Crea un diagrama que muestre:

- Las 3 fuentes de datos (SAP PM, IoT Platform, GMAO)
- Las 4 zonas: Landing → Bronze → Silver → Gold
- Los flujos de datos entre zonas
- Las entidades de hechos y dimensiones en la zona Gold
- Los formatos de almacenamiento asociados a cada zona

**Tu diagrama:**

```
[Pega o dibuja aquí tu diagrama usando el formato que prefieras:
 SVG, Mermaid, o descripción textual estructurada]

Estructura sugerida:

FUENTES ──────► LANDING ──────► BRONZE ──────► SILVER ──────► GOLD
                                                            │
                                                            ├── dim_activos
                                                            ├── dim_tiempo
                                                            ├── dim_ubicacion
                                                            ├── fact_ordenes_mantenimiento
                                                            ├── fact_telemetria
                                                            └── fact_partes_trabajo
```

### Paso 4: Detallar Transformaciones

Para cada flujo entre zonas, documenta las transformaciones aplicadas:

**Template:**

```markdown
ZONA A → ZONA B

[Tabla_Source] → [Tabla_Dest]

Transformaciones:
1. [Transformación 1]
2. [Transformación 2]
3. [Transformación 3]

Validaciones:
- [Validación 1]
- [Validación 2]
```

**Plantilla para documentar cada flujo:**

```markdown
[Fuente] → [Tabla_Landing]

Transformaciones:
1.

Validaciones:
-

[Tabla_Landing] → [Tabla_Bronze]

Transformaciones:
1.

Validaciones:
-

[Tabla_Bronze] → [Tabla_Silver]

Transformaciones:
1.

Validaciones:
-
```

### Paso 5: Especificar Formatos de Almacenamiento

Investiga qué formato, partición y compresión son apropiados para cada zona. Justifica tus decisiones basándote en las características de cada zona.

**Tu respuesta:**

| Zona | Formato | Partición | Compresión | Justificación |
|------|---------|-----------|------------|---------------|
| Landing | | | | |
| Bronze | | | | |
| Silver | | | | |
| Gold | | | | |

---

## Entregable

En 30 minutos, entrega:

1. **Diagrama de flujo completo** con todas las fuentes, zonas y entidades
2. **Tabla de transformaciones** documentada para al menos 3 flujos (SAP→Landing→Bronze, IoT→Landing→Bronze, GMAO→Landing→Bronze)
3. **Tabla de formatos** con justificaciones para cada zona
4. **Esquema star** detallado en la zona gold que muestre cómo se relacionan los hechos con sus dimensiones

**Formato preferido**: SVG drawable o descripción textual estructurada

---

## Siguiente Paso

Este diagrama servirá como referencia para la construcción de pipelines en los módulos 06 y 07.
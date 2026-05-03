**Módulo 09** | **Duración: 15 minutos** | **Tipo: Mini-reto individual** | **Case Study: TransCore**

# Lab 1: Mini-reto - Contrato de Consumo para KPI Crítico

---

## Objetivo

Diseñar un contrato de consumo completo (schema + SLA + documentación) para el KPI "Disponibilidad de activos críticos" del caso TransCore.

---

## Contexto

TransCore necesita publicar el dataset gold de KPIs de mantenimiento para el equipo de operaciones. El KPI "Disponibilidad de activos críticos" es un indicador de negocio crítico que determina el porcentaje de tiempo que los activos de infraestructura (grúas, puentes móviles, sistemas de control) están operativos.

Como Data Engineer, debes definir el contrato de consumo que permitirá a los consumidores (dashboard de operaciones, equipos de mantenimiento,管理层) acceder a este dato de forma confiable.

---

## Requisitos Previos

- Conocimientos básicos de JSON Schema
- Comprensión de conceptos de SLA y documentación de datos
- Familiaridad con arquitectura de datos (zonas bronze/silver/gold)

---

## Recursos Proporcionados

Se asume que existe en la capa gold el dataset `gold.asset_availability_kpi` con la siguiente estructura base:

```json
{
  "asset_id": "string",
  "asset_name": "string",
  "asset_type": "string",
  "location": "string",
  "availability_percentage": "float",
  "downtime_hours": "float",
  "last_maintenance_date": "date",
  "next_scheduled_maintenance": "date",
  "status": "string",
  "calculation_timestamp": "timestamp"
}
```

---

## Instrucciones

### Paso 1: Definir el Schema del Dataset (5 min)

Define la estructura completa del dataset utilizando JSON Schema. El contrato debe incluir:

1. **Metadatos del dataset**:
   - Nombre oficial del dataset
   - Versión del contrato
   - Propietario (owner)
   - Descripción funcional

2. **Schema de columnas**:
   - Cada columna con nombre, tipo de dato, descripción, y si es requerida u opcional
   - Constraints de validación (ej: `availability_percentage` entre 0 y 100)
   - Identificar clave primaria

3. **Ejemplo de registro válido**:
   - Proporcionar un ejemplo de documento que cumpla con el schema

### Paso 2: Definir Frecuencia de Actualización (3 min)

Documenta la frecuencia de actualización del dataset:

1. **Frecuencia de refresco**:
   - ¿Cada cuánto se actualiza el dataset? (real-time, hourly, daily)
   - Justificar la frecuencia elegida

2. **Ventana de procesamiento**:
   - ¿Qué ventana de datos cubre cada actualización?
   - ¿Se incluyen datos históricos o solo el período actual?

3. **Latencia aceptada**:
   - Tiempo máximo entre la generación del dato y su disponibilidad en gold

### Paso 3: Definir SLA de Disponibilidad (3 min)

Establece los SLAs que el equipo de datos se compromete a cumplir:

1. **SLA de disponibilidad del servicio**:
   - Porcentaje de uptime del dataset (ej: 99.5%)
   - Ventana de mantenimiento permitida

2. **SLA de calidad**:
   - Porcentaje mínimo de registros válidos
   - Umbrales de calidad aceptables

3. **SLA de latencia**:
   - Tiempo máximo de actualización
   - Tiempo de respuesta para queries

### Paso 4: Documentación de Metadatos (4 min)

Completa la documentación del dataset incluyendo:

1. **Lineage (Linaje)**:
   - Fuentes de origen de los datos
   - Transformaciones aplicadas

2. **Clasificación de sensibilidad**:
   - Nivel de confidencialidad (bajo/medio/alto/crítico)

3. **Documentación de uso**:
   - Casos de uso permitidos
   - Restricciones de uso
   - Contacto del equipo de soporte

---

## Entregable

Genera un documento de contrato de consumo con el siguiente formato:

```markdown
# Contrato de Consumo: Disponibilidad de Activos Críticos

## 1. Información General del Dataset
[Completa aquí]

## 2. JSON Schema
[Incluye el JSON Schema completo]

## 3. Ejemplo de Registro
[Un ejemplo válido]

## 4. Frecuencia y Latencia
[Documenta frecuencia y SLAs]

## 5. SLA de Disponibilidad
[Define SLAs]

## 6. Linaje de Datos
[Documenta origen y transformaciones]

## 7. Clasificación y Documentación
[Clasificación y guías de uso]
```

---

## Recursos Adicionales

- Referencia: JSON Schema https://json-schema.org/
- Caso TransCore: Ver slides del Módulo 9 sobre "Contratos de consumo"

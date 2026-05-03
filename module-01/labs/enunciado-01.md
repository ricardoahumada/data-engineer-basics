# Ejercicio 1: Mapa RACI del Dominio de Mantenimiento

**Módulo 01** | **Duración: 15 minutos** | **Tipo: Ejercicio individual**

---

## Objetivo

Crear un mapa RACI que identifique las responsabilidades del **Data Engineer** frente a otros roles de datos en el contexto de TransCore.

---

## Contexto

En TransCore, empresa de gestión de activos ferroviarios, el equipo de datos está compuesto por varios roles que deben colaborar para construir una infraestructura de datos robusta:

- **Data Engineer**: Habilitador central de la infraestructura de datos
- **Data Analyst de Operaciones**: Genera informes semanales de disponibilidad de activos
- **Data Scientist de Predictivo**: Construye modelos predictivos de mantenimiento
- **Data Architect**: Diseña la arquitectura general del Data Lakehouse

---

## Significado de RACI

| Código | Significado | Descripción |
|--------|-------------|-------------|
| **R** | Responsible | Quien ejecuta la tarea |
| **A** | Accountable | Quien tiene la responsabilidad final |
| **C** | Consulted | Quien aporta información antes de la decisión |
| **I** | Informed | Quien recibe información sobre resultados |

> **Regla**: Solo puede haber un **Accountable** por actividad.

---

## Actividades del Dominio

Completa la matriz RACI para las siguientes 10 actividades:

1. Ingesta de datos desde SAP PM
2. Ingesta de datos desde plataforma IoT
3. Ingesta de datos desde GMAO
4. Limpieza y validación de datos crudos
5. Modelado de datos en schema star
6. Construcción de dashboards operativos
7. Entrenamiento de modelos predictivos
8. Monitoreo de calidad de datos
9. Documentación de linaje de datos
10. Publicación de datasets para consumo interno

---

## Plantilla de Entrega

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                           MATRIZ RACI - DOMINIO MANTENIMIENTO                  │
├─────────────────┬──────────────┬──────────────┬───────────────┬────────────────┤
│ Actividad       │ Data Engineer│ Data Analyst │ Data Scientist│ Data Architect │
├─────────────────┼──────────────┼──────────────┼───────────────┼────────────────┤
│ 1. Ingesta SAP  │              │              │               │                │
├─────────────────┼──────────────┼──────────────┼───────────────┼────────────────┤
│ 2. Ingesta IoT  │              │              │               │                │
├─────────────────┼──────────────┼──────────────┼───────────────┼────────────────┤
│ 3. Ingesta GMAO │              │              │               │                │
├─────────────────┼──────────────┼──────────────┼───────────────┼────────────────┤
│ 4. Limpieza     │              │              │               │                │
├─────────────────┼──────────────┼──────────────┼───────────────┼────────────────┤
│ 5. Modelado     │              │              │               │                │
├─────────────────┼──────────────┼──────────────┼───────────────┼────────────────┤
│ 6. Dashboards   │              │              │               │                │
├─────────────────┼──────────────┼──────────────┼───────────────┼────────────────┤
│ 7. ML Predictivo│              │              │               │                │
├─────────────────┼──────────────┼──────────────┼───────────────┼────────────────┤
│ 8. Monitoreo    │              │              │               │                │
├─────────────────┼──────────────┼──────────────┼───────────────┼────────────────┤
│ 9. Documentacion│              │              │               │                │
├─────────────────┼──────────────┼──────────────┼───────────────┼────────────────┤
│ 10. Publicacion │              │              │               │                │
└─────────────────┴──────────────┴──────────────┴───────────────┴────────────────┘
```

---

## Preguntas de Análisis

Responde brevemente:

1. ¿Hay alguna actividad sin **Accountable**? ¿Por qué sería problemático?
2. ¿Hay alguna actividad donde todos los roles son solo **Informed**? ¿Qué implica?
3. ¿Dónde hay más de un **Responsible**? ¿Puede generar conflictos?

---

## Entregable

Envía tu matriz RACI completa con:
1. Códigos RACI asignados para las 10 actividades
2. Respuestas a las 3 preguntas de análisis

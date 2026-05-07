# Data Governance - Guía Qlik

**Fuente:** [Qlik - Data Governance](https://www.qlik.com/us/data-governance)

---

## ¿Qué es Data Governance?

Data Governance es el conjunto de **roles, procesos, políticas y herramientas** que aseguran la calidad adecuada de los datos durante todo su lifecycle y el uso correcto en toda la organización. Permite a los usuarios encontrar, preparar, usar y compartir datasets de confianza de forma autónoma, sin depender de IT.

---

## ¿Por qué es Importante?

**Beneficios principales:**
- Datos de alta calidad para analytics y BI → mejores decisiones de negocio
- Mejora la precisión, completitud y consistencia de datos
- Previene el mal uso de datos
- Acuerdo en definiciones comunes de datos
- Elimina silos entre departamentos y sistemas
- Aumenta la confianza en datos para análisis y toma de decisiones
- Facilita el cumplimiento de regulaciones: GDPR, HIPAA

> **Tendencia:** Las regulaciones están combinando gestión de datos, seguridad, privacidad e identidad. Gobernanza y seguridad son prioridad cuando se comparten APIs y datos con partners.

---

## Framework de Data Governance

El framework tiene **3 componentes principales**: Personas, Procesos y Tecnología.

![Framework de Data Governance - Personas, Procesos, Tecnología](https://assets.qlik.com/image/upload/w_1060/q_auto/qlik/glossary/data-governance/seo-data-governance-framework_y0prmm.png)

### Personas

| Rol | Descripción |
|-----|-------------|
| **Steering Committee** | CDO y ejecutivos de cada unidad de negocio. Define políticas, estándares, misión y objetivos. |
| **Governance Team** | Gestionado por un data governance manager. Compuesto por data architects y especialistas de IT. |
| **Data Stewards** | Gestiona datasets y es responsable de la calidad y políticas por dominio. |
| **Data Consumers** | Usuarios que acceden a los datos para proyectos y análisis. |

### Procesos

Procesos formales para garantizar ejecución y aplicación consistente de políticas. Se describen en flow charts que aclaran inputs y tareas para cada caso de uso.

### Tecnología

Herramientas y técnicas para mantener seguridad, integridad, linaje, usabilidad y disponibilidad de datos. Un **data catalog** moderno profilea y documenta cada data source y define quién puede realizar qué acciones.

---

## Mejores Prácticas

### 1. Escribir un Glossary

Un data glossary (o diccionario) que defina términos y conceptos de negocio proporciona contexto consistente across tools. Ejemplo: definir qué califica como "Marketing Qualified Lead" o "Inactive Customer".

### 2. Mapear y Clasificar Datos

- **Mapear** dónde residen los datos → saber en qué sistema están y cómo fluyen
- **Clasificar** datasets según privacidad o sensibilidad → determinar cómo se aplican las políticas

### 3. Establecer un Data Catalog

Un catálogo de datos basado en casos de uso permite hacer diferentes tipos de datos disponibles a diferentes usuarios rápidamente, sin comprometer el riesgo.

![Data Catalog de Qlik Sense](https://assets.qlik.com/image/upload/w_2004/q_auto/qlik/glossary/data-governance/seo-data-governance-qlik-catalog_qphxbv.png)

---

## El Rol de Data Lineage

**Data lineage** rastrea todos los cambios hechos a los datos en su journey desde la fuente hasta la ubicación actual.

**Utilidad:**
- Entender y visualizar cambios y flujos de datos
- Saber de dónde vino un dato específico
- Cómo se split y merge con otros datos
- Qué transformaciones se aplicaron
- **Traza de errores** hasta la causa raíz

Un data steward o data engineer usa la visualización de linaje para confiar en los datos.

![Data Lineage - Flujo de datos fuente a destino](https://assets.qlik.com/image/upload/w_2552/q_auto/qlik/glossary/data-management/seo-data-lineage-how-it-works_zwb0ta.png)

---

## Desafío Clave: Balancear Velocidad y Riesgo

**Tensión tradicional:**
- **Proveedores de datos**: trabajan responsablemente para provisiónar datos a todos sin riesgo
- **Consumidores de datos**: quieren datos para proyectos **inmediatamente**

**Solución: Sistema de niveles (funnel)**

![Funnel de Governance - Balanceando velocidad y riesgo](https://assets.qlik.com/image/upload/w_1060/q_auto/qlik/glossary/data-governance/seo-data-governance-balancing-speed-risk_mb2zyk.jpg)

| Etapa | Descripción |
|-------|-------------|
| **Identified** | Datos identificados y catalogados |
| **Available** | Datos disponibles para usuarios autorizados |
| **Fit for Purpose** | Datos validados para casos de uso específicos |
| **Curated** | Datos curados con altos estándares de calidad |

Este sistema permite:
- Focus en comprensión breadth (amplitud) a nivel enterprise
- Restricciones a datos sensibles
- Depth (profundidad) para un número menor de data assets críticos

---

## Resumen

| Concepto | Descripción |
|----------|-------------|
| **Data Governance** | Roles, procesos, políticas y herramientas para calidad y uso correcto de datos |
| **Framework** | 3 componentes: Personas (Steering Committee, Data Stewards), Procesos, Tecnología |
| **Data Catalog** | Registro centralizado con metadatos, linaje y control de acceso |
| **Data Lineage** | Tracking del journey de datos desde fuente hasta destino final |
| **Best Practices** | Glossary, classification, data catalog |
| **Desafío** | Balancear velocidad de provisión con control de riesgos |

---

## Referencia

**Fuente:** Qlik - Data Governance Guide  
**URL:** https://www.qlik.com/us/data-governance  
**Última actualización:** 2026
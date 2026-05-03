**Módulo 10** | **Duración: 30 minutos** | **Tipo: Práctica guiada** | **Case Study: TransCore Data Lakehouse**

# Lab 1: Práctica C - Matriz de Permisos y Alta en Catálogo

## Objetivo

Crear una matriz de control de acceso basado en roles (RBAC) para el Data Lake TransCore y registrar un dataset gold en el catálogo empresarial, documentando nombre, owner, clasificación y linaje.

---

## Contexto

TransCore ha implementado un Data Lakehouse con múltiples zonas (landing, bronze, silver, gold). El equipo de seguridad te ha solicitado:

1. Definir una matriz de control de acceso basado en roles (RBAC) para regular quién puede acceder a qué datos en cada zona
2. Registrar el dataset `gold.order_summary` en el catálogo empresarial con toda su metadata de gobernanza

Este lab se divide en dos partes:
- **Parte A**: Matriz de permisos RBAC (15 min)
- **Parte B**: Alta de dataset en Purview (15 min)

---

## Parte A: Matriz de Permisos RBAC

### Zonas del Data Lake

| Zona | Descripción | Contenido |
|------|-------------|-----------|
| `landing` | Raw data ingestado | Archivos recibidos de fuentes |
| `bronze` | Raw data auditado | Datos crudos con metadata de ingesta |
| `silver` | Datos Cleansed | Datos validados y limpiados |
| `gold` | Datos Business-Ready | Aggregaciones y datasets de negocio |

### Roles Definidos

| Rol | Descripción |
|-----|-------------|
| **Data Owner** | Responsable del negocio que genera/usa los datos. Tiene permisos de lectura y aprobación |
| **Data Steward** | Profesional técnico que gestiona la calidad y gobernanza. Tiene permisos de lectura, escritura y curación |
| **Data Consumer** | Usuario de negocio que consulta datos. Tiene permisos de solo lectura |
| **Data Engineer** | Responsable de pipelines y arquitectura. Tiene permisos de lectura y escritura en todas las zonas excepto gold |
| **Data Security Officer** | Responsable de seguridad y cumplimiento. Tiene permisos de lectura en todas las zonas |

### Datasets de Ejemplo

| Dataset | Zona | Sensibilidad |
|---------|------|---------------|
| `orders.csv` | landing | Alta |
| `customers.parquet` | bronze | Media |
| `silver.orders` | silver | Alta |
| `silver.customers` | silver | Media |
| `gold.order_summary` | gold | Alta |
| `gold.inventory_status` | gold | Crítica |

### Instrucciones Parte A

#### Paso 1: Crear Matriz de Permisos

Construye una matriz que muestre qué operaciones (Read, Write, Delete, Admin) puede realizar cada rol en cada zona.

**Formato de la matriz:**

| Rol | Landing | Bronze | Silver | Gold |
|-----|---------|--------|--------|------|
| Data Owner | | | | |
| Data Steward | | | | |
| Data Consumer | | | | |
| Data Engineer | | | | |
| Data Security Officer | | | | | |

**Leyenda de permisos:**
- **R**: Read (lectura)
- **W**: Write (escritura/ingesta)
- **D**: Delete (eliminación)
- **A**: Admin (administración total)

#### Paso 2: Justificar Permisos

Para cada permiso concedido, escribe una breve justificación (1-2 oraciones) explicando por qué ese rol necesita ese nivel de acceso.

#### Paso 3: Verificar Cumplimiento Normativo

Identifica qué controles AAA (Autenticación, Autorización, Auditoría) aplican a cada zona.

---

## Parte B: Alta de Dataset en Azure Purview

### Instrucciones Parte B

#### Paso 1: Completar Ficha de Metadatos

Completa la siguiente ficha para el dataset `gold.order_summary`:

## Ficha de Dataset - Azure Purview

### Información Básica
| Campo | Valor |
|-------|-------|
| **Nombre técnico** | `gold.order_summary` |
| **Nombre de negocio** | |
| **Descripción** | |
| **Owner** | |
| **Contacto** | |
| **Zona** | Gold |
| **Tipo** | Tabular (Parquet) |

### Clasificación de Datos
| Campo | Valor |
|-------|-------|
| **Sensibilidad** | |
| **Categoría RGPD** | |
| **Etiquetas de compliance** | |

### Linaje
| Campo | Valor |
|-------|-------|
| **Fuente origen** | |
| **Pipeline** | |
| **Transformaciones** | |
| **Frecuencia** | |

### SLA
| Campo | Valor |
|-------|-------|
| **Refresh** | |
| **SLA de disponibilidad** | |
| **Latencia máxima** | |

#### Paso 2: Definir Permisos de Acceso

Documenta qué roles pueden acceder a este dataset y con qué nivel de acceso:

| Rol | Permiso | Justificación |
|-----|---------|---------------|
| | | |

#### Paso 3: Documentar Linaje Completo

Dibuja o describe el linaje desde las fuentes hasta el dataset gold:

```
[Fuente] → [Pipeline] → [Zona Landing] → [Zona Bronze] → [Zona Silver] → [Zona Gold]
    ↓              ↓              ↓                  ↓              ↓              ↓
 
```

---

## Entregable Final

Entrega un documento que contenga:

1. **Matriz RBAC completa** con permisos por zona y justificación
2. **Ficha de dataset** completa para `gold.order_summary`
3. **Diagrama de linaje** documentado

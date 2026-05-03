**Módulo 04** | **Duración: 15 minutos** | **Tipo: Demo Guiada** | **Jornada: J1**

# Lab 1: Organización de Bucket y Definición de Lifecycle

## Objetivo

Diseñar la estructura de un bucket S3 para TransCore con zonas landing/bronze/silver/gold, y definir políticas de lifecycle para automatizar la transición entre clases de almacenamiento y la expiración de datos.

## Prerrequisitos

- Cuenta AWS con acceso a S3
- AWS CLI configurado con credenciales válidas
- Permisos para crear buckets y aplicar políticas de lifecycle
- Conocimientos básicos de estructura de buckets S3

## Desarrollo

### Parte 1: Diseño de Estructura de Bucket

#### Paso 1: Definir la Estructura de Carpetas

Para el caso TransCore, diseña la estructura de prefijos dentro del bucket `transcore-infra-prod-eu-west-1`.

El sistema debe soportar:
- **Zona landing**: datos crudos de ingestión
- **Zona raw**: datos sin transformar
- **Zona silver**: datos curados
- **Zona gold**: datos agregados para analytics
- **Zona archive**: archivo en glacier

Cada zona debe incluir subcarpetas para:
- obra-lineal (topografía, ingeniería, mantenimiento)
- activos-ferroviarios (vías, estaciones, señalización, catenaria)
- sensores-iot (temperatura, vibración, posición GPS)

Define la estructura de carpetas y documéntala:

#### Paso 2: Convenciones de Particionamiento

Define un formato de particionamiento que permita pruning eficiente en consultas. Utiliza formato Hive-style partitioning (`año=YYYY/mes=MM/dia=DD`) para organizar los datos por fecha.

Diseña el formato de rutas para cada zona:

```
landing/<dominio>/<formato_particion>/<fichero>
raw/<dominio>/<formato_particion>/<fichero>
```

---

### Parte 2: Crear Bucket desde Consola AWS

#### Paso 3: Crear el Bucket

Desde la consola AWS (S3), crea un bucket en la región `eu-west-1` con un nombre único que siga la convención `transcore-infra-prod-<region>`.

#### Paso 4: Habilitar Versionado

Desde las propiedades del bucket, habilita el versionado para protegerte contra eliminaciones accidentales.

#### Paso 5: Habilitar Encriptación por Defecto

Desde las propiedades del bucket, configura encriptación AES-256 por defecto para todos los objetos.

---

### Parte 3: Definir Políticas de Lifecycle

#### Paso 6: Crear Política de Lifecycle Completa

Crea un archivo JSON con la política de lifecycle. Define transiciones y expiraciones para las siguientes zonas:

| Zona | Día → Standard-IA | Día → Glacier | Día → Glacier Deep Archive | Expiración |
|------|-------------------|---------------|---------------------------|------------|
| landing/ | ? | ? | - | ? |
| raw/ | ? | - | ? | ? |
| silver/ | - | ? | - | ? |
| gold/ | - | ? | - | ? |
| archive/ | - | - | ? | ? |

Además, incluir reglas para:
- Limpieza de uploads incompletos
- Expiración de versiones antiguas

#### Paso 7: Aplicar Política de Lifecycle al Bucket

Desde la consola AWS (Propiedades → Gestión del ciclo de vida), crea las reglas de lifecycle para cada zona definida en el Paso 6.

---

### Parte 4: Verificación

#### Paso 8: Verificar Configuración

Desde la consola AWS verifica:

1. **Versionado**: Propiedades → Versionado → "Habilitado"
2. **Encriptación**: Propiedades → Encriptación por defecto → "Habilitado" con AES-256
3. **Política de lifecycle**: Propiedades → Gestión del ciclo de vida → Reglas creadas
4. **Estructura**: Objetos → Ver prefijos creados

---

## Entregables

Al finalizar la demo, debes tener:

1. Bucket creado con nombre `transcore-infra-prod-eu-west-1`
2. Versionado habilitado
3. Encriptación AES-256 por defecto
4. Políticas de lifecycle aplicadas para cada zona
5. Estructura de carpetas documentada

## Comandos de Limpieza (Opcional)

Desde la consola AWS:
- Eliminar política de lifecycle desde Propiedades → Gestión del ciclo de vida
- Deshabilitar versionado desde Propiedades → Versionado
- Eliminar bucket vaciado previamente
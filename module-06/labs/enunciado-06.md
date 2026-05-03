**Módulo 06** | **Duración: 60 minutos** | **Tipo: Laboratorio Práctico** | **Jornada: J2**

# Laboratorio 1: Ingesta File → Landing + Informe de Perfilado

---

## Objetivo

Implementar un pipeline de ingesta desde archivo CSV hasta zona landing en S3, y ejecutar un proceso de profiling de datos para entender la estructura, tipos de datos, valores nulos y calidad general de los datos ingestados. Al finalizar, generar un informe de perfilado con estadísticas descriptivas y hallazgos de calidad.

---

## Prerrequisitos

- Cuenta AWS con acceso a S3, Lambda, Glue, CloudWatch
- AWS CLI configurado con credenciales válidas
- Python 3.9+ instalado con librerías: pandas, pyarrow, s3fs
- Conocimientos básicos de pandas para análisis de datos
- Bucket S3 ya creado (o crear durante el lab)

---

## Recursos Necesarios

### Archivos de Datos de Prueba

Se utilizará un dataset de ejemplo: `partes_trabajo.csv` (datos de partes de trabajo de mantenimiento SAP PM)

El dataset contiene registros con los siguientes campos:

| Campo | Descripción |
|-------|-------------|
| id_parte | Identificador único del parte de trabajo |
| id_equipo | Identificador del equipo asociado |
| fecha_inicio | Fecha y hora de inicio del trabajo |
| fecha_fin | Fecha y hora de finalización del trabajo |
| horas_trabajo | Horas dedicadas al trabajo |
| tipo_mantenimiento | Tipo: PREVENTIVO, CORRECTIVO, PREDICTIVO |
| estado | Estado: COMPLETADO, EN_PROCESO, ABIERTO, CANCELADO |
| descripcion | Descripción textual del trabajo |

### Herramientas

- Python 3.9+ con pandas, numpy, pyarrow
- AWS CLI
- Editor de texto (VS Code recomendado)
- Jupyter Notebook o terminal

---

## Desarrollo

### Parte 1: Preparación del Entorno

#### Paso 1: Crear Estructura de Carpetas Locales

Crear la siguiente estructura de directorios para el proyecto:

```
~/data-engineer-lab/lab-ingesta/
├── data/
│   ├── raw/
│   ├── landing/
│   └── profile_reports/
```

#### Paso 2: Crear Dataset de Prueba

Crear el archivo `data/raw/partes_trabajo.csv` con el contenido del dataset de ejemplo proporcionado en la sección de recursos.

#### Paso 3: Instalar Dependencias Python

Instalar las librerías necesarias:

```bash
pip install pandas numpy pyarrow s3fs awswrangler jupyter
```

---

### Parte 2: Pipeline de Ingesta a Landing

#### Paso 4: Crear Script de Ingesta

Crear archivo `ingesta_landing.py` que implemente las siguientes funcionalidades:

1. **Lectura del archivo fuente** CSV desde `data/raw/partes_trabajo.csv`
2. **Validación de formato** - verificar que el DataFrame contiene las columnas esperadas:
   - id_parte, id_equipo, fecha_inicio, fecha_fin, horas_trabajo, tipo_mantenimiento, estado, descripcion
3. **Añadir metadatos de ingesta**:
   - `_ingesta_timestamp`: timestamp ISO de la ingesta
   - `_ingesta_usuario`: nombre del usuario que ejecuta la ingesta
   - `_source_file`: nombre del archivo fuente original
4. **Generar clave única para S3** con estructura de directorios por fecha:
   ```
   landing/obra-lineal/mantenimiento/año={YYYY}/mes={MM}/dia={DD}/partes_trabajo_{HHMMSS}.csv
   ```
5. **Subir archivo a S3** en el bucket `transcore-infra-prod-eu-west-1`
6. **Calcular checksum SHA256** del archivo antes de subirlo
7. **Guardar metadata de ingesta** en archivo JSON junto al CSV en S3

**Indicaciones técnicas:**
- Usar `boto3` para interacción con S3
- Usar `pandas` para manipulación de datos
- Usar `hashlib` para cálculo de SHA256
- Implementar logging básico para seguimiento de ejecución

#### Paso 5: Ejecutar Pipeline de Ingesta

Ejecutar el script y verificar que el archivo se ha subido correctamente a S3.

---

### Parte 3: Profiling de Datos

#### Paso 6: Crear Script de Profiling

Crear archivo `profiling_report.py` que genere un informe completo de profiling con las siguientes secciones:

1. **Metadata del informe:**
   - Nombre del archivo origen
   - Fecha de generación
   - Número de registros y columnas

2. **Análisis por columna:**
   - Tipo de dato
   - Número y porcentaje de valores nulos
   - Número de valores únicos
   - Completitud (porcentaje de valores no nulos)
   - Para columnas numéricas: min, max, media, mediana, desviación estándar
   - Para columnas categóricas: top 5 valores más frecuentes

3. **Resumen ejecutivo:**
   - Total de registros y columnas
   - Completitud global del dataset
   - Score de calidad

4. **Hallazgos de calidad:**
   - Identificar registros sin `id_equipo`
   - Identificar registros sin `fecha_fin` que no estén en estado EN_PROCESO
   - Identificar valores de `horas_trabajo` fuera del rango válido [0-24]
   - Identificar valores de `tipo_mantenimiento` que no sean PREVENTIVO, CORRECTIVO o PREDICTIVO

El script debe generar dos archivos de salida:
- `data/profile_reports/informe_profiling.json`
- `data/profile_reports/informe_profiling.md`

**Indicaciones técnicas:**
- Usar `pandas` y `numpy` para análisis estadístico
- Usar la función `isna()` para detectar valores nulos
- Usar `value_counts()` para identificar valores más frecuentes
- Implementar validación de reglas de negocio

#### Paso 7: Ejecutar Profiling

Ejecutar el script y verificar que se generan los archivos de informe.

---

## Entregables

Al finalizar el laboratorio, entregar:

1. **Script de ingesta** (`ingesta_landing.py`) funcionando correctamente
2. **Script de profiling** (`profiling_report.py`) que genera informes en JSON y Markdown
3. **Archivo CSV subido a S3** en la zona landing con estructura de directorios por fecha
4. **Archivo JSON de metadata** de ingesta en S3
5. **Informe de profiling** (`informe_profiling.json` e `informe_profiling.md`) con el análisis completo
6. **Captura de pantalla** mostrando la verificación de los archivos en S3 (opcional)

---

## Preguntas de Análisis

1. ¿Qué columnas tienen el mayor porcentaje de valores nulos? ¿Cuál podría ser la causa?
2. ¿Hay algún registro con horas de trabajo fuera del rango esperado [0-24]? ¿Cómo afectarían estos datos a un informe de KPIs?
3. ¿Los hallazgos de calidad encontrados requieren acción correctiva antes de procesar los datos en zonas posteriores?

---

##Plantilla de Informe de Profiling

| Métrica | Valor |
|---------|-------|
| Total Registros | |
| Total Columnas | |
| Completitud Global | |
| Score Calidad | |

### Análisis por Columna

| Columna | Tipo Dato | Nulos | % Nulos | Únicos | Completitud |
|---------|-----------|-------|---------|--------|-------------|
| id_parte | | | | | |
| id_equipo | | | | | |
| fecha_inicio | | | | | |
| fecha_fin | | | | | |
| horas_trabajo | | | | | |
| tipo_mantenimiento | | | | | |
| estado | | | | | |
| descripcion | | | | | |

### Hallazgos de Calidad

| # | Tipo | Campo | Gravedad | Descripción | Impacto | Recomendación |
|---|------|-------|----------|-------------|---------|---------------|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

# Solución Lab 1: Organización de Bucket y Definición de Lifecycle

---

## Solución Paso a Paso

### Parte 1: Diseño de Estructura de Bucket

#### Paso 1: Definir la Estructura de Carpetas

**Estructura Completa del Bucket `transcore-infra-prod-eu-west-1`:**

```
transcore-infra-prod-eu-west-1/
│
├── landing/                          # Zona landing: datos crudos ingestados
│   ├── obra-lineal/                   # Topografía e ingeniería civil
│   │   └── año=YYYY/mes=MM/dia=DD/
│   ├── activos-ferroviarios/          # Vías, estaciones, señalización, catenaria
│   │   └── año=YYYY/mes=MM/dia=DD/
│   └── sensores-iot/                 # Temperatura, vibración, GPS
│       └── año=YYYY/mes=MM/dia=DD/
│
├── raw/                              # Zona raw: datos sin transformar (bronze)
│   ├── obra-lineal/
│   │   └── año=YYYY/mes=MM/dia=DD/
│   ├── activos-ferroviarios/
│   │   └── año=YYYY/mes=MM/dia=DD/
│   └── sensores-iot/
│       └── año=YYYY/mes=MM/dia=DD/
│
├── silver/                           # Zona silver: datos curados
│   ├── obra-lineal/
│   │   └── año=YYYY/mes=MM/dia=DD/
│   ├── activos-ferroviarios/
│   │   └── año=YYYY/mes=MM/dia=DD/
│   └── sensores-iot/
│       └── año=YYYY/mes=MM/dia=DD/
│
├── gold/                             # Zona gold: datos para consumo final
│   ├── obra-lineal/
│   ├── activos-ferroviarios/
│   └── sensores-iot/
│
└── archive/                          # Zona archive: archivo en Glacier
    ├── obra-lineal/
    │   └── año=YYYY/
    ├── activos-ferroviarios/
    │   └── año=YYYY/
    └── sensores-iot/
        └── año=YYYY/
```

**Puntos Clave para el Formador:**
- La estructura sigue el patrón `zona/dominio/año=YYYY/mes=MM/día=DD` para Hive-style partitioning
- Cada zona tiene los mismos subdominios para trazabilidad
- Archive se particiona solo por año (datos históricos, no se consultan frecuentemente)

---

#### Paso 2: Convenciones de Particionamiento

**Formato Hive-style partitioning:**

```
# Formato general
<zona>/<dominio>/año=YYYY/mes=MM/día=DD

# Ejemplos concretos
landing/sensores-iot/año=2026/mes=05/día=03
silver/activos-ferroviarios/año=2026/mes=05/día=02
gold/obra-lineal/año=2026/mes=04/día=30
```

**Conexión con el Modelo de Hechos y Dimensiones (M03):**

La estructura S3 de las zonas silver/gold materializa el modelo star schema definido en el módulo 3:

```
┌──────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA MEDALLION                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   RAW (Bronze)            SILVER (Star Schema)    GOLD (Consumo) │
│   ──────────              ─────────────────        ───────────── │
│                                                                  │
│   archivos CSV             tablas Parquet             dashboards │
│   originales               particionadas               reports   │
│                                                                  │
│   ┌──────────┐          ┌───────────────┐          ┌───────────┐ │
│   │ CSV raw  │  ──▶    │ fact_ordenes  │  ──▶     │ KPIs      │ │
│   │ sap_     │  ETL     │ dim_activos   │ aggreg.  │ mensuales │ │
│   │ extractos│          │ dim_tiempo    │          └───────────┘ │
│   └──────────┘          │ dim_ubicacion │                        │
│                         └───────────────┘                        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

| Etapa S3 | Contenido Módulo 3 | Formato |
|----------|-------------------|---------|
| `landing/` | Archivos ingestados (CSV originales) | `.csv` |
| `raw/` | Datos sin transformar por dominio | `.csv` o `.parquet` |
| `silver/` | `fact_ordenes`, `dim_activos`, `dim_tiempo` | `.parquet` particionado |
| `gold/` | Agregados: `kpis_mensuales_obra_lineal` | `.csv`/`.parquet` |

**Ejemplo: Dominio Activos Ferroviarios**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     RAW (Bronze)                                            │
│  s3://transcore-infra-prod-eu-west-1/raw/activos-ferroviarios/              │
│   ├── año=2026/mes=05/día=03/                                               │
│   │   └── sap_extractos_obra_20260503.csv      ← CSV original del SAP       │
│   └── año=2026/mes=05/día=04/                                               │
│       └── sap_extractos_obra_20260504.csv                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │ ETL (Spark)
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     SILVER (Star Schema)                                    │
│  s3://transcore-infra-prod-eu-west-1/silver/activos-ferroviarios/           │
│   ├── año=2026/mes=05/día=03/                                               │
│   │   ├── fact_ordenes_2026-05-03.parquet     ← Tabla de hechos             │
│   │   ├── dim_activos_2026-05-03.parquet      ← Dimensión                   │
│   │   ├── dim_tiempo_2026-05-03.parquet       ← Dimensión tiempo            │
│   │   └── dim_ubicacion_2026-05-03.parquet    ← Dimensión ubicación         │
│   └── año=2026/mes=05/día=04/                                               │
│       └── fact_ordenes_2026-05-04.parquet                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │ Agregación
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     GOLD (Consumo)                                          │
│  s3://transcore-infra-prod-eu-west-1/gold/activos-ferroviarios/             │
│   ├── kpis_mensuales_activos_2026-05.csv       ← KPIs mensuales             │
│   └── report_disponibilidad_q1_2026.csv       ← Reporte trimestral          │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Modelo de hechos y dimensiones en Silver:**

| Tabla | Tipo | Descripción |
|-------|------|-------------|
| `fact_ordenes` | **Hecho** | Órdenes de mantenimiento ejecutadas |
| `dim_activos` | **Dimensión** | Activos ferroviarios (vías, señales, estaciones) |
| `dim_tiempo` | **Dimensión** | Calendario (año, mes, día) |
| `dim_ubicacion` | **Dimensión** | Geografías (región, zona, tramo) |

**Beneficios del particionamiento:**
- **Query pruning**: AWS Athena y Spark pueden eliminar particiones no relevantes
- **Mantenimiento**: Easy de eliminar datos por partición (DROP PARTITION)
- **Parallelism**: Differential carga de particiones

---

### Parte 2: Crear Bucket desde Consola AWS

#### Paso 3: Crear el Bucket

**Desde Consola AWS (S3):**

1. Ir a https://s3.console.aws.amazon.com/
2. Click "Crear bucket"
3. Configurar:
   - **Nombre del bucket**: `transcore-infra-prod-eu-west-1`
   - **Región**: `EU (Ireland) eu-west-1`
   - **Configuración de bucket**: Dejar opciones por defecto (Block all public access)
4. Click "Crear bucket"

**Comando AWS CLI equivalente:**
```bash
aws s3 mb s3://transcore-infra-prod-eu-west-1 --region eu-west-1
```

---

#### Paso 4: Habilitar Versionado

**Desde Consola AWS:**

1. Click en el bucket `transcore-infra-prod-eu-west-1`
2. Ir a "Propiedades"
3. En "Control de versiones de bucket", click "Editar"
4. Seleccionar "Habilitar"
5. Click "Guardar cambios"

**Comando AWS CLI equivalente:**
```bash
aws s3api put-bucket-versioning \
    --bucket transcore-infra-prod-eu-west-1 \
    --versioning-configuration Status=Enabled
```

**Resultado esperado:**
```
{
    "VersioningConfiguration": {
        "Status": "Enabled"
    }
}
```

**Puntos Clave para el Formador:**
- El versionado protege contra eliminaciones accidentales
- Cada UPDATE crea una nueva versión, las anteriores se mantienen
- La eliminación de un objeto solo marca como "deleted marker", no elimina físicamente
- Coste adicional: cada versión ocupa storage

---

#### Paso 5: Habilitar Encriptación por Defecto

**Desde Consola AWS:**

1. En el bucket, ir a "Propiedades"
2. En "Encriptación por defecto", click "Editar"
3. Seleccionar "Habilitar"
4. **Tipo de encriptación**: "Clave administrada de Amazon S3 (SSE-S3)"
5. Click "Guardar cambios"

**Comando AWS CLI equivalente:**
```bash
aws s3api put-bucket-encryption \
    --bucket transcore-infra-prod-eu-west-1 \
    --server-side-encryption-configuration '{
        "Rules": [
            {
                "ApplyServerSideEncryptionByDefault": {
                    "SSEAlgorithm": "AES256"
                }
            }
        ]
    }'
```

**Resultado esperado:**
```
{
    "ServerSideEncryptionConfiguration": {
        "Rules": [
            {
                "ApplyServerSideEncryptionByDefault": {
                    "SSEAlgorithm": "AES256"
                }
            }
        ]
    }
}
```

**Puntos Clave para el Formador:**
- SSE-S3 (AES-256) es suficiente para la mayoría de casos
- Para compliance más strict, usar SSE-KMS con CMK
- Todos los objetos nuevos se encriptan automáticamente
- Objetos existentes NO se encriptan (hay que re-encriptarlos manualmente si es necesario)

---

### Parte 3: Definir Políticas de Lifecycle

#### Paso 6: Crear Política de Lifecycle Completa

**Archivo JSON con la política de lifecycle:**

- module-04\resources\lifecycle-policy.json

**Explicación de Transiciones y Expiraciones:**

| Zona | Standard-IA | Glacier | Glacier Deep Archive | Expiración | Justificación |
|------|-------------|---------|---------------------|------------|---------------|
| **landing/** | 30 días | 90 días | - | 1 año | Datos crudos para reprocesamiento si hay errores |
| **raw/** | 30 días | - | 180 días | 2 años | Bronze data para debugging, retention más largo |
| **silver/** | - | 90 días | - | 3 años | Datos curados para analytics medianos |
| **gold/** | - | 180 días | - | 5 años | Datos de alto valor para reporting |
| **archive/** | - | 1 día | - | 10 años | Archivo regulatorio, compliance |

---

#### Paso 7: Aplicar Política de Lifecycle al Bucket

**Desde Consola AWS:**

1. En el bucket, ir a "Propiedades"
2. En "Reglas de lifecycle", click "Crear regla de lifecycle"
3. Configurar:
   - **Nombre de regla**: `transcore-lifecycle-policy`
   - **Ámbito de la regla**: "Aplicar a todos los objetos en el bucket"
   - **Acciones**: Seleccionar "Mover a una clase de almacenamiento diferente" y "Expirar"
4. Click "Crear"

**Comando AWS CLI equivalente:**
```bash
aws s3api put-bucket-lifecycle-configuration \
    --bucket transcore-infra-prod-eu-west-1 \
    --lifecycle-configuration file://lifecycle-policy.json
```

---

### Parte 4: Verificación

#### Paso 8: Verificar Configuración

**Verificar Versionado:**
```bash
aws s3api get-bucket-versioning --bucket transcore-infra-prod-eu-west-1
```
**Resultado esperado:**
```json
{
    "Status": "Enabled"
}
```

**Verificar Encriptación:**
```bash
aws s3api get-bucket-encryption --bucket transcore-infra-prod-eu-west-1
```
**Resultado esperado:**
```json
{
    "ServerSideEncryptionConfiguration": {
        "Rules": [
            {
                "ApplyServerSideEncryptionByDefault": {
                    "SSEAlgorithm": "AES256"
                }
            }
        ]
    }
}
```

**Verificar Lifecycle:**
```bash
aws s3api get-bucket-lifecycle-configuration --bucket transcore-infra-prod-eu-west-1
```
**Resultado esperado:** JSON con todas las reglas creadas

---

## Puntos de Discusión

### Preguntas Frecuentes de Estudiantes

**P1: ¿Por qué no hacer transiciones más rápidas (ej: landing a Glacier en 7 días)?**
R: Necesitamos mantener landing disponible para reprocesamiento en caso de errores en ETL. Si hay un bug en la transformación, necesitamos acceso rápido a los datos crudos. 30 días es un balance entre coste y disponibilidad.

**P2: ¿Qué pasa si necesito acceder a datos en Glacier antes de 90 días?**
R: Puedes hacer una restauración temporal desde Glacier a Standard. El proceso toma 3-12 horas dependiendo de si usas Glacier Retrieval acelerado o no. Hay coste adicional de restauración.

**P3: ¿Por qué separate rules para NoncurrentVersion?**
R: Cuando habilitas versionado, cada update crea una nueva versión. Las versiones antiguas siguen ocupando storage. La regla `clean-old-versions` asegura que después de 365 días las versiones antiguas se eliminan (excepto las 2 más recientes si usas MRG).

### Conexiones Conceptuales

- Esta práctica materializa la arquitectura de zonas de M02 y M03
- El particionamiento Hive-style conecta con el procesamiento distribuido (Spark, Athena)
- Las políticas de lifecycle son parte de Data Governance

---

## Errores Comunes y Soluciones

| Error Común | Causa | Solución | Punto de Enseñanza |
|-------------|-------|----------|-------------------|
| No habilitar versionado | "Ocupará más espacio" | Habilitarlo siempre para prod; el coste extra vale la protección | Protection > Cost |
| Policy con prefijo incorrecto | Copiar/pegar sin verificar | Usar nombres exactos: "landing/", "raw/", "silver/" | Prefix es literal |
| Expiración muy corta | Querer ahorrar coste | Mantener landing al menos 30 días para reprocesamiento | Retención mínima |
| Olvidar incomplete uploads | No considerar multipart | Siempre añadir la regla de abort | Prevenir orphan data |


---

## Recursos de Referencia

- Sección 3.1 del módulo 4: Amazon S3 y conceptos fundamentales
- Sección 3.4: Políticas de Lifecycle
- [S3 Lifecycle Configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
- [S3 Storage Classes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html)

---

## Notas para el Formador

**Timing estimado (15 min):**
1. Explicar estructura: 3 min
2. Crear bucket: 2 min
3. Habilitar versionado + encriptación: 2 min
4. Crear y aplicar lifecycle: 5 min
5. Verificación: 3 min

**Comandos de cleanup para CloudShell (después de la demo):**
```bash
BUCKET="transcore-infra-prod-eu-west-1"

# 1. Eliminar lifecycle
aws s3api delete-bucket-lifecycle --bucket "$BUCKET"

# 2. Deshabilitar versionado
aws s3api put-bucket-versioning --bucket "$BUCKET" --versioning-configuration Status=Suspended

# 3. Eliminar todas las versiones de objetos y delete markers
echo "Eliminando versiones de objetos..."
while true; do
  # Obtener listado de versiones
  RESPONSE=$(aws s3api list-object-versions --bucket "$BUCKET" --output json 2>/dev/null)
  
  # Eliminar versiones actuales (Versions)
  VERSIONS=$(echo "$RESPONSE" | jq -r '.Versions // [] | .[0:1000] | map({Key: .Key, VersionId: .VersionId}) | {Objects: .}' 2>/dev/null)
  if [ "$VERSIONS" != '{"Objects":[]}' ] && [ -n "$VERSIONS" ]; then
    echo "$VERSIONS" | aws s3api delete-objects --bucket "$BUCKET" --delete file:///dev/stdin --output json > /dev/null 2>&1
  fi
  
  # Eliminar delete markers
  MARKERS=$(echo "$RESPONSE" | jq -r '.DeleteMarkers // [] | .[0:1000] | map({Key: .Key, VersionId: .VersionId}) | {Objects: .}' 2>/dev/null)
  if [ "$MARKERS" != '{"Objects":[]}' ] && [ -n "$MARKERS" ]; then
    echo "$MARKERS" | aws s3api delete-objects --bucket "$BUCKET" --delete file:///dev/stdin --output json > /dev/null 2>&1
  fi
  
  # Verificar si quedan objetos
  COUNT=$(echo "$RESPONSE" | jq '(.Versions // [] | length) + (.DeleteMarkers // [] | length)' 2>/dev/null)
  if [ -z "$COUNT" ] || [ "$COUNT" -eq 0 ]; then
    break
  fi
  echo "  Eliminadas versiones en este lote. Continuando..."
done
echo "Todas las versiones eliminadas."

# 4. Eliminar incomplete multipart uploads
aws s3api list-multipart-uploads --bucket "$BUCKET" --output json --query 'Uploads[].[Key,UploadId]' --output json | \
  jq -r '.[] | "--key \(.[0]) --upload-id \(.[1])"' | \
  while read -r params; do
    aws s3api abort-multipart-upload --bucket "$BUCKET" $params 2>/dev/null || true
  done

# 5. Vaciar bucket
aws s3 rb s3://"$BUCKET" --force
```

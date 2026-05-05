# Ejemplos de Datos por Zona - Dominio Activos Ferroviarios

Este directorio contiene archivos de ejemplo para demostrar la estructura de datos en cada zona del bucket S3.

## Estructura de Archivos

```
data_examples/
├── landing/
│   └── activos-ferroviarios/
│       └── año=2026/mes=05/día=03/
│           └── ordenes_mantenimiento_20260503.csv
│
├── raw/
│   └── activos-ferroviarios/
│       └── año=2026/mes=05/día=03/
│           └── ordenes_mantenimiento_2026-05-03.csv
│
├── silver/
│   └── activos-ferroviarios/
│       └── año=2026/mes=05/día=03/
│           ├── fact_ordenes_2026-05-03.csv
│           ├── dim_activos_2026-05-03.csv
│           ├── dim_contratista_2026-05-03.csv
│           ├── dim_tiempo_2026-05-03.csv
│           └── dim_ubicacion_2026-05-03.csv
│
└── gold/
    └── activos-ferroviarios/
        └── kpis_mensuales_activos_2026-05.csv
```

## Descripción de Archivos

### Landing Zone
| Archivo | Descripción | Formato |
|---------|-------------|---------|
| `ordenes_mantenimiento_20260503.csv` | CSV original extraído del SAP | `;` delimitado |

### Raw Zone
| Archivo | Descripción | Formato |
|---------|-------------|---------|
| `ordenes_mantenimiento_2026-05-03.csv` | CSV sin transformar, enriquecido con timestamp de extracción | `;` delimitado |

### Silver Zone
| Archivo | Tipo | Descripción |
|---------|------|-------------|
| `fact_ordenes_2026-05-03.csv` | **Hecho** | Órdenes de mantenimiento con claves foráneas a dimensiones |
| `dim_activos_2026-05-03.csv` | **Dimensión** | Catálogo de activos ferroviarios |
| `dim_contratista_2026-05-03.csv` | **Dimensión** | Catálogo de contratistas |
| `dim_tiempo_2026-05-03.csv` | **Dimensión** | Dimensión tiempo con atributos de calendario |
| `dim_ubicacion_2026-05-03.csv` | **Dimensión** | Dimensión geografía |

### Gold Zone
| Archivo | Descripción |
|---------|-------------|
| `kpis_mensuales_activos_2026-05.csv` | KPIs agregados mensuales listos para reporting |

## Comandos AWS S3 de Ejemplo

### Subir archivos a landing
```bash
aws s3 cp ordenes_mantenimiento_20260503.csv \
  s3://transcore-infra-prod-eu-west-1/landing/activos-ferroviarios/año=2026/mes=05/día=03/
```

### Subir archivos a raw
```bash
aws s3 cp ordenes_mantenimiento_2026-05-03.csv \
  s3://transcore-infra-prod-eu-west-1/raw/activos-ferroviarios/año=2026/mes=05/día=03/
```

### Subir archivos a silver
```bash
aws s3 cp fact_ordenes_2026-05-03.csv \
  s3://transcore-infra-prod-eu-west-1/silver/activos-ferroviarios/año=2026/mes=05/día=03/

aws s3 cp dim_activos_2026-05-03.csv \
  s3://transcore-infra-prod-eu-west-1/silver/activos-ferroviarios/año=2026/mes=05/día=03/
```

### Subir archivos a gold
```bash
aws s3 cp kpis_mensuales_activos_2026-05.csv \
  s3://transcore-infra-prod-eu-west-1/gold/activos-ferroviarios/
```

### Listar contenido del bucket
```bash
aws s3 ls s3://transcore-infra-prod-eu-west-1/ --recursive --summarize
```

## Notas
- Los archivos usan `;` como delimitador (formato europeo)
- Los fechas siguen el formato `YYYY-MM-DD` en paths y `YYYYMMDD` en nombres de archivo para distinguish purposes
- Los datos son sintéticos y no representan información real

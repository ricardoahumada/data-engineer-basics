# Module 07_0 Resources - Big Data Ecosystem: Hadoop & Spark

This folder contains resources for the **Local vs Cloud Spark Execution Comparison Lab**.

## Contents

| File | Description |
|------|-------------|
| `docker-compose.yml` | Spark local environment with Jupyter notebook |
| `generate_dataset.py` | Script to generate 1M telemetry records |
| `README.md` | This file |

## Quick Start

### 1. Start Local Spark Environment

```bash
docker-compose up -d
```

Access Jupyter at: http://localhost:8888

### 2. Generate Dataset

From the resources directory:

```bash
# Create data directory
mkdir -p data

# Generate 1M records (creates data/eventos_telemetria_1M.csv)
python generate_dataset.py
```

### 3. Run the Lab

1. Open Jupyter at http://localhost:8888
2. Create a new notebook
3. Run the transformation from `lab-01.md`

## Prerequisites

- Docker Desktop (for local Spark)
- Python 3.8+ (for dataset generation)
- Databricks Community Edition account (for cloud comparison)

## Lab Overview

The lab compares Spark execution performance:

| Environment | Setup | Use Case |
|-------------|-------|----------|
| **Local (Docker)** | `docker-compose up` | Development, testing |
| **Cloud (Databricks)** | Manual cluster creation | Production, scaling |

## Dataset Schema

| Field | Type | Description |
|-------|------|-------------|
| `event_id` | string | Unique event ID (EV-XXXXXXXX) |
| `activo_id` | string | Asset ID (ACT-XXXX) |
| `timestamp` | datetime | Event timestamp |
| `sensor_type` | string | temperatura, vibracion, presion, humedad |
| `value` | float | Sensor reading (0-100) |
| `status` | string | normal (85%), warning (10%), critical (5%) |

## Notes

- The dataset generator uses random.seed(42) for reproducibility
- Default size: 1M records (~100MB CSV)
- Data simulates 30 days of sensor telemetry (2026-01-01 to 2026-01-30)

## Troubleshooting

**Jupyter not accessible?**
```bash
docker-compose logs jupyter
```

**Clean up:**
```bash
docker-compose down
```
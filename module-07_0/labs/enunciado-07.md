**Módulo 07_0** | **Duración: 20 minutos** | **Tipo: Laboratorio Práctico** | **Jornada: 2**

# Laboratorio 1: Comparativa Ejecución Local vs Cloud

---

## Objetivo

Comparar el rendimiento y la operativa de una misma transformación Spark ejecutada en dos entornos diferentes:
- **Entorno Local**: Spark en Docker (docker-compose con Jupyter)
- **Entorno Cloud**: Databricks Community Edition

Al finalizar, serás capaz de:
- Ejecutar jobs Spark en entornos locales y cloud
- Medir y comparar tiempos de ejecución
- Documentar diferencias operacionales entre ambos modelos
- Tomar decisiones informadas sobre dónde ejecutar jobs según el contexto

---

## Requisitos Previos

- Conceptos básicos de Spark DataFrames
- Python intermedio
- Acceso a Docker Desktop (para entorno local)
- Cuenta en Databricks Community Edition (para entorno cloud)

---

## Dataset de Trabajo

Trabajarás con un dataset de **1 millón de registros** de eventos de telemetría:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `event_id` | string | Identificador único del evento |
| `activo_id` | string | Identificador del activo |
| `timestamp` | datetime | Fecha y hora del evento |
| `sensor_type` | string | Tipo de sensor (temperatura, vibracion, presion) |
| `value` | float | Valor leído por el sensor |
| `status` | string | Estado del sensor (normal, warning, critical) |

---

## Transformación a Ejecutar

La transformación a comparar será:
1. Leer dataset de eventos
2. Filtrar eventos con status 'critical' o 'warning'
3. Calcular estadísticas por activo y tipo de sensor
4. Guardar resultado agregado

Esta transformación simula un caso de uso real: **identificar activos con eventos críticos para generar alertas**.

---

## Instrucciones del Laboratorio

### Paso 1: Preparar entorno local con Docker

Crear archivo `docker-compose.yml` para el entorno Spark local con las especificaciones necesarias.

Ejecutar el contenedor y verificar que está corriendo correctamente.

**Entregable:** Captura de pantalla mostrando el contenedor Spark corriendo.

---

### Paso 2: Crear dataset de prueba (1M registros)

En Jupyter (local) o Databricks, crear un script que genere un dataset de 1 millón de registros con la siguiente estructura:
- 1,000,000 registros
- 4 tipos de sensores: temperatura, vibracion, presion, humedad
- Distribución de estados: 85% normal, 10% warning, 5% critical
- Fechas entre 2026-01-01 y 2026-01-30 (30 días de datos)

Guardar el dataset como CSV.

**Entregable:** Archivo CSV generado (aproximadamente 100MB).

---

### Paso 3: Ejecutar transformación en entorno LOCAL (Spark Local)

En Jupyter del contenedor Docker, crear un script Spark que:
1. Cree una sesión Spark en modo local
2. Mida el tiempo de lectura del dataset
3. Filtre eventos con status 'critical' o 'warning'
4. Calcule estadísticas por activo y tipo de sensor (count, avg, min, max)
5. Guarde el resultado en formato CSV
6. Mida y muestre el tiempo total de ejecución

**Registrar resultados:**

| Métrica | Valor |
|---------|-------|
| Tiempo de lectura | ___ segundos |
| Tiempo total | ___ segundos |
| Memoria asignada | ___ |
| Registros filtrados | ___ |
| Grupos resultantes | ___ |

---

### Paso 4: Ejecutar transformación en DATABRICKS Cloud

1. Acceder a Databricks Community Edition
2. Crear un cluster con 2 workers
3. Subir el archivo CSV generado al Databricks FileStore
4. Crear un notebook con el mismo código de transformación, adaptando las rutas a DBFS
5. Ejecutar y medir tiempos

**Registrar resultados:**

| Métrica | Valor |
|---------|-------|
| Tiempo de lectura | ___ segundos |
| Tiempo total | ___ segundos |
| Workers | 2 × ___ cores |
| Registros filtrados | ___ |
| Grupos resultantes | ___ |

---

### Paso 5: Documentar diferencias operacionales

Completar la siguiente tabla con tus observaciones:

| Aspecto | Local (Docker) | Cloud (Databricks) | Observaciones |
|---------|----------------|---------------------|---------------|
| **Tiempo de ejecución** | ___ min | ___ min | Diferencia: ___% |
| **Configuración** | | | |
| **Escalabilidad** | | | |
| **Coste** | | | |
| **Latencia** | | | |
| **Debugging** | | | |
| **Disponibilidad** | | | |
| **Seguridad datos** | | | |

---

### Paso 6: Conclusiones y recomendaciones

Escribir un breve resumen (3-5 oraciones) sobre cuándo usar cada entorno, considerando:
- Volumen de datos
- Frecuencia de ejecución
- Requisitos de disponibilidad
- Restricciones de presupuesto

---

## Tabla Comparativa Final (completar)

| Métrica | Local | Cloud | Ganador |
|---------|-------|-------|---------|
| Tiempo lectura | ___s | ___s | ___ |
| Tiempo total | ___s | ___s | ___ |
| Facilidad setup | | | |
| Coste | | | |
| Escalabilidad | | | |

---

## Comandos de Referencia

```bash
# Ver recursos de Docker
docker stats

# Ver logs de Spark
docker logs spark_local

# Detener cluster
docker-compose down
```

---

*TransCore - Data Engineer Básico - Módulo 07_0*
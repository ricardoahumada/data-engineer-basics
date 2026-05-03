"""
Script de generación de datasets sintéticos para el curso Data Engineer.
Genera datos realistas de la empresa TransCore Railway con problemas de calidad intencionales.

Uso: python data/generate_datasets.py
"""

import random
import string
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

# Configuración de reproducibilidad
random.seed(42)

# Rutas
DATA_DIR = Path("d:/Shared/MyServices/axia/1.cursos/data-engineer/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = DATA_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def generate_nulls(value, null_rate=0.05):
    """Introduce valores nulos con probabilidad null_rate."""
    if random.random() < null_rate:
        return None
    return value


def random_date(start_date, end_date):
    """Genera fecha aleatoria entre start_date y end_date."""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def generate_partes_trabajo():
    """Genera dataset de partes de trabajo (M6)."""
    tipos = ["PREVENTIVO", "CORRECTIVO", "INSPECCION", "EMERGENCIA"]
    estados = ["COMPLETADO", "EN_PROCESO", "PENDIENTE"]
    
    records = []
    for i in range(1, 61):
        fecha_inicio = random_date(
            datetime(2026, 1, 1),
            datetime(2026, 4, 15)
        )
        horas = random.randint(1, 12)
        fecha_fin = fecha_inicio + timedelta(hours=horas)
        
        records.append({
            "id_parte": f"PT-{i:04d}",
            "id_equipo": f"EQ-{random.randint(1, 50):03d}",
            "fecha_inicio": fecha_inicio.isoformat() if generate_nulls(1) else None,
            "fecha_fin": fecha_fin.isoformat() if generate_nulls(1) else None,
            "horas_trabajo": generate_nulls(horas, 0.08),
            "tipo_mantenimiento": random.choice(tipos),
            "estado": random.choice(estados),
            "descripcion": generate_nulls(
                f"Mantenimiento {random.choice(tipos).lower()} en equipo EQ-{random.randint(1,50):03d}",
                0.05
            )
        })
    
    df = pd.DataFrame(records)
    df.to_csv(RAW_DIR / "partes_trabajo.csv", index=False)
    print(f"Generado: partes_trabajo.csv ({len(df)} registros)")


def generate_telemetria_parque_mes():
    """Genera dataset de telemetría mensual (M7)."""
    activos = [f"EQ-{i:03d}" for i in range(1, 51)]
    sensores = ["TEMP-001", "VIB-001", "PRES-001"]
    
    start_ts = datetime(2026, 4, 1)
    end_ts = datetime(2026, 4, 30, 23, 59, 59)
    
    records = []
    record_count = 0
    target_records = 50000
    
    current_ts = start_ts
    while record_count < target_records and current_ts <= end_ts:
        for activo in random.sample(activos, k=random.randint(10, 20)):
            if record_count >= target_records:
                break
            
            for sensor in sensores:
                if record_count >= target_records:
                    break
                
                sensor_type = "temperatura" if "TEMP" in sensor else "vibracion" if "VIB" in sensor else "presion"
                
                if sensor_type == "temperatura":
                    value = random.uniform(15, 95)
                    value = generate_nulls(value, 0.03)
                elif sensor_type == "vibracion":
                    value = random.uniform(0, 50)
                    value = generate_nulls(value, 0.04)
                else:
                    value = random.uniform(1, 10)
                    value = generate_nulls(value, 0.03)
                
                records.append({
                    "activo_id": activo,
                    "timestamp": current_ts.isoformat(),
                    "sensor_id": sensor,
                    "temperatura": value if sensor_type == "temperatura" else generate_nulls(None, 1),
                    "vibracion": value if sensor_type == "vibracion" else generate_nulls(None, 1),
                    "estado_operativo": random.choices([1, 0], weights=[85, 15])[0]
                })
                record_count += 1
        
        current_ts += timedelta(minutes=15)
    
    df = pd.DataFrame(records)
    df.to_csv(RAW_DIR / "telemetria_parque_mes.csv", index=False)
    print(f"Generado: telemetria_parque_mes.csv ({len(df)} registros)")


def generate_activos():
    """Genera dataset de activos (M7)."""
    tipos = ["VIA", "ESTACION", "SENALIZACION", "CATENARIA", "SUBESTACION", "PASO_NIVEL"]
    estados = ["ACTIVO", "INACTIVO", "MANTENIMIENTO"]
    ubicaciones = [
        "PK 10+500", "PK 25+300", "PK 42+100", "PK 58+750",
        "Estación Central", "Estación Norte", "Estación Sur",
        "Depósito Principal", "Taller Central"
    ]
    
    records = []
    for i in range(1, 51):
        tipo = random.choice(tipos)
        ubicacion = random.choice(ubicaciones)
        
        records.append({
            "activo_id": f"ACT-{i:04d}",
            "activo_nombre": f"{tipo}-{i:03d} {ubicacion}",
            "activo_tipo": tipo,
            "ubicacion": ubicacion if generate_nulls(1) else None,
            "fecha_alta": random_date(
                datetime(2018, 1, 1),
                datetime(2024, 12, 31)
            ).date().isoformat() if generate_nulls(1) else None,
            "estado": random.choice(estados)
        })
    
    df = pd.DataFrame(records)
    df.to_parquet(RAW_DIR / "activos.parquet", index=False)
    print(f"Generado: activos.parquet ({len(df)} registros)")


def generate_ordenes_mantenimiento():
    """Genera dataset de órdenes de mantenimiento (M7)."""
    tipos_orden = ["PREVENTIVO", "CORRECTIVO", "PREDICTIVO"]
    estados = ["ABIERTA", "EN_PROCESO", "COMPLETADA", "CANCELADA"]
    prioridades = ["ALTA", "MEDIA", "BAJA"]
    
    records = []
    for i in range(1, 551):
        fecha_creacion = random_date(
            datetime(2026, 1, 1),
            datetime(2026, 4, 20)
        )
        
        estado = random.choice(estados)
        fecha_ejecucion = None
        if estado in ["COMPLETADA", "EN_PROCESO"]:
            fecha_ejecucion = fecha_creacion + timedelta(days=random.randint(1, 15))
        
        records.append({
            "orden_id": f"OM-{i:05d}",
            "activo_id": f"ACT-{random.randint(1, 50):04d}",
            "tipo_orden": random.choice(tipos_orden),
            "fecha_creacion": fecha_creacion.isoformat() if generate_nulls(1) else None,
            "fecha_ejecucion": fecha_ejecucion.isoformat() if fecha_ejecucion and generate_nulls(1) else None,
            "estado": estado,
            "prioridad": random.choice(prioridades),
            "descripcion": generate_nulls(
                f"Orden de {random.choice(tipos_orden).lower()} para activo ACT-{random.randint(1,50):04d}",
                0.06
            )
        })
    
    df = pd.DataFrame(records)
    df.to_csv(RAW_DIR / "ordenes_mantenimiento.csv", index=False)
    print(f"Generado: ordenes_mantenimiento.csv ({len(df)} registros)")


def generate_sap_extractos_obra():
    """Genera dataset de extractos SAP (M8)."""
    centros = [f"CC-{i:03d}" for i in range(1, 11)]
    cuentas = [
        "400000", "400100", "400200", "410000", "410100",
        "430000", "430100", "610000", "610100", "620000"
    ]
    obras = [f"OL-{i:03d}" for i in range(1, 51)]
    
    records = []
    for i in range(1, 1001):
        importe = round(random.uniform(-50000, 100000), 2) if random.random() > 0.1 else None
        
        records.append({
            "documento": f"SAP-{random.randint(100000, 999999)}",
            "fecha_documento": random_date(
                datetime(2026, 1, 1),
                datetime(2026, 4, 28)
            ).date().isoformat() if generate_nulls(1) else None,
            "centro": random.choice(centros),
            "cuenta": random.choice(cuentas),
            "importe": importe,
            "texto": generate_nulls(
                f"Extracto obra {random.choice(obras)} - {random.choice(['Factura', 'Abono', 'Nota crédito'])}",
                0.04
            ),
            "ref_obra": random.choice(obras) if generate_nulls(1) else None
        })
    
    df = pd.DataFrame(records)
    df.to_csv(RAW_DIR / "sap_extractos_obra.csv", index=False)
    print(f"Generado: sap_extractos_obra.csv ({len(df)} registros)")


def generate_eventos_telemetria_1m():
    """Genera dataset de 1M de eventos de telemetría (M7_0)."""
    activos = [f"EQ-{i:03d}" for i in range(1, 51)]
    sensor_types = ["temperatura", "vibracion", "presion"]
    
    start_ts = datetime(2026, 4, 1)
    
    records = []
    target = 1000000
    
    print("Generando 1,000,000 registros de eventos de telemetría...")
    
    current_ts = start_ts
    batch_size = 50000
    
    while len(records) < target:
        for _ in range(batch_size):
            sensor_type = random.choice(sensor_types)
            
            if sensor_type == "temperatura":
                value = random.uniform(10, 100)
            elif sensor_type == "vibracion":
                value = random.uniform(0, 60)
            else:
                value = random.uniform(0.5, 12)
            
            status = random.choices(
                ["normal", "warning", "critical"],
                weights=[85, 10, 5]
            )[0]
            
            records.append({
                "event_id": f"EVT-{len(records)+1:010d}",
                "activo_id": random.choice(activos),
                "timestamp": current_ts.isoformat(),
                "sensor_type": sensor_type,
                "value": round(value, 2),
                "status": status
            })
            
            if len(records) >= target:
                break
        
        current_ts += timedelta(seconds=10)
        
        if len(records) % 100000 == 0:
            print(f"  Progreso: {len(records):,} registros...")
    
    df = pd.DataFrame(records)
    df.to_csv(RAW_DIR / "eventos_telemetria_1m.csv", index=False)
    print(f"Generado: eventos_telemetria_1m.csv ({len(df):,} registros)")


def main():
    """Ejecuta la generación de todos los datasets."""
    print("=" * 60)
    print("Generando datasets sintéticos para curso Data Engineer")
    print("Empresa: TransCore Railway")
    print("=" * 60)
    
    print("\n[1/6] Generando partes_trabajo.csv...")
    generate_partes_trabajo()
    
    print("\n[2/6] Generando telemetria_parque_mes.csv...")
    generate_telemetria_parque_mes()
    
    print("\n[3/6] Generando activos.parquet...")
    generate_activos()
    
    print("\n[4/6] Generando ordenes_mantenimiento.csv...")
    generate_ordenes_mantenimiento()
    
    print("\n[5/6] Generando sap_extractos_obra.csv...")
    generate_sap_extractos_obra()
    
    print("\n[6/6] Generando eventos_telemetria_1m.csv...")
    generate_eventos_telemetria_1m()
    
    print("\n" + "=" * 60)
    print("¡Generación completada!")
    print(f"Ubicación: {RAW_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
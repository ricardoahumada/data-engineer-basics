#!/usr/bin/env python3
"""
Validación de datos para partes_trabajo.csv
Implementa reglas de validación del módulo M06
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Tuple

class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.valid = True
        
    def add_error(self, row_idx: int, field: str, code: str, message: str):
        self.errors.append({
            'row': row_idx,
            'field': field,
            'code': code,
            'message': message
        })
        self.valid = False
        
    def add_warning(self, row_idx: int, field: str, code: str, message: str):
        self.warnings.append({
            'row': row_idx,
            'field': field,
            'code': code,
            'message': message
        })


def validate_id_parte(value: str, row_idx: int, result: ValidationResult):
    """F01: Validar formato id_parte = PT-{YYYYMMDD}-{SEQ:6}"""
    if pd.isna(value):
        result.add_error(row_idx, 'id_parte', 'F01', 'Identificador no puede ser nulo')
        return
    # Formato: PT-YYYYMMDD-NNNNNN
    import re
    if not re.match(r'^PT-\d{8}-\d{6}$', str(value)):
        result.add_warning(row_idx, 'id_parte', 'F01', 
            f'Formato inesperado: {value}. Esperado: PT-YYYYMMDD-NNNNNN')


def validate_fecha_inicio(value, row_idx, result):
    """F03: Validar fecha_inicio - no nulo, formato ISO 8601"""
    if pd.isna(value):
        result.add_error(row_idx, 'fecha_inicio', 'F03', 'Fecha inicio no puede ser nula')
        return
    try:
        dt = pd.to_datetime(value)
        if dt > datetime.now():
            result.add_warning(row_idx, 'fecha_inicio', 'F03', 'Fecha inicio es futura')
    except:
        result.add_error(row_idx, 'fecha_inicio', 'F03', f'Formato de fecha inválido: {value}')


def validate_fecha_fin(value, fecha_inicio, estado, row_idx, result):
    """F04: Validar fecha_fin >= fecha_inicio, no nulo si estado=COMPLETADO"""
    if pd.isna(value):
        if estado == 'COMPLETADO':
            result.add_error(row_idx, 'fecha_fin', 'F04', 
                'Fecha fin es obligatoria para estado COMPLETADO')
        return
    try:
        fin = pd.to_datetime(value)
        inicio = pd.to_datetime(fecha_inicio) if not pd.isna(fecha_inicio) else None
        if inicio and fin < inicio:
            result.add_error(row_idx, 'fecha_fin', 'F04', 
                f'Fecha fin ({fin}) anterior a fecha inicio ({inicio})')
    except:
        result.add_error(row_idx, 'fecha_fin', 'F04', f'Formato de fecha fin inválido: {value}')


def validate_horas_trabajo(value, row_idx, result):
    """F05: Validar horas_trabajo > 0, <= 24"""
    if pd.isna(value):
        result.add_warning(row_idx, 'horas_trabajo', 'F05', 'Horas trabajo nulas')
        return
    try:
        horas = float(value)
        if horas < 0:
            result.add_error(row_idx, 'horas_trabajo', 'F05', 'Horas trabajo no pueden ser negativas')
        elif horas > 24:
            result.add_warning(row_idx, 'horas_trabajo', 'F05', 
                f'Horas trabajo ({horas}) excede rango normal (0-24)')
    except (ValueError, TypeError):
        result.add_error(row_idx, 'horas_trabajo', 'F05', f'Valor no numérico: {value}')


TIPOS_VALIDOS = {'PREVENTIVO', 'CORRECTIVO', 'PREDICTIVO'}
ESTADOS_VALIDOS = {'ABIERTO', 'EN_PROCESO', 'COMPLETADO', 'CANCELADO'}

def validate_tipo_mantenimiento(value, row_idx, result):
    """F06: Validar tipo_mantenimiento ∈ {PREVENTIVO, CORRECTIVO, PREDICTIVO}"""
    if pd.isna(value):
        result.add_error(row_idx, 'tipo_mantenimiento', 'F06', 'Tipo mantenimiento es obligatorio')
    elif value not in TIPOS_VALIDOS:
        result.add_warning(row_idx, 'tipo_mantenimiento', 'F06', 
            f'Tipo "{value}" no reconocido. Validos: {TIPOS_VALIDOS}')


def validate_estado(value, row_idx, result):
    """F07: Validar estado ∈ {ABIERTO, EN_PROCESO, COMPLETADO, CANCELADO}"""
    if pd.isna(value):
        result.add_error(row_idx, 'estado', 'F07', 'Estado es obligatorio')
    elif value not in ESTADOS_VALIDOS:
        result.add_warning(row_idx, 'estado', 'F07', 
            f'Estado "{value}" no reconocido. Validos: {ESTADOS_VALIDOS}')


def validate_dataset(csv_path: str) -> ValidationResult:
    """
    Ejecuta todas las validaciones sobre el dataset.
    
    Args:
        csv_path: Ruta al archivo CSV a validar
        
    Returns:
        ValidationResult con errores y advertencias
    """
    result = ValidationResult()
    df = pd.read_csv(csv_path)
    
    for idx, row in df.iterrows():
        validate_id_parte(row.get('id_parte'), idx, result)
        validate_fecha_inicio(row.get('fecha_inicio'), idx, result)
        validate_fecha_fin(row.get('fecha_fin'), row.get('fecha_inicio'), 
                          row.get('estado'), idx, result)
        validate_horas_trabajo(row.get('horas_trabajo'), idx, result)
        validate_tipo_mantenimiento(row.get('tipo_mantenimiento'), idx, result)
        validate_estado(row.get('estado'), idx, result)
        
    return result


def main():
    import sys
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        csv_path = 'data/raw/partes_trabajo.csv'
    
    print(f"Validando dataset: {csv_path}")
    result = validate_dataset(csv_path)
    
    print(f"\n=== RESULTADO VALIDACIÓN ===")
    print(f"Válido: {result.valid}")
    print(f"Errores: {len(result.errors)}")
    print(f"Advertencias: {len(result.warnings)}")
    
    if result.errors:
        print("\n--- ERRORES ---")
        for e in result.errors:
            print(f"  [{e['code']}] Fila {e['row']}: {e['field']} - {e['message']}")
    
    if result.warnings:
        print("\n--- ADVERTENCIAS ---")
        for w in result.warnings:
            print(f"  [{w['code']}] Fila {w['row']}: {w['field']} - {w['message']}")


if __name__ == "__main__":
    main()
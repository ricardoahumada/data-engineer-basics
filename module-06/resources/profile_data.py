#!/usr/bin/env python3
"""
Genera informes de profiling para datasets CSV.
Útil para el laboratorio M06 - Ingesta y Calidad del Dato
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
from typing import Dict, Any


def profile_column(series: pd.Series) -> Dict[str, Any]:
    """Genera estadísticas para una columna individual."""
    info = {
        'tipo_datos': str(series.dtype),
        'valores_nulos': int(series.isna().sum()),
        'porcentaje_nulos': round(series.isna().sum() / len(series) * 100, 2),
        'valores_unicos': int(series.nunique()),
        'completitud': round((1 - series.isna().sum() / len(series)) * 100, 2)
    }
    
    if pd.api.types.is_numeric_dtype(series):
        info['min'] = float(series.min()) if not series.isna().all() else None
        info['max'] = float(series.max()) if not series.isna().all() else None
        info['mean'] = round(float(series.mean()), 2) if not series.isna().all() else None
        info['median'] = float(series.median()) if not series.isna().all() else None
        info['std'] = round(float(series.std()), 2) if not series.isna().all() else None
    else:
        top_values = series.value_counts().head(5).to_dict()
        info['top_values'] = {k: int(v) for k, v in top_values.items()}
    
    return info


def generate_profile_report(csv_path: str, output_dir: str) -> Dict[str, Any]:
    """
    Genera informe completo de profiling para un dataset.
    
    Args:
        csv_path: Ruta al archivo CSV
        output_dir: Directorio donde guardar los informes
        
    Returns:
        Diccionario con el informe completo
    """
    df = pd.read_csv(csv_path)
    
    informe = {
        'metadata': {
            'archivo': os.path.basename(csv_path),
            'fecha_generacion': datetime.utcnow().isoformat(),
            'num_registros': len(df),
            'num_columnas': len(df.columns),
            'columnas': list(df.columns)
        },
        'columnas': {},
        'resumen_ejecutivo': {}
    }
    
    # Analizar cada columna
    for col in df.columns:
        informe['columnas'][col] = profile_column(df[col])
    
    # Resumen ejecutivo
    total_celulas = len(df) * len(df.columns)
    total_nulos = df.isna().sum().sum()
    
    informe['resumen_ejecutivo'] = {
        'total_registros': len(df),
        'total_columnas': len(df.columns),
        'total_celulas': total_celulas,
        'celulas_nulas': int(total_nulos),
        'completitud_global': round((1 - total_nulos / total_celulas) * 100, 2)
    }
    
    # Guardar JSON
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, 'informe_profiling.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(informe, f, indent=2, ensure_ascii=False)
    
    # Generar Markdown
    md_path = os.path.join(output_dir, 'informe_profiling.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"# Informe de Perfilado\n\n")
        f.write(f"**Archivo:** {informe['metadata']['archivo']}\n")
        f.write(f"**Fecha:** {informe['metadata']['fecha_generacion']}\n\n")
        f.write(f"## Resumen\n\n")
        f.write(f"| Métrica | Valor |\n|---------|-------|\n")
        f.write(f"| Registros | {informe['resumen_ejecutivo']['total_registros']} |\n")
        f.write(f"| Columnas | {informe['resumen_ejecutivo']['total_columnas']} |\n")
        f.write(f"| Completitud | {informe['resumen_ejecutivo']['completitud_global']}% |\n\n")
        f.write(f"## Columnas\n\n")
        for col, info in informe['columnas'].items():
            f.write(f"### {col}\n\n")
            f.write(f"- Tipo: {info['tipo_datos']}\n")
            f.write(f"- Nulos: {info['valores_nulos']} ({info['porcentaje_nulos']}%)\n")
            f.write(f"- Únicos: {info['valores_unicos']}\n")
            f.write(f"- Completitud: {info['completitud']}%\n")
            if 'min' in info:
                f.write(f"- Rango: [{info['min']}, {info['max']}]\n")
                f.write(f"- Media: {info['mean']}, Mediana: {info['median']}\n")
            if 'top_values' in info:
                f.write(f"- Top valores: {info['top_values']}\n")
            f.write(f"\n")
    
    return informe


if __name__ == "__main__":
    import sys
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'data/raw/partes_trabajo.csv'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'data/profile_reports'
    
    print(f"Perfilando: {csv_path}")
    informe = generate_profile_report(csv_path, output_dir)
    
    print(f"\nRegistros: {informe['resumen_ejecutivo']['total_registros']}")
    print(f"Completitud global: {informe['resumen_ejecutivo']['completitud_global']}%")
    print(f"Informe guardado en: {output_dir}")
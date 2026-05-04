# Recursos - Módulo 06: Ingesta y Calidad del Dato

## Archivos Incluidos

| Archivo | Descripción |
|---------|-------------|
| `partes_trabajo.csv` | Dataset de ejemplo con 8 registros de partes de trabajo de mantenimiento |
| `validate_data.py` | Script de validación con reglas F01-F07 |
| `profile_data.py` | Script de profiling para generar informes JSON/Markdown |

## Uso

### Validación de Datos

```bash
python validate_data.py [ruta_csv]
```

Ejemplo:
```bash
python validate_data.py partes_trabajo.csv
```

### Generación de Informe de Profiling

```bash
python profile_data.py [ruta_csv] [directorio_salida]
```

Ejemplo:
```bash
python profile_data.py partes_trabajo.csv ./reports
```

## Dependencias

```bash
pip install pandas numpy
```

## Notas

- Ambos scripts son utilidades auxiliares para el laboratorio M06
- Los scripts asumen que el CSV tiene las columnas definidas en el esquema
- Para uso en el lab, copiar estos archivos al directorio de trabajo del estudiante
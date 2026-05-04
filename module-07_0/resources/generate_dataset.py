#!/usr/bin/env python3
"""
Generate sample telemetry dataset for TransCore Spark comparison lab.
Creates 1 million records of sensor events.

Usage:
    python generate_dataset.py [num_records] [output_path]

Examples:
    python generate_dataset.py                    # Default: 1M records
    python generate_dataset.py 500000              # 500K records
    python generate_dataset.py 1000000 data/       # Custom path
"""

import argparse
import random
import csv
from datetime import datetime, timedelta
from pathlib import Path


def generate_telemetry_dataset(num_records: int = 1_000_000, output_path: str = "data") -> str:
    """
    Generate a CSV file with telemetry sensor data.
    
    Args:
        num_records: Number of records to generate (default: 1,000,000)
        output_path: Directory to save the CSV file
        
    Returns:
        Path to the generated CSV file
    """
    # Configuration
    sensores = ['temperatura', 'vibracion', 'presion', 'humedad']
    estados = ['normal', 'warning', 'critical']
    pesos_estados = [0.85, 0.10, 0.05]  # 85% normal, 10% warning, 5% critical
    
    # Create output directory
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "eventos_telemetria_1M.csv"
    
    print(f"Generating {num_records:,} telemetry records...")
    print(f"Output: {output_file.absolute()}")
    
    start_time = datetime.now()
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow(['event_id', 'activo_id', 'timestamp', 'sensor_type', 'value', 'status'])
        
        # Generate records
        for i in range(num_records):
            activo_num = random.randint(1, 1000)
            timestamp = datetime(2026, 1, 1) + timedelta(
                minutes=random.randint(0, 43200)  # 30 days of minutes
            )
            
            writer.writerow([
                f'EV-{i:08d}',
                f'ACT-{activo_num:04d}',
                timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                random.choice(sensores),
                round(random.uniform(0, 100), 2),
                random.choices(estados, weights=pesos_estados, k=1)[0]
            ])
            
            # Progress indicator
            if (i + 1) % 100000 == 0:
                elapsed = (datetime.now() - start_time).total_seconds()
                rate = (i + 1) / elapsed
                print(f"  Progress: {i + 1:,} records ({rate:.0f} records/sec)")
    
    elapsed = (datetime.now() - start_time).total_seconds()
    file_size_mb = output_file.stat().st_size / (1024 * 1024)
    
    print(f"\nDataset generated successfully!")
    print(f"  Records: {num_records:,}")
    print(f"  File size: {file_size_mb:.2f} MB")
    print(f"  Time: {elapsed:.2f} seconds")
    
    return str(output_file.absolute())


def main():
    parser = argparse.ArgumentParser(
        description='Generate telemetry dataset for TransCore Spark lab'
    )
    parser.add_argument(
        'num_records', 
        nargs='?', 
        default=1_000_000,
        type=int,
        help='Number of records to generate (default: 1,000,000)'
    )
    parser.add_argument(
        'output_path', 
        nargs='?', 
        default='data',
        help='Output directory path (default: data)'
    )
    
    args = parser.parse_args()
    
    output_file = generate_telemetry_dataset(args.num_records, args.output_path)
    print(f"\nTo use with Spark: {output_file}")


if __name__ == '__main__':
    main()
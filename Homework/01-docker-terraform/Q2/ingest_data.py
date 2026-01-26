#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

@click.group()
def cli():
    """NYC Taxi Data Ingestor"""
    pass

@cli.command()
@click.option('--pg-user', default='postgres', help='PostgreSQL user')
@click.option('--pg-pass', default='postgres', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='green_taxi_trips', help='Target table name for green taxi data')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading data')
def ingest_green_trips(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table, chunksize):
    """Ingest green taxi trip data from Parquet file."""
    
    url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet'
    
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    
    print(f"Downloading and processing green taxi data from: {url}")
    
    df = pd.read_parquet(url)
    
    print(f"Data shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Remove columns that might cause issues with PostgreSQL
    # (especially if they're not needed or contain complex types)
    columns_to_drop = []
    for col in df.columns:
        if df[col].dtype == 'object':
            # Check if it's a string column that might be too long
            try:
                max_len = df[col].astype(str).str.len().max()
                if max_len > 1000:
                    print(f"Column '{col}' has very long strings (max {max_len} chars), consider dropping or processing")
            except:
                pass
    
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)
    
    # Process in chunks
    total_rows = len(df)
    print(f"Total rows: {total_rows:,}")
    
    for i in tqdm(range(0, total_rows, chunksize), desc="Ingesting chunks"):
        chunk = df.iloc[i:i+chunksize]
        
        if i == 0:
            # First chunk - create/replace table
            chunk.to_sql(
                name=target_table,
                con=engine,
                if_exists='replace',
                index=False,
                method='multi'  # Faster insertion
            )
        else:
            # Subsequent chunks - append
            chunk.to_sql(
                name=target_table,
                con=engine,
                if_exists='append',
                index=False,
                method='multi'
            )
    

@cli.command()
@click.option('--pg-user', default='postgres', help='PostgreSQL user')
@click.option('--pg-pass', default='postgres', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5433, type=int, help='PostgreSQL port (5433 for your setup)')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='taxi_zone_lookup', help='Target table name for zone lookup data')
def ingest_zones(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table):
    """Ingest taxi zone lookup data from CSV file."""
    
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'
    
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    
    print(f"Downloading and processing taxi zone data from: {url}")
    
    df = pd.read_csv(url)
    
    print(f"Data shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    dtype_mapping = {
        'LocationID': 'Int64',
        'Borough': 'string',
        'Zone': 'string',
        'service_zone': 'string'
    }
    
    for col, dtype in dtype_mapping.items():
        if col in df.columns:
            df[col] = df[col].astype(dtype)
    
    df.to_sql(
        name=target_table,
        con=engine,
        if_exists='replace',
        index=False
    )
    

@cli.command()
@click.option('--pg-user', default='postgres', help='PostgreSQL user')
@click.option('--pg-pass', default='postgres', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
def ingest_all(pg_user, pg_pass, pg_host, pg_port, pg_db):
    """Ingest both green taxi trips and zone lookup data."""
    
    ctx = click.get_current_context()
    
    ctx.invoke(ingest_zones, 
               pg_user=pg_user, pg_pass=pg_pass, 
               pg_host=pg_host, pg_port=pg_port, 
               pg_db=pg_db, target_table='taxi_zone_lookup')
    
    ctx.invoke(ingest_green_trips, 
               pg_user=pg_user, pg_pass=pg_pass, 
               pg_host=pg_host, pg_port=pg_port, 
               pg_db=pg_db, target_table='green_taxi_trips',
               chunksize=100000)

if __name__ == '__main__':
    cli()
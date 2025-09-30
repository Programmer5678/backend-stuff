#!/usr/bin/env python3

import argparse
import pandas as pd
import psycopg
import os

# --- Hardcoded PostgreSQL connection ---
DB_NAME = "db"
DB_USER = "codya"
DB_PASSWORD = "030103"
DB_HOST = "localhost"
DB_PORT = 5432

def map_dtype(dtype):
    """Map pandas dtype to SQL type"""
    if pd.api.types.is_integer_dtype(dtype):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(dtype):
        return "FLOAT"
    elif pd.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"
    else:
        return "TEXT"

def insert_rows(conn, table_name, df):
    """Insert all rows from the DataFrame into the table"""
    if df.empty:
        return

    columns = df.columns.tolist()
    placeholders = ", ".join(["%s"] * len(columns))
    column_names = ", ".join(columns)
    insert_sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

    with conn.cursor() as cur:
        for row in df.itertuples(index=False, name=None):
            cur.execute(insert_sql, row)
    conn.commit()
    print(f"Inserted {len(df)} rows into '{table_name}'.")

def main():
    
    parser = argparse.ArgumentParser(description="Create a PostgreSQL table from a CSV file and insert data.")
    parser.add_argument("csv_file", help="Path to the CSV file")
    args = parser.parse_args()

    # Determine table name from CSV filename
    table_name = os.path.splitext(os.path.basename(args.csv_file))[0]

    # Load CSV
    df = pd.read_csv(args.csv_file)

    # Generate column definitions
    column_defs = ", ".join(f"{col} {map_dtype(dtype)}" for col, dtype in zip(df.columns, df.dtypes))

    # SQL commands
    drop_sql = f"DROP TABLE IF EXISTS {table_name};"
    create_sql = f"CREATE TABLE {table_name} ({column_defs});"

    # Connect and execute
    conn_str = f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}"
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(drop_sql)
            cur.execute(create_sql)
            conn.commit()
            print(f"Table '{table_name}' created successfully!")

        # Insert rows
        insert_rows(conn, table_name, df)

if __name__ == "__main__":
    main()

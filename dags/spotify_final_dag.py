import datetime as date
from airflow import DAG
import pandas as pd
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
import psycopg2

#from airflow.hooks.postgres_hook import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from sqlalchemy import create_engine


from spotify_etl import spotify_etl


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': date.datetime(2023,7,12),
    #'retries': 1,
    #'retry_delay': date.timedelta(minutes=1)
}

import traceback
import logging

def ETL():
    try:
        print("Starting ETL process")
        load_df = spotify_etl()
        
        # Retrieve connection details
        conn = BaseHook.get_connection('postgre_sql')
        
        # Detailed connection information logging
        print(f"Connection Details:")
        print(f"Host: {conn.host}")
        print(f"Port: {conn.port}")
        print(f"Schema: {conn.schema}")
        print(f"Login: {conn.login}")
        print(f"Password: {'*' * len(conn.password) if conn.password else 'None'}")
        
        # Create SQLAlchemy engine with explicit error handling
        try:
            engine = create_engine('postgresql://airflow:airflow@postgres:5432/spotify_db')
            
            # Test connection
            with engine.connect() as connection:
                print("Database connection successful")
                
            # Proceed with data loading
            conn2 = engine.connect()
            
            # Load DataFrames to SQL
            load_df[0].to_sql('top50tracks', con=conn2, index=False, if_exists='append')
            load_df[2].to_sql('track_count_per_artist', con=conn2, index=False, if_exists='append')
            
            # Handle artist info insertion with more robust method
            try:
                conn3 = psycopg2.connect(
                    host=conn.host,
                    port=conn.port,
                    database=conn.schema,
                    user=conn.login,
                    password=conn.password
                )
                conn3.autocommit = True
                cursor = conn3.cursor()
                
                # Prepare artist info insertion
                artist_records = list(load_df[1].to_records(index=False))
                
                # Batch insert to handle large datasets
                insert_query = """
                INSERT INTO artist_info(artist_name, artist_ID, total_followers, genres, image_url, popularity) 
                VALUES (%s, %s, %s, %s, %s, %s) 
                ON CONFLICT (artist_ID) DO NOTHING
                """
                
                # Execute batch insert
                cursor.executemany(insert_query, [
                    (str(record[0]), str(record[1]), int(record[2]), 
                     str(record[3]), str(record[4]), int(record[5]))
                    for record in artist_records
                ])
                
                print(f"Inserted {cursor.rowcount} artist records")
                
            except (Exception, psycopg2.Error) as artist_insert_error:
                print(f"Error inserting artist info: {artist_insert_error}")
                traceback.print_exc()
                
            finally:
                if 'conn3' in locals():
                    conn3.close()
                
        except Exception as engine_error:
            print(f"SQLAlchemy Engine Creation Error: {engine_error}")
            traceback.print_exc()
        
    except Exception as e:
        print(f"General ETL Error: {e}")
        traceback.print_exc()


with DAG("spotify_final_dag", default_args=default_args,
    schedule_interval="@daily",description='Spotify ETL process 1-day', catchup=False) as dag:
    create_table_Top50Tracks= PostgresOperator(
        task_id='create_table_Top50Tracks',
        postgres_conn_id='postgre_sql',
        #schema='spotify_db',
        sql="""
        CREATE TABLE IF NOT EXISTS Top50Tracks(
        artist_id VARCHAR(200),
        artist_name VARCHAR(200),
        track_id VARCHAR(200),
        track_name VARCHAR(200),
        playlist_date DATE,
        PRIMARY KEY (track_id,playlist_date)); """
    )
    
    create_table_Artist_Info= PostgresOperator(
        task_id='create_table_Artist_Info',
        postgres_conn_id='postgre_sql',
        #schema='spotify_db',
        sql="""
        CREATE TABLE IF NOT EXISTS Artist_Info(
        artist_name VARCHAR(200),
        artist_ID VARCHAR(200),
        total_followers bigint,
        genres VARCHAR(200),
        image_url VARCHAR(500),
        popularity int,
        PRIMARY KEY (artist_ID));"""
    )

    create_table_TrackCount= PostgresOperator(
        task_id='create_table_TrackCount',
        postgres_conn_id='postgre_sql',
        #schema='spotify_db',
        sql="""
        CREATE TABLE IF NOT EXISTS Track_Count_per_Artist(
        artist_ID VARCHAR(200),
        artist_name VARCHAR(200),
        count int,
        playlist_date DATE,
        PRIMARY KEY (artist_ID,playlist_date));"""
    )

    run_etl = PythonOperator(
        task_id='spotify_etl_final',
        python_callable=ETL
    )

    [create_table_Top50Tracks,create_table_Artist_Info,create_table_TrackCount] >> run_etl


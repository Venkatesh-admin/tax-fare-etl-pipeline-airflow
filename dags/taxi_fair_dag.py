from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.utils.dates import days_ago
from transform_clean import transform_and_clean_data,load_to_mysql
import pandas as pd
import os

# Define the default_args dictionary
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 0,
}

# Define the DAG
dag = DAG(
    'etl_sample_taxi',
    default_args=default_args,
    description='An ETL pipeline for sample taxi data',
    schedule_interval=None,
)

# Task 0: Create table in MySQL if it does not exist
create_table_task = MySqlOperator(
    task_id='create_table',
    mysql_conn_id='mysql_taxi',
    sql='./sql_scripts/create_taxi_table.sql',
    dag=dag,
)

# Task 1: Extract ZIP file
extract_zip_task = BashOperator(
    task_id='extract_zip',
    bash_command='unzip -o /opt/airflow/dags/datasets/sample_taxi_data.zip -d /opt/airflow/dags/staging/',
    dag=dag,
)

# Task 2: Transform and clean data
transform_and_clean_task = PythonOperator(
    task_id='transform_and_clean',
    python_callable=transform_and_clean_data,
    dag=dag,
)

# Task 3: Load cleaned data into MySQL
load_to_database = PythonOperator(
    task_id='load_to_database',
    python_callable=load_to_mysql,
    dag=dag,
)

# Define the task dependencies
create_table_task >> extract_zip_task >> transform_and_clean_task >> load_to_database

import pandas as pd
import os
from airflow.hooks.mysql_hook import MySqlHook

def transform_and_clean_data():
    # Define the path to your staging folder
    staging_folder = '/opt/airflow/dags/staging'
    
    # List all CSV files in the staging folder
    csv_files = [file for file in os.listdir(staging_folder) if file.endswith('.csv')]
    
    # Initialize an empty list to store DataFrames
    df_list = []
    
    # Iterate over each CSV file
    for file in csv_files:
        file_path = os.path.join(staging_folder, file)
        # Read CSV file into a DataFrame
        df = pd.read_csv(file_path,parse_dates=['pickup_datetime', 'dropoff_datetime'])
        # Append DataFrame to list
        df_list.append(df)
    
    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # Perform transformations and cleaning on the combined DataFrame
    combined_df['pickup_datetime'] = pd.to_datetime(combined_df['pickup_datetime'])
    combined_df['dropoff_datetime'] = pd.to_datetime(combined_df['dropoff_datetime'])
    combined_df['trip_duration'] = (combined_df['dropoff_datetime'] - combined_df['pickup_datetime']).dt.total_seconds() / 60
    combined_df = combined_df.dropna(subset=['passenger_count', 'trip_duration'])
    combined_df = combined_df[combined_df['trip_duration'] > 0]
    # Example: Calculate fare per mile
    combined_df['fare_per_mile'] = combined_df['fare_amount'] / combined_df['trip_distance']
    
    # Save cleaned data to another staging folder
    cleaned_folder = '/opt/airflow/dags/staging_clean'
    os.makedirs(cleaned_folder, exist_ok=True)
    cleaned_csv_file = os.path.join(cleaned_folder, 'cleaned_sample_taxi_data.csv')
    combined_df.to_csv(cleaned_csv_file, index=False)
    
    

def load_to_mysql():
    cleaned_folder = '/opt/airflow/dags/staging_clean'
    cleaned_csv_file = os.path.join(cleaned_folder, 'cleaned_sample_taxi_data.csv')
    df=pd.read_csv(cleaned_csv_file)
    # Connect to MySQL using Airflow connection
    mysql_hook = MySqlHook(mysql_conn_id='mysql_taxi')
    conn = mysql_hook.get_conn()
    cursor = conn.cursor()

   # Iterate over DataFrame rows and insert into MySQL table
    for index, row in df.iterrows():
        # Prepare SQL query
        sql = """
    INSERT INTO taxi_trips (pickup_datetime, dropoff_datetime, passenger_count, trip_distance, fare_amount, tip_amount, trip_duration, fare_per_mile)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""
        # Extract values from DataFrame row
        values = (
    row['pickup_datetime'],
    row['dropoff_datetime'],
    int(row['passenger_count']),
    float(row['trip_distance']),
    float(row['fare_amount']),
    float(row['tip_amount']),
    float(row['trip_duration']),
    float(row['fare_per_mile'])
)
        # Execute SQL query
        cursor.execute(sql, values)
    
    conn.commit()
    conn.close()
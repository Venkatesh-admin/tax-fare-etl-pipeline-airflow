CREATE TABLE IF NOT EXISTS taxi_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        pickup_datetime DATETIME,
        dropoff_datetime DATETIME,
        passenger_count INT,
        trip_distance FLOAT,
        fare_amount FLOAT,
        tip_amount FLOAT,
        trip_duration FLOAT
    )
CREATE TABLE IF NOT EXISTS taxi_trips (
    pickup_datetime DATETIME,
    dropoff_datetime DATETIME,
    passenger_count INTEGER,
    trip_distance FLOAT,
    fare_amount FLOAT,
    tip_amount FLOAT,
    trip_duration FLOAT,
    fare_per_mile FLOAT
);

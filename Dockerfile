# Use the official Airflow image with Python 3.9
FROM apache/airflow:latest-python3.9

# Update package lists and install necessary tools
USER root
RUN apt-get update && \
    apt-get install -y \
        zip \
        unzip \
        vim \
        && \
    rm -rf /var/lib/apt/lists/*

# Switch back to the airflow user
USER airflow

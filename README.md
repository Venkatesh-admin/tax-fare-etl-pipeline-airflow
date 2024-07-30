# Airflow Architecture
![Alt text](airflow-architecture.png)


1. **Scheduler**: Schedules and monitors DAGs, determining which tasks need to be executed. Continuously checks for new tasks and sends them to the Executor.

2. **Executor**: Manages task execution based on the configured backend (e.g., LocalExecutor, CeleryExecutor, KubernetesExecutor). Determines how and where tasks are executed.

3. **Workers**: Nodes that execute the tasks received from the Executor. Their configuration and number can be scaled according to workload.

4. **Web Server**: Provides a user interface for monitoring and managing workflows. Built using the Flask web framework.

5. **Metadata Database**: Stores information about DAGs, task instances, and other metadata. Typically a relational database such as PostgreSQL or MySQL.

6. **DAG (Directed Acyclic Graph)**: A collection of tasks with defined dependencies, represented as Python code. Used to define and manage workflows.
# Airflow Docker Deployment

This repository provides a Docker-based deployment setup for Apache Airflow using Docker Compose. It includes a PostgreSQL database and initializes the Airflow database with a default admin user.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/your-username/airflow-docker.git
cd airflow-docker
```

2. Build the Docker images:

```bash
docker-compose build
```

3. Start the Airflow services:

```bash
docker-compose up -d
```

This will start the following services:

- `postgres`: PostgreSQL database for Airflow
- `init`: Initializes the Airflow database and creates a default admin user
- `webserver`: Airflow webserver
- `scheduler`: Airflow scheduler

4. Access the Airflow webserver at `http://localhost:8080` using the following credentials:

   - Username: `admin`
   - Password: `admin`

## Configuration

The Docker Compose file defines the following environment variables for configuring Airflow:

```yaml
x-environment: &airflow_environment
  - AIRFLOW__CORE__EXECUTOR=LocalExecutor
  - AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS=False
  - AIRFLOW__CORE__LOAD_EXAMPLES=False
  - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://airflow:airflow@postgres:5432/airflow
  - AIRFLOW__CORE__STORE_DAG_CODE=True
  - AIRFLOW__CORE__STORE_SERIALIZED_DAGS=True
  - AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True
  - AIRFLOW__WEBSERVER__RBAC=False
```

You can modify these variables to customize your Airflow setup.

## Volumes

The Docker Compose file mounts the following volumes:

- `./dags:/opt/airflow/dags`: Mounts the `dags` directory in the current directory to the Airflow DAGs directory inside the containers.
- `logs:/opt/airflow/logs`: Mounts a named volume for storing Airflow logs.

## Extending the Setup

You can extend this setup by adding more services or modifying the existing ones based on your requirements. For example, you can add a Redis service for using the CeleryExecutor or modify the PostgreSQL service to use a different version or configuration.

## Troubleshooting

If you encounter any issues during deployment, check the logs of the affected services using the following command:

```bash
docker-compose logs <service-name>
```

Replace `<service-name>` with the name of the service you want to check the logs for (e.g., `webserver`, `scheduler`, `postgres`).

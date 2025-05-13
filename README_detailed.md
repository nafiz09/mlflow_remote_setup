# MLflow Remote Server Setup

This project sets up a **remote MLflow server** using Docker Compose. It includes:

- **PostgreSQL** as the backend store for MLflow metadata.
- **MinIO** as the artifact store for model outputs and other files.
- **MLflow Tracking Server** running in a Docker container.
- A simple Python example to demonstrate logging parameters, metrics, and artifacts to the remote MLflow server.

---

## 📦 Project Structure

```
.
├── docker-compose.yml          # Defines services: PostgreSQL, MinIO, MLflow server
├── Dockerfile                  # Custom Dockerfile for MLflow server
├── simple_logging_example.py  # Example script to log to the MLflow server
└── README.md                   # You are here
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Docker and Docker Compose installed
- Open ports `3050`, `5432`, `9000`, and `9001` (or adjust in `docker-compose.yml`)
- Python 3.x (for the example script)

---

## 🐳 docker-compose.yml Detailed Breakdown

This file defines and orchestrates three main services: **PostgreSQL**, **MinIO**, and **MLflow**.

### 📌 Services Overview

#### 🔹 PostgreSQL (MLflow backend store)
```yaml
postgres:
  image: postgres:13
  container_name: mlflow_postgres
  restart: always
  environment:
    POSTGRES_DB: mlflow_db
    POSTGRES_USER: mlflow_user
    POSTGRES_PASSWORD: mlflow_pass
  volumes:
    - /home/ssclml/mlflow_postgres:/var/lib/postgresql/data
  ports:
    - "5432:5432"
```
- Stores experiment metadata (runs, metrics, params).
- Data is persisted in `/home/ssclml/mlflow_postgres` on the host.

#### 🔹 MinIO (Artifact storage - S3-compatible)
```yaml
minio:
  image: minio/minio
  container_name: mlflow_minio
  restart: always
  command: server /data --console-address ":9001"
  environment:
    MINIO_ROOT_USER: minio
    MINIO_ROOT_PASSWORD: minio123
  volumes:
    - /mnt/drive1/mlflow:/data
  ports:
    - "9000:9000"
    - "9001:9001"
```
- Stores files and artifacts logged by MLflow.
- UI available at `http://localhost:9001`.
- Artifacts are stored under `/mnt/drive1/mlflow` on the host.

#### 🔹 MLflow Tracking Server
```yaml
mlflow:
  build:
    context: .
    dockerfile: Dockerfile
  container_name: mlflow_server
  depends_on:
    - postgres
    - minio
  ports:
    - "3050:3050"
  environment:
    MLFLOW_S3_ENDPOINT_URL: http://minio:9000
    AWS_ACCESS_KEY_ID: minio
    AWS_SECRET_ACCESS_KEY: minio123
```
- Built from local `Dockerfile`.
- Exposes MLflow UI on `http://localhost:3050`.
- Configured to use MinIO for artifact storage.

---

## 🐋 Dockerfile Detailed Breakdown

Defines how the MLflow server container is built.

### 🧱 Dockerfile
```Dockerfile
FROM python:3.9-slim

RUN pip install mlflow boto3 psycopg2-binary

EXPOSE 3050

CMD mlflow server     --backend-store-uri postgresql://mlflow_user:mlflow_pass@postgres:5432/mlflow_db     --default-artifact-root s3://mlflow/     --host 0.0.0.0     --port 3050
```

### 🔍 Explanation

- `FROM python:3.9-slim`: lightweight Python base image.
- `RUN pip install ...`: installs MLflow and dependencies.
- `EXPOSE 3050`: makes the MLflow port accessible.
- `CMD mlflow server ...`: starts the tracking server with PostgreSQL and MinIO configured.

---

## ▶️ Run the Services

```bash
docker-compose up -d --build
```

Once everything is up, access:

- **MLflow UI**: [http://localhost:3050](http://localhost:3050)
- **MinIO Console**: [http://localhost:9001](http://localhost:9001)

---

## 🧪 Test Logging with Python Script

```bash
python simple_logging_example.py
```

Logs:
- Parameters (`learning_rate`, `epochs`)
- Metric (`accuracy`)
- Artifacts (text file, plot)

Output includes a link to view the run in MLflow UI.

---

## 🔐 Credentials Summary

| Service    | Username  | Password   |
|------------|-----------|------------|
| PostgreSQL | mlflow_user | mlflow_pass |
| MinIO      | minio     | minio123    |

---

## 🧼 Teardown

```bash
docker-compose down
docker-compose down -v  # Also removes volumes (data)
```

---

## 📚 References

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [MinIO Documentation](https://min.io/docs/)
- [Docker Compose](https://docs.docker.com/compose/)
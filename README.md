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

### 2. Configuration Overview

| Component  | Purpose                     | Port | Credentials               |
|------------|-----------------------------|------|---------------------------|
| PostgreSQL | MLflow backend store        | 5432 | `POSTGRES_USER` / `POSTGRES_PASSWORD` |
| MinIO      | MLflow artifact store       | 9000 | `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`      |
| MLflow     | Tracking UI & API server    | 3050 | N/A                       |

Artifacts are stored in `postgres_volume_to_mount` and PostgreSQL data in `minio_mlflow_artifacts_volume_to_mount`.

---

### 3. Start the Services

```bash
docker-compose up -d --build
```

Wait for the services to initialize.

---

### 4. Access the Services

- **MLflow UI**: http://IP_ADDRESS_OF_REMOTE_MACHINE:3050
- **MinIO Console**: http://IP_ADDRESS_OF_REMOTE_MACHINE:9001
---

### 5. Run the Logging Example

> Make sure environment variables match your local setup or edit them in the script.

```bash
python simple_logging_example.py
```

This will:
- Log parameters and a metric
- Upload an example artifact and image
- Print a link to view the run in the MLflow UI

---

## 🐳 docker-compose.yml Breakdown
This file defines and connects the services: PostgreSQL, MinIO, and MLflow. 
### 🧩 Services

1. PostgreSQL
```
  postgres:
    image: postgres:13
    container_name: mlflow_postgres
    restart: always
    environment:
      POSTGRES_DB: mlflow_db
      POSTGRES_USER: POSTGRES_USER
      POSTGRES_PASSWORD: POSTGRES_PASSWORD
    volumes:
      - postgres_volume_to_mount:/var/lib/postgresql/data
    ports:
      - "5432:5432"

```

| Key           | Purpose                                                        |
| ------------- | -------------------------------------------------------------- |
| `image`       | Uses official PostgreSQL v13 image.                            |
| `environment` | Sets up DB name and credentials.                               |
| `volumes`     | Persists database data across restarts.                        |
| `ports`       | Maps container port 5432 to host, enabling external DB access. |

2. MinIO (S3-Compatible Storage)
```
  minio:
    image: minio/minio
    container_name: mlflow_minio
    restart: always
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: MINIO_ROOT_USER
      MINIO_ROOT_PASSWORD: MINIO_ROOT_PASSWORD
    volumes:
      - minio_mlflow_artifacts_volume_to_mount:/data
    ports:
      - "9000:9000"
      - "9001:9001"

```

| Key           | Purpose                                                              |
| ------------- | -------------------------------------------------------------------- |
| `image`       | Uses official MinIO image.                                           |
| `command`     | Tells MinIO to serve files from `/data` and run web UI on port 9001. |
| `environment` | Sets access key & secret key.                                        |
| `volumes`     | Stores artifacts (models, logs, etc.).                               |
| `ports`       | 9000 for S3 API, 9001 for web dashboard.                             |



3. MLflow Server
```
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

| Key           | Purpose                                                              |
| ------------- | -------------------------------------------------------------------- |
| `build`       | Builds image using the custom `Dockerfile` in the project root.      |
| `depends_on`  | Waits for `postgres` and `minio` to be ready before starting MLflow. |
| `ports`       | Exposes MLflow UI/API on port 3050.                                  |
| `environment` | Passes S3 (MinIO) access credentials to MLflow server.               |



## 🐳 Dockerfile Overview

The `Dockerfile` builds a container that launches the MLflow server and connects it to the PostgreSQL and MinIO services using environment variables:

```Dockerfile
CMD mlflow server     --backend-store-uri postgresql://POSTGRES_USER:POSTGRES_PASSWORD@postgres:5432/mlflow_db     --default-artifact-root s3://mlflow/     --host 0.0.0.0     --port 3050
```

## 🔗 How Everything Connects
```
MLflow Server
  ├─> PostgreSQL (stores experiment metadata)
  └─> MinIO (stores models/artifacts in "mlflow" bucket)

Docker Compose ensures these services:
  - Start in correct order
  - Are networked together
  - Persist their data
```

---

## 📁 Volumes and Data Persistence

- **PostgreSQL Data**: `postgres_volume_to_mount`
- **MinIO Buckets**: `minio_mlflow_artifacts_volume_to_mount`
  - These ensure your experiment metadata and artifacts persist across container restarts.

---

## 🛠 Environment Variables Summary

| Variable               | Value                  | Used By     |
|------------------------|------------------------|-------------|
| `POSTGRES_DB`          | `mlflow_db`            | PostgreSQL  |
| `POSTGRES_USER`        | `POSTGRES_USER`          | PostgreSQL  |
| `POSTGRES_PASSWORD`    | `POSTGRES_PASSWORD`          | PostgreSQL  |
| `MINIO_ROOT_USER`      | `MINIO_ROOT_USER`                | MinIO       |
| `MINIO_ROOT_PASSWORD`  | `MINIO_ROOT_PASSWORD`             | MinIO       |
| `AWS_ACCESS_KEY_ID`    | `MINIO_ROOT_USER`                | MLflow & client |
| `AWS_SECRET_ACCESS_KEY`| `MINIO_ROOT_PASSWORD`             | MLflow & client |
| `MLFLOW_S3_ENDPOINT_URL` | `http://minio:9000`  | MLflow & client |

---

## 📌 Notes

- MLflow uses **S3-style URIs** for artifact storage (e.g., `s3://mlflow/`).
- Ensure `mlflow` bucket exists in MinIO or configure MLflow to create it automatically.
---

## 🧼 Teardown

To stop and remove containers:

```bash
docker-compose down
```

To also remove volumes:

```bash
docker-compose down -v
```

---

## 📚 References

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [MinIO Documentation](https://min.io/docs/)
- [Docker Compose](https://docs.docker.com/compose/)